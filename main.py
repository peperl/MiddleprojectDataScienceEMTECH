import math
from lifestore_file import *

"""
Funciones genéricas
Funciones para que se usen en diferentes contextos
"""
def imprimirReporteVentas(result):
	for key in result.keys():
	    print(key)
	    for llave, valor in result[key].items():
	        print(f'\t {llave}: {valor}')

def imprimirDiccionario(diccionario):

	for key, value in diccionario.items():
		print(key, ' : ', value)
	return

def getProductosDiccionario(productos):
	result = {}
	for producto in productos:
		result[producto[0]] = producto[1:]
	return result

"""
	Devuelve un diccionario con la siguiente estructura: 
	key = idproducto
	value = review
"""
def getReviews(ventas):
	# Diccionario de reviews por id
	prods_reviews = {}
	for sale in ventas:
	    prod_id = sale[1]
	    review = sale[2]
	    if prod_id not in prods_reviews.keys():
	        prods_reviews[prod_id] = []
	    prods_reviews[prod_id].append(review)
	return prods_reviews

def clasificarVentas_X_Producto(productos, ventas, seConsideranDevoluciones):
	productosVendidos = [[venta[0], venta[1], venta[4]] for venta in ventas]
	productos_clasificados = {}
	for par in productosVendidos:
		if not seConsideranDevoluciones:
			if( not par[2]):

				producto = par[1]
				if producto not in productos_clasificados.keys():
					productos_clasificados[producto] = 1
				else:
					productos_clasificados[producto] += 1
		else:
			producto = par[1]
			if producto not in productos_clasificados.keys():
				productos_clasificados[producto] = 1
			else:
				productos_clasificados[producto] += 1
	return productos_clasificados

"""
Clasificar productos por categoria
"""
def clasificarProductos_X_categoria(productos):
	id_categoria = [[producto[0], producto[3]] for producto in productos]

	productos_clasificados = {}
	for par in id_categoria:
		id = par[0]
		categoria = par[1]
		if categoria not in productos_clasificados.keys():
			productos_clasificados[categoria] = []
		productos_clasificados[categoria].append(id)
	return productos_clasificados

"""
Clasificar las ventas por mes, devolviendo un diccionario con los id del producto
"""
def clasificarVentas_x_mes(ventas):
	id_venta = [[venta[1], venta[3], venta[4]] for venta in ventas]
	ventasclasificadas = {}
	for par in id_venta:
		id = par[0]
		_, mes, _ = par[1].split('/')
		seDevolvioElProducto = par[2]
		if not seDevolvioElProducto:
			if mes not in ventasclasificadas.keys():
				ventasclasificadas[mes] = []
			ventasclasificadas[mes].append(id)
	return ventasclasificadas

"""
Clasificar productos por categoria
"""
def clasificarBusquedas_x_Producto(busquedas):
	busquedas_clasificadas = {}
	for par in busquedas:
		idProducto = par[1]
		if idProducto not in busquedas_clasificadas.keys():
			busquedas_clasificadas[idProducto] = 1
		else:
			busquedas_clasificadas[idProducto] += 1
	return busquedas_clasificadas

"""
	Ordena un listado de productos por ventas
	Argumento 1 tipo booleando. Si es True se ordena ascendentemente, si es false se ordena descendentemente
	Argumento 2. Productos a ordenar
	Argumento 3. Si es falso no se consideran ventas que hayan sido devueltas
"""
def ordenarProductos_X_ventas(esAscendente, productos, ventas, seConsideranDevoluciones ):

	ventasX_Producto = clasificarVentas_X_Producto(productos,ventas, seConsideranDevoluciones)
	if esAscendente:
		ventasX_Producto = sorted(ventasX_Producto.items(), key=lambda item : item[1])
	else:
		ventasX_Producto = sorted(ventasX_Producto.items())
	productosDiccionario = getProductosDiccionario(productos)
	resultado = [[venta[0]] for venta in ventasX_Producto]

	for x in range(len(ventasX_Producto)):
		resultado[x].append(productosDiccionario[resultado[x][0]][0])
		resultado[x].append(productosDiccionario[resultado[x][0]][1])
		resultado[x].append(productosDiccionario[resultado[x][0]][2])
		resultado[x].append(productosDiccionario[resultado[x][0]][3])
		resultado[x].append(ventasX_Producto[x][1])

	return resultado

