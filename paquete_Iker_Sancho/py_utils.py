import math 
import collections
import numpy as np
import pandas as pd
import seaborn as sns
from . import py_s4 as s4
import matplotlib.pyplot as plt


# Función para determinar si una lista es numérica
# será usada a menudo a lo largo del script
def es_numerica(variable):
    return all(isinstance(x, (int, float)) for x in variable)

# Función para determinar si una columna es continua
def es_continua(columna):
    return all(isinstance(x, (int, float)) for x in columna)



#===================================#
#         DISCRETIZACIÓN            #
#===================================#

# Discretización por Igual Anchura (Equal Width Binning):
# Esta función divide el rango de los datos en intervalos de igual tamaño (anchura).
# Parámetros:
#   - data: el dataset que será discretizado. Puede ser una variable única o un dataset tipo s4.
#   - num_intervalos: número de intervalos en los cuales se divíde el rango de los valores.
# Output:
#   - discretized_data: lista de etiquetas de bin asignadas a cada valor en los datos. Es decir, un
#                       individuo o un conjunto de ellos con valores categóricos
#   - lista_intervalos: lista de tuplas que representan los límites de cada intervalo.
#
#  Ejemplo:
#  si el rango de los valores de un atributo es de 0 a 10 y deseas 2 intervalos 
#  cada intervalo tendría una anchura de 5: (0, 5) (6, 10).

def igual_anchura(dataset, num_intervalos):
    
    # Subrutina para discretizar una lista de valores
    # los outputs y los inputs son los mismos que los
    # de la función en si.
    def discretizar_unico(datos, num_intervalos):

        minimo = min(datos)
        maximo = max(datos)
        tam_intervalo = (maximo - minimo) / num_intervalos
        intervalos = [(minimo + i * tam_intervalo, minimo + (i + 1) * tam_intervalo) for i in range(num_intervalos)]
        
        datos_discretizados = []
        
        for valor in datos:

            # Asigna cada valor al intervalo adecuado
            for indice, (lim_inferior, lim_superior) in enumerate(intervalos):
                
                # Incluye el valor en el último intervalo si es igual al límite superior
                if lim_inferior <= valor < lim_superior or (indice == num_intervalos - 1 and valor == lim_superior):
                    datos_discretizados.append(f'Bin_{indice+1}')
                    break
        
        return datos_discretizados, intervalos

    # Caso 1: Discretizar cada columna si 'dataset' 
    # es una instancia de dataset s4
    if isinstance(dataset, s4.S4Dataset):

        columnas = list(zip(*dataset.data))  
        dataset_discretizado = []
        lista_intervalos = []
        
        # Se aplica la discretización por cada columna
        for columna in columnas:
            datos_discretizados, intervalos = discretizar_unico(columna, num_intervalos)
            dataset_discretizado.append(datos_discretizados)  
            lista_intervalos.append(intervalos) 
        
        # Se revierte la transposición para devolver la estructura original
        # y se convierte en un objeto s4 
        dataset_discretizado = [list(elem) for elem in list(zip(*dataset_discretizado))]
        
        try:
            dataset_discretizado = s4.S4Dataset(dataset_discretizado)
        except (TypeError, ValueError, IndexError) as e:
            print("Error:", e)

        return dataset_discretizado, lista_intervalos

    # Caso 2: Discretizar directamente una lista de valores si no es S4Dataset
    else:
        return discretizar_unico(dataset, num_intervalos)





# Discretización por Igual Frecuencia (Equal Frequency Binning):
# Esta función divide los datos en intervalos que contienen aproximadamente la misma cantidad de individuos.
# Parámetros:
#   - data: el dataset a discretizar. Puede ser una variable única o un dataset s4.
#   - num_intervalos: número de intervalos en los cuales se dividen los datos.
# Output:
#   - discretized_data: lista de etiquetas de bin asignadas a cada valor en los datos. Es decir, un
#                       individuo o un conjunto de ellos con valores categóricos
#   - lista_intervalos: lista de tuplas que representan los límites de cada intervalo.
#
# Eejemplo:
# si tienes 10 datos y deseas 2 intervalos, cada intervalo tendría 5 datos y,
# independientemente del valor de los mismos

