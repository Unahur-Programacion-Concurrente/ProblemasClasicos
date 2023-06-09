from threading import Thread, Lock, Event
import time, random
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


mutex = Lock()

#Intervalos en segundos
clienteIntervaloMin = 5
clienteIntervaloMax = 15
tiempoCorteMin = 3
tiempoCorteMax = 15

class Barberia:
    clientesEsperando = []

    def __init__(self, barbero, cantidadDeSillas):
        self.barbero = barbero
        self.cantidadDeSillas = cantidadDeSillas
        logging.info(f'Barberia inciada con {cantidadDeSillas} sillas')
        logging.info(f'Cliente Intervalo Minimo {clienteIntervaloMin}')
        logging.info(f'Cliente Intervalo Maximo {clienteIntervaloMax}')
        logging.info(f'Tiempo min de corte {tiempoCorteMin}')
        logging.info(f'Tiempo max de corte {clienteIntervaloMax}')
        logging.info(f'---------------------------------------')

    def abreBarberia(self):
        logging.info(f'La barberia esta abriendo')
        workingThread = Thread(target = self.barberoTrabajando)
        workingThread.start()

    def barberoTrabajando(self):
        while True:
            mutex.acquire()

            if len(self.clientesEsperando) > 0:
                c = self.clientesEsperando[0]
                del self.clientesEsperando[0]
                mutex.release()
                self.barbero.cortePelo(c)
            else:
                mutex.release()
                logging.info(f'No hay mas clientes, me voy a dormir!')
                barbero.sleep()
                logging.info(f'El barbero se despierta')

    def entraClienteABarberia(self, cliente):
        mutex.acquire()
        logging.info(f'>> {cliente.name} entro a la barberia y esta buscando silla')

        if len(self.clientesEsperando) == self.cantidadDeSillas:
            logging.info(f'Sala de espera llena, {cliente.name} se retira')
            mutex.release()
        else:
            logging.info(f'{cliente.name} sentado en la sala de espera')
            self.clientesEsperando.append(c)
            mutex.release()
            barbero.despertar()

class cliente:
    def __init__(self, name):
        self.name = name

class barbero:
    barberoTrabajandoEvento = Event()

    def sleep(self):
        self.barberoTrabajandoEvento.wait()

    def despertar(self):
        self.barberoTrabajandoEvento.set()

    def cortePelo(self, cliente):
        #Set barbero ocupado
        self.barberoTrabajandoEvento.clear()

        logging.info(f'cortando el pelo a {cliente.name}')

        tiempoCorteDePelo = random.randrange(tiempoCorteMin, tiempoCorteMax+1)
        time.sleep(tiempoCorteDePelo)
        logging.info(f'{cliente.name} corte terminado')


if __name__ == '__main__':
    clientes = []
    clientes.append(cliente('Bernardo'))
    clientes.append(cliente('Ariel'))
    clientes.append(cliente('Ignacio'))
    clientes.append(cliente('Axel'))
    clientes.append(cliente('Andres'))
    clientes.append(cliente('Alberto'))
    clientes.append(cliente('Marcelo'))
    clientes.append(cliente('Sergio'))
    clientes.append(cliente('Oscar'))
    clientes.append(cliente('Bruno'))
    clientes.append(cliente('Guillermo'))
    clientes.append(cliente('Mario'))
    clientes.append(cliente('Raul'))
    clientes.append(cliente('Fernando'))
    clientes.append(cliente('Tomas'))
    clientes.append(cliente('Felipe'))
    clientes.append(cliente('Horacio'))

    barbero = barbero()

    Barberia = Barberia(barbero, cantidadDeSillas=3)
    Barberia.abreBarberia()

    while len(clientes) > 0:
        c = clientes.pop()
        #Nuevo cliente entra a la Barberia
        Barberia.entraClienteABarberia(c)
        clienteInterval = random.randrange(clienteIntervaloMin,clienteIntervaloMax+1)
        time.sleep(clienteInterval)

