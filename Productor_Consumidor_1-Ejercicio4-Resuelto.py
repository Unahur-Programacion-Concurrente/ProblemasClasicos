import threading
import queue
import random
import logging
import time

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)



class Productor(threading.Thread):
    def __init__(self, cola):
        super().__init__()
        self.cola = cola


    def run(self):
        while True:
            item = random.randint(0,100)
            self.cola.put(item)
            logging.info(f'produjo el item: {item}')
            time.sleep(random.randint(1,5))


class Consumidor(threading.Thread):
    def __init__(self, cola):
        super().__init__()
        self.cola = cola

    def run(self):
        while True:
            elemento = self.cola.get()
            logging.info(f'consumio el item {elemento}')
            time.sleep(random.randint(1,5))


def main():
    hilos = []
    cola = queue.Queue(4)


    for i in range(4):
        productor = Productor(cola)
        consumidor = Consumidor(cola)
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
