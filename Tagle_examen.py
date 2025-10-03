
from abc import ABC, abstractmethod
from datetime import datetime


class Libro:
    """Representa un libro en la biblioteca"""
    def __init__(self, id, titulo, autor, isbn, disponible=True):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = disponible


class Prestamo:
    """Representa un préstamo de libro a un usuario"""
    def __init__(self, id, libro_id, usuario, fecha):
        self.id = id
        self.libro_id = libro_id
        self.usuario = usuario
        self.fecha = fecha
        self.devuelto = False



class EstrategiaBusqueda(ABC):
    

    @abstractmethod
    def buscar(self, libros, valor):
        pass


class BusquedaPorTitulo(EstrategiaBusqueda):

    def buscar(self, libros, valor):
        resultados = []
        for libro in libros:
            if valor.lower() in libro.titulo.lower():
                resultados.append(libro)
        return resultados


class BusquedaPorAutor(EstrategiaBusqueda):

    def buscar(self, libros, valor):
        resultados = []
        for libro in libros:
            if valor.lower() in libro.autor.lower():
                resultados.append(libro)
        return resultados


class BusquedaPorISBN(EstrategiaBusqueda):

    def buscar(self, libros, valor):
        resultados = []
        for libro in libros:
            if libro.isbn == valor:
                resultados.append(libro)
        return resultados


class BusquedaPorDisponibilidad(EstrategiaBusqueda):
    def buscar(self, libros, valor):
        resultados = []
        disponible = valor.lower() == "true"
        for libro in libros:
            if libro.disponible == disponible:
                resultados.append(libro)
        return resultados


class ValidadorBiblioteca:

    @staticmethod
    def validar_titulo(titulo):
        if not titulo or len(titulo) < 2:
            return False, "Error: Título inválido"
        return True, ""

    @staticmethod
    def validar_autor(autor):
        if not autor or len(autor) < 3:
            return False, "Error: Autor inválido"
        return True, ""

    @staticmethod
    def validar_isbn(isbn):
        if not isbn or len(isbn) < 10:
            return False, "Error: ISBN inválido"
        return True, ""

    @staticmethod
    def validar_usuario(usuario):
        if not usuario or len(usuario) < 3:
            return False, "Error: Nombre de usuario inválido"
        return True, ""


class ServicioNotificaciones:
    def enviar_notificacion_prestamo(self, usuario, libro_titulo):
        print(f"[NOTIFICACIÓN] {usuario}: Préstamo de '{libro_titulo}'")

    def enviar_notificacion_devolucion(self, usuario, libro_titulo):
        print(f"[NOTIFICACIÓN] {usuario}: Devolución de '{libro_titulo}'")

class IRepositorio(ABC):

    @abstractmethod
    def guardar(self, datos):
        pass

    @abstractmethod
    def cargar(self):
        pass


class RepositorioArchivo(IRepositorio):
    def __init__(self, nombre_archivo="biblioteca.txt"):
        self.archivo = nombre_archivo

    def guardar(self, datos):
        with open(self.archivo, 'w') as f:
            f.write(f"Libros: {datos.get('num_libros', 0)}\n")
            f.write(f"Préstamos: {datos.get('num_prestamos', 0)}\n")

    def cargar(self):
        try:
            with open(self.archivo, 'r') as f:
                data = f.read()
            return True
        except:
            return False


class RepositorioMemoria(IRepositorio):
    def __init__(self):
        self.datos_memoria = {}

    def guardar(self, datos):
        self.datos_memoria = datos.copy()
        print(f"[MEMORIA] Datos guardados: {self.datos_memoria}")

    def cargar(self):
        return bool(self.datos_memoria)

class SistemaBiblioteca:
    def __init__(self, repositorio: IRepositorio):
        self.libros = []
        self.prestamos = []
        self.contador_libro = 1
        self.contador_prestamo = 1

        self.repositorio = repositorio

        self.validador = ValidadorBiblioteca()
        self.notificador = ServicioNotificaciones()

        self.estrategias_busqueda = {
            "titulo": BusquedaPorTitulo(),
            "autor": BusquedaPorAutor(),
            "isbn": BusquedaPorISBN(),
            "disponible": BusquedaPorDisponibilidad()
        }

    def agregar_libro(self, titulo, autor, isbn):
        es_valido, mensaje = self.validador.validar_titulo(titulo)
        if not es_valido:
            return mensaje

        es_valido, mensaje = self.validador.validar_autor(autor)
        if not es_valido:
            return mensaje

        es_valido, mensaje = self.validador.validar_isbn(isbn)
        if not es_valido:
            return mensaje

        libro = Libro(self.contador_libro, titulo, autor, isbn)
        self.libros.append(libro)
        self.contador_libro += 1

        self._guardar_en_repositorio()

        return f"Libro '{titulo}' agregado exitosamente"

    def buscar_libro(self, criterio, valor):
        estrategia = self.estrategias_busqueda.get(criterio)
        if estrategia:
            return estrategia.buscar(self.libros, valor)
        return []

    def realizar_prestamo(self, libro_id, usuario):
        es_valido, mensaje = self.validador.validar_usuario(usuario)
        if not es_valido:
            return mensaje

        libro = None
        for l in self.libros:
            if l.id == libro_id:
                libro = l
                break

        if not libro:
            return "Error: Libro no encontrado"

        if not libro.disponible:
            return "Error: Libro no disponible"

        prestamo = Prestamo(
            self.contador_prestamo,
            libro_id,
            usuario,
            datetime.now().strftime("%Y-%m-%d")
        )

        self.prestamos.append(prestamo)
        self.contador_prestamo += 1
        libro.disponible = False

        self._guardar_en_repositorio()

        self.notificador.enviar_notificacion_prestamo(usuario, libro.titulo)

        return f"Préstamo realizado a {usuario}"

    def devolver_libro(self, prestamo_id):
        prestamo = None
        for p in self.prestamos:
            if p.id == prestamo_id:
                prestamo = p
                break

        if not prestamo:
            return "Error: Préstamo no encontrado"

        if prestamo.devuelto:
            return "Error: Libro ya devuelto"

        for libro in self.libros:
            if libro.id == prestamo.libro_id:
                libro.disponible = True
                break

        prestamo.devuelto = True
        self._guardar_en_repositorio()

        return "Libro devuelto exitosamente"

    def obtener_todos_libros(self):
        return self.libros

    def obtener_libros_disponibles(self):
        return [libro for libro in self.libros if libro.disponible]

    def obtener_prestamos_activos(self):
        return [p for p in self.prestamos if not p.devuelto]

    def _guardar_en_repositorio(self):
        datos = {
            'num_libros': len(self.libros),
            'num_prestamos': len(self.prestamos)
        }
        self.repositorio.guardar(datos)