def igual_frecuencia(dataset, num_intervalos):

    # Subrutina para discretizar una lista de valores
    # los outputs y los inputs son los mismos que los
    # de la función en si.
    def discretizar_unico(dataset, num_intervalos):
        
        datos_ordenados = sorted(dataset)
        num_elementos = len(dataset)
        # Se calcula el tamaño de cada intervalo dividiendo el número de 
        # elementos por el número de intervalos
        tam_intervalo = num_elementos // num_intervalos

        intervalos = []
        datos_discretizados = [None] * num_elementos

        for i in range(num_intervalos):
            
            # Se calculan los índices inferiores y superiores para el intervalo actual
            indice_inferior = i * tam_intervalo
            indice_superior = indice_inferior + tam_intervalo if i < num_intervalos - 1 else num_elementos

            # Determina los límites inferior y superior del intervalo
            limite_inferior = datos_ordenados[indice_inferior]
            limite_superior = datos_ordenados[indice_superior - 1] if indice_superior > indice_inferior else limite_inferior
            
            intervalos.append((limite_inferior, limite_superior))

            for j in range(indice_inferior, indice_superior):
                valor = datos_ordenados[j]

                for indice, v in enumerate(dataset):
                    if v == valor and datos_discretizados[indice] is None:
                        datos_discretizados[indice] = f'Bin_{i+1}'
                        break

        return datos_discretizados, intervalos

    # Caso 1: Discretizar cada columna si 'dataset' 
    # es una instancia de dataset s4    
    if isinstance(dataset, s4.S4Dataset):
        
        columnas = list(zip(*dataset.data))
        dataset_discretizado = []
        lista_intervalos = []
        
        # Se aplica la discretización por cada columna
        for valores in columnas:
            
            datos_discretizados, intervalos = discretizar_unico(valores, num_intervalos)
            dataset_discretizado.append(datos_discretizados)
            lista_intervalos.append(intervalos)
        
        # Se reestructura el dataset discretizado y se convierte en un objeto s4
        dataset_discretizado = [list(elem) for elem in list(zip(*dataset_discretizado))]

        try:
            dataset_discretizado = s4.S4Dataset(dataset_discretizado)
        except (TypeError, ValueError, IndexError) as e:
            print("Error:", e)

        return dataset_discretizado, lista_intervalos

    # Caso 2: Discretizar directamente una lista de valores si no es S4Dataset    
    else:
        return discretizar_unico(dataset, num_intervalos)




#===================================#
#          NORMALIZACIÓN            #
#===================================#

# Función para normalizar las variables numéricas en un dataset o una variable única.
# La normalización ajusta los valores de los datos a un rango entre 0 y 1.
# Parámetros:
#   - dataset: dataset a normalizar. Puede ser una variable numérica o un dataset tipo s4.
# Output:
#   - datos_transformados: variable numérica única o conjunto de datos con los valores 
#                          normalizados para cada columna numérica.

def normalizar_dataset(dataset):

    # Caso 1: Si dataset es una variable única (lista de valores numéricos)
    if isinstance(dataset, list) and es_numerica(dataset):
        
        min_val = min(dataset)
        max_val = max(dataset)
        rango = max_val - min_val
        
        # Evitar división por cero
        if rango == 0:
            return [0] * len(dataset)  
        
        else:
            return [(x - min_val) / rango for x in dataset]

    # Caso 2: Si el dataset es una instancia del tipo s4
    datos_transformados = []
    
    for fila in dataset.data:
        datos_transformados.append(fila[:])  
    
    # Normalizar cada columna por separado
    num_columnas = dataset.numero_variables
    
    for col in range(num_columnas):
        columna = []
        
        for fila in datos_transformados:
            valor = fila[col]
            
            if isinstance(valor, (int, float)):
                columna.append(valor)
        
        # Calcular mínimo, máximo y rango de la columna si tiene valores numéricos
        if columna:
            
            min_val = min(columna)
            max_val = max(columna)
            rango = max_val - min_val
            
            for fila in datos_transformados:
                
                if isinstance(fila[col], (int, float)):    
                    fila[col] = (fila[col] - min_val) / rango if rango != 0 else 0

    # Se reestructura la salida como un objeto s4
    try:
        datos_transformados = s4.S4Dataset(datos_transformados)
    except (TypeError, ValueError, IndexError) as e:
        print("Error:", e)

    return datos_transformados



#===================================#
#        ESTANDARIZACIÓN            #
#===================================#

# Función para estandarizar las variables numéricas en un dataset o en una variable único.
# La estandarización ajusta los valores de los datos de cada columna para que tengan una 
# media de 0 y desviación estándar de 1.
# Parámetros:
#   - dataset: datset a estandarizar. Puede ser una lista de valores numéricos o un dataset s4.
# Output:
#   - datos_transformados: conjunto de datos con los valores estandarizados para cada columna numérica.

