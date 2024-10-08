from flask import Flask, render_template, request, redirect, url_for, session, flash
from main_code import Archivo_Pelicula, Archivo_Clientes, Archivo_Compra, Pelicula, Clientes, Compra, SistemaReportes

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_super_segura'

# Instanciar archivos
archivo_peliculas = Archivo_Pelicula('peliculas.json')
archivo_clientes = Archivo_Clientes('clientes.json')
archivo_compras = Archivo_Compra('compras.json')

### Página principal mostrando 5 películas
@app.route('/')
def index():
    peliculas = archivo_peliculas.leer_pelicula()[:4] if archivo_peliculas.leer_pelicula() else []
 
    peliculalista = archivo_peliculas.leer_pelicula()  if archivo_peliculas.leer_pelicula() else []
    directores = list(set([pelicula['director'] for pelicula in peliculalista]))[:5]
    generos = list(set([pelicula['genero'] for pelicula in peliculalista]))[:5]
    anios = sorted(set(int(pelicula['año']) for pelicula in peliculalista))[:5]


    return render_template('index.html', peliculas=peliculas, directores=directores, generos=generos, anios=anios)

# Página de administrador: listar todas las películas
@app.route('/peliculas', methods=['GET'])
def listar_peliculas():
    peliculas = archivo_peliculas.leer_pelicula()  
    return render_template('listar_peliculas.html', peliculas=peliculas)

@app.route('/buscar', methods=['POST'])
def buscar_peliculas():
    query = request.form.get('query', '').strip().lower()  # Obtener la consulta en minúsculas

    peliculas = archivo_peliculas.leer_pelicula()  

    # Filtrar películas según el criterio de búsqueda
    peliculas_encontradas = [
        pelicula for pelicula in peliculas
        if (query in pelicula['titulo'].lower() or
            query in pelicula['director'].lower() or
            query in pelicula['genero'].lower() or
            query in pelicula['id'].lower() or
            int(query) == pelicula['año'])
    ]

    return render_template('listar_peliculas.html', peliculas=peliculas_encontradas, query=query)

# Agregar una película
@app.route('/agregar_pelicula', methods=['POST'])
def agregar_pelicula():
    id = request.form['id']
    titulo = request.form['titulo']
    director = request.form['director']
    año = request.form['año']
    genero = request.form['genero']
    precio = request.form['precio']

    nueva_pelicula = Pelicula(id, titulo, director, año, genero, precio)
    archivo_peliculas.agregar_pelicula(nueva_pelicula)
    return redirect(url_for('listar_peliculas'))

# Eliminar una película
@app.route('/eliminar_pelicula/<id>', methods=['POST'])
def eliminar_pelicula(id):
    archivo_peliculas.eliminar_pelicula(id)
    return redirect(url_for('listar_peliculas'))

@app.route('/abrir_modal_pelicula/<id>')
def abrir_modal_pelicula(id):
    
    peliculas = archivo_peliculas.leer_pelicula()  # 
    pelicula = next((p for p in peliculas if str(p['id']) == str(id)), None)

    if pelicula:
        session['modal_pelicula'] = pelicula
        session['modal_abierto'] = True
    else:
        session['modal_pelicula'] = None
        session['modal_abierto'] = False

    return redirect(url_for('listar_peliculas')) 

@app.route('/cerrar_modal_pelicula')
def cerrar_modal_pelicula():
    session['modal_abierto'] = False
    session['modal_pelicula'] = None  
    return redirect(url_for('listar_peliculas'))

@app.route('/actualizar_pelicula/<id>', methods=['POST'])
def actualizar_pelicula(id):
    
    peliculas = archivo_peliculas.leer_pelicula()  # 
    pelicula = None
    
    for p in peliculas:
        if str(p['id']) == str(id):  
            pelicula = p
            break

    if pelicula is None:
    
        return redirect(url_for('listar_peliculas'))

    pelicula['titulo'] = request.form['titulo']
    pelicula['director'] = request.form['director']
    pelicula['año'] = request.form['año']
    pelicula['genero'] = request.form['genero']
    pelicula['precio'] = request.form['precio']

    archivo_peliculas.actualizar_pelicula(peliculas)  # 
    session['modal_abierto'] = False
    return redirect(url_for('listar_peliculas'))  

# Buscar películas por director
@app.route('/buscar/director/<director>')
def buscar_por_director(director):
    peliculas_encontradas = archivo_peliculas.buscar_pelicula_por_director(director)
    return render_template('resultados.html', peliculas=peliculas_encontradas)

# Buscar películas por género
@app.route('/buscar/genero/<genero>')
def buscar_por_genero(genero):
    peliculas_encontradas = archivo_peliculas.buscar_pelicula_por_genero(genero)
    return render_template('resultados.html', peliculas=peliculas_encontradas)

# Buscar películas por año
@app.route('/buscar/anio/<anio>')
def buscar_por_anio(anio):
    try:
        peliculas_encontradas = archivo_peliculas.buscar_pelicula_por_año(int(anio))
        return render_template('resultados.html', peliculas=peliculas_encontradas)
    except ValueError:
        return "Año inválido.", 400

### --- CRUD Clientes ---
@app.route('/clientes')
def listar_clientes():
    clientes = archivo_clientes.leer_clientes()
 
    return render_template('clientes.html', clientes=clientes, )

