Guía de Usuario 

# py_utils.py   

Este script contiene funciones útiles para la manipulación y análisis de datos, 
incluyendo discretización, normalización, estandarización, cálculo de métricas, 
visualización y filtrado. A continuación, se describen brevemente las funciones principales.

## 1. Requisitos

    Librerías necesarias: math, collections, numpy, pandas, seaborn, matplotlib.
    Importación adicional de py_s4.


## 2. Funciones Principales
    
    2.1 Discretización

        igual_anchura(dataset, num_intervalos): Divide los datos en intervalos de igual anchura. 
        Se puede aplicar a un conjunto de datos completo o a una lista de valores numéricos.
        
        igual_frecuencia(dataset, num_intervalos): Divide los datos en intervalos con una cantidad
        similar de observaciones en cada uno.

    2.2 Normalización y Estandarización

        normalizar_dataset(dataset): Escala los valores de los datos a un rango de [0, 1].
        estandarizar_dataset(dataset): Ajusta los valores para que tengan media 0 y desviación estándar 1.

    2.3 Cálculo de Correlación

        calcular_correlacion(dataset): Calcula la correlación de Pearson para variables numéricas y la 
        información mutua para variables categóricas. Genera una matriz de correlación o información mutua.

    2.4 Cálculo de Métricas

        calcular_varianza(columna): Calcula la varianza de una columna.
        calcular_auc(clase, columna): Calcula el Área Bajo la Curva (AUC) en relación a una clase binaria.
        calcular_entropia(columna): Calcula la entropía de una columna discreta.

    2.5 Visualización

        plot_auc(resultados): Genera un gráfico de barras para visualizar los valores de AUC por variable numérica.
        plot_matriz_correlacion(correlaciones): Muestra una matriz de correlación/información mutua en formato de heatmap.

    2.6 Filtrado

        filtrar_por_condicion(dataset, tipo, condicion, umbral, supervisado=False, variable_clase=None): Filtra
        variables en función de condiciones específicas aplicadas sobre AUC, varianza o entropía.




# py_s4.py      

## 1. Requisitos

    No requiere librerías adicionales.

## 2. Clase S4Dataset

    La clase permite crear y manipular un dataset organizado en una lista de listas. Cada sublista
    representa un individuo (fila), y cada elemento de la sublista representa una variable (columna).

    __init__(self, data): Constructor que inicializa un dataset. data debe ser una lista de listas
    con la misma cantidad de variables en cada sublista. Verifica el tipo y estructura de data.

    __repr__(self): Representación en texto del dataset, mostrando los datos y las dimensiones (número
    de individuos y variables).

    print_dataset_data(self): Imprime cada individuo del dataset en una nueva línea, útil para inspeccionar
    los datos rápidamente.

    añadir_individuo(self, new_individual): Agrega un nuevo individuo (fila) al dataset. new_individual 
    debe tener el mismo número de variables que el resto del dataset.

    eliminar_individuo(self, index): Elimina el individuo en el índice especificado. Lanza un error si el
    índice está fuera del rango.

    añadir_variable(self, nueva_variable): Agrega una nueva variable (columna) al dataset. nueva_variable
    debe tener el mismo número de elementos que el número de individuos existentes.

    eliminar_variable(self, index): Elimina la variable en el índice especificado. Lanza un error si el 
    índice está fuera del rango de variables.