def estandarizar_dataset(dataset):

    # Caso 1:  Si dataset es una variable único (lista de valores numéricos)
    if isinstance(dataset, list) and es_numerica(dataset):
        
        media = sum(dataset) / len(dataset)
        desviacion = (sum((x - media) ** 2 for x in dataset) / len(dataset)) ** 0.5
        
        # Evitar división por cero
        if desviacion == 0:
            return [0] * len(dataset)  
        
        else:
            return [(x - media) / desviacion for x in dataset]

    # Caso 2: Si dataset es un dataset s4 completo
    datos_transformados = []
    
    for fila in dataset.data:
        datos_transformados.append(fila[:])  
    
    # Estandarizar cada columna por separado
    num_columnas = dataset.numero_variables
    
    for col in range(num_columnas):
        columna = []
    
        for fila in datos_transformados:
            valor = fila[col]
    
            if isinstance(valor, (int, float)):
                columna.append(valor)
        
        # Calcular media y desviación estándar si
        # los valores de la columna son numéricos
        if columna:
            media = sum(columna) / len(columna)
            desviacion = (sum((x - media) ** 2 for x in columna) / len(columna)) ** 0.5
    
            for fila in datos_transformados:
    
                if isinstance(fila[col], (int, float)):
                    fila[col] = (fila[col] - media) / desviacion if desviacion != 0 else 0

    # Se reestructura la salida como un objeto s4
    try:
        datos_transformados = s4.S4Dataset(datos_transformados)
    except (TypeError, ValueError, IndexError) as e:
        print("Error:", e)

    return datos_transformados



#===================================#
#          CORRELACIÓN              #
#===================================#

# Función para calcular la correlación de Pearson y la información mutua entre
# pares de variables en un dataset.
#   - numérica - numérica: Correlación de Pearson
#   - categórica - categórica: Información mutua
#   - numerica - categórica: Na
# Parámetros:
#   - dataset: un dataset del tipo s4
# Output:
#   - resultados: diccionario que contiene la correlación para cada par de 
#                 variables compatibles, donde cada clave es el par de variables
#                 y el valor es otro diccionario con el tipo de correlación
#                 y el valor calculado.

def calcular_correlacion(dataset):

    # Función para calcular la correlación de Pearson
    # entre dos variables numéricas.
    def calcular_pearson(x, y):
        
        n = len(x)
        
        media_x = sum(x) / n
        media_y = sum(y) / n
        var_x   = sum((xi - media_x) ** 2 for xi in x) / n
        var_y   = sum((yi - media_y) ** 2 for yi in y) / n
        cov_xy  = sum((xi - media_x) * (yi - media_y) for xi, yi in zip(x, y)) / n
        
        return cov_xy / ((var_x * var_y) ** 0.5) if var_x and var_y else 0

    # FUnción para calcular la información mutua entre
    # dos variables de categóricas
    def calcular_informacion_mutua(x, y):
        
        # Para calcular la frecuencia aprovecharemos
        # la librería collections
        total = len(x)
        freq_x  = collections.Counter(x)
        freq_y  = collections.Counter(y)
        freq_xy = collections.Counter(zip(x, y))
        
        info_mutua = 0
        
        for (xi, yi), count_xy in freq_xy.items():
            p_xy = count_xy / total
            p_x = freq_x[xi] / total
            p_y = freq_y[yi] / total
            info_mutua += p_xy * math.log(p_xy / (p_x * p_y), 2)
        
        return info_mutua

    # Se caclulan los resultados para cada par
    # de variables compatibles:
    # numérica - numérica :: Pearson
    # categórica - numérica :: incompatible
    # categórica - categórica :: Info mutua
    resultados = {}
    
    for i in range(dataset.numero_variables):
        
        for j in range(i + 1, dataset.numero_variables):
            var_i = [row[i] for row in dataset.data]
            var_j = [row[j] for row in dataset.data]

            if es_numerica(var_i) and es_numerica(var_j):
                correlacion = calcular_pearson(var_i, var_j)
                tipo = "Correlación de Pearson"
                resultados[f"Var_{i+1}-Var_{j+1}"] = {"tipo": tipo, "valor": correlacion}

            elif not(es_numerica(var_i)) and not(es_numerica(var_j)):
                correlacion = calcular_informacion_mutua(var_i, var_j)
                tipo = "Información mutua"
                resultados[f"Var_{i+1}-Var_{j+1}"] = {"tipo": tipo, "valor": correlacion}

            else:
                resultados[f"Var_{i+1}-Var_{j+1}"] = {"tipo": "incompatibles", "valor": "-"}

    return resultados



