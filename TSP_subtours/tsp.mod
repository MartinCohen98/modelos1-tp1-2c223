/*********************************************
 * OPL 12.10.0.0 Data
 * Author: Pablo
 * Creation Date: 3 jun. 2022 at 12:31:42
*********************************************/

/*****************************************************************************
 *
 * DATA
 * 
*****************************************************************************/

// Cities
int n = 100;
range Cities = 1 .. n;

// Edges -- sparse set
tuple edge {
  float i;
  float j;
}
setof ( edge ) Edges = {< i, j > | ordered i, j in Cities};
float dist[Edges];

// Decision variables
dvar boolean x[Edges];

tuple Subtour {
  int size;
  int subtour[Cities];
}
{Subtour} subtours = ...;

tuple location {
  float x;
  float y;
}
location cityLocation[Cities] = ...;

//Solucion inicial
//int values[e in Edges] = ((e.j==e.i+1) || (e.i==1 && e.j==n)) ? 1 : 0;

execute {
  function getDistance(city1, city2) {
    return Opl.sqrt(Opl.pow(city1.x - city2.x, 2)
        + Opl.pow(city1.y - city2.y, 2));
  }

  for ( var e in Edges) {
    dist[e] = getDistance(cityLocation[e.i], cityLocation[e.j]);
  }
}


/*****************************************************************************
 *
 * MODEL
 * 
*****************************************************************************/

// Objective
minimize
  sum ( < i, j > in Edges ) dist[< i, j >] * x[< i, j >];
subject to {
  // Each city is linked with two other cities
  forall ( j in Cities )
    sum ( < i, j > in Edges ) x[< i, j >] + sum ( < j, k > in Edges ) x[< j,
       k >] == 2;

  // Subtour elimination constraints.
  forall ( s in subtours )
    sum ( i in Cities : s.subtour[i] != 0 ) x[< minl ( i, s.subtour[i] ), maxl 
      ( i, s.subtour[i] ) >] <= s.size - 1;

}
;

// POST-PROCESSING to find the subtours

// Solution information
int thisSubtour[Cities];
int newSubtourSize;
int newSubtour[Cities];

// Auxiliary information
int visited[i in Cities] = 0;
setof ( float ) adj[j in Cities] = {i | < i, j > in Edges : x[< i,
   j >] == 1} union {k | < j, k > in Edges : x[< j, k >] == 1};
execute {


  newSubtourSize = n;
  for ( var i in Cities) { // Find an unexplored node
    if (visited[i] == 1)
      continue;
    var start = i;
    var node = i;
    var thisSubtourSize = 0;
    for ( var j in Cities)
      thisSubtour[j] = 0;
    while (node != start || thisSubtourSize == 0) {
      visited[node] = 1;
      var succ = start;
      for (i in adj[node])
        if (visited[i] == 0) {
          succ = i;
          break;
        }

      thisSubtour[node] = succ;
      node = succ;
      ++thisSubtourSize;
    }

    writeln("Found subtour of size : ", thisSubtourSize);
    if (thisSubtourSize < newSubtourSize) {
      for (i in Cities)
        newSubtour[i] = thisSubtour[i];
      newSubtourSize = thisSubtourSize;
    }
  }
  if (newSubtourSize != n)
    writeln("Best subtour of size ", newSubtourSize);
}



/*****************************************************************************
 *
 * SCRIPT
 * 
*****************************************************************************/

main {
  var opl = thisOplModel
  var mod = opl.modelDefinition;
  var dat = opl.dataElements;

  var status = 0;
  var it = 0;
  while (1) {
    var cplex1 = new IloCplex();
    opl = new IloOplModel(mod, cplex1);
    opl.addDataSource(dat);
    opl.generate();
    it++;

    //cplex1.addMIPStart(opl.x,opl.values);
    writeln("Iteration ", it, " with ", opl.subtours.size, " subtours.");
    if (!cplex1.solve()) {
      writeln("ERROR: could not solve");
      status = 1;
      opl.end();
      break;
    }
    opl.postProcess();
    writeln("Current solution : ", cplex1.getObjValue());

    if (opl.newSubtourSize == opl.n) {
      opl.end();
      cplex1.end();
      break; // not found
    }

    dat.subtours.add(opl.newSubtourSize, opl.newSubtour);

    opl.end();
    cplex1.end();
  }

  status;
}

