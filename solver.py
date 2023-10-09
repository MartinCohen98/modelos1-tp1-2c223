import math
from datetime import datetime


class Sucursal:

    numero = 0
    demanda = 0
    x = 0
    y = 0

    def __init__(self, numero) -> None:
        self.numero = numero

    def setDemanda(self, cantidad) -> None:
        self.demanda = cantidad
    
    def setCoordenadas(self, coordenadaX, coordenadaY) -> None:
        self.x = coordenadaX
        self.y = coordenadaY

    def getDemanda(self) -> int:
        return self.demanda
    
    def getX(self) -> float:
        return self.x
    
    def getY(self) -> float:
        return self.y
    
    def getNumero(self) -> int:
        return self.numero
    

def distanciaSucursales(sucursal1: Sucursal, sucursal2: Sucursal):
    return math.sqrt((sucursal1.getX() - sucursal2.getX()) ** 2 + (sucursal1.getY() - sucursal2.getY()) ** 2)
    

class Modelo:

    sucursales = {}
    sucursales: dict[int, Sucursal]
    capacidadMaxima = 0

    def __init__(self, capacidad) -> None:
        self.capacidadMaxima = capacidad

    def agregarSucursal(self, numero) -> None:
        self.sucursales[numero] = Sucursal(numero)

    def agregarDemandaSucursal(self, numero, demanda) -> None:
        self.sucursales[numero].setDemanda(demanda)

    def agregarCoordenadasSucursal(self, numero, x, y):
        self.sucursales[numero].setCoordenadas(x, y)

    def getCantidadSucursales(self) -> int:
        return len(self.sucursales)

    def getCapacidadMaxima(self) -> int:
        return self.capacidadMaxima
    
    def getSucursal(self, numero) -> Sucursal:
        return self.sucursales[numero]
    
    def getSucursales(self) -> list[Sucursal]:
        return list(self.sucursales.values())

    def printSucursal(self, numero):
        sucursal = self.sucursales[numero]
        print(str(numero) + ": Demanda: " + str(sucursal.getDemanda()) + " Coordinadas: " + str(sucursal.getX()) + ", " + str(sucursal.getY()))


def scoreSolucion(modelo: Modelo, ordenado: list[int]) -> float:
    distancia = 0
    if not ordenado:
        return distancia
    sucursalOrigen = modelo.getSucursal(ordenado[0])
    sucursalAnterior = sucursalOrigen

    for numero in ordenado:
        sucursal = modelo.getSucursal(numero)
        distancia = distancia + distanciaSucursales(sucursal, sucursalAnterior)

        sucursalAnterior = sucursal

    distancia = distancia + distanciaSucursales(sucursalAnterior, sucursalOrigen)
    
    return distancia

def scoreSolucionPrint(modelo: Modelo, ordenado: list[int], nombre: str) -> float:
    saldo = 0
    distancia = 0
    if not ordenado:
        return distancia
    sucursalOrigen = modelo.getSucursal(ordenado[0])
    sucursalAnterior = sucursalOrigen

    for numero in ordenado:
        sucursal = modelo.getSucursal(numero)
        saldo = saldo + sucursal.getDemanda()
        distancia = distancia + distanciaSucursales(sucursal, sucursalAnterior)

        if(saldo < 0) or saldo > modelo.getCapacidadMaxima():
            print("Solucion " + nombre + " imposible.")

        sucursalAnterior = sucursal

    distancia = distancia + distanciaSucursales(sucursalAnterior, sucursalOrigen)

    print("Score solcion " + nombre + ": " + str(distancia))
    
    return distancia

def distanciaQueAgrega(sucursal: Sucursal, sucursalAnterior: Sucursal, sucursalProxima: Sucursal) -> float:
    distanciaSinAnterior = distanciaSucursales(sucursalAnterior, sucursalProxima)
    distanciaConAnterior = distanciaSucursales(sucursalAnterior, sucursal) + distanciaSucursales(sucursal, sucursalProxima)
    distanciaAgregada = distanciaConAnterior - distanciaSinAnterior
    return distanciaAgregada

