import matplotlib.pyplot as plt
from timeit import default_timer as timer
from sudokucsp import SudokuCSP
from csp import backtracking_search, mrv, unordered_domain_values, forward_checking, mac, no_inference
import random

# Para los experimentos, inicializamos el sudoku con los valores de solución del sudoku mas dificil del mundo
sudoku1=[[]*9]*9
sudoku1[0] = [8, 1, 2, 7, 5, 3, 6, 4, 9]
sudoku1[1] = [9, 4, 3, 6, 8, 2, 1, 7, 5]
sudoku1[2] = [6, 7, 5, 4, 9, 1, 2, 8, 3]
sudoku1[3] = [1, 5, 4, 2, 3, 7, 8, 9, 6]
sudoku1[4] = [3, 6, 9, 8, 4, 5, 7, 2, 1]
sudoku1[5] = [2, 8, 7, 1, 6, 9, 5, 3, 4]
sudoku1[6] = [5, 2, 1, 9, 7, 4, 3, 6, 8]
sudoku1[7] = [4, 3, 8, 5, 2, 6, 9, 1, 7]
sudoku1[8] = [7, 9, 6, 3, 1, 8, 4, 5, 2]



variables_cero=[]                       # En la lista variables cero guardamos los índices de las entradas que son vacías en el sudoku mas difícil
for e in range(9):
    if (e!=0):
        variables_cero.append([0,e])    # Seguimos el patrón de ceros fila por fila
    if (e!=2 and e!=3):
        variables_cero.append([1,e])
    if (e!=1 and e!=4 and e!=6):    
        variables_cero.append([2,e])
    if (e!=1 and e!=5):
        variables_cero.append([3,e])
    if (e!=4 and e!=5 and e!=6):
        variables_cero.append([4,e])
    if (e!=3 and e!=7):    
        variables_cero.append([5,e])
    if (e!=2 and e!=7 and e!=8):                
        variables_cero.append([6,e])
    if (e!=2 and e!=3 and e!=7):
        variables_cero.append([7,e])
    if (e!=1 and e!=6):
        variables_cero.append([8,e])

times=list()                            # times es la lista de tiempos que usaremos para la gráfica
casillas_llenas=list()                  # Casillas llenas es la lista que muestra cuantas casillas se llenan en cada iteración
casillas=list()                         # Lista auxiliar de casillas
for j in range(1,13):                   # Realizaremos 13 extracciones del sudoku completo, en cada una extraemos 6 casillas mas que en la anterior
    time=0                              
    if(j<11):                           # Si llevamos menos de 10 iteraciones, podemos extraer las casillas del conjunto de variables en cero, puesto que 
                                            # con 10 iteraciones habremos extraído máximo 60 casillas, lo cual es la cantidad justa de casillas vacías que tiene 
                                                # el sudoku mas dificil del mundo
        casillas_a_vaciar=random.sample(variables_cero,6*j)     
    else:                               # Si van más de 10 iteraciones, extraemos aleatoriamente las más de 60 casillas a vaciar
        if(len(casillas)==0):
            for k in range(9):
                for l in range(9):
                    casillas.append([k,l])
        casillas_a_vaciar=random.sample(casillas,6*j)    
    sudoku=sudoku1
    for i in range(len(casillas_a_vaciar)):
        sudoku[casillas_a_vaciar[i][0]][casillas_a_vaciar[i][1]]=0      # Reasignamos las casillas que elegimos con un cero como entrada
    s = SudokuCSP(sudoku)                                               # Convertimos el sudoku en un CSP
    inf, suv = no_inference, mrv                                        # Definimos el tipo de inferencia
    start = timer()                                                     # Calculamos el tiempo y ejecutamos la funcion de backtracking
    a = backtracking_search(s, select_unassigned_variable=suv, order_domain_values=unordered_domain_values,inference=inf)
    end = timer()
    time=round(end-start, 5)
    casillas_llenas.append(81-6*j)                                      # Agregamos a las listas las cantidades para la gráfica
    times.append(time)    

plt.xlabel('Cantidad de casillas llenas')
plt.ylabel('Tiempo')                                                   # Hacemos uso de plt para mostrar la gráfica aproximada con cada punto
plt.title('Prueba restringiendo el número de casillas llenas (sin inferencia)')
plt.plot(casillas_llenas,times, 'bo',casillas_llenas,times, 'k')
plt.show()
plt.clf()
plt.savefig("CasillasLlenas.jpg", bbox_inches='tight')





# Pruebas sobre el tipo de inferencia
for i in range(len(variables_cero)):
        sudoku[variables_cero[i][0]][variables_cero[i][1]]=0        # Tomamos el sudoku más difícil como normalmente se presenta, con 60 casillas vacías

times=list()
time=0                                                              # Inicializamos el tiempo para cada iteración
for j in range(1,10):                                               # Para cada inferencia ejecutaremos el código 10 veces y calculamos un promedio
    s = SudokuCSP(sudoku)                                           # Planteamos el problema como CSP
    inf, suv = no_inference, mrv                                    # Definimos el tipo de inferencia
    start = timer()
    a = backtracking_search(s, select_unassigned_variable=suv, order_domain_values=unordered_domain_values,inference=inf)
    end = timer()                                                   
    time+=round(end-start, 5)                                       # Calculamos el tiempo y el algoritmo, luego sumamos el tiempo y lo promediamos
times.append(time/10)
time=0                                                              # Inicializamos el tiempo para cada iteración
for j in range(1,10):                                               # Para cada inferencia ejecutaremos el código 10 veces y calculamos un promedio
    s = SudokuCSP(sudoku)                                           # Planteamos el problema como CSP
    inf, suv = forward_checking, mrv                                # Definimos el tipo de inferencia
    start = timer()
    a = backtracking_search(s, select_unassigned_variable=suv, order_domain_values=unordered_domain_values,inference=inf)
    end = timer()
    time+=round(end-start, 5)                                       # Calculamos el tiempo y el algoritmo, luego sumamos el tiempo y lo promediamos  
times.append(time/10)
time=0                                                              # Inicializamos el tiempo para cada iteración   
for j in range(1,10):
    s = SudokuCSP(sudoku)
    inf, suv = mac, mrv
    start = timer()
    a = backtracking_search(s, select_unassigned_variable=suv, order_domain_values=unordered_domain_values,inference=inf)
    end = timer()
    time+=round(end-start, 5)  
times.append(time/10)       

plt.xlabel('Cantidad de casillas llenas')                          # Haciendo uso de la libreria plt, imprimimos las 3 parejas para la gráfica
plt.ylabel('Tiempo')
plt.title('Prueba de inferencias con el sudoku más díficil')
plt.plot(["Sin inferencia","FC","MAC"],times, 'bo',["Sin inferencia","FC","MAC"],times, 'k')
plt.show()
plt.savefig("Inferencias.jpg", bbox_inches='tight')


