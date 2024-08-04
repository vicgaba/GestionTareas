import datetime
import json

class Tarea:
    def __init__(self, id, titulo, descripcion, fecha_ingreso, fecha_vencimiento, estado):
        self.id = self.validar_id(id)
        self.titulo = self.validar_titulo(titulo)
        self.descripcion = descripcion
        self.fecha_ingreso = fecha_ingreso
        self.fecha_vencimiento = self.validar_fecha_vencimiento(fecha_vencimiento)
        self.estado = self.validar_estado(estado)

    def __str__(self):
        return f"{self.descripcion} - Ingreso: {self.fecha_ingreso} - Vencimiento: {self.fecha_vencimiento} - Estado: {self.estado}"
    
    @property
    def id(self):
        return self.__id
    @property
    def titulo(self):
        return self.__titulo
    @property
    def descripcion(self):
        return self.__descripcion
    @property
    def fecha_ingreso(self):
        return self.__fecha_ingreso
    @property
    def fecha_vencimiento(self):
        return self.__fecha_vencimiento
    @property
    def estado(self):
        return self.__estado
    @fecha_ingreso.setter
    def fecha_ingreso(self, fecha_ingreso):
        self.__fecha_ingreso = fecha_ingreso
    @fecha_vencimiento.setter
    def fecha_vencimiento(self, fecha_vencimiento):
        self.__fecha_vencimiento = self.validar_fecha_vencimiento(fecha_vencimiento)
        return self.__fecha_vencimiento
    @estado.setter
    def estado(self, estado):
        self.__estado = self.validar_estado(estado)
    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion
    @id.setter
    def id(self, id):
        self.__id = self.validar_id(id)

    @titulo.setter
    def titulo(self, titulo):
        self.__titulo = self.validar_titulo(titulo)
        return self.__titulo
    
    def validar_titulo(self, titulo):
        if not isinstance(titulo, str) or not titulo.strip():
            raise ValueError("El título no puede estar vacío.")
        return titulo
    
    def validar_id(self, id):
        #ToDo validar que el id no exista para los nuevos y si exista para update y delete
        if not isinstance(int(id), int) or int(id) <= 0:
            raise ValueError("El ID debe ser un número entero positivo.")
        return id

    def validar_fecha_vencimiento(self, fecha_vencimiento):
        try:
            if fecha_vencimiento < datetime.datetime.now().strftime('%Y-%m-%d'):
                raise ValueError("La fecha de vencimiento no puede ser en el pasado.")
        except ValueError as e:
            raise ValueError(f"Fecha de vencimiento inválida: {e}")
        return fecha_vencimiento
    
    def validar_estado(self, estado):
        if estado not in ["pendiente", "en progreso", "completada"]:
            raise ValueError("Estado inválido. Debe ser 'pendiente', 'en progreso' o 'completada'.")
        return estado
    
    def to_dict(self):
        return {
            "id": self.__id,
            "titulo": self.__titulo,
            "descripcion": self.__descripcion,
            "fecha_ingreso": self.__fecha_ingreso,
            "fecha_vencimiento": self.__fecha_vencimiento,
            "estado": self.__estado
        }

class GestionTareas:
    def __init__(self, archivo):
        self.archivo = archivo

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            datos = []
        return datos
    def agregar_tarea(self, tarea):
        datos = self.leer_datos()
        datos.append(tarea.to_dict())
        self.guardar_datos(datos)
        print("Tarea agregada correctamente.")

    def guardar_datos(self, datos):
        with open(self.archivo, 'w') as file:
            json.dump(datos, file, indent=4)
    def mostrar_tareas(self):
        datos = self.leer_datos()
        if not datos:
            print("No hay tareas registradas.")
        else:
            for tarea in datos:
                print(Tareas(**tarea))
        print("-----------------------------------------------------------------------------")

    def eliminar_tarea(self, descripcion):
        datos = self.leer_datos()
        datos_filtrados = [tarea for tarea in datos if tarea["descripcion"] != descripcion]
        if len(datos_filtrados) == len(datos):
            print(f"No se encontró una tarea con la descripción '{descripcion}'.")
        else:
            self.guardar_datos(datos_filtrados)
            print(f"Tarea con descripción '{descripcion}' eliminada correctamente.")