def topSucursalAumentaScore(modelo: Modelo, ordenado: list[int], sucursalesIgnorar: list[int]) -> int:
    if not ordenado:
        return None
    if not sucursalesIgnorar:
        sucursalesIgnorar = []
    sucursalAnteriorAnterior = None
    sucursalAnterior = None
    sucursalActual = None
    distanciaAgregadaMaxima = 0
    sucursalMaxDistancia = None

    for numero in ordenado:
        sucursalActual = modelo.getSucursal(numero)

        if sucursalAnterior and sucursalAnteriorAnterior:

            distanciaAgregada = distanciaQueAgrega(sucursalAnterior, sucursalAnteriorAnterior, sucursalActual)
  
            if(distanciaAgregada > distanciaAgregadaMaxima) and (sucursalAnterior.getNumero() not in sucursalesIgnorar):
                distanciaAgregadaMaxima = distanciaAgregada
                sucursalMaxDistancia = sucursalAnterior



        sucursalAnteriorAnterior = sucursalAnterior
        sucursalAnterior = sucursalActual

    sucursalFinal = sucursalActual
    sucursalInicial = modelo.getSucursal(ordenado[0])

    distanciaAgregada = distanciaQueAgrega(sucursalFinal, sucursalAnteriorAnterior, sucursalInicial)
    if(distanciaAgregada > distanciaAgregadaMaxima) and (sucursalAnterior.getNumero() not in sucursalesIgnorar):
        distanciaAgregadaMaxima = distanciaAgregada
        sucursalMaxDistancia = sucursalAnterior

    print("Sucursal que mas distancia agrega: " + str(sucursalMaxDistancia.getNumero()))
    print("Agrega " + str(distanciaAgregadaMaxima) + " de distancia")
    
    return sucursalMaxDistancia.getNumero()




class SolucionTrivial:

    modeloOrdenado = []

    def __init__(self, modelo: Modelo) -> None:
        
        saldo = 0

        for i in range(0, modelo.getCantidadSucursales()):
            sucursal = modelo.getSucursal(i + 1)

            saldo = saldo + sucursal.getDemanda()

            if(saldo < 0) or saldo > modelo.getCapacidadMaxima():
                print("Solucion trivial imposible.")
                return
            
            self.modeloOrdenado.append(sucursal.getNumero())

    def getModeloOrdenado(self) -> list[int]:
        return self.modeloOrdenado
    
    def imprimirSolucion(self) -> str:

        texto = ""

        if not self.modeloOrdenado:
            return texto
        
        for numero in self.modeloOrdenado:
            texto = texto + str(numero) + ' '
        

        return texto[:-1]
    

class SolucionGreedy:

    modeloOrdenado = []

    def __init__(self, modelo: Modelo) -> None:
        
        saldo = 0
        sucursales = modelo.getSucursales()

        sucursalActual = Sucursal(0)
        sucursalActual.setCoordenadas(0,0)


        while sucursales:
            distanciaMinima = None
            proximaSucursal = None
            for sucursal in sucursales:
                distancia = distanciaSucursales(sucursalActual, sucursal)
                nuevoSaldo = saldo + sucursal.getDemanda()

                if((nuevoSaldo >= 0) and (nuevoSaldo <= modelo.getCapacidadMaxima()) and
                   ((distanciaMinima is None) or (distanciaMinima > distancia))):
                    distanciaMinima = distancia
                    proximaSucursal = sucursal
            
            self.modeloOrdenado.append(proximaSucursal.getNumero())
            sucursales.remove(proximaSucursal)
            sucursalActual = proximaSucursal
            saldo = saldo + sucursalActual.getDemanda()

    def getModeloOrdenado(self) -> list[int]:
        return self.modeloOrdenado
    
    def imprimirSolucion(self) -> str:

        texto = ""

        if not self.modeloOrdenado:
            return texto
        
        for numero in self.modeloOrdenado:
            texto = texto + str(numero) + ' '
        

        return texto[:-1]
    

