from csp import *

# La clase SudokuCSP toma como valor inicial un tablero y plantea el problema como un CSP
class SudokuCSP(CSP):

    def __init__(self, board):

        
        self.domains = {}                                       # Definimos dos diccionarios uno para guardar el dominio de cada variable
        self.neighbors = {}                                     # Otra para guardar los vecinos de las variables; los vecinos son las variables donde no se pueden repetir numeros
        for v in range(81):
            self.neighbors.update({'CELL' + str(v): {}})        # La casilla numero n se llamará CELL n y viene dada por la formula n=9*i+j, con i el número de la fila y j el de la colmuna 
        for i in range(9):
            for j in range(9):
                name = (i * 9 + j)
                var = "CELL"+str(name)                          # Agregamos la vecindad correspondiente a cada variable, obteniendo su fila, columna y cuadrado correspondiente
                self.add_neighbor(var, self.get_row(i) | self.get_column(j) | self.get_square(i, j))
                if board[i][j] != 0:
                    self.domains.update({var: str(board[i][j])}) # Actualizamos el dominio de las variables, si en el tablero esta ya tiene un valor, su dominio es únicamente este valor
                else:
                    self.domains.update({var: '123456789'})     # Si la variable no tiene valor, es decir es 0, entonces su domino son los números del 1-9


        # Creamos el CSP según el archivo csp.py dando el problema, los dominios, las vecindades y la restricción a seguir específicada en csp.py
        CSP.__init__(self, None, self.domains, self.neighbors, different_values_constraint) 

    # La función get square retorna todos los elementos del bloque en el que se encuentra la casilla i,j
    def get_square(self, i, j):
        # Identificaremos cada bloque por la casilla de su esquina superior esquina.
            # Teniendo en cuenta la numeración que planteamos con anterioridad 
                # Así que el primer bloque irá con la casilla 0
                # El segundo bloque irá con la casilla 3
                # El tercer bloque irá con la casilla 6
                # El cuarto bloque irá con la casilla 27
                # Y así sucesivamente
        if i < 3:                                   # Si i es menor que 3, entonces estamos en uno de los 3 primeros bloques
            if j < 3:                               # El indíce de j determina si estamos en el primero
                return self.get_square_box(0)
            elif j < 6:                             # En el segundo
                return self.get_square_box(3)
            else:                                   # O en el tercero
                return self.get_square_box(6)
        if i < 6:                                   # Si i es menor que 6 y mayor que 3, entonces estamos en uno de los 3 bloques del medio
            if j < 3:                               # El indíce de j determina si estamos en el cuarto
                return self.get_square_box(27)
            elif j < 6:                             # En el quinto
                return self.get_square_box(30)
            else:                                   # O en el sexto
                return self.get_square_box(33)
        else:                                       # Si i es menor que 9 y mayor a 6, entonces estamos en uno de los 3 últimos bloques
            if j < 3:                               # El indíce de j determina si estamos en el séptimo
                return self.get_square_box(54)
            elif j < 6:                             # En el octavo
                return self.get_square_box(57)
            else:                                   # O en el noveno
                return self.get_square_box(60)
               

    # La funcion square box toma el índice con el que identificamos cada bloque y retorna un conjunto en el que agregamos cada una de las casillas
    def get_square_box(self, index):
        tmp = set()
        tmp.add("CELL"+str(index))          #Casilla superior izquierda ((0,0) en el bloque)
        tmp.add("CELL"+str(index+1))        #Casilla superior media ((0,1) en el bloque)
        tmp.add("CELL"+str(index+2))        #Casilla superior derecha ((0,2) en el bloque)
        tmp.add("CELL"+str(index+9))        #Casilla media izquierda ((1,0) en el bloque)
        tmp.add("CELL"+str(index+10))       #Casilla central ((1,1) en el bloque)
        tmp.add("CELL"+str(index+11))       #Casilla media derecha ((1,2) en el bloque)
        tmp.add("CELL"+str(index+18))       #Casilla inferior izquierda ((2,0) en el bloque)
        tmp.add("CELL"+str(index+19))       #Casilla inferior media ((2,1) en el bloque)
        tmp.add("CELL"+str(index+20))       #Casilla inferior derecha ((2,2) en el bloque)
        return tmp

    # La funcion get column recorre las columnas saltando de 9 en 9
    def get_column(self, index):
        return {'CELL'+str(j) for j in range(index, index+81, 9)}

    # La funcion get row recorre las filas con la numeración establecida 
    def get_row(self, index):
            return {('CELL' + str(x + index * 9)) for x in range(9)}

    # La función add neighbor toma conjuntos y los agrega a la vecindad de una variable, omitiendo la misma para no caer en paradojas
    def add_neighbor(self, var, elements):
        self.neighbors.update({var: {x for x in elements if x != var}})

