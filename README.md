## Requisitos previos

Con instrucciones para instalar en
#### Linux (Debian)
- Python 3.8 o superior
<br>`sudo apt install python3 python3-pip -y`<br>
- Graphviz 14 o superior
<br>`sudo apt install graphviz -y`<br>

#### Windows
- Python 3.8 o superior
Descargar y ejecutar el `.exe` en su pagina web `https://www.python.org/downloads/?hl=ES` o a traves de Microsoft Store

- Graphviz 14 o superior
Descargar y ejecutar el `.exe` en su pagina web `https://graphviz.org/download/`<br>
Luego ejecuta en Powershell o Cmd el siguiente comando `pip install graphviz`<br>
## Para la ejecucion
Simplemente ejecutar el archivo `.py`, la entrada fue la dada en los ejemplos y estan en `entrada.txt` (archivo modificable para pruebas).
# ¡Aviso!
# Deje muchos ejemplos en ```entrada.txt```, recomiendo usar los ejemplos poco a poco en las actividades 1 y 2 para que no se creen demasiadas imagenes.

---------------------------------------------------------------------------------------------------------------------------------------------------

# Documentacion de las actividades

## Tarea 1 (Analizador sintáctico en Python)

Ya que usaria la gramatica vista en las diapositivas:
```
E->E opsuma T
E->T
T->T opmul F
T->F F->id
F->num
F->pari E pard
```
La modifique para adaptarse a codigo de python
```
E -> T ( ( + | - ) T )*
T -> F ( ( * | / ) F )*
F -> num | id | ( E )
```
<img width="264" height="233" alt="image" src="https://github.com/user-attachments/assets/3cdfbed4-f29b-4a88-83d6-b97a0833d38f" /><br>
------------------------------------------------------------------------------------------------------------------------------------
Entonces lo dividi el funcionamiento en 3 metodos (E, T y F)
#### - Metodo E:
<img width="394" height="195" alt="image" src="https://github.com/user-attachments/assets/308d42ab-888f-4883-a834-82e0cd352092" /><br>
Mientras haya un `+` o `-`, se crea un nodo con el operador. 

#### - Metodo T:
<img width="382" height="208" alt="image" src="https://github.com/user-attachments/assets/abba0ef3-4bbf-4c0d-a99a-b675480ba6dd" /><br>
Mientras haya un `*` o `/`, se crea un nodo con el operador. (este tiene mas precedencia que E )

#### - Metodo F:
<img width="350" height="379" alt="image" src="https://github.com/user-attachments/assets/b1971ec6-c5a1-448a-b059-c070ac88e460" /><br>
Si hay un numero o identificador lo asigna como hoja y crea el nodo; si contiene paréntesis, lo asigna como sub-arbol y crea los nodos. (este tiene mas precedencia que T)
<br>
#### Al final se crea un .png con los arboles.

## Tarea 2 (comparación del algoritmos)
Use la misma gramatica de la tarea 1

### Recorrido del árbol (LL(0))
Este analizador sintactico recorre el arbol de izquierda a derecha profundizando los nodos, ademas de que tiene una complejidad de o(n). 
Se divide en 3 metodos (E, T y F), exactamente iguales a los de la tarea 1 <br>
<img width="425" height="765" alt="image" src="https://github.com/user-attachments/assets/39cb9247-f708-4b04-9869-773739acaeeb" /><br>
pero lo mas importante es como recorre el arbol sintactico:<br>
<img width="391" height="341" alt="image" src="https://github.com/user-attachments/assets/aa7d57cb-e703-4759-9853-e068dd26b1b4" /><br>
implemente un recorrido DFS que enumera cada nodo en orden de visita, esto permite ver como el parser recorrio la expresion

### Algoritmo CYK
Este algoritmo combina subcadenas y llena la tabla dinámicamente, por esta razon no se puede graficar su recorrido en forma de arbol y esto lo registre asi:<br> `(i, j, símbolo, dependencias)`<br><br>
<img width="626" height="796" alt="image" src="https://github.com/user-attachments/assets/f218a835-60ee-4cea-bf5e-87a3062f16e2" /><br>

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
### Medicion de tiempos
Para saber cuanto se tarda cada algoritmo en recorrer el arbol sintactico vamos a utilizar `time.perf_counter()`<br>
<img width="573" height="443" alt="image" src="https://github.com/user-attachments/assets/41977967-107f-4192-babf-d825e957555a" />
<br>

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Tarea 3 (Asociatividad y Precedencia)
Para este punto use una gramatica basica que define numero, parentesis, suma, resta, multiplicacion y division.<br>
<img width="403" height="74" alt="image" src="https://github.com/user-attachments/assets/31d1a585-c012-4694-929b-747c5d5f54c6" /><br><br>
Cree 3 parser para cada uno de los casos
#### 1. Asociatividad izquierda (el normalito)
Evalúa de izquierda a derecha<br>
<img width="275" height="545" alt="image" src="https://github.com/user-attachments/assets/79d3d365-896b-4895-950a-59ea4d9636fa" />
<br><br>

#### 2. Asociatividad derecha
Evalúa de derecha a izquierda<br>
<img width="654" height="563" alt="image" src="https://github.com/user-attachments/assets/7df385bb-0b73-4065-bc41-d7aa9afbf56a" />
<br><br>

#### 3. Precedencia invertida
`+` tiene mayor prioridad que `*`<br>
<img width="425" height="643" alt="Captura de pantalla 2026-03-26 104804" src="https://github.com/user-attachments/assets/78f9f9c5-51db-4a79-90bf-140fa646c60e" />

--------------------------------------------------------------------------------------------------------------------------------
