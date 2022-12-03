from tkinter import *
from timeit import default_timer as timer
from tkinter import messagebox
import threading
import copy
import GenerateBoard as BG

from sudokucsp import SudokuCSP
from csp import backtracking_search, mrv, unordered_domain_values, forward_checking, mac, no_inference


MARGIN = 20                                             # Margen para el tablero
SIDE = 50                                               # Tamaño de cada celda
WIDTH_B = HEIGHT_B = MARGIN * 2 + SIDE * 9              # Ancho completo del tablero
WIDTH = WIDTH_B + 180                                   # Ancho del tablero junto con los botones complementarios

# La clase  SudokuUI  creará una ventana, se visualizará un tablero de sudoku con los valores ingresados
class SudokuUI(Frame):

    # Constructor, se recibe un b para la informacion del sudoku y un main como parametro para poder conectar las 3 clases principales
    def __init__(self, parent,b,main):                  
        self.main=main
        self.parent = parent
        self.original_board = b                                     # Inicializamos el tablero con los valores ingresados por el usuario
        self.current_board = copy.deepcopy(self.original_board)     # El tablero actual copia la información del original
        var_aux=0
        for i in range(9):
            var_aux+=self.original_board[i].count(0)
        self.cont_var=81-var_aux                                    # cont_var cuenta cuantas casillas encontramos con algun valor introducido
        Frame.__init__(self, parent)
        self.row, self.col = 0, 0
        self.__initUI()                                             # Ejecutamos la funcion que construirá la interfaz

    # __initUI construirá los elementos para la interfaz gráfica 
    def __initUI(self):
        self.pack(fill=BOTH, expand=1)                                  # Usamos la libreria Canvas paa la construcción de disntitos elementos y la "mallalización" de la ventana
        self.canvas = Canvas(self, width=WIDTH_B, height=HEIGHT_B)
        self.canvas.pack(fill=BOTH, side=TOP)
        self.canvas.grid(row=0, column=0, rowspan=30, columnspan=60)

        self.cont= StringVar()                                         # Mostramos, mediante un StringVar, el número de casillas llenas en el sudoku
        self.cont.set("Content: "+str(self.cont_var))
        self.time = StringVar()                                         # Mostramos, mediante un StringVar, el tiempo que se tarda el algoritmo en hallar la solución al algoritmo
        self.time.set("Tiempo:                    ")
        self.n_bt = StringVar()                                         # Analogamente mostramos el número de backtracks que se usaron
        self.n_bt.set("N. BT:   ")


        # El botón clear se usa para borrar los valores conseguidos por el algoritmo y dejar el sudoku en su estado inicial
        self.clear_button = Button(self, text="Reset", command=self.__clear_board, width=15, height=5)
        self.clear_button.grid(row=10, column=61, padx=20, columnspan=3)

        # El botón solve se usa para ejecutar el algoritmo y hallar la solución del sudoku en cuestión
        self.solve_button = Button(self, text="Solve", command=self.solve_clicked, width=15, height=5)
        self.solve_button.grid(row=13, column=61, padx=20, columnspan=3)

        # El botón new se usa para ingresar un sudoku nuevo
        self.new_sudoku_button=Button(self, text="New Sudoku", command=self.__change_level, width=15, height=5)
        self.new_sudoku_button.grid(row=25, column=61, padx=20, columnspan=3)

        # Agregamos los labels para almacenar la información del tiempo, los backtracks y las variables llenas
        lbltime = Label(self, textvariable=self.time)
        lblBT = Label(self, textvariable=self.n_bt)
        lblInfo = Label(self, textvariable=self.cont)

        Label(self, text="Inference:               ").grid(row=14, column=61)
        lbltime.grid(row=30, column=0)
        lblBT.grid(row=32, column=0)
        lblInfo.grid(row=34, column=0)

        # Construimos un menu con radio buttons que nos permitan elegir la inferencia con la que queremos hallar la solución del sudoku
        self.inference = StringVar()
        self.radio = []
        self.radio.append(Radiobutton(self, text="No Inference", variable=self.inference, value="NO_INFERENCE"))
        self.radio[0].grid(row=15, column=62, padx=2)
        self.radio.append(Radiobutton(self, text="FC                  ", variable=self.inference, value="FC"))
        self.radio[1].grid(row=16, column=62)
        self.radio.append(Radiobutton(self, text="MAC              ", variable=self.inference, value="MAC"))
        self.radio[2].grid(row=17, column=62)
        self.inference.set("NO_INFERENCE")

        Label(self, text="Variable to choose:").grid(row=18, column=61)
        lbltime.grid(row=30, column=0)

        lblBT.grid(row=32, column=0)

        self.var_to_choose = StringVar()
        self.radio.append(Radiobutton(self, text="MRV", variable=self.var_to_choose, value="MRV"))
        self.radio[3].grid(row=20, column=62)

        self.var_to_choose.set("MRV")

        #Finalmente dibujamos la malla y el sudoku en cuestión
        self.__draw_grid()
        self.__draw_puzzle()


    # La función solve clicked se activa cuando se presiona el botón de resolver. Desactiva todos los botones para que no se puedan cometer errores
    def solve_clicked(self):
        for rb in self.radio:                               # Desactivamos los radio button que afectan al algoritmo
            rb.config(state=DISABLED)
        self.clear_button.config(state=DISABLED)
        self.solve_button.config(state=DISABLED)
        self.new_sudoku_button.config(state=DISABLED)       # Desactivamos los botones que afectan el tablero y el sudoku en sí
        p = threading.Thread(target=self.solve_sudoku)      # Desarrollamos un thread para ejecutar la solución del sudoku sin dejar de mostrar la interfaz, mediante uso de hilos
        p.start()
        messagebox.showinfo("Working", "We are looking for a solution, please wait some seconds ...")


    # La función solve_sudoku hace uso de la clase SudokuCSP y encuentra la solución del sudoku, actualizando el current board
    def solve_sudoku(self):


        s = SudokuCSP(self.current_board)                           # Creamos un elemento de la clase SudokuCSP, ingresando la información del tablero actual
        inf, suv = None, None                                       # Creamos atributos para saber la inferencia y la variable

        if self.inference.get() == "NO_INFERENCE":
            inf = no_inference
        elif self.inference.get() == "FC":                          # Inicializamos las variables según lo que se haya elegido en la interfaz gráfica haciendo uso del archivo csp.py
            inf = forward_checking
        elif self.inference.get() == "MAC":
            inf = mac

        if self.var_to_choose.get() == "MRV":
            suv = mrv

        # Inicializamos el contador de tiempo y usando el archivo csp hacemos llamado a la función de busqueda mediante backtrackin
        start = timer()
        a = backtracking_search(s, select_unassigned_variable=suv, order_domain_values=unordered_domain_values,
                                inference=inf)
        end = timer()
        # Es importante notar que si a no es nulo, entonces se encontró una solución al sudoku
            # Si a es nulo entonces quiere decir que el sudoku inicial no cumple con alguna de las restricciones, asi que arrojamos un error
        if a:
            for i in range(9):
                for j in range(9):
                    index = i * 9 + j
                    self.current_board[i][j] = a.get("CELL" + str(index))                           # Si a no es nulo, entonces obtenemos la solución de aquí y la agregamos al current board    
        else:
            messagebox.showerror("Error", "Invalid sudoku puzzle, please check the initial state")  # Si a es nulo, mostramos el error y el current board se mantiene igual

        
        self.__draw_puzzle()
        self.time.set("Time: "+str(round(end-start, 5))+" seconds")                                 # Imprimimos la solución del problema junto con el tiempo y el número de backtrakcs
        self.n_bt.set("N. BR: "+str(s.n_bt))

       
        for rb in self.radio:
            rb.config(state=NORMAL)
        self.clear_button.config(state=NORMAL)
        self.solve_button.config(state=NORMAL)                                                       # Re habilitamos los botones después de haber calculado la solución
        self.new_sudoku_button.config(state=NORMAL)

    #La función change_level ejecuta ingresar sudoku para cerrar la ventana actual y re ingresar un nuevo sudoku
    def __change_level(self):
        self.main.ingresar_sudoku()



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

   # La función draw puzzle mostrará el sudoku con los valores necesarios
    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        self.time.set("Time:                  ")
        self.n_bt.set("N. BT:   ")
        for i in range(9):
            for j in range(9):
                cell = self.current_board[i][j]                                                 # Guardamos la variable del tablero actual, el cual puede ser el sudoku ya solucionado
                if cell != 0:                                                                   # Consideramos solo las entradas que no sean cero, las que son cero se tomarán como casillas vacías
                    x = MARGIN + j * SIDE + SIDE / 2                                            # Definimos las coordenadas paras escribir
                    y = MARGIN + i * SIDE + SIDE / 2
                    if str(cell) == str(self.original_board[i][j]):                             # Si el elemento en cuestión es igual al del tablero original, entonces lo imprimimos de color negro
                        self.canvas.create_text(x, y, text=cell, tags="numbers", fill="black")
                    else:                                                                       # Si el elemento no es igual al del tablero original, entonces estamos imprimiendo parte de la solución, lo imprimiremos rojo en ese caso
                        self.canvas.create_text(x, y, text=cell, tags="numbers", fill="red")


    # clear_board reinicia el tablero a su estado original y lo re dibuja para borrar los datos sobrantes
    def __clear_board(self):
        self.current_board = copy.deepcopy(self.original_board)
        self.__draw_puzzle()




