import threading
import random
import logging
import time
from rwlock import RWLock

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

equipos = ["Boca", "River", "Racing", "Independiente", "San Lorenzo", "Huracán", "Gimnasia",
           "Estudiantes", "Velez", "Ferro", "Lanus", "Quilmes"]

partido = ["",0,"",0]

marker= RWLock()

def escritor(id_number):
    global partido
    global equipos
    name = 'Escritor-' + str(id_number)
    while True:
        equipo1 = random.randint(0, len(equipos)-1)
        equipo2 = random.randint(0, len(equipos)-1)
        while equipo1 == equipo2:
            equipo2 = random.randint(0, len(equipos)-1)
        marker.w_acquire()
        try:
            partido[0] = equipos[equipo1]
            partido[1] = random.randint(0,4)
            partido[2] = equipos[equipo2]
            partido[3] = random.randint(0,4)
            logging.info(f'{name} Actualizo el partido')

        finally:
            marker.w_release()
            time.sleep(random.randint(1,2))


def lector(id_number):
    global partido
    global equipos
    name = 'Lector-' + str(id_number)
    while True:
        marker.r_acquire()
        try:
            logging.info(f'{name} el resultado fue: {partido[0]} {partido[1]} - {partido[2]} {partido[3]}')

        finally:
            marker.r_release()
            time.sleep(random.randint(1,2))


def main():
    hilos = []
    for i in range(1):
        writer = threading.Thread(target=escritor, args=(i,))
        logging.info(f'Arrancando escritor-{i}')
        writer.start()
        hilos.append(writer)

    for i in range(4):
        reader = threading.Thread(target=lector, args=(i,))
        logging.info(f'Arrancando lector-{i}')
        reader.start()
        hilos.append(escritor)

    for t in hilos:
        t.join()

if __name__ == "__main__":
    main()

