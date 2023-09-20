
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

    def printSucursal(self, numero):
        sucursal = self.sucursales[numero]
        print(str(numero) + ": Demanda: " + str(sucursal.getDemanda()) + " Coordinadas: " + str(sucursal.getX()) + ", " + str(sucursal.getY()))


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

modelo.printSucursal(1)
modelo.printSucursal(89)
modelo.printSucursal(5)