class SolucionSearch:

    modeloOrdenado = []

    def __init__(self, modelo: Modelo) -> None:
        
        sucursales = modelo.getSucursales()
        sucursalActual = None

        i = 0

        while sucursalActual is None:
            unaSucursal = sucursales[i]
            if unaSucursal.getDemanda() > 0:
                sucursalActual = unaSucursal
            i = i + 1
        
        self.modeloOrdenado.append(sucursalActual.getNumero())
        sucursales.remove(sucursalActual)

        while sucursales:

            sucursalesRecorrido = sucursales.copy()

            for sucursal in sucursalesRecorrido:
                
                nuevoModeloOrdenado = None

                for i in range(0, len(self.modeloOrdenado) + 1):

                    if(self.esPosibleIncluir(modelo, i, sucursal)):
                        modeloConNuevoIncluido = self.modeloOrdenado.copy()
                        modeloConNuevoIncluido.insert(i, sucursal.getNumero())

                        if(nuevoModeloOrdenado == None) or (scoreSolucion(modelo, nuevoModeloOrdenado) > scoreSolucion(modelo, modeloConNuevoIncluido)):
                            nuevoModeloOrdenado = modeloConNuevoIncluido.copy()

                if(nuevoModeloOrdenado):
                    self.modeloOrdenado = nuevoModeloOrdenado.copy()
                    sucursales.remove(sucursal)

    def esPosibleIncluir(self, modelo: Modelo, posicion: int, sucursalPorUbicar: Sucursal) -> bool:
        
        i = 0
        saldo = 0
        esPosible = True

        for numeroSucursal in self.modeloOrdenado:
            sucursal = modelo.getSucursal(numeroSucursal)

            if i == posicion:
                saldo = saldo + sucursalPorUbicar.getDemanda()
                if (saldo < 0) or (saldo > modelo.getCapacidadMaxima()):
                    esPosible = False
            
            saldo = saldo + sucursal.getDemanda()
            
            if (saldo < 0) or (saldo > modelo.getCapacidadMaxima()):
                esPosible = False
            
            i = i + 1

        if i == posicion:
            saldo = saldo + sucursalPorUbicar.getDemanda()
            if (saldo < 0) or (saldo > modelo.getCapacidadMaxima()):
                esPosible = False

        return esPosible


    def getModeloOrdenado(self) -> list[int]:
        return self.modeloOrdenado
    
    def imprimirSolucion(self) -> str:

        texto = ""

        if not self.modeloOrdenado:
            return texto
        
        for numero in self.modeloOrdenado:
            texto = texto + str(numero) + ' '
        

        return texto[:-1]
    

