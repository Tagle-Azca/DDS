# Diagramas de Clases - Examen SOLID
**Alumno:** Tagle

---

## Diagrama 1: Ejercicio OCP - Patrón Strategy para Búsqueda

```mermaid
classDiagram
    %% Patrón Strategy para búsqueda extensible (OCP)
    class EstrategiaBusqueda {
        <<abstract>>
        +buscar(libros, valor)* List~Libro~
    }

    class BusquedaPorTitulo {
        +buscar(libros, valor) List~Libro~
    }

    class BusquedaPorAutor {
        +buscar(libros, valor) List~Libro~
    }

    class BusquedaPorISBN {
        +buscar(libros, valor) List~Libro~
    }

    class BusquedaPorDisponibilidad {
        +buscar(libros, valor) List~Libro~
    }

    class SistemaBiblioteca {
        -estrategias_busqueda: dict
        +buscar_libro(criterio, valor) List~Libro~
    }

    class Libro {
        +id: int
        +titulo: str
        +autor: str
        +isbn: str
        +disponible: bool
    }

    EstrategiaBusqueda <|-- BusquedaPorTitulo : implementa
    EstrategiaBusqueda <|-- BusquedaPorAutor : implementa
    EstrategiaBusqueda <|-- BusquedaPorISBN : implementa
    EstrategiaBusqueda <|-- BusquedaPorDisponibilidad : implementa
    SistemaBiblioteca o-- EstrategiaBusqueda : usa
    EstrategiaBusqueda ..> Libro : opera sobre
```

**Explicación OCP:**
- Abierto a extensión: Se pueden agregar nuevas estrategias (ej: BusquedaPorAño)
- Cerrado a modificación: No se modifica `buscar_libro()` al agregar estrategias
- El diccionario `estrategias_busqueda` permite extensibilidad

---

## Diagrama 2: Ejercicio SRP - Separación de Responsabilidades

```mermaid
classDiagram
    %% Separación de responsabilidades (SRP)
    class SistemaBiblioteca {
        -libros: List~Libro~
        -prestamos: List~Prestamo~
        -validador: ValidadorBiblioteca
        -notificador: ServicioNotificaciones
        -repositorio: IRepositorio
        +agregar_libro(titulo, autor, isbn) str
        +buscar_libro(criterio, valor) List~Libro~
        +realizar_prestamo(libro_id, usuario) str
        +devolver_libro(prestamo_id) str
    }

    class ValidadorBiblioteca {
        <<service>>
        +validar_titulo(titulo)$ Tuple
        +validar_autor(autor)$ Tuple
        +validar_isbn(isbn)$ Tuple
        +validar_usuario(usuario)$ Tuple
    }

    class ServicioNotificaciones {
        <<service>>
        +enviar_notificacion_prestamo(usuario, libro)
        +enviar_notificacion_devolucion(usuario, libro)
    }

    class Libro {
        +id: int
        +titulo: str
        +autor: str
        +isbn: str
        +disponible: bool
    }

    class Prestamo {
        +id: int
        +libro_id: int
        +usuario: str
        +fecha: str
        +devuelto: bool
    }

    SistemaBiblioteca --> ValidadorBiblioteca : valida con
    SistemaBiblioteca --> ServicioNotificaciones : notifica con
    SistemaBiblioteca "1" *-- "*" Libro : contiene
    SistemaBiblioteca "1" *-- "*" Prestamo : gestiona
```

**Explicación SRP:**
- **ValidadorBiblioteca**: Solo responsable de validar datos
- **ServicioNotificaciones**: Solo responsable de notificar
- **SistemaBiblioteca**: Solo responsable de lógica de negocio (coordinación)
- Cada clase tiene una única razón para cambiar

---

## Diagrama 3: Ejercicio DIP - Inversión de Dependencias

```mermaid
classDiagram
    %% Inversión de dependencias (DIP)
    class SistemaBiblioteca {
        -repositorio: IRepositorio
        +agregar_libro(titulo, autor, isbn) str
        +realizar_prestamo(libro_id, usuario) str
    }

    class IRepositorio {
        <<interface>>
        +guardar(datos)*
        +cargar()*
    }

    class RepositorioArchivo {
        -archivo: str
        +guardar(datos)
        +cargar()
    }

    class RepositorioMemoria {
        -datos_memoria: dict
        +guardar(datos)
        +cargar()
    }

    SistemaBiblioteca --> IRepositorio : depende de abstracción
    IRepositorio <|.. RepositorioArchivo : implementa
    IRepositorio <|.. RepositorioMemoria : implementa

    note for SistemaBiblioteca "Recibe IRepositorio por\ninyección de dependencias\nen el constructor"

    note for IRepositorio "Abstracción de alto nivel\nNo depende de detalles"
```

