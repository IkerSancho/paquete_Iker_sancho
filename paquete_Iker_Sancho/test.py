import py_s4 as s4
import py_utils as utils


variable = [5.1, 3.5, 1.4, 3, 56]


data_num = [[1.1, 3.5, 11.4],
            [4.9, 3.1, 34.3],
            [6.2, 3.60, 9.2],
            [5.9, 3.12,  44],
            [5.3, 3.28,  90],
            [2.5, 3.9, 10.9],
            [1.4, 3.58,  80],
            [0.8, 3.72,  20]]

data_cat = [["A", "B", "C"],
            ["B", "C", "A"],
            ["A", "B", "B"],
            ["A", "C", "B"],]

data_num_cat = [[1.2, 2.2, 1.1, "A", "B"], 
                [1.3, 4.2, 2.1, "B", "A"], 
                [1.4, 3.2, 3.1, "B", "B"], 
                [1.5, 2.2, 4.1, "C", "B"], 
                [1.6, 1.2, 1.1, "C", "A"],
                [5.3, 3.2, 2.1, "A", "C"]]

data_supervs = [[1.2, 1.0, 4.2, "A", "1"],
                [2.5, 0.1, 4.7, "A", "0"],
                [3.1, 0.7, 3.0, "B", "1"],
                [1.9, 0.3, 4.6, "A", "0"],
                [2.4, 0.0, 3.2, "B", "0"],]



#===================================#
#     Creación y visualización      #
# de los dataset y sus dimensiones  #
#===================================#
try:
    dataset_num = s4.S4Dataset(data_num)

    dataset_cat = s4.S4Dataset(data_cat)

    dataset_num_cat = s4.S4Dataset(data_num_cat)

    dataset_supervs = s4.S4Dataset(data_supervs)

except (TypeError, ValueError, IndexError) as e:
    print("Error:", e)


'''
#========================#
# Funciones de clase s4  #
#========================#
print(dataset_num_cat)

dataset_num_cat.print_dataset_data()

dataset_num_cat.añadir_variable([0,0,0,"C","C"])
dataset_num_cat.print_dataset_data()

dataset_num_cat.eliminar_variable(3)
dataset_num_cat.print_dataset_data()

dataset_num_cat.añadir_variable(["A","B","C"])
dataset_num_cat.print_dataset_data()

dataset_num_cat.eliminar_variable(5)
dataset_num_cat.print_dataset_data()
'''

#========================#
# Discretización - anch  #
#========================#
print("\n")
num_intervalos = 3
discretized_dataset, bins_dict = utils.igual_anchura(dataset_num_cat, num_intervalos)
discretized_dataset.print_dataset_data()
print("Intervalos (igual anchura):", bins_dict)
print("\n")
discretized_dataset, bins_dict = utils.igual_anchura(variable, num_intervalos)
print("Datos discretizados (igual anchura):", discretized_dataset)
print("Intervalos (igual anchura):", bins_dict)
#========================#


#========================#
# Discretización - frec  #
#========================#
print("\n")
num_intervalos = 3
discretized_dataset, bins_dict = utils.igual_frecuencia(dataset_num_cat, num_intervalos)
discretized_dataset.print_dataset_data()
print("Intervalos (igual frecuencia):", bins_dict)
print("\n")
discretized_dataset, bins_dict = utils.igual_frecuencia(variable, num_intervalos)
print(discretized_dataset)
print("Intervalos (igual frecuencia):", bins_dict)
#========================#

'''
#========================#
# Normalización          #
#========================#
print("\n")
normalized_dataset = utils.normalizar_dataset(dataset_num_cat)
normalized_dataset.print_dataset_data()
print("\n")
#normalized_dataset = utils.normalizar_dataset(variable)
#normalized_dataset = [round(elem, 3) for elem in normalized_dataset]
#print("Datos normalizados:", normalized_dataset)
#========================#


#========================#
# Estandarización        #
#========================#
print("\n")
estandarized_dataset = utils.estandarizar_dataset(dataset_num_cat)
estandarized_dataset.print_dataset_data()
print("\n")
estandarized_dataset = utils.estandarizar_dataset(variable)
estandarized_dataset = [round(elem, 3) for elem in estandarized_dataset]
print("Datos estandarizados:", estandarized_dataset)
#========================#


#========================#
# Correlación            #
#========================#
print("\n")
correlaciones = utils.calcular_correlacion(dataset_num_cat)
for pares, info in correlaciones.items():
        print(f"Variables: {pares}\n\tTipo: {info['tipo']}\n\tValor: {info['valor']}\n")
#========================#


#========================#
# Métricas               #
#========================#
# DataSet NO supervisado
resultados = utils.calcular_metricas(dataset_num_cat) 
for variable, metricas in resultados.items():
    print(f"Variable: {variable}")
    for nombre_metrica, valor in metricas.items():
        print(f"\tMétrica: {nombre_metrica}")
        print(f"\tValor: {round(valor, 2) if isinstance(valor, float) else valor}\n")

# DataSet supervisado
resultados = utils.calcular_metricas(dataset_supervs, variable_clase=4, supervisado=True) 
for variable, metricas in resultados.items():
    print(f"Variable: {variable}")
    for nombre_metrica, valor in metricas.items():
        print(f"\tMétrica: {nombre_metrica}")
        print(f"\tValor: {round(valor, 2) if isinstance(valor, float) else valor}\n")
#========================#


#========================#
# Graficaciones          #
#========================#
utils.plot_auc(resultados)
utils.plot_matriz_correlacion(correlaciones)
#========================#


#========================#
# Filtrado de datos      #
#========================#
#Filtrar las columnas con una varianza superior a 10
print("\ncaso0")
dataset_num_cat.print_dataset_data()
utils.filtrar_por_condicion(dataset_num_cat, tipo="Varianza", condicion="mayor", umbral=10) 
print("\n")
dataset_num_cat.print_dataset_data()


#Filtrar las columnas con una Entropia diferente a 1.0
print("\ncaso1")
dataset_cat.print_dataset_data()
utils.filtrar_por_condicion(dataset_cat, tipo="Entropia", condicion="desigual", umbral=1.0) 
print("\n")
dataset_cat.print_dataset_data()

#Filtrar las columnas con un AUC igual a 1.0 en un dataSet supervisado
print("\ncaso2")
dataset_supervs.print_dataset_data()
utils.filtrar_por_condicion(dataset_supervs, tipo="AUC", condicion="igual", umbral=1.0, supervisado=True, variable_clase=4) 
print("\n")
dataset_supervs.print_dataset_data()
#========================#
'''
