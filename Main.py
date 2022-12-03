from tkinter import *
from gui import SudokuUI
import GenerateBoard as BG

# Este es el archivo a ejecutar para mostrar la interfaz  de usuario 
#Clase main que se encarga de conectar las dos interfaces gráficas para preservar la información 
class main:
    def __init__(self):
        self.GenerateBoard=NONE         # Ventana donde el usuario podrá ingresar el sudoku a resolver
        self.root = NONE                # Ventana donde se resolverá el sudoku indicado
        self.b=NONE                     # Variable para almacenar la información del sudoku ingresado
        self.ingresar_sudoku()          # Llamado a la función


    #La función ingresar sudoku cerrará la ventana root en caso de estar abierta y recibirá la información del usuario
    def ingresar_sudoku(self):
        if(self.root!=NONE):
            self.root.destroy()    
        self.GenerateBoard=Tk()                         # Se genera la ventana
        board=BG.Board_Gen(self.GenerateBoard,self)     # Se crea un elemento de la clase Board_Gen
        self.GenerateBoard.title("Crea tu sudoku")      
        self.GenerateBoard.mainloop()                   
        self.b=board.cur_board                          # Almacenamos en b la información del tablero creado
        self.resolver_sudoku()                          # Llamado a la función resolver para abrir la nueva ventana

    def resolver_sudoku(self):
        self.root=Tk()                                  # Se genera la ventana de resolución
        SudokuUI(self.root,self.b,self)                 # Se crea el elemento de la clase SudokuUI, entregando la información del sudoku creado
        self.root.title("Sudoku")
        self.root.mainloop()
        

m=main()        # Creamos un elemento main para la correcta ejecución del código