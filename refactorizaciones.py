from abc import ABC, abstractmethod


# 1. REPLACE METHOD WITH METHOD OBJECT

# ------------ ANTES ------------
class FacturaAntes:
    def __init__(self, precio, cantidad):
        self.precio = precio
        self.cantidad = cantidad

    def total(self):
        subtotal = self.precio * self.cantidad
        descuento = 0
        if subtotal > 100:
            descuento = subtotal * 0.1
        iva = (subtotal - descuento) * 0.19
        return subtotal - descuento + iva


# ------------ DESPUES ------------
class CalculadoraFactura:
    def __init__(self, factura):
        self.factura = factura
        self.subtotal = 0
        self.descuento = 0
        self.iva = 0

    def calcular(self):
        self.subtotal = self.factura.precio * self.factura.cantidad
        self.calcular_descuento()
        self.calcular_iva()
        return self.subtotal - self.descuento + self.iva

    def calcular_descuento(self):
        if self.subtotal > 100:
            self.descuento = self.subtotal * 0.1

    def calcular_iva(self):
        self.iva = (self.subtotal - self.descuento) * 0.19


class FacturaDespues:
    def __init__(self, precio, cantidad):
        self.precio = precio
        self.cantidad = cantidad

    def total(self):
        return CalculadoraFactura(self).calcular()


# aqui se separaron los calculos para que el metodo no quede tan largo.
# tambien es mas facil mirar cada parte por separado.


# 2. EXTRACT CLASS

# ------------ ANTES ------------
class PersonaAntes:
    def __init__(self, nombre, indicativo, numero):
        self.nombre = nombre
        self.indicativo = indicativo
        self.numero = numero

    def telefono(self):
        return f"+{self.indicativo} {self.numero}"

    def telefono_valido(self):
        return self.numero.isdigit() and len(self.numero) == 10

    def es_celular(self):
        return self.numero.startswith("3")


# ------------ DESPUES ------------
class Telefono:
    def __init__(self, indicativo, numero):
        self.indicativo = indicativo
        self.numero = numero

    def completo(self):
        return f"+{self.indicativo} {self.numero}"

    def es_valido(self):
        return self.numero.isdigit() and len(self.numero) == 10

    def es_celular(self):
        return self.numero.startswith("3")


class PersonaDespues:
    def __init__(self, nombre, telefono):
        self.nombre = nombre
        self.telefono = telefono


# se saco lo del telefono de Persona y se puso en otra clase.
# asi Persona no tiene que hacer tantas cosas.


# 3. REPLACE CONDITIONAL WITH POLYMORPHISM

# ------------ ANTES ------------
class AnimalAntes:
    def __init__(self, tipo):
        self.tipo = tipo

    def sonido(self):
        if self.tipo == "perro":
            return "guau"
        elif self.tipo == "gato":
            return "miau"
        elif self.tipo == "vaca":
            return "muu"


# ------------ DESPUES ------------
class Animal(ABC):
    @abstractmethod
    def sonido(self):
        pass


class Perro(Animal):
    def sonido(self):
        return "guau"


class Gato(Animal):
    def sonido(self):
        return "miau"


class Vaca(Animal):
    def sonido(self):
        return "muu"


# antes se usaba un if para saber el sonido.
# ahora cada clase tiene su propio sonido y queda mas separado.


# 4. FORM TEMPLATE METHOD

# ------------ ANTES ------------
class SaludoFormalAntes:
    def saludar(self, nombre):
        inicio = "Buenos dias"
        return f"{inicio}, {nombre}. Que tenga buen dia."


class SaludoInformalAntes:
    def saludar(self, nombre):
        inicio = "Hola"
        return f"{inicio}, {nombre}. Que tengas buen dia."


# ------------ DESPUES ------------
class Saludo(ABC):
    def saludar(self, nombre):
        return f"{self.inicio()}, {nombre}. {self.despedida()}"

    @abstractmethod
    def inicio(self):
        pass

    @abstractmethod
    def despedida(self):
        pass


class SaludoFormal(Saludo):
    def inicio(self):
        return "Buenos dias"

    def despedida(self):
        return "Que tenga buen dia."


class SaludoInformal(Saludo):
    def inicio(self):
        return "Hola"

    def despedida(self):
        return "Que tengas buen dia."


# los dos saludos tenian casi la misma estructura.
# deje la parte repetida en la clase Saludo.


# 5. REPLACE INHERITANCE WITH DELEGATION

# ------------ ANTES ------------
class PilaAntes(list):
    def apilar(self, x):
        self.append(x)

    def desapilar(self):
        return self.pop()


# como hereda de list se pueden usar metodos que no deberia tener una pila.


# ------------ DESPUES ------------
class PilaDespues:
    def __init__(self):
        self.elementos = []

    def apilar(self, x):
        self.elementos.append(x)

    def desapilar(self):
        return self.elementos.pop()


# ahora la lista esta adentro de la clase.
# de esta forma la pila usa solo lo que necesita.


# pruebas
if __name__ == "__main__":
    print(FacturaAntes(60, 2).total(), FacturaDespues(60, 2).total())

    p1 = PersonaAntes("Ana", 57, "3001234567")
    p2 = PersonaDespues("Ana", Telefono(57, "3001234567"))

    print(p1.telefono(), p2.telefono.completo(), p1.es_celular(), p2.telefono.es_celular())

    print(AnimalAntes("gato").sonido(), Gato().sonido())

    print(SaludoFormal().saludar("Pedro"))
    print(SaludoInformal().saludar("Pedro"))

    p = PilaDespues()
    p.apilar(1)
    p.apilar(2)
    print(p.desapilar())