#===================================#
#           MÉTRICAS                #
#===================================#

# Función para calcular la varianza de una lista de valores numéricos.
# Parámetros:
#   - columna: lista de valores numéricos.
# Output:
#   - varianza: valor de la varianza calculada para la lista de entrada.

def calcular_varianza(columna):
    media = sum(columna) / len(columna)
    varianza = sum((x - media) ** 2 for x in columna) / len(columna)
    return varianza


# Función para calcular el AUC (Área bajo la curva ROC) para una variable 
# continua en relación a una clase binaria.
# Parámetros:
#   - clase: lista que representa la clase de cada individuo.
#   - columna: lista de valores numéricos continuos a evaluar en relación a la clase.
# Output:
#   - auc: valor del AUC calculado para la variable continua.

def calcular_auc(clase, columna):
    
    # Por convención en mi s4 se pasarán las clases categóricas
    # y binarias como strings.
    clase = [int(c) for c in clase]
    
    # 1- Convertir los datos en pares (valor, etiqueta)
    # 2- Contar el número de positivos y negativos
    # 3- Calcular AUC usando la fórmula de suma de rangos
    
    pares = list(zip(columna, clase))
    pares.sort(key=lambda x: x[0])

    positivos = sum(clase)  
    negativos = len(clase) - positivos  

    rank_sum = 0
    for rank, (valor, etiqueta) in enumerate(pares):
        if etiqueta == 1:  
            rank_sum += rank + 1 

    auc = (rank_sum - positivos * (positivos + 1) / 2) / (positivos * negativos)
    return auc


# Función para calcular la entropía de una columna discreta.
# La entropía mide la incertidumbre o el desorden en los valores de la columna.
# Parámetros:
#   - columna: lista de valores discretos de una columna a evaluar.
# Output:
#   - entropia: valor de la entropía calculada para la columna.

def calcular_entropia(columna):
    
    contador = collections.Counter(columna)
    total = sum(contador.values())
    entropia = 0
    
    for count in contador.values():
        probabilidad = count / total 
        
        if probabilidad > 0:
            entropia -= probabilidad * (math.log(probabilidad) / math.log(2))  
    
    return entropia


# Función para calcular la varianza, AUC y entropía para cada variable en un dataset.
# Evalúa si cada variable es continua o discreta y calcula la métrica adecuada.
# En caso de tener un dataset supervisado, calcula el AUC respecto a la variable clase.
# Parámetros:
#   - dataset: dataset del tipo s4.
#   - variable_clase: índice de la variable clase en el dataset (opcional).
#   - supervisado: booleano que indica si el dataset es supervisado o no
# Output:
#   - resultados: diccionario que contiene las métricas calculadas (Varianza, AUC, Entropía)
#                 para cada variable según su tipo.

def calcular_metricas(dataset, variable_clase=None, supervisado=False):
    
    # Transponer los datos para acceder a las columnas fácilmente
    variables = list(zip(*dataset.data))
    resultados = {}

    # Extraer la variable clase como una lista si hace falta
    clase = [row[variable_clase] for row in dataset.data] if supervisado else None 

    for i, columna in enumerate(variables):
        
        # Saltar la variable clase
        if i == variable_clase:
            continue  
        
        if es_continua(columna):
            varianza = calcular_varianza(columna)
            auc = calcular_auc(clase, columna) if supervisado and len(set(clase)) == 2 else None
            resultados[f'Variable_{i}'] = {'Varianza': varianza, 'AUC': auc}
        
        else:
            entropia = calcular_entropia(columna)
            resultados[f'Variable_{i}'] = {'Entropía': entropia}

    return resultados



#===================================#
#           GRÁFICOS                #
#===================================#

# Función para graficar los valores AUC de variable numérica.    
# Parámetros:
#   - resultados: diccionario que contiene las métricas calculadas 
#                 (Varianza, AUC, Entropía) para cada variable según su tipo.
# Output:
#   - 

def plot_auc(resultados):

    variables  = []
    auc_values = []

    # Guaradar las variables y los valores AUC
    # correspondientes a cada una.
    for variable, metricas in resultados.items():
        
        for nombre_metrica, valor in metricas.items():
            
            if nombre_metrica == 'AUC':
                variables.append(variable)
                auc_values.append(valor)
    
    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    sns.barplot(x=auc_values, y=variables, palette="viridis")
    plt.xlabel('AUC')
    plt.ylabel('Variable')
    plt.title('AUC por Variable Numérica')
    plt.show()


