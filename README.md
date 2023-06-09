# Problemas Clasicos de Programación Concurrente 1

# Productor Consumidor

## Ejercicio 1
````
Productor_Consumidor_1.py
````
El siguiente archivo python, contiene la definición de la clase ***listaFinita***, que extiende la clase list ([]) de modo que puede establecerse un limite máximo
    al tamaño (cantidad de objetos) de la lista.

A continuación implementa dos objetos derivados de Thread, un "Productor" que inserta elementos en la lista y un "Consumidor" que extrae elementos de la lista.

Finalmente instancia una lista (listaFinita) de un tamaño especifico y dos conjuntos de hilos Productor y Consumidor


 
1. Leer y analizar que hace el código de este programa. 
**Analizar hasta comprender todas las líneas del código**

2. Ejecute el programa y analice los resultados. Con mucha probabilidad va a observar resultados inconsistentes y/o errores. Explique a que se deben.

3. **Utilizando Locks o RLocks solamente**, modificar los objetos Productor y Consumidor de modo que solucionen los erroes e inconsistencias.

## Ejercicio 2

**Utilizando Semáforos solamente**, implementar la solución al Ejercicio 1.

## Ejercicio 3

Modificar la clase listaFinita de modo que implemente una **"cola bloqueante"**, e implementar la solución al Ejercicio 1.

## Ejercicio 4

Implementar la "cola bloqueante" utilizando un objeto **queue** e implementar la solución al Ejercicio 1.


## Ejercicio 5

Utilizando cualquiera de las soluciones de **cola bloqueante**, modificar el programa de modo que el productor inserte objetos tupla de strings **tomados al azar** de la siguiente lista. 
```
[("España","Madrid"), ("Francia","Paris"),("Italia","Roma"),("Inglaterra","Londres"),("Alemania","Berlin",("Rusia","Moscu"),
("Turquia","Istambul"),("China","Pekin"), ("Japon","Tokio"),("Emiratos Arabes","Dubai"),("Argentina","Buenos Aires"),
("Brasil","Brasilia"),("Colombia","Bogota"),("Uruguay","Montevideo")]
```
Esta lista contiene tuplas ("pais", "capital"). 


Modificar el consumidor de modo que imprima un mensaje: "La capital de "pais" es "capital".

Por ejemplo:
````
La capital de Argentina es Buenos Aires
````

El programa no debe mostrar inconsistencias ni errores debidos a condiciones de carrera o falta de sincronización.

**Nota: para la impresión de mensajes utlizar preferentemente el módulo *logging***.



# Lectores - Escritor

## Ejercicio 6

````
rwlock.py
````

El siguiente archivo python, contiene la definición de la clase ***RWLock***, que utilizamos en uno de los ejemplos en la clase en vivo del 30/4.
Esta clase implementa reader-writers locks con PREFERENCIA de LECTURA (Read Preffering RW Locks).

Métodos:

    r_acquire()     # Adquiere READ LOCK
    
    r_relaase()     # libera READ LOCK
    
    w_aquire()      # Adquiere READ LOCK
    
    w_release()     # libera READ LOCK
    
1. Leer y analizar que hace el código de este programa. **Analizar hasta comprender todas las líneas del código** y responder:

    a. Cuantos Locks hay definidos y cual de ellos asegura exclusión mútua a los writers?
    
    b. Del análisis de los métodos r_acquire() y r_release(), que se transcribe a continuación:
    
```
    def r_acquire(self):
        self.num_r_lock.acquire()
        self.num_r += 1
        if self.num_r == 1:
            self.w_lock.acquire()
        self.num_r_lock.release()

    def r_release(self):
        assert self.num_r > 0
        self.num_r_lock.acquire()
        self.num_r -= 1
        if self.num_r == 0:
            self.w_lock.release()
        self.num_r_lock.release()
```

    b-1. Que cuenta la variable numerica num_r ?
    
    b-2. Si n procesos lectores solicitan concurrentemente el w_lock para lectura (llamando a r_acquire), cual de todos obtiene efectivamente 
    el w_lock? Que ocurre con  los demás procesos que lo requirieron? Se bloquean o continúan la ejecución? Por que?

    b-3. En que circunstancias el proceso lector libera el lock w_lock?

    b-4. Que ocurre si n procesos lectores solicitaron el w_lock  para lectura (llamando a r_acquire) y un proceso escritor solicita el w_lock 
    para escritura (llamando a w_acquire)? Se le da prioridad al escritor o debe esperar a que todos los lectores terminen?
    
    
    
    
    
## Ejercicio 7


1. Utilizando la clase RWLock escribir un programa que implemente la siguiente aplicación Lectores-Escritor:
   
Los procesos lectores y escritores utlizan una lista común (partido) como la siguiente: *partido = ["equipo1", int_goles1, "equipo2", int_goles2]*, por ejemplo:

`````
["Gimnasia", 1, "Estudiantes", 0]
`````

**Escritor**

Debe ejecutar un loop infinito en el cual actualice la lista ***partido*** de la siguiente manera:

Debe tomar un par de equipos ("equipo1" y "equipo2") al azar de la siguiente lista:

````
equipos = ["Boca", "River", "Racing", "Independiente", "San Lorenzo", "Huracán", "Gimnasia", 
"Estudiantes", "Velez", "Ferro", "Lanus", "Quilmes"]
````
Los goles anotados por cada equipo (int_goles1, int_goles2) serán valores enteros entre 0 y 3 generados aleatoriamente. 

Luego de actualizar la lista *partidos*, debe imprimr un mensaje indicando que hizo la actualización, indentificando al hilo que hizo el cambio. No es necesario que incluya el detalle del partido en ese mensaje. 

Por ejemplo:

````
Partido actualizado por Escritor-1
````
**Nota: para la impresión de mensajes utlizar preferentemente el módulo *logging***.

Incluir un retardo (sleep) aleatorio entre 1 y 2 segundos antes de la siguiente iteración en el loop infinito.

**Lector**

En un loop infinito, el **lector** debe leer los datos de la lista ***partido*** e imprimir un mensaje con el resultado del partido. El mensaje debe identificar al lector. 

Por ejemplo:

````
Lector-14: el resultado fue: Gimnasia 1 - Estudiantes 0
````
**Nota: para la impresión de mensajes utlizar preferentemente el módulo *logging***.

Incluir un retardo (sleep) aleatorio entre 1 y 2 segundos **luego liberar los locks** y antes de la próxima iteración. Por ejemplo:
````
finally:
     mi_rwlock.r_release()
     time.sleep(random.randint(1,2))  # Colocar el retardo DESPUES de liberar el lock, no antes.
`````


El programa debe arrancar 1 hilo escritor y 4 hilos lectores.
Agregar el código que sea necesario para que le hilo principal no termine el progama al lanzar todas las threads.


2. Modificar al **lector**, colocando el retardo aleatorio (entre 1 y 2 segundos) **ANTES de liberar los locks**, la idea es simular que el lector realiza mas operaciones antes de liberar el lock. Por ejemplo:
```` 
finally:
    time.sleep(random.randint(1,2))  # Colocar el retardo ANTES de liberar el lock.
    mi_rwlock.r_release() 
`````
Ejecute el programa y observe el resultado. Hay alguna inconsistencia o error? A que se debe?

***Nota: este ejercicio es muy dependiente de como hayan implementado la solución. Si no observa ninguna inconsistencia, consulte con el profesor.***


3. Que cambiaría si se utilizara in Reading-Writing lock de preferencia de escritura, en vez del que estamos usando (preferencia de lectura).
