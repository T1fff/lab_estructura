import json
from datetime import datetime

class Pelicula:
    def __init__(self, id, titulo, director, año, genero, precio):
        self.id = id
        self.titulo = titulo
        self.director = director
        self.año = int(año)
        self.genero = genero
        self.precio = float(precio)

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'director': self.director,
            'año': self.año,
            'genero': self.genero,
            'precio': self.precio
        }


import json
from datetime import datetime

class Pelicula:
    def __init__(self, id, titulo, director, año, genero, precio):
        self.id = id
        self.titulo = titulo
        self.director = director
        self.año = int(año)
        self.genero = genero
        self.precio = float(precio)

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'director': self.director,
            'año': self.año,
            'genero': self.genero,
            'precio': self.precio
        }

class Archivo_Pelicula:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo

    def validar_pelicula(self, pelicula):
        pelicula.id = pelicula.id.strip()
        pelicula.titulo = pelicula.titulo.strip()
        pelicula.director = pelicula.director.strip()
        pelicula.genero = pelicula.genero.strip()

    def agregar_pelicula(self, pelicula):
        self.validar_pelicula(pelicula)
        if self.existe_id(pelicula.id):
            raise ValueError(f"Ya existe una película con el ID {id}")
        else:
            peliculas = self.leer_pelicula()
            peliculas.append(pelicula.to_dict())
            self.actualizar_pelicula(peliculas)

    def existe_id(self, id_pelicula):
        peliculas = self.leer_pelicula()
        return any(pelicula['id'] == id_pelicula for pelicula in peliculas)

    def leer_pelicula(self):
        try:
            with open(self.nombre_archivo, 'r') as archivo:
                return json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def mostrar_peliculas(self):
        peliculas = self.leer_pelicula()
        if peliculas:
          print("Lista de películas:")
          for pelicula in peliculas:
            print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Director: {pelicula['director']}, Año: {pelicula['año']}, Género: {pelicula['genero']}, Precio: {pelicula['precio']}")
        else:
            print("No hay películas en la lista.")

    def actualizar_pelicula(self, peliculas):
      with open(self.nombre_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(peliculas, archivo,ensure_ascii=False ,indent=4)

    def actualizar_info_pelicula(self, id_actualizar, titulo, director, año, genero, precio):
        peliculas = self.leer_pelicula()
        for pelicula in peliculas:
            if pelicula['id'] == id_actualizar:
                pelicula['titulo'] = titulo
                pelicula['director'] = director
                pelicula['año'] = año
                pelicula['genero'] = genero
                pelicula['precio'] = precio
        self.guardar_peliculas(peliculas)

    def eliminar_pelicula(self, id_pelicula):
        if self.existe_id(id_pelicula):
          peliculas = self.leer_pelicula()
          peliculas = [pelicula for pelicula in peliculas if pelicula['id'] != id_pelicula]
          self.actualizar_pelicula(peliculas)

          archivo_compras = Archivo_Compra('compras.json')
          archivo_compras.actualizar_compras_sin_pelicula(peliculas)
        else:
          print("No existe una pelicula con este ID")

    def buscar_pelicula(self, id_pelicula):
        peliculas = self.leer_pelicula()
        for pelicula in peliculas:
            if pelicula['id'] == id_pelicula:
                return pelicula
        return None  

    def buscar_pelicula_por_director(self, director_pelicula):
        peliculas = self.leer_pelicula()
        peliculas_encontradas = [
            pelicula for pelicula in peliculas 
            if pelicula['director'].lower() == director_pelicula.lower()
        ]
        return peliculas_encontradas

    def buscar_pelicula_por_titulo(self, titulo_pelicula):
        peliculas = self.leer_pelicula()
        peliculas_encontradas = [
            pelicula for pelicula in peliculas 
            if pelicula['titulo'].lower() == titulo_pelicula.lower()
        ]
        return peliculas_encontradas

    def buscar_pelicula_por_genero(self, genero_pelicula):
        peliculas = self.leer_pelicula()
        peliculas_encontradas = [
            pelicula for pelicula in peliculas 
            if pelicula['genero'].lower() == genero_pelicula.lower()
        ]
        return peliculas_encontradas

    def buscar_pelicula_por_año(self, año_pelicula):
        peliculas = self.leer_pelicula()
        peliculas_encontradas = [
            pelicula for pelicula in peliculas 
            if pelicula['año'] == año_pelicula
        ]
        return peliculas_encontradas

    def peliculas_recientes(self, cantidad):
        peliculas = self.leer_pelicula()
        peliculas_recientes = sorted(
            peliculas, key=lambda p: p['año'], reverse=True
        )[:cantidad]
        return peliculas_recientes

archivo_peliculas = Archivo_Pelicula('peliculas.json')

class Clientes:
    def __init__(self, id, nombre, correo, direccion):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.direccion = direccion

    def to_dict(self):
        return {
            'id':self.id,
            'nombre': self.nombre,
            'correo': self.correo,
            'direccion': self.direccion
        }

class Archivo_Clientes:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo

    def validar_cliente(self, cliente):
        cliente.id = cliente.id.strip()
        cliente.nombre = cliente.nombre.strip()
        cliente.correo = cliente.correo.strip()
        cliente.direccion = cliente.direccion.strip()

    def agregar_cliente(self, cliente):
        self.validar_cliente(cliente)
        if self.existe_id(cliente.id):
            return f"Ya existe un cliente con el ID {cliente.id}"
        else:
            clientes = self.leer_clientes()
            clientes.append(cliente.to_dict())
            self.actualizar_clientes(clientes)

    def existe_id(self, id_cliente):
        clientes = self.leer_clientes()
        return any(cliente['id'] == id_cliente for cliente in clientes)

    def leer_clientes(self):
        try:
            with open(self.nombre_archivo, 'r') as archivo:
                return json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def buscar_cliente(self, id_cliente):
        clientes = self.leer_clientes()
        aux = 0
        for cliente in clientes:
            if cliente['id'] == id_cliente:
                cliente_encontrado = cliente
                aux = 1
        if aux != 1:
          print("No se encontro el cliente")
        elif aux == 1:
          print(f"ID: {cliente_encontrado['id']}, Nombre: {cliente_encontrado['nombre']}, Correo: {cliente_encontrado['correo']}, Dirección: {cliente_encontrado['direccion']}")


    def mostrar_clientes(self):
        clientes = self.leer_clientes()
        if clientes:
            print("Lista de clientes:")
            for cliente in clientes:
                print(f"ID: {cliente['id']}, Nombre: {cliente['nombre']}, Correo: {cliente['correo']}, Dirección: {cliente['direccion']}")
        else:
            print("No hay clientes en la lista.")

    def actualizar_clientes(self, clientes):
        with open(self.nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(clientes, archivo, ensure_ascii=False, indent=4)

    def actualizar_info_cliente(self, id_actualizar):
        clientes = self.leer_clientes()
        for cliente in clientes:
          if cliente['id'] == id_actualizar:
            cliente['nombre'] = input("Ingrese el nuevo nombre: ")
            cliente['correo'] = input("Ingrese el nuevo correo: ")
            cliente['direccion'] = input("Ingrese la nueva direccion: ")
        self.actualizar_clientes(clientes)


    def eliminar_cliente(self, id_cliente):
      if self.existe_id(id_cliente):
        clientes = self.leer_clientes()
        clientes = [cliente for cliente in clientes if cliente['id'] != id_cliente]
        self.actualizar_clientes(clientes)
        archivo_compras = Archivo_Compra('compras.json')
        archivo_compras.actualizar_compras_sin_cliente(clientes)
      else:
        print("No existe cliente con ese ID")

class Compra:
    def __init__(self, id_compra, id_cliente, id_pelicula, fecha):
        self.id_compra = id_compra
        self.id_cliente = id_cliente
        self.id_pelicula = id_pelicula
        self.fecha = fecha

    def to_dict(self):
        return {
            'id_compra': self.id_compra,
            'id_cliente': self.id_cliente,
            'id_pelicula': self.id_pelicula,
            'fecha': self.fecha
        }

class Archivo_Compra:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo

    def validar_compra(self, compra):
        compra.id_compra = compra.id_compra.strip()
        compra.id_cliente = compra.id_cliente.strip()
        compra.id_pelicula = compra.id_pelicula.strip()
        compra.fecha = compra.fecha.strip()

    def agregar_compra(self, compra):
        self.validar_compra(compra)
        
        if self.existe_id(compra.id_compra, self.leer_compra(), id='id_compra'):
            return f"Ya existe una compra con el ID {compra.id_compra}"
        
        archivo_clientes = Archivo_Clientes('clientes.json')
        archivo_peliculas = Archivo_Pelicula('peliculas.json')

        # Verificar si el ID de cliente existe
        if not self.existe_id(compra.id_cliente, archivo_clientes.leer_clientes(), id='id'):
            return f"No existe un cliente con el ID {compra.id_cliente}"

        # Verificar si el ID de película existe
        if not self.existe_id(compra.id_pelicula, archivo_peliculas.leer_pelicula(), id='id'):
            return f"No existe una película con el ID {compra.id_pelicula}"

        # Si las validaciones son satisfactorias, agregar la compra
        compras = self.leer_compra()
        compras.append(compra.to_dict())
        self.actualizar_compra(compras)

        return "Compra agregada exitosamente."

    def existe_id(self, id_compra, diccionario, id='id'):
      return any(compra[id] == id_compra for compra in diccionario)

    def leer_compra(self):
        try:
            with open(self.nombre_archivo, 'r') as archivo:
                return json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def buscar_compra(self, id_compra):
        compras = self.leer_compra()
        aux = 0
        for compra in compras:
            if compra['id_compra'] == id_compra:
                compra_encontrada = compra
                aux = 1
        if aux != 1:
          print("No se encontro la compra")
        elif aux == 1:
          print(f"ID de Compra: {compra_encontrada['id_compra']}, ID de Cliente: {compra_encontrada['id_cliente']}, ID de Película: {compra_encontrada['id_pelicula']}, Fecha: {compra_encontrada['fecha']}")

    def mostrar_compra(self):
        compras = self.leer_compra()
        if compras:
            print("Lista de compras:")
            for compra in compras:
                print(f"ID de Compra: {compra['id_compra']}, ID de Cliente: {compra['id_cliente']}, ID de Película: {compra['id_pelicula']}, Fecha: {compra['fecha']}")
        else:
            print("No hay compras en la lista.")

    def actualizar_compra(self, compras):
        with open(self.nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(compras, archivo, ensure_ascii=False, indent=4)

    def actualizar_info_compra(self, id_actualizar):
        compras = self.leer_compra()
        for compra in compras:
          if compra['id_compra'] == id_actualizar:
            compra['fecha'] = input("Ingrese la nueva fecha de la compra (YYYY-MM-DD): ")
        self.actualizar_compra(compras)

    def eliminar_compra(self, id_compra):
        compras = self.leer_compra()
        if self.existe_id(id_compra, compras, 'id_compra'):
          compras = [compra for compra in compras if compra['id_compra'] != id_compra]
          self.actualizar_compra(compras)
        else:
          print("No existe compra con este ID")

    def actualizar_compras_sin_cliente(self, lista_clientes):
      compras = self.leer_compra()
      compras_actualizadas = []
      clientes_ids = [cliente['id'] for cliente in lista_clientes]
      for compra in compras:
        if compra['id_cliente'] not in clientes_ids:
            print(f"Compra con ID {compra['id_compra']} tiene un cliente eliminado (ID: {compra['id_cliente']}). Será eliminada.")
        else:
            compras_actualizadas.append(compra)
      self.actualizar_compra(compras_actualizadas)


    def actualizar_compras_sin_pelicula(self, lista_peliculas):
      compras = self.leer_compra()
      compras_actualizadas = []
      peliculas_ids = [pelicula['id'] for pelicula in lista_peliculas]

      for compra in compras:
        if compra['id_pelicula'] not in peliculas_ids:
            print(f"Compra con ID {compra['id_compra']} tiene una película eliminada (ID: {compra['id_pelicula']}). Será eliminada.")
        else:
            compras_actualizadas.append(compra)

      self.actualizar_compra(compras_actualizadas)