class SolucionOptimizador():

    modeloOrdenado = []

    def __init__(self, modelo: Modelo, modeloOrdenado: list[int]) -> None:

        modeloRecorido = modeloOrdenado.copy()
        self.modeloOrdenado = modeloOrdenado.copy()
        iteraciones = 0

        while iteraciones < 1:

            paradasRecorridas = 0

            for numeroSucursalReordenando in modeloRecorido:

                scoreOptimo = scoreSolucion(modelo, self.modeloOrdenado)
                copiaModeloOrdenado = self.modeloOrdenado.copy()
                copiaModeloOrdenado.remove(numeroSucursalReordenando)
                sucursal = modelo.getSucursal(numeroSucursalReordenando)
                nuevoModeloOrdenado = None

                for i in range(0, len(self.modeloOrdenado)):

                    modeloConNuevoIncluido = copiaModeloOrdenado.copy()

                    if(self.esPosibleIncluir(modelo, i, sucursal, copiaModeloOrdenado)):
                        modeloConNuevoIncluido.insert(i, sucursal.getNumero())
                        scoreNuevo = scoreSolucion(modelo, modeloConNuevoIncluido)
                        if(scoreOptimo > scoreNuevo):
                            nuevoModeloOrdenado = modeloConNuevoIncluido.copy()
                            print("Nuevo optimo encontrado, se restaron " + str(scoreOptimo - scoreNuevo) + " puntos")
                            scoreOptimo = scoreNuevo

                
                
                if(nuevoModeloOrdenado):
                    self.modeloOrdenado = nuevoModeloOrdenado.copy()

                paradasRecorridas = paradasRecorridas + 1
                print("Recorridas en optimizador: " + str(paradasRecorridas))

            modeloRecorido = self.modeloOrdenado.copy()

            iteraciones = iteraciones + 1
            print("Iteracion numero: " + str(iteraciones))


    def esPosibleIncluir(self, modelo: Modelo, posicion: int, sucursalPorUbicar: Sucursal, orden: list[int]) -> bool:
        
        i = 0
        saldo = 0
        esPosible = True

        for numeroSucursal in orden:
            sucursal = modelo.getSucursal(numeroSucursal)

            if i == posicion:
                saldo = saldo + sucursalPorUbicar.getDemanda()
                if (saldo < 0) or (saldo > modelo.getCapacidadMaxima()):
                    esPosible = False
            
            saldo = saldo + sucursal.getDemanda()
            
            if (saldo < 0) or (saldo > modelo.getCapacidadMaxima()):
                esPosible = False
            
            i = i + 1

        if i == posicion:
            saldo = saldo + sucursalPorUbicar.getDemanda()
            if (saldo < 0) or (saldo > modelo.getCapacidadMaxima()):
                esPosible = False

        return esPosible


    def getModeloOrdenado(self) -> list[int]:
        return self.modeloOrdenado
    
    def imprimirSolucion(self) -> str:

        texto = ""

        if not self.modeloOrdenado:
            return texto
        
        for numero in self.modeloOrdenado:
            texto = texto + str(numero) + ' '
        

        return texto[:-1]
    

class SolucionNuevoOptimizador():

    modeloOrdenado = []

    def __init__(self, modelo: Modelo, modeloOrdenado: list[int]) -> None:

        self.modeloOrdenado = modeloOrdenado.copy()
        iteraciones = 0
        sucursalesIgnorar = []

        while iteraciones < 100:

            numeroSucursalReordenando = topSucursalAumentaScore(modelo, self.modeloOrdenado, sucursalesIgnorar)

            scoreOptimo = scoreSolucion(modelo, self.modeloOrdenado)
            copiaModeloOrdenado = self.modeloOrdenado.copy()
            copiaModeloOrdenado.remove(numeroSucursalReordenando)
            sucursal = modelo.getSucursal(numeroSucursalReordenando)
            nuevoModeloOrdenado = None

            for i in range(0, len(self.modeloOrdenado)):

                modeloConNuevoIncluido = copiaModeloOrdenado.copy()

                if(distanciaSucursales(modelo.getSucursal(self.modeloOrdenado[i]), sucursal) < 500):

                    modeloConNuevoIncluido.insert(i, sucursal.getNumero())
                    scoreNuevo = scoreSolucion(modelo, modeloConNuevoIncluido)
                    if(scoreOptimo > scoreNuevo):
                        if(self.esPosibleIncluir(modelo, i, sucursal, copiaModeloOrdenado)):
                            nuevoModeloOrdenado = modeloConNuevoIncluido.copy()
                            print("Nuevo optimo encontrado, se restaron " + str(scoreOptimo - scoreNuevo) + " puntos")
                            scoreOptimo = scoreNuevo
            
            
            if(nuevoModeloOrdenado):
                self.modeloOrdenado = nuevoModeloOrdenado.copy()
            else:
                sucursalesIgnorar.append(numeroSucursalReordenando)


            iteraciones = iteraciones + 1
            print("Iteracion numero: " + str(iteraciones))


    def esPosibleIncluir(self, modelo: Modelo, posicion: int, sucursalPorUbicar: Sucursal, orden: list[int]) -> bool:
        
        i = 0
        saldo = 0
        esPosible = True

        for numeroSucursal in orden:
            sucursal = modelo.getSucursal(numeroSucursal)

            if i == posicion:
                saldo = saldo + sucursalPorUbicar.getDemanda()
                if (saldo < 0) or (saldo > modelo.getCapacidadMaxima()):
                    esPosible = False
            
            saldo = saldo + sucursal.getDemanda()
            
            if (saldo < 0) or (saldo > modelo.getCapacidadMaxima()):
                esPosible = False
            
            i = i + 1

        if i == posicion:
            saldo = saldo + sucursalPorUbicar.getDemanda()
            if (saldo < 0) or (saldo > modelo.getCapacidadMaxima()):
                esPosible = False

        return esPosible


    def getModeloOrdenado(self) -> list[int]:
        return self.modeloOrdenado
    
    def imprimirSolucion(self) -> str:

        texto = ""

        if not self.modeloOrdenado:
            return texto
        
        for numero in self.modeloOrdenado:
            texto = texto + str(numero) + ' '
        

        return texto[:-1]
        