@app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    id = request.form['id']
    nombre = request.form['nombre']
    correo = request.form['correo']
    direccion = request.form['direccion']

    nuevo_cliente = Clientes(id, nombre, correo, direccion)
    archivo_clientes.agregar_cliente(nuevo_cliente)
    return redirect(url_for('listar_clientes'))

@app.route('/abrir_modal/<id>')
def abrir_modal(id):
    clientes = archivo_clientes.leer_clientes()
    cliente = next((c for c in clientes if str(c['id']) == str(id)), None)

    if cliente:
        session['modal_cliente'] = cliente
        session['modal_abierto'] = True
    else:
        session['modal_cliente'] = None
        session['modal_abierto'] = False

    return redirect(url_for('listar_clientes')) 

@app.route('/actualizar_cliente/<id>', methods=['POST'])
def actualizar_cliente(id):
    
    clientes = archivo_clientes.leer_clientes()  
    cliente = None
    
    for c in clientes:
        if c['id'] == id:  
            cliente = c
            break

    if cliente is None:
        
        return redirect(url_for('listar_clientes'))  

   
    cliente['nombre'] = request.form['nombre']
    cliente['correo'] = request.form['correo']
    cliente['direccion'] = request.form['direccion']

    archivo_clientes.actualizar_clientes(clientes)  
    session['modal_abierto'] = False
    return redirect(url_for('listar_clientes'))  

@app.route('/buscar_clientes', methods=['POST'])
def buscar_clientes():
    query = request.form.get('query', '').strip().lower()  

    clientes = archivo_clientes.leer_clientes()  
    clientes_encontrados = [
        cliente for cliente in clientes
        if (query in cliente['id'].lower() or 
            query in cliente['nombre'].lower())
    ]

    return render_template('clientes.html', clientes=clientes_encontrados, query=query)

@app.route('/cerrar_modal')
def cerrar_modal():
    session['modal_abierto'] = False  
    return redirect(url_for('listar_clientes')) 

@app.route('/eliminar_cliente/<id>', methods=['POST'])
def eliminar_cliente(id):
    archivo_clientes.eliminar_cliente(id)
    return redirect(url_for('listar_clientes'))

### --- CRUD Compras ---
@app.route('/compras')
def listar_compras():
    compras = archivo_compras.leer_compra()
    return render_template('compras.html', compras=compras)


@app.route('/agregar_compra', methods=['POST'])
def agregar_compra():
    id_compra = request.form['id_compra']
    id_cliente = request.form['id_cliente']
    id_pelicula = request.form['id_pelicula']
    fecha = request.form['fecha']

    nueva_compra = Compra(id_compra, id_cliente, id_pelicula, fecha)
    mensaje = archivo_compras.agregar_compra(nueva_compra)
    flash(mensaje)
    print(mensaje)
    return redirect(url_for('listar_compras'))

@app.route('/buscar_compras', methods=['POST'])
def buscar_compras():
    query = request.form.get('query', '').strip().lower() 

    compras = archivo_compras.leer_compra()  
    compras_encontradas = [
        compra for compra in compras
        if query in str(compra['id_compra']).lower()  
    ]
    return render_template('compras.html', compras=compras_encontradas, query=query)

@app.route('/eliminar_compra/<id_compra>', methods=['POST'])
def eliminar_compra(id_compra):
    archivo_compras.eliminar_compra(id_compra)
    return redirect(url_for('listar_compras'))

@app.route('/abrir_modal_compra/<id>', methods=['GET'])
def abrir_modal_compra(id):
    compras = archivo_compras.leer_compra()  
    compra = next((c for c in compras if str(c['id_compra']) == str(id)), None)

    if compra:
        session['modal_compra'] = compra
        session['modal_abierto'] = True
    else:
        session['modal_compra'] = None
        session['modal_abierto'] = False

    return redirect(url_for('listar_compras'))  

@app.route('/actualizar_compra/<id>', methods=['POST'])
def actualizar_compra(id):
    compras = archivo_compras.leer_compra()  
    compra = None
    
    for c in compras:
        if str(c['id_compra']) == str(id):  
            compra = c
            break

    if compra is None:
        return redirect(url_for('listar_compras'))  

    
    
    compra['fecha'] = request.form['fecha']

    archivo_compras.actualizar_compra(compras)  
    session['modal_abierto'] = False
    return redirect(url_for('listar_compras'))  


@app.route('/reportes', methods=['GET', 'POST'])
def reportes():
    sistema_reportes = SistemaReportes(archivo_compras, archivo_peliculas, archivo_clientes)

    if request.method == 'POST':
        reporte = request.form.get('reporte')

        if reporte == 'peliculas_mas_vendidas':
            peliculas_mas_vendidas = sistema_reportes.obtener_peliculas_mas_vendidas()
            return render_template('reportes.html', peliculas_mas_vendidas=peliculas_mas_vendidas)

        elif reporte == 'clientes_mas_compras':
            clientes_mas_compras = sistema_reportes.obtener_clientes_con_mas_compras()
            return render_template('reportes.html', clientes_mas_compras=clientes_mas_compras)

        elif reporte == 'ventas_por_intervalo':
            fecha_inicio = request.form.get('fecha_inicio')
            fecha_fin = request.form.get('fecha_fin')
            ventas_por_intervalo = sistema_reportes.ventas_por_intervalo(fecha_inicio, fecha_fin)
            return render_template('reportes.html', ventas_por_intervalo=ventas_por_intervalo)

    return render_template('reportes.html')

if __name__ == '__main__':
    app.run(debug=True)