**Explicación DIP:**
- **Alto nivel** (SistemaBiblioteca) depende de abstracción (IRepositorio)
- **Bajo nivel** (RepositorioArchivo, RepositorioMemoria) implementan abstracción
- Inversión: Módulos de alto nivel NO dependen de módulos de bajo nivel
- Ambos dependen de abstracciones
- Inyección de dependencias en constructor

---

## Diagrama 4: Arquitectura Completa (SOLID Integrado)

```mermaid
classDiagram
    %% Arquitectura completa aplicando todos los principios SOLID

    class SistemaBiblioteca {
        -libros: List~Libro~
        -prestamos: List~Prestamo~
        -validador: ValidadorBiblioteca
        -notificador: ServicioNotificaciones
        -repositorio: IRepositorio
        -estrategias_busqueda: dict
        +__init__(repositorio: IRepositorio)
        +agregar_libro(titulo, autor, isbn) str
        +buscar_libro(criterio, valor) List~Libro~
        +realizar_prestamo(libro_id, usuario) str
        +devolver_libro(prestamo_id) str
    }

    %% Dominio
    class Libro {
        +id: int
        +titulo: str
        +autor: str
        +isbn: str
        +disponible: bool
    }

    class Prestamo {
        +id: int
        +libro_id: int
        +usuario: str
        +fecha: str
        +devuelto: bool
    }

    %% SRP - Servicios
    class ValidadorBiblioteca {
        <<service>>
        +validar_titulo(titulo)$ Tuple
        +validar_autor(autor)$ Tuple
        +validar_isbn(isbn)$ Tuple
        +validar_usuario(usuario)$ Tuple
    }

    class ServicioNotificaciones {
        <<service>>
        +enviar_notificacion_prestamo(usuario, libro)
        +enviar_notificacion_devolucion(usuario, libro)
    }

    %% DIP - Repositorios
    class IRepositorio {
        <<interface>>
        +guardar(datos)*
        +cargar()*
    }

    class RepositorioArchivo {
        -archivo: str
        +guardar(datos)
        +cargar()
    }

    class RepositorioMemoria {
        -datos_memoria: dict
        +guardar(datos)
        +cargar()
    }

    %% OCP - Estrategias de búsqueda
    class EstrategiaBusqueda {
        <<abstract>>
        +buscar(libros, valor)* List~Libro~
    }

    class BusquedaPorTitulo {
        +buscar(libros, valor) List~Libro~
    }

    class BusquedaPorAutor {
        +buscar(libros, valor) List~Libro~
    }

    class BusquedaPorISBN {
        +buscar(libros, valor) List~Libro~
    }

    class BusquedaPorDisponibilidad {
        +buscar(libros, valor) List~Libro~
    }

    %% Relaciones principales
    SistemaBiblioteca "1" *-- "*" Libro
    SistemaBiblioteca "1" *-- "*" Prestamo
    SistemaBiblioteca --> ValidadorBiblioteca : SRP
    SistemaBiblioteca --> ServicioNotificaciones : SRP
    SistemaBiblioteca --> IRepositorio : DIP
    SistemaBiblioteca o-- EstrategiaBusqueda : OCP

    IRepositorio <|.. RepositorioArchivo
    IRepositorio <|.. RepositorioMemoria

    EstrategiaBusqueda <|-- BusquedaPorTitulo
    EstrategiaBusqueda <|-- BusquedaPorAutor
    EstrategiaBusqueda <|-- BusquedaPorISBN
    EstrategiaBusqueda <|-- BusquedaPorDisponibilidad

    note for SistemaBiblioteca "Clase principal que aplica\nSOLID: SRP, OCP, DIP"
```

---

## Resumen de Principios SOLID Aplicados

| Principio | Implementación | Beneficio |
|-----------|---------------|-----------|
| **SRP** | ValidadorBiblioteca, ServicioNotificaciones separados | Cada clase tiene una sola responsabilidad |
| **OCP** | Patrón Strategy con EstrategiaBusqueda | Extensible sin modificar código existente |
| **LSP** | Todas las estrategias sustituyen a EstrategiaBusqueda | Polimorfismo correcto |
| **ISP** | Interfaces pequeñas (IRepositorio simple) | Clientes no dependen de métodos innecesarios |
| **DIP** | SistemaBiblioteca depende de IRepositorio (abstracción) | Fácil cambio de implementación |

---

## Cómo visualizar estos diagramas

1. **GitHub**: Los diagramas se renderizan automáticamente en archivos .md
2. **VS Code**: Instalar extensión "Markdown Preview Mermaid Support"
3. **Online**: Copiar código a https://mermaid.live/

---

**Fin de los diagramas**