f = open("segundo_problema.txt", "r")

capacidad = int(f.readline().split(": ")[1])
dimension = int(f.readline().split(": ")[1])

modelo = Modelo(capacidad)

# DEMANDAS
f.readline()

for i in range(0, dimension):
    demanda = f.readline().split(' ')
    modelo.agregarSucursal(int(demanda[0]))
    modelo.agregarDemandaSucursal(int(demanda[0]), int(demanda[1]))

# FIN DEMANDAS
f.readline()

edgeWeightType = f.readline().split(": ")[1]

print("Edge Weight Type: " + edgeWeightType)

# NODE_COORD_SECTION
f.readline()

for i in range(0, dimension):
    coordenada = f.readline().split(' ')
    modelo.agregarCoordenadasSucursal(int(coordenada[0]), float(coordenada[1]), float(coordenada[2]))

f.close()

# solucionTrivial = SolucionTrivial(modelo)

print("Resolviendo solucion greedy")
t = datetime.now()
solucionGreedy = SolucionGreedy(modelo)
elapsed_time = datetime.now() - t
print(f"Solcuion greedy tardo: {elapsed_time}")

#print("Resolviendo solucion search")
#solucionSearch = SolucionSearch(modelo)

#print("Optimizando solucion greedy")
#t = datetime.now()
#solucionGreedyOptimizada = SolucionOptimizador(modelo, solucionGreedy.getModeloOrdenado())
#elapsed_time = datetime.now() - t
#print(f"Optimizacion de solcuion greedy tardo: {elapsed_time}")

#print("Optimizando solucion search")
#solucionSearchOptimizada = SolucionOptimizador(modelo, solucionSearch.getModeloOrdenado())

print("Optimizando solucion greedy con nuevo optimizador")
t = datetime.now()
solucionGreedyOptimizadaNew = SolucionNuevoOptimizador(modelo, solucionGreedy.getModeloOrdenado())
elapsed_time = datetime.now() - t
print(f"Optimizacion de solcuion greedy tardo: {elapsed_time}")


scoreSolucionPrint(modelo, solucionGreedy.getModeloOrdenado(), "greedy")
#scoreSolucionPrint(modelo, solucionSearch.getModeloOrdenado(), "search")
#scoreSolucionPrint(modelo, solucionGreedyOptimizada.getModeloOrdenado(), "greedy optimizada")
#scoreSolucionPrint(modelo, solucionSearchOptimizada.getModeloOrdenado(), "search optimizada")
scoreSolucionPrint(modelo, solucionGreedyOptimizadaNew.getModeloOrdenado(), "greedy optimizada")

f = open("solucion.txt", "w")
f.write(solucionGreedyOptimizadaNew.imprimirSolucion())