def main():

    print("\nEXAMEN - BIBLIOTECA VIRTUAL")
    print("\nAndres Gomez Tagle Azcarraga")
    print("\nExp: 739678")
    print("\nCarrera: Ingeniería en desarrollo de software")

    #Ejercicio Inyección de Dependencias
    repositorio_archivo = RepositorioArchivo("biblioteca.txt")
    sistema = SistemaBiblioteca(repositorio_archivo)


    print("\nEJERCICIO: Separación de Responsabilidades")
 

    print("\n=== AGREGANDO LIBROS =)==")
    print(sistema.agregar_libro("How to be Free", "Epicteto", "9780060883287"))
    print(sistema.agregar_libro("Beyond Good and Evil", "Fredrich Nietzsche", "9780156012195"))
    print(sistema.agregar_libro("El arte de tener razón", "Arthur Schopenhauer", "9780451524935"))
    print(sistema.agregar_libro("El arte de la guerra", "Sun Tzu", "9788424936464"))


    print("\nEJERCICIO Búsqueda Extensible")


    print("="*70)

    print("\n=== BÚSQUEDA POR TÍTULO ===")
    resultados = sistema.buscar_libro("titulo", "how to be free")
    for libro in resultados:
        print(f"- {libro.titulo} - {libro.autor}")
        
    

    print("\n=== BÚSQUEDA POR AUTOR ===")
    resultados = sistema.buscar_libro("autor", "tzu")
    for libro in resultados:
        print(f"- {libro.titulo} - {libro.autor}")

    print("\n=== BÚSQUEDA POR ISBN ===")
    resultados = sistema.buscar_libro("isbn", "9788424936464")
    for libro in resultados:
        print(f"- {libro.titulo} (ISBN: {libro.isbn})")

    print("\n=== BÚSQUEDA POR DISPONIBILIDAD===")
    resultados = sistema.buscar_libro("disponible", "true")
    for libro in resultados:
        print(f"- {libro.titulo}")

    print("\n=== REALIZAR PRÉSTAMO ===")
    print(sistema.realizar_prestamo(1, "Fernando Alonso"))

    print("\n=== LIBROS DISPONIBLES DESPUÉS DEL PRÉSTAMO ===")
    disponibles = sistema.obtener_libros_disponibles()
    for libro in disponibles:
        print(f"- {libro.titulo}")

    print("\n=== DEVOLVER LIBRO ===")
    print(sistema.devolver_libro(1))

    print("\n=== PRÉSTAMOS ACTIVOS ===")
    activos = sistema.obtener_prestamos_activos()
    print(f"Total de préstamos activos: {len(activos)}")

    print("="*70)

    repositorio_memoria = RepositorioMemoria()
    sistema_memoria = SistemaBiblioteca(repositorio_memoria)

    print("\n--- Sistema con repositorio en memoria ---\n")
    print(sistema_memoria.agregar_libro("El príncipe", "Nicolás Maquiavelo", "9788420651163"))

    print("\n=== LIBROS DISPONIBLES ===")
    disponibles = sistema_memoria.obtener_libros_disponibles()
    for libro in disponibles:
        print(f"- {libro.titulo} - {libro.autor}")

    print("\nRESUMEN DE PRINCIPIOS SOLID APLICADOS")
    
    print("""
    OCP :
   - Búsqueda usa patrón Strategy
   - Se pueden agregar nuevas búsquedas sin modificar buscar_libro
   - Ejemplo: BusquedaPorDisponibilidad agregada sin cambios al código

    SRP:
   - ValidadorBiblioteca: solo validación
   - ServicioNotificaciones: solo notificaciones
   - RepositorioArchivo/Memoria: solo persistencia
   - SistemaBiblioteca: solo lógica de negocio

    DIP:
   - IRepositorio es la abstracción
   - SistemaBiblioteca depende de IRepositorio
   - Inyección de dependencias en el constructor
   - Fácil cambio entre RepositorioArchivo y RepositorioMemoria
    """)
    


if __name__ == "__main__":
    main()
