# Sudoku Solver
Este repositorio contiene el proyecto final para la clase de Introducción a la inteligencia artificial 2022-II realizado por 
- Santiago Tovar Mosquera
- Estevan Garcia Niño
- Jaime Macias Sanchez

## Reporte escrito
AGREGAR LINK DEL REPORTE
## Vídeo
AGREGAR LINK DEL VIDEO

# ¿Cómo se usa la interfaz gráfica?
Para correr de manera correcta la GUI programada, se deberá compilar y ejecutar el archivo Main.py.


A continuación se abrirá una ventana emergente; un cuadro con células donde se podrá ingresar un sudoku incompleto para que el programa lo complete.
Existen dos maneras para crear este sudoku: A mano, ingresando cada uno de los valores en su casilla correspondiente o con el botón random, el cual creará
un sudoku aleatorio de 6 posibles.


Una vez se tenga el sudoku deseado, se oprime el botón submit para ingresarlo, la ventana se cerrará y se abrirá una nueva con el sudoku ya implementado; permitiendo al usuario resolverlo con 3 inferencias diferentes. 

Cuando se resolvió el sudoku, se puede resetear para intentar resolverlo con una inferencia diferente, o volver a la pantalla anterior para agregar uno nuevo.

Adicionalmente, debajo del sudoku se pueden ver los datos sobre la ejecución del algoritmo: El tiempo, la cantidad de backtracks y las casillas del tablero incial que tenían datos.

# ¿Cómo se ejecutan los experimentos?
Para la correcta replicación de los experimentos es tan sencillo como compilar y ejecutar el archivo Experimentos.py.

Este archivo toma el sudoku más difícil del mundo y lo altera según el test que queramos probar. Si buscamos ver como se afecta el algoritmo por la cantidad de casillas llenas que se ingresen, entonces tomaremos el sudoku solucionado e iremos quitando casillas para ver que tanto tiempo le toma al programa resolverlo. Obteniendo al final una gráfica de tiempo vs cantidad de casillas llenas. Si por otro lado buscamos ver como afecta la inferencia, es tan sencillo como tomar el sudoku original y ejecutarlo con cada una de ellas. 
