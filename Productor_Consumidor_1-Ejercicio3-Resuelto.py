import threading
import random
import logging
import time

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

"""
    Clase listaFinita, extiende la clase list ([]) de modo que puede establecerse un limite máximo
    al tamaño (cantidad de objetos) de la lista.

    Uso:
    Declaración
    lista = listaFinita(Numero_Maximo_Items)
    # Crea una lista VACIA que admitirá hasta un máximo de Numero_Maximo_Items items

    El acceso a los elementos es igual que en una lista standard, la diferencia es que
    si se intenta agregar un elemento cuando la lista tiene Numero_Maximo_Items items, dara
    un mensaje de error y terminara el programa.

    Ejemplos
    Acceso al elemento i:

    a = lista[i]

    insertar un elemento en la posicón i.
    lista.insert(i, dato)  # si i es mayor que Numero_Maximo_Items termina el programa y da error

    o

    lista[i] = dato   # Si i es mayor que Numero_Maximo_Items termina el programa y da error.

    agregar un elemento al final de la lista

    lista.append(dato)  # Si la lista tiene Numero_Maximo_Items termina el programa y da error.

"""

class listaFinita(list):

    def __init__(self, max_elementos):
            self.max_elementos = max_elementos
            super().__init__()
            self.vacio = threading.Semaphore(max_elementos)
            self.lleno = threading.Semaphore(0)
            self.lock = threading.Lock()


    def pop(self, index):
        self.lleno.acquire()
        self.lock.acquire()
        try:
            return super().pop(index)
        finally:
            self.lock.release()
            self.vacio.release()


    def append(self, item):
        self.vacio.acquire()
        self.lock.acquire()
        try:
            super().append(item)
        finally:
            self.lock.release()
            self.lleno.release()

    def insert(self, index, item):
        assert index < self.max_elementos, "indice invalido"
        super().insert(index, item)

    def full(self):
        if len(self) == self.max_elementos:
            return True
        else:
            return False



class Productor(threading.Thread):
    def __init__(self, lista):
        super().__init__()
        self.lista = lista


    def run(self):
        while True:
            self.lista.append(random.randint(0,100))
            logging.info(f'produjo el item: {self.lista[-1]}')
            time.sleep(random.randint(1,5))


class Consumidor(threading.Thread):
    def __init__(self, lista):
        super().__init__()
        self.lista = lista

    def run(self):
        while True:
            elemento = self.lista.pop(0)
            logging.info(f'consumio el item {elemento}')
            time.sleep(random.randint(1,5))


def main():
    hilos = []
    lista = listaFinita(4)


    for i in range(4):
        productor = Productor(lista)
        consumidor = Consumidor(lista)
        hilos.append(productor)
        hilos.append(consumidor)

        logging.info(f'Arrancando productor {productor.name}')
        productor.start()

        logging.info(f'Arrancando consumidor {consumidor.name}')
        consumidor.start()

    for h in hilos:
        h.join()


if __name__ == '__main__':
    main()
