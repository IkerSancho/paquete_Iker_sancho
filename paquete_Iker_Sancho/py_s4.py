class S4Dataset:
    
    # Inicialización
    def __init__(self, data):
        
        # Validación de tipo para asegurar que el dataSet es una lista de listas
        if not isinstance(data, list) or not all(isinstance(row, list) for row in data):
            raise TypeError("El atributo 'data' debe ser una lista de listas.")
        
        # Comprobar que todas las filas tienen la misma longitud
        numero_variables = len(data[0]) if data else 0
        if any(len(row) != numero_variables for row in data):
            raise ValueError("Cada fila debe tener el mismo número de variables (columnas).")
        
        # Asignar los datos y dimensiones
        self.data = data
        self.numero_individuos = len(data)
        self.numero_variables = numero_variables


    # Definición del output para el print    
    def __repr__(self):
        return f"<S4Dataset data=\n{self.data}\n numero_individuos={self.numero_individuos}, numero_variables={self.numero_variables}>"


    # Printeo de los datos del dataSet
    def print_dataset_data(self):
        for elem in self.data: 
            print(elem)


    # Método para añadir un individuo al dataSet
    def añadir_individuo(self, new_individual):

        if len(new_individual) != self.numero_variables:
            raise ValueError(f"El nuevo individuo debe tener {self.numero_variables} variables.")
        
        self.data.append(new_individual)
        self.numero_individuos += 1


    # Método para eliminar un individuo del dataSet
    def eliminar_individuo(self, index):
       
        if index < 0 or index >= self.numero_individuos:
            raise IndexError("Índice fuera de rango.")
        
        del self.data[index]
        self.numero_individuos -= 1


    # Método para añadir una nueva variable (columna) al dataSet
    def añadir_variable(self, nueva_variable):
        
        if len(nueva_variable) != self.numero_individuos:
            raise ValueError(f"La nueva variable debe tener {self.numero_individuos} valores.")
        
        for i, valor in enumerate(nueva_variable):
            self.data[i].append(valor)
        
        self.numero_variables += 1


    # Método para eliminar la i-ésima variable (columna) del dataSet
    def eliminar_variable(self, index):
        
        if index < 0 or index >= self.numero_variables:
            raise IndexError("Índice de variable fuera de rango.")
        
        for row in self.data:
            del row[index]
        
        self.numero_variables -= 1

