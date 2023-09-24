import math


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

        sucursalActual = None

        i = 0

        while sucursalActual is None:
            unaSucursal = sucursales[i]
            if unaSucursal.getDemanda() > 0:
                sucursalActual = unaSucursal
            i = i + 1
        
        self.modeloOrdenado.append(sucursalActual.getNumero())
        sucursales.remove(sucursalActual)
        saldo = sucursalActual.getDemanda()

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
                
                aumentoDistanciaMinima = None
                sucursalAnterior = None
                proximaSucursal = None
                nuevaPocision = None
                i = 0

                for numeroSucursal in self.modeloOrdenado:

                    proximaSucursal = modelo.getSucursal(numeroSucursal)

                    if i == 0:
                        aumentoDistancia = distanciaSucursales(sucursal, proximaSucursal)
                    else:
                        aumentoDistancia = distanciaSucursales(sucursalAnterior, sucursal) + distanciaSucursales(sucursal, proximaSucursal)

                    if (aumentoDistanciaMinima == None) or (aumentoDistancia < aumentoDistanciaMinima):

                        if(self.esPosibleIncluir(modelo, i, sucursal)):
                            aumentoDistanciaMinima = aumentoDistancia
                            nuevaPocision = i

                    sucursalAnterior = proximaSucursal
                    i = i + 1

                aumentoDistancia = distanciaSucursales(sucursalAnterior, sucursal)

                if (aumentoDistanciaMinima == None) or (aumentoDistancia < aumentoDistanciaMinima):

                    if(self.esPosibleIncluir(modelo, i, sucursal)):
                        aumentoDistanciaMinima = aumentoDistancia
                        nuevaPocision = i

                if nuevaPocision is not None:
                    self.modeloOrdenado.insert(nuevaPocision, sucursal.getNumero())
                    sucursales.remove(sucursal)
                    print("Insertada la sucursal: " + str(sucursal.getNumero()) + " de " + str(len(self.modeloOrdenado)))

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

        for numeroSucursalReordenando in modeloRecorido:
            
            self.modeloOrdenado.remove(numeroSucursalReordenando)
            sucursal = modelo.getSucursal(numeroSucursalReordenando)
            aumentoDistanciaMinima = None
            sucursalAnterior = None
            proximaSucursal = None
            nuevaPocision = None
            i = 0

            for numeroSucursal in self.modeloOrdenado:

                proximaSucursal = modelo.getSucursal(numeroSucursal)

                if i == 0:
                    aumentoDistancia = distanciaSucursales(sucursal, proximaSucursal)
                else:
                    aumentoDistancia = distanciaSucursales(sucursalAnterior, sucursal) + distanciaSucursales(sucursal, proximaSucursal)

                if (aumentoDistanciaMinima == None) or (aumentoDistancia < aumentoDistanciaMinima):

                    if(self.esPosibleIncluir(modelo, i, sucursal)):
                        aumentoDistanciaMinima = aumentoDistancia
                        nuevaPocision = i

                sucursalAnterior = proximaSucursal
                i = i + 1

            aumentoDistancia = distanciaSucursales(sucursalAnterior, sucursal)

            if (aumentoDistanciaMinima == None) or (aumentoDistancia < aumentoDistanciaMinima):

                if(self.esPosibleIncluir(modelo, i, sucursal)):
                    aumentoDistanciaMinima = aumentoDistancia
                    nuevaPocision = i

            if nuevaPocision is not None:
                self.modeloOrdenado.insert(nuevaPocision, sucursal.getNumero())
                print("Insertada la sucursal: " + str(sucursal.getNumero()) + " de " + str(len(self.modeloOrdenado)))

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
        



f = open("primer_problema.txt", "r")

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
solucionGreedy = SolucionGreedy(modelo)
solucionSearch = SolucionSearch(modelo)
solucionOptimizada = SolucionOptimizador(modelo, solucionSearch.getModeloOrdenado())

print(solucionOptimizada.getModeloOrdenado())

f = open("entrega_primer_problema.txt", "w")
f.write(solucionSearch.imprimirSolucion())