# Función para calcula la matriz de correlaciones / información mutua.
# Printea la matriz y plotea un heatMap acorde a la misma.
# Parámetros:
#   - correlaciones: diccionario que contiene la correlación para cada par de 
#                  variables compatibles, donde cada clave es el par de variables
#                  y el valor es otro diccionario con el tipo de correlación
#                  y el valor calculado.
# Output:
#   -

def plot_matriz_correlacion(correlaciones):

    # Obtención de la matriz de correlaciones partiendo 
    # del objeto correlaciones.
    #   - Buscar las n variables Ddividiendo los nombres "var_i-var_j"
    #   - Inicializar una matriz con np.nan-s. Se usarán np.nan-s para
    #     asignar ese valor a las variables incompatibles y no tener
    #     conflictos en el heatmap
    #   - Rellenar la matriz con los valores correspondientes

    variables = []
    
    for pares in correlaciones.keys():
        var1, var2 = pares.split('-')
    
        if var1 not in variables:
            variables.append(var1)
        
        if var2 not in variables:
            variables.append(var2)

    variables.sort()    
    matriz_correlacion = pd.DataFrame(np.nan, index=variables, columns=variables)
    np.fill_diagonal(matriz_correlacion.values, 1)

    for pares, info in correlaciones.items():
        var1, var2 = pares.split('-')
        
        if info['tipo'] != 'incompatibles':
            matriz_correlacion.loc[var1, var2] = info['valor']
            matriz_correlacion.loc[var2, var1] = info['valor']
    
    print(matriz_correlacion)

    plt.figure(figsize=(10, 8))
    sns.heatmap(matriz_correlacion, annot=True, fmt=".2f", cmap="coolwarm", square=True, cbar_kws={"shrink": .8})
    plt.title("Matriz de Correlación / Información Mutua")
    plt.show()


#===================================#
#           FILTRADO                #
#===================================#

# Función filtrar los datos del dataSet en función de los
# requerimientos especificádos.
# Parámetros:
#   - dataset: un objeto del tipo dataset s4
#   - tipo: el tipo métrica que queremos aplicar en el filtro ("AUC", "Varianza" o "Entropia")
#   - condicion: la condicion que se aplicará sobre el umbral numerico que sea 
#                decidido ()"menor", "mayor", "igual" o "desigual").
#   - umbral: el umbral numerico con el que será comparada la metrica especifica de
#             una columna para ser filtrada o no
#   - supervisado: booleano que indíca si un dataset es supervisado o no
#   - variable_clase: el índice de la variable que funciona como clase en los datasets supervisados
# Output:
#   -

def filtrar_por_condicion(dataset, tipo, condicion, umbral, supervisado=False, variable_clase=None):

    if condicion not in ["menor", "mayor", "igual", "desigual"]:
        print("Condición no valida. Condiciones válidas:\n\tmenor\n\tmayor\n\tigual\n\tdesigual") 
        return

    if tipo not in ["AUC", "Varianza", "Entropia"]:
        print("Tipo no válido. Los tipos válidos son:\n\tAUC\n\tVarianza\n\tEntropia")
        return
    
    # Función que evalúa la condición sobre un valor dado.
    # (Es usada para evitar redundancias en el código)
    def cumple_condicion(valor):
        
        if condicion == "menor":
            return valor < umbral
        
        elif condicion == "mayor":
            return valor > umbral
        
        elif condicion == "igual":
            return valor == umbral
        
        elif condicion == "desigual":
            return valor != umbral
        
        else:
            print("Condición no válida")
            return None

    clase = [row[variable_clase] for row in dataset.data] if supervisado else None
    indices_a_eliminar = []
    
    for i, columna in enumerate(zip(*dataset.data)):

        # Evitar que la variable clase se elimine en un dataset supervisado
        if supervisado and i == variable_clase:
            continue

        # Seleccionar métrica según el tipo especificado
        if supervisado and tipo == "AUC":
            valor_metrica = calcular_auc(clase, columna)
        
        elif es_numerica(columna) and tipo == "Varianza":
            valor_metrica = calcular_varianza(columna)
        
        elif not es_numerica(columna) and tipo == "Entropia":
            valor_metrica = calcular_entropia(columna)
        
        # Filtrar variable si no cumple la condición
        if cumple_condicion(valor_metrica):
            indices_a_eliminar.append(i)

    # Ordenar índices en orden descendente y eliminar columnas
    for i in sorted(indices_a_eliminar, reverse=True):
        dataset.eliminar_variable(i)