"""
Generar un listado de los 5 productos menos vendidos por categoria.
"""
def listadoProductos_X_Categoria_con_MenoresVentas(numeroDeElementos):
	productosOrdenados = ordenarProductos_X_ventas(True, lifestore_products, lifestore_sales, False)
	resultado = clasificarProductos_X_categoria(productosOrdenados)

	### al resultado se acotará la lista a 5 elementos
	for key, value in resultado.items():
		resultado[key] = resultado[key][:numeroDeElementos]
	resultado = dict(sorted(resultado.items()))

	return resultado

"""
Generar un listado de los 5 productos con mayores ventas por mes.
"""
def listadoProductos_X_Mes_con_MeyoresVentas(numeroDeElementos):
	ventasXMes = clasificarVentas_x_mes(lifestore_sales)
	result = {}
	for key, value in ventasXMes.items():
		aux = {}
		for idProducto in value:
			if idProducto not in aux:
				aux[idProducto] = 1
			else:
				aux[idProducto] += 1
		#Si numeroDeElementos es igual a 0 devuelve todos los elementos
		if numeroDeElementos == 0:
			result[key] = dict( sorted(aux.items(), key=lambda item:item[1],reverse=True))
		else:
			result[key] = dict( sorted(aux.items(), key=lambda item:item[1],reverse=True)[:numeroDeElementos] )
	return sorted(result.items())

"""
Generar un listado de los 10 productos con mayores/menores búsquedas.
"""
def listadoBusquedas_X_Producto(numeroDeElementos,isTop):
	if isTop:
		result = sorted(clasificarBusquedas_x_Producto(lifestore_searches).items(), key=lambda item: item[1],reverse=True)[:numeroDeElementos]
	else:
		result = sorted(clasificarBusquedas_x_Producto(lifestore_searches).items(), key=lambda item: item[1])[:numeroDeElementos]
	return result
	
"""
un listado para 20 productos con las mejores reseñas, considerando los productos con devolución.
"""
"""
un listado para 20 productos con las peores reseñas, considerando los productos con devolución.
"""
def promedioReviews_x_producto(elOrdenEsAscendente, numeroDeElementos):

	# De las ventas obtenemos el id_product y reseña, no necesitamos el resto de info
	# tampoco filtramos si fue o no devolucion, nos sigue interesando esa reseña.
	id_reviews_not_separated = [[sale[1], sale[2]] for sale in lifestore_sales]

	# Para llevar la cuenta usaremos un diccionario, esto quiere decir que en
	# nuestros calculos solamente incluiremos productos con reseña., por cada prod
	# guardaremos una lista de sus reviews
	id_reviews_count = {}
	reviewsPromedio_X_Producto = {}

	for par in id_reviews_not_separated:
	    # Tengo ID y review
	    id = par[0]
	    review = par[1]
	    # Si el id del producto aun no existe como llave, la creamos para tener
	    # un lugar donde guardar la review (una lista vacia)
	    if id not in id_reviews_count.keys():
	        id_reviews_count[id] = []
	    # En el diccionario, dentro agregamos la review al producto correspondiente
	    id_reviews_count[id].append(review)


	"""
	explicacion de la variable id_reviews_count:

	id_reviews_count 
	Es un diccionario, cuyas llaves son id's de productos.
	Cada llave del diccionario es un numero entero, entrega de resultado una lista
	de cada review que existe para ese producto.
	"""

	# Encontrar el promedio de review de cada producto:
	for id_product in id_reviews_count.keys():
	    lista_reviews = id_reviews_count[id_product]
	    promedio = sum(lista_reviews) / len(lista_reviews)
	    # Arreglo promedio a 2 decimales
	    decimales = 2
	    multiplicador = 10 ** decimales
	    promedio = math.ceil(promedio * multiplicador) / multiplicador
	    reviewsPromedio_X_Producto[id_product] = promedio

	if elOrdenEsAscendente:
		reviewsPromedio_X_Producto = sorted(reviewsPromedio_X_Producto.items(), key=lambda item: item[1])[:numeroDeElementos]
	else:
		reviewsPromedio_X_Producto = sorted(reviewsPromedio_X_Producto.items(), key=lambda item: item[1], reverse=True)[:numeroDeElementos]
	return reviewsPromedio_X_Producto
	
"""
Total de ingresos y ventas promedio mensuales,
"""
"""
 y meses con más ventas al año
	1er parametro selecciona el orden de los meses
		1 = orden cronologico
		2 = orden por más ventas
		3 = orden por menores ventas
"""
def reporteVentas_x_mes(orden):

	ventas_x_mes = dict (listadoProductos_X_Mes_con_MeyoresVentas(0))
	ganancias_x_mes = {}
	# Ventas por categorias
	result = {}
	productosDiccionario = getProductosDiccionario(lifestore_products)

	for mes, value in ventas_x_mes.items():
		ganancias_x_mes[mes] = 0
		for idProducto, ventasDelProducto in value.items():
			costoProducto = productosDiccionario[idProducto][1]
			ganancias_x_mes[mes] += costoProducto
	
	for mes, ganancia in ganancias_x_mes.items():

		ventas = ventas_x_mes[mes]
		total_venta = 0
		for idProducto, venta in ventas.items():
			total_venta += venta 
		result[mes] = {'ganancia_mensual': ganancia,
	        	               'venta_mensual': total_venta}
	if orden == 2:
		result = dict(sorted(result.items(), key=lambda item: item[1]["venta_mensual"],reverse=True))
	elif orden == 3:
		result = dict(sorted(result.items(), key=lambda item: item[1]["venta_mensual"],reverse=False))
	return result

"""
total anual
"""
def totalAnual():
	reporteMensual = reporteVentas_x_mes(0)
	ganancia_total = 0
	venta_total = 0
	
	for mes, reporte in reporteMensual.items():
		ganancia_total += reporte['ganancia_mensual']
		venta_total += reporte['venta_mensual']
	print('La ganancia total anual fue de', ganancia_total)
	print('La venta total anual fue de', venta_total)


# print('El valor promedio de los primeros 10 prod: ', suma/10)


def login():
    """
    Login
    credenciales:

    usuario:
        jimmy
    contrase;a:
        ymmij
    """

    usuarioAccedio = False
    intentos = 0

    # Bienvenida!
    mensaje_bienvenida = 'Bienvenide al sistema!\nAccede con tus credenciales'
    print(mensaje_bienvenida)

    # Recibo constantemente sus intentos
    while not usuarioAccedio:
        # Primero ingresa Credenciales
        usuario = input('Usuario: ')
        contras = input('Contrase;a: ')
        intentos += 1
        # Reviso si el par coincide
        if usuario == 'jimmy' and contras == 'ymmij':
            usuarioAccedio = True
            print('Hola de nuevo!')
        else:
            # print('Tienes', 3 - intentos, 'intentos restantes')
            print(f'Tienes {3 - intentos} intentos restantes')
            if usuario == 'jimmy':
                print('Te equivocaste en la contrase;a')
            else:
                print(f'El usuario: "{usuario}" no esta registrado')

        if intentos == 3:
            exit()


def menu():
    login()
    while True:
        print('Que operacion desea hacer:')
        print('\t1. Realizar el punto 1')
        print('\t2. Realizar el punto 2')
        print('\t2. Realizar el punto 3')
        print('\t0. Salir')
        seleccion = input('> ')
        if seleccion == '1':
        	result1 = listadoProductos_X_Categoria_con_MenoresVentas(5)
        	result2 = listadoProductos_X_Mes_con_MeyoresVentas(5)
        	result3 = listadoBusquedas_X_Producto(10,True)
        	result4 = listadoBusquedas_X_Producto(10,False)
        	print('\n')
        elif seleccion == '2':
        	result5 = promedioReviews_x_producto(True,20)
        	result6 = promedioReviews_x_producto(False,20)
        	print('\n')
        elif seleccion == '3':
        	result7 = reporteVentas_x_mes(1)
        	result8 = reporteVentas_x_mes(2)
        	result9 = totalAnual()
        	print('\n')
        elif seleccion == '0':
            exit()
        else:
            print('Opcion invalida!')

menu()