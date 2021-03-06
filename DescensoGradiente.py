#ALUMNO: ANGEL, GINER VIDAL
#EJERCICIO 3.8
#LENGUAJE EMPLEADO: PYTHON

#Implementar en el lenguaje de programacion que se desee el algoritmo de descenso por gradiente para minimizar la funcion de Rosenbrock.  
#Mostrar una traza de ejecucion hasta convergencia, con rho_k = K/k (donde K es una constante a determinar empiricamente), inicializando los parametros en el punto (-1, 1)^t.

#PARA EJECUTAR EL CODIGO: python DescensoGradiente.py -1 1 0 1 0.01 1000

#importamos las librerias sys para que podamos pasarle los parametros a la hora de ejecucion
# y la libreria math para hacer la raiz que necesitamos en la funcion euclidea
import sys
import math

#Funcion que nos devuelve los valores derivados de las coordenadas x e y de un punto
def DerivadaRosenbrock( x , y ):
    dx = 2*(20*(x**3) - 20*x*y + x - 1)
    dy = 20*(y-(x**2))
    return dx, dy
 
#Funcion de Rosenbrock que devuelve el valor, pasandole las coordenadas x e y de un punto
def FuncionRosenbrock(x , y ):
    val = 10*(y-x**2)**2+(1-x)**2
    return val
    
#Funcion que toma como parametros dos puntos y duevuelve la distancia euclidea entre esos puntos
def DistanciaEuclidea(fx , fy , rx , ry ):
    val = math.sqrt((rx - fx)**2 + (ry - fy)**2)
    return val

#Funcion que llamamos para cada k, toma como parametros un punto(x,y) la k que se esta comprobando
#y un maximo de iteraciones
def Gradiente( x , y , k, maxI ):
    #Guardamos los valores iniciales en las variables
    fx = x
    fy = y
    solx = x
    soly = y
    cont = 0
    for j in range(1, maxI):
        #Por cada iteracion reducimos el factor de aprendizaje, que es la magnitud que mueve el punto
        factApr = k/j
        try:
            dx,dy = DerivadaRosenbrock(fx,fy)
        except:
            #print(dx,dy)
            #print("OverflowError: (34, 'Numerical result out of range')")
            break
        #Guardamos los nuevos puntos
        rx = fx- dx * factApr
        ry = fy- dy * factApr
        try:
            distancia = DistanciaEuclidea(fx,fy,rx,ry)
            #Si la distancia es menor que el factor distancia que consideramos solucion guardamos 
            #el punto solucion y la iteracion en la que se ha encontrado solucion y terminamos el bucle
            if(distancia <= 0.00001): #Si aumentamos el valor de la condicion aumentaran el numero de soluciones, si lo reducimos se reduciran
                solx = fx
                soly = fy
                cont = 1
                break
        except:
            #print(distancia)
            #print("OverflowError: (34, 'Numerical result out of range')")
            break
        
        #Si no ha encontrado solucion se sobreescribe el punto anterior por el desplazado y guardamos la solucion
        fx = rx
        fy = ry
        solx = fx
        soly = fy
    if(cont != 1):
    	solx = -1
    return solx, soly

def EncuentraK( x , y , kmin , kmax , step , maxI ):
    #Creamos 3 listas con los valores de k, x e y
    listaK = []
    listaX = []
    listaY = []
    i = kmax
    j = 0
    while i >= kmin:
        #Obtenemos el punto solucion y su iteracion mediante la funcion anterior, y los anadimos a sus listas
        solx, soly = Gradiente( x , y , i, maxI )
        listaK.append(i)
        listaX.append(solx)
        listaY.append(soly)
        #Reducimos la k que comprobamos y incrementamos j en 1 por cada solucion que anadimos
        i -= step
        j = j +1

    for l in range(0, j):
        #if(l+15 < j):
        if(listaX[l] != -1):
        #pintarTraza(x , y , kopti , maxI)
            #Aqui llamamos a la funcion pintarTraza, que imprime la traza para cada k solucion
            pintarTraza(x , y , listaK[l] , maxI)
            #Aqui imprimimos la el valor de k y el ulimo punto al que llega justo antes de considerarlo solucion
            print('Valor de k: ',round(listaK[l],3),' Punto(',round(listaX[l], 5),round(listaY[l], 5))

def pintarTraza( x , y , k, maxI ):
    #Guardamos los valores iniciales en las variables
    fx = x
    fy = y
    solx = x
    soly = y
    listaX = []
    listaY = []
    l = 0
    listaX.append(fx)
    listaY.append(fy)
    for j in range(1, maxI):
        #Por cada iteracion reducimos el factor de aprendizaje, que es la magnitud que mueve el punto
        factApr = k/j
        try:
            dx,dy = DerivadaRosenbrock(fx,fy)
        except:
            print(dx,dy)
            print("OverflowError: (34, 'Numerical result out of range')")
            break
        #Guardamos los nuevos puntos
        rx = fx- dx * factApr
        ry = fy- dy * factApr
        try:
            distancia = DistanciaEuclidea(fx,fy,rx,ry)
            #Si la distancia es menor que el factor distancia que consideramos solucion guardamos 
            #el punto solucion y la iteracion en la que se ha encontrado solucion y terminamos el bucle
            if(distancia <= 0.00001):
                solx = fx
                soly = fy
                l = l +1
                listaX.append(solx)
                listaY.append(soly)
                break
        except:
            print(distancia)
            print("OverflowError: (34, 'Numerical result out of range')")
            break
        
        #Si no ha encontrado solucion se sobreescribe el punto anterior por el desplazado y guardamos la solucion
        fx = rx
        fy = ry
        solx = fx
        soly = fy
        l = l +1
        listaX.append(solx)
        listaY.append(soly)
        #Por otra parte imprimimos el valor de k y todas laas iteraciones, de aquellas k que guardamos y por tanto consideramos solucion.
    for x in range(0, l):
        print('Valor de k: ',round(k, 3),'Iteracion: ',x,' Punto(',round(listaX[x], 5),round(listaY[x], 5))
    
    

if __name__ == "__main__":
    if len(sys.argv) == 7:
        x = float(sys.argv[1])        #Punto x inicial
        y = float(sys.argv[2])        #Punto y inicial  
        kmin = float(sys.argv[3])     #k minima que queremos considerar
        kmax = float(sys.argv[4])     #k maxima que queremos considerar
        step = float(sys.argv[5])     #Desplazamiento entre k
        maxI = int(sys.argv[6])       #Maximo de iteraciones en caso de no llegar a converger
        EncuentraK(x,y,kmin,kmax,step,maxI)
    else:
    	
        syntax()
