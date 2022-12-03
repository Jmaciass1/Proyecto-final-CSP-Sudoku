from tkinter import *
import copy
from tkinter import ttk
from tkinter import messagebox
import random


MARGIN = 23                                     # Margen para el tablero de ingreso
SIDE = 53                                       # Tamaño de cada celda
WIDTH_B = HEIGHT_B = MARGIN * 2 + SIDE * 9      # Ancho completo del tablero
WIDTH = WIDTH_B + 180                           # Ancho del tablero junto con los botones complementarios

# La clase  Board_Gen  creará una ventana, se visualizará un tablero de sudoku vacío en donde el usuario podrá
    # ingresar los valores del sudokku que quiera resolver, siempre y cuando se cumplan las reglas básicas del mismo
class Board_Gen(Frame):
    
    # Constructor, se recibe un main como parametro para poder conectar las 3 clases principales
    def __init__(self, parent,main):
        self.main=main
        self.parent = parent
        self.orig_board = [[0 for j in range(9)] for i in range(9)]                 # Inicializamos la información del tablero con 0's
        self.cur_board = copy.deepcopy(self.orig_board)                             # El tablero actual irá variando según las específicaciones del usuario, en principio copiamos la inofmración del original
        Frame.__init__(self, parent)                                                # Creamos el frame con sus ajustes correspondientes
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width=WIDTH_B, height=HEIGHT_B)
        self.canvas.pack(fill=BOTH, side=TOP)
        self.canvas.grid(row=0, column=0, rowspan=30, columnspan=60)


        # La variable list entrys es una lista donde almacenamos cada uno de los cuados de textos que tendrán la información ingresada por el usuario
        self.list_entrys=[[ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5)],[ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5)],[ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5)],[ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5)],[ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5)],[ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5)],[ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5)],[ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5)],[ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5),ttk.Entry(width=5)]]

        # El botón submit se oprimirá cuando la información esté completa          
        self.submit_button = Button(self, text="Submit", command=self.__sub_board, width=15, height=5)
        self.submit_button.grid(row=10, column=61, padx=20, columnspan=3)
        
        # El botón random genera un sudoku aleatorí entre 6 posibles de diferentes dificultades     
        self.random = Button(self, text="Random sudoku", command=self.generar_azar, width=15, height=5)
        self.random.grid(row=20, column=61, padx=20, columnspan=3)
        
        self.generate()                                                            


    # La función generate, dibuja lo que queremos ver en la ventana
    def generate(self):
        self.__draw_grid()
        self.__draw_puzzle()

    # Como su nombre lo indica, la función draw gird dibuja la malla para el tablero de sudoku
    def __draw_grid(self):

        
        for i in range(10):                                         # Recorremos cada una de las lineas a dibujar
            if i % 3 == 0:
                color = "black"                                     # Cada tercer linea será negra para diferenciar "las células"
            else:
                color = "gray"
            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT_B - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)    # Creamos las líneas verticales con las coordenadas adecuadas
            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH_B - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)   # Dibujamos, con canvas, las lineas horizontales

    # La función draw puzzle inserta las cajas de texto en cada una de las casillas del tablero según las coordenadas
    def __draw_puzzle(self):
        for i in range(9):
            for j in range(9):
                self.list_entrys[i][j].place(x=MARGIN + j * SIDE+4.7,y=MARGIN + i * SIDE+(SIDE-3)/2-5)
                
    # Submit board o sub board se ejecuta al oprimir el boton, y tomará los valores ingresados en cada una de las entradas de texto y las guardará en el curr_board
    def __sub_board(self):
        for i in range(9):
            for j in range(9):
                if(self.list_entrys[i][j].get()!=''):                                       # Solo miramos las entradas que no sean vacías, las demás se asumirán somo 0 y representan un espacio vacío en el tablero de juego
                    self.cur_board[i][j]=int(self.list_entrys[i][j].get())                  # Almacenamos el valor en cur board
                    if(self.cur_board[i][j]<0 or self.cur_board[i][j]>9):                   # Comprobamos que los valores sean válidos para el juego y se ejecuta un error en caso de que no
                        messagebox.showerror("Error", "Invalid sudoku puzzle, please check the initial state")
                        self.cur_board = copy.deepcopy(self.orig_board)
                        return
                else:
                    self.cur_board[i][j]=0
        self.main.GenerateBoard.destroy()                                               
        

    # La función comprobación toma las filas, columnas y células y verifica que no se repitan valores, como el algoritmo nos arroja cuando un sudoku no está bien inicializado, esta función no aporta
    '''def comprobacion(self):
        filas=self.cur_board                                                       #  Cur_board se guarda por filas
        columnas=[[]]*9
        cells=[[]]*9
        for i in range(9):
            lista_aux=list()
            for j in range(9):
                lista_aux.append(self.cur_board[j][i])
            columnas[i]=lista_aux                                                  # Almacenamos la misma información en forma de columnas
        cells[0]=[self.cur_board[i][j] for i in range(3) for j in range(3)]        # Analogo con las células
        cells[1]=[self.cur_board[i][j] for i in range(3) for j in range(3,6)]
        cells[2]=[self.cur_board[i][j] for i in range(3) for j in range(6,9)]
        cells[3]=[self.cur_board[i][j] for i in range(3,6) for j in range(3)]
        cells[4]=[self.cur_board[i][j] for i in range(3,6) for j in range(3,6)]
        cells[5]=[self.cur_board[i][j] for i in range(3,6) for j in range(6,9)]
        cells[6]=[self.cur_board[i][j] for i in range(6,9) for j in range(3)]
        cells[7]=[self.cur_board[i][j] for i in range(6,9) for j in range(3,6)]
        cells[8]=[self.cur_board[i][j] for i in range(6,9) for j in range(6,9)]
        for i in range(9):                                                          # Para cada fila, columna y célula, verificamos que los dígitos del 1-9 no estén más de una vez; en caso de que sí retornamos un error
            for e in range(1,10):
                if(filas[i].count(e)>=2 or columnas[i].count(e)>=2 or cells[i].count(e)>=2):
                    messagebox.showerror("Error", "Invalid sudoku puzzle, please check the initial state")
                    self.cur_board = copy.deepcopy(self.orig_board)
                    return 0'''


    # generar_azar rellena las entradas de texto con los valores de uno entre 6 sudokus aleatoriamente
    def generar_azar(self):
        sudoku1=[[]*9]*9
        sudoku1[0] = [0, 6, 0, 3, 0, 0, 8, 0, 4]
        sudoku1[1] = [5, 3, 7, 0, 9, 0, 0, 0, 0]
        sudoku1[2] = [0, 4, 0, 0, 0, 6, 0, 0, 7]
        sudoku1[3] = [0, 9, 0, 0, 5, 0, 0, 0, 0]
        sudoku1[4] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        sudoku1[5] = [7, 1, 3, 0, 2, 0, 0, 4, 0]
        sudoku1[6] = [3, 0, 6, 4, 0, 0, 0, 1, 0]
        sudoku1[7] = [0, 0, 0, 0, 6, 0, 5, 2, 3]
        sudoku1[8] = [1, 0, 2, 0, 0, 9, 0, 8, 0]
        sudoku2=[[]*9]*9
        sudoku2[0] = [7, 9, 0, 4, 0, 2, 3, 8, 1]
        sudoku2[1] = [5, 0, 3, 0, 0, 0, 9, 0, 0]
        sudoku2[2] = [0, 0, 0, 0, 3, 0, 0, 7, 0]
        sudoku2[3] = [0, 0, 0, 0, 0, 5, 0, 0, 2]
        sudoku2[4] = [9, 2, 0, 8, 1, 0, 7, 0, 0]
        sudoku2[5] = [4, 6, 0, 0, 0, 0, 5, 1, 9]
        sudoku2[6] = [0, 1, 0, 0, 0, 0, 2, 3, 8]
        sudoku2[7] = [8, 0, 0, 0, 4, 1, 0, 0, 0]
        sudoku2[8] = [0, 0, 9, 0, 8, 0, 1, 0, 4]
        sudoku3=[[]*9]*9
        sudoku3[0] = [0, 3, 0, 5, 0, 6, 2, 0, 0]
        sudoku3[1] = [8, 2, 0, 0, 0, 1, 0, 0, 4]
        sudoku3[2] = [6, 0, 7, 8, 3, 0, 0, 9, 1]
        sudoku3[3] = [0, 0, 0, 0, 0, 0, 0, 2, 9]
        sudoku3[4] = [5, 0, 0, 6, 0, 7, 0, 0, 3]
        sudoku3[5] = [3, 9, 0, 0, 0, 0, 0, 0, 0]
        sudoku3[6] = [4, 5, 0, 0, 8, 9, 1, 0, 2]
        sudoku3[7] = [9, 0, 0, 1, 0, 0, 0, 4, 6]
        sudoku3[8] = [0, 0, 3, 7, 0, 4, 0, 5, 0]
        sudoku4=[[]*9]*9
        sudoku4[0] = [8, 0, 0, 0, 0, 0, 0, 0, 0]
        sudoku4[1] = [0, 0, 3, 6, 0, 0, 0, 0, 0]
        sudoku4[2] = [0, 7, 0, 0, 9, 0, 2, 0, 0]
        sudoku4[3] = [0, 5, 0, 0, 0, 7, 0, 0, 0]
        sudoku4[4] = [0, 0, 0, 0, 4, 5, 7, 0, 0]
        sudoku4[5] = [0, 0, 0, 1, 0, 0, 0, 3, 0]
        sudoku4[6] = [0, 0, 1, 0, 0, 0, 0, 6, 8]
        sudoku4[7] = [0, 0, 8, 5, 0, 0, 0, 1, 0]
        sudoku4[8] = [0, 9, 0, 0, 0, 0, 4, 0, 0]
        sudoku5=[[]*9]*9
        sudoku5[0] = [2, 0, 0, 0, 0, 0, 0, 4, 3]
        sudoku5[1] = [1, 9, 0, 0, 3, 0, 0, 0, 0]
        sudoku5[2] = [0, 6, 0, 0, 0, 5, 0, 0, 0]
        sudoku5[3] = [0, 5, 0, 2, 6, 0, 0, 0, 8]
        sudoku5[4] = [0, 0, 0, 0, 7, 0, 0, 0, 0]
        sudoku5[5] = [6, 0, 0, 0, 5, 3, 0, 1, 0]
        sudoku5[6] = [0, 0, 0, 6, 0, 0, 0, 2, 0]
        sudoku5[7] = [0, 0, 0, 0, 8, 0, 0, 3, 4]
        sudoku5[8] = [9, 1, 0, 0, 0, 0, 0, 0, 6]
        sudoku6=[[]*9]*9
        sudoku6[0] = [0, 0, 0, 0, 2, 0, 0, 0, 5]
        sudoku6[1] = [0, 0, 1, 6, 0, 0, 0, 0, 0]
        sudoku6[2] = [0, 6, 0, 7, 0, 0, 0, 8, 1]
        sudoku6[3] = [0, 0, 0, 3, 0, 0, 5, 0, 0]
        sudoku6[4] = [3, 0, 8, 5, 0, 6, 2, 0, 9]
        sudoku6[5] = [0, 0, 4, 0, 0, 7, 0, 0, 0]
        sudoku6[6] = [7, 4, 0, 0, 0, 9, 0, 1, 0]
        sudoku6[7] = [0, 0, 0, 0, 0, 5, 9, 0, 0]
        sudoku6[8] = [8, 0, 0, 0, 7, 0, 0, 0, 0]

        sudokus=[sudoku1,sudoku2,sudoku3,sudoku4,sudoku5,sudoku6]           # Producimos una lista de diferentes sudokus a llenar

        eleg=random.choice(sudokus)                                         # Elejimos un elmento aleatorio de dicha lista

        for i in range(9):
            for j in range(9):
                self.list_entrys[i][j].delete(0,END)                        # Vaciamos las entradas de texto de cualquier valor que puedan contener
                if(eleg[i][j]!=0):              
                    self.list_entrys[i][j].insert(0,string=eleg[i][j])      # Rellenamos el texto con los valores numéricos distintos a cero