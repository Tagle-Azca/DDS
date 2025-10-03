### a) Explica qué es LSP y cómo se aplica al ejemplo:

```python
class Usuario:
    def calcular_limite_prestamos(self):
        return 3

class Estudiante(Usuario):
    def calcular_limite_prestamos(self):
        return 3
```
el lsp establece que las clases deribadas deben de poder sustitur a sus clases base sin tneer que alterar el comportamiento correcto 

En este ejemplo :
Estudiante hereda de Usuario y sobrescribe el método calcular_limite_prestamos
Si se recolecta un Usuario puede recibir un estudiante sin tema
El comportamiento es predecible y consistente con la clase base

---

Da un ejemplo que VIOLE LSP y explica por qué:

```python
class Usuario:
    def calcular_limite_prestamos(self):
        return 3

class UsuarioVIP(Usuario):
    def calcular_limite_prestamos(self):
        return None  

class UsuarioRestringido(Usuario):
    def calcular_limite_prestamos(self):
        raise Exception("Usuario sin permisos") 
```

**Explicación:**

Estos ejemplos violan LSP por las siguientes razones:

1. **UsuarioVIP:**
   - Retorna `None` en lugar de un número entero
   - Si el código espera hacer operaciones matemáticas (`limite + 1`), fallará
   - Rompe el contrato implícito de la clase base

2. **UsuarioRestringido:**
   - Lanza una excepción que la clase base no lanza
   - El código que usa `Usuario` no espera manejar excepciones
   - Comportamiento inesperado que rompe la sustituibilidad

**Impacto:** Si sustituimos `Usuario` por estas clases, el programa puede fallar o comportarse incorrectamente, violando el principio LSP.

---

## Pregunta 2: ISP

### a) ¿Por qué esta interfaz VIOLA ISP?

```python
class IGestionBiblioteca:
    def agregar_libro(self): pass
    def buscar_libro(self): pass
    def realizar_prestamo(self): pass
    def generar_reporte(self): pass
    def hacer_backup(self): pass
```

**Respuesta:**

Esta interfaz Viola ISP por las siguientes razones:

1. **Es demasiado amplia**
   - Fuerza a las clases implementadoras a definir TODOS los métodos
   - Incluso si no necesitan toda la funcionalidad

2. **Responsabilidades mezcladas:**
   - Operaciones de gestión (`agregar_libro`, `buscar_libro`, `realizar_prestamo`)
   - Operaciones administrativas (`generar_reporte`, `hacer_backup`)
   - Son preocupaciones diferentes que no todas las clases necesitan

3. **Problema concreto:**
   - Un cliente que solo necesita buscar libros se ve obligado a implementar `hacer_backup`
   - Viola el principio: "ningún cliente debe depender de métodos que no usa"

---

### b) Propón cómo segregar esta interfaz:

```
Interface 1: IGestionLibros
Métodos: agregar_libro(), buscar_libro()

Interface 2: IGestionPrestamos
Métodos: realizar_prestamo()

Interface 3: IAdministracion
Métodos: generar_reporte(), hacer_backup()
```

Justificación:

aqui mejora ya que 
1. **IGestionLibros:** Operaciones básicas sobre libros (CRUD)
2. **IGestionPrestamos:** Lógica específica de préstamos
3. **IAdministracion:** Funciones administrativas/mantenimiento

**Ventajas:**
- Cada clase implementa solo lo que necesita
- Mayor flexibilidad y mantenibilidad
- Respeta el principio ISP: interfaces pequeñas y cohesivas
- Facilita testing (mocks más simples)

**Ejemplo de uso:**
```python
class VisorLibros(IGestionLibros):
    pass

class SistemaCompleto(IGestionLibros, IGestionPrestamos, IAdministracion):
    pass
```

---

## Resumen de Principios


**LSP**: Las clases derivadas deben ser sustituibles por sus clases base 
**ISP**: Los clientes no deben depender de interfaces que no usan 

---

**Fin de las respuestas teóricas**
