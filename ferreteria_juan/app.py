"""
Ferreterías Juan - Aplicación Web Vulnerable
Proyecto educativo de ciberseguridad
SOLO PARA ENTORNO DE LABORATORIO
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from mysql.connector import Error
import os
from werkzeug.utils import secure_filename
import hashlib
import logging
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'ferreteria_juan_secret_key_123'  # ⚠️ Clave débil intencional (Vulnerable a CSRF y manipulación de sesión)


# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'ferreteria_juan',
    'user': 'ferreteria_user',
    'password': 'ferreteria_pass123',  # ⚠️ Contraseña débil intencional
    'port': 3306
}

# Configuración de uploads (VULNERABLE)
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'php', 'py'}  # ⚠️ Permite archivos peligrosos
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Configurar logging para el Blue Team
logging.basicConfig(
    filename='ferreteria_juan.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_db_connection():
    """Obtener conexión a la base de datos"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        app.logger.error(f"Error conectando a MySQL: {e}")
        return None

def init_database():
    """Inicializar base de datos con datos de ejemplo"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()

        # Crear tabla productos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(200) NOT NULL,
            precio DECIMAL(10,2) NOT NULL,
            categoria VARCHAR(100) NOT NULL,
            descripcion TEXT,
            stock INT DEFAULT 0,
            imagen VARCHAR(200),
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Crear tabla usuarios
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(150),
            rol VARCHAR(50) DEFAULT 'cliente',
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Crear tabla comentarios
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS comentarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            email VARCHAR(150),
            comentario TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Insertar productos de ejemplo
        productos_ejemplo = [
            ('Martillo Carpintero 500g', 15.99, 'Herramientas Manuales', 'Martillo de carpintero con mango de madera resistente', 50, 'martillo.jpg'),
            ('Destornillador Phillips', 8.50, 'Herramientas Manuales', 'Destornillador Phillips de precisión', 75, 'destornillador.jpg'),
            ('Taladro Eléctrico 650W', 89.99, 'Herramientas Eléctricas', 'Taladro eléctrico profesional 650W', 25, 'taladro.jpg'),
            ('Tornillos 4x50mm (100 uds)', 12.75, 'Tornillería', 'Pack de 100 tornillos galvanizados 4x50mm', 200, 'tornillos.jpg'),
            ('Pintura Blanca 4L', 25.90, 'Pintura', 'Pintura acrílica blanca mate interior/exterior', 30, 'pintura.jpg'),
            ('Cable Eléctrico 2.5mm', 45.00, 'Electricidad', 'Cable eléctrico 2.5mm por metro', 500, 'cable.jpg'),
            ('Llave Inglesa 10"', 18.25, 'Herramientas Manuales', 'Llave inglesa ajustable 10 pulgadas', 40, 'llave.jpg'),
            ('Sierra Eléctrica Circular', 120.00, 'Herramientas Eléctricas', 'Sierra circular eléctrica 1200W', 15, 'sierra.jpg'),
            ('Clavos 3" (1 kg)', 5.99, 'Tornillería', 'Clavos de acero galvanizado 3 pulgadas', 100, 'clavos.jpg'),
            ('Brocha 2"', 7.50, 'Pintura', 'Brocha para pintura 2 pulgadas', 60, 'brocha.jpg'),
            ('Interruptor Simple', 3.25, 'Electricidad', 'Interruptor eléctrico simple blanco', 80, 'interruptor.jpg'),
            ('Alicates Universales', 22.80, 'Herramientas Manuales', 'Alicates universales profesionales', 35, 'alicates.jpg'),
            ('Amoladora Angular 4.5"', 85.00, 'Herramientas Eléctricas', 'Amoladora angular 4.5 pulgadas 850W', 20, 'amoladora.jpg'),
            ('Tuercas M8 (50 uds)', 8.90, 'Tornillería', 'Pack de 50 tuercas hexagonales M8', 150, 'tuercas.jpg'),
            ('Imprimante Universal', 18.75, 'Pintura', 'Imprimante universal para superficies', 25, 'imprimante.jpg'),
            ('Enchufe Schuko', 4.50, 'Electricidad', 'Enchufe con toma de tierra Schuko', 90, 'enchufe.jpg'),
            ('Nivel de Burbuja 60cm', 16.99, 'Herramientas Manuales', 'Nivel de burbuja profesional 60cm', 30, 'nivel.jpg'),
            ('Soldador Eléctrico 40W', 65.00, 'Herramientas Eléctricas', 'Soldador eléctrico de estaño 40W', 25, 'soldador.jpg'),
            ('Arandelas M6 (100 uds)', 6.25, 'Tornillería', 'Pack de 100 arandelas planas M6', 180, 'arandelas.jpg'),
            ('Rodillo Pintura 22cm', 9.99, 'Pintura', 'Rodillo para pintura lisa 22cm', 45, 'rodillo.jpg')
        ]

        cursor.executemany("""
        INSERT IGNORE INTO productos (nombre, precio, categoria, descripcion, stock, imagen) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """, productos_ejemplo)

        # Insertar usuarios de ejemplo
        usuarios_ejemplo = [
            ('admin', 'admin123', 'admin@ferreteriajuan.com', 'administrador'),
            ('juan', 'ferreteria2024', 'juan@ferreteriajuan.com', 'empleado'),
            ('maria', 'cliente123', 'maria@cliente.com', 'cliente'),
            ('test', 'test', 'test@test.com', 'cliente')
        ]

        cursor.executemany("""
        INSERT IGNORE INTO usuarios (username, password, email, rol) 
        VALUES (%s, %s, %s, %s)
        """, usuarios_ejemplo)

        connection.commit()
        cursor.close()
        connection.close()
        print("✓ Base de datos inicializada correctamente")

@app.route('/')
def index():
    """Página principal"""
    connection = get_db_connection()
    productos_destacados = []

    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos LIMIT 6")
        productos_destacados = cursor.fetchall()
        cursor.close()
        connection.close()

    return render_template('index.html', productos=productos_destacados)

@app.route('/whoAreUs')
def quienes_somos():
    return render_template('whoAreUs.html')


@app.route('/catalogo')
def catalogo():
    """Catálogo de productos con búsqueda VULNERABLE"""
    search = request.args.get('search', '')
    categoria = request.args.get('categoria', '')

    connection = get_db_connection()
    productos = []
    categorias = ['Herramientas Manuales', 'Herramientas Eléctricas', 'Tornillería', 'Pintura', 'Electricidad']

    if connection:
        cursor = connection.cursor(dictionary=True)

        # ⚠️ VULNERABILIDAD SQL INJECTION INTENCIONAL
        if search:
            # Log para el Blue Team TODO
            # app.logger.info(f"Búsqueda realizada: {search} desde IP: {request.remote_addr}")

            # Query vulnerable - NO sanitizada
            query = f"SELECT * FROM productos WHERE nombre LIKE '%{search}%' OR descripcion LIKE '%{search}%'"
            if categoria:
                query += f" AND categoria = '{categoria}'"

            try:
                cursor.execute(query)
                productos = cursor.fetchall()
            except Error as e:
                app.logger.error(f"Error SQL: {e} - Query: {query}")
                flash(f"Error en la búsqueda: {str(e)}", 'danger')
                # Mostrar error para facilitar explotación (VULNERABLE) TODO
                return render_template('catalogo.html', productos=[], categorias=categorias, 
                                     search=search, categoria=categoria, error=str(e))
        else:
            if categoria:
                cursor.execute("SELECT * FROM productos WHERE categoria = %s", (categoria,))
            else:
                cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()

        cursor.close()
        connection.close()

    return render_template('catalogo.html', productos=productos, categorias=categorias, 
                         search=search, categoria=categoria)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login vulnerable a SQL Injection"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Log intento de login TODO
        #app.logger.info(f"Intento de login: {username} desde IP: {request.remote_addr}")

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)

            # ⚠️ VULNERABILIDAD SQL INJECTION EN LOGIN
            query = f"SELECT * FROM usuarios WHERE username = '{username}' AND password = '{password}'"

            try:
                cursor.execute(query)
                user = cursor.fetchone()

                if user:
                    session['logged_in'] = True
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['rol'] = user['rol']

                    app.logger.info(f"Login exitoso: {username}")
                    flash(f'Bienvenido {username}!', 'success')

                    if user['rol'] == 'administrador':
                        return redirect(url_for('admin'))
                    else:
                        return redirect(url_for('index'))
                else:
                    flash('Usuario o contraseña incorrectos', 'danger')

            except Error as e:
                #app.logger.error(f"Error SQL en login: {e} - Query: {query}")
                # Mostrar error SQL para facilitar explotación TODO:
                flash(f'Error en el sistema: {str(e)}', 'danger')

            cursor.close()
            connection.close()

    return render_template('login.html')

@app.route('/comentarios', methods=['GET', 'POST'])
def comentarios():
    """Sección de comentarios VULNERABLE a XSS"""
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        comentario = request.form['comentario']

        # Log comentario TODO:
        #app.logger.info(f"Nuevo comentario de: {nombre} ({email})")

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()

            # ⚠️ INSERTAR SIN SANITIZAR - VULNERABLE A XSS STORED
            cursor.execute("""
            INSERT INTO comentarios (nombre, email, comentario) 
            VALUES (%s, %s, %s)
            """, (nombre, email, comentario))

            connection.commit()
            cursor.close()
            connection.close()

            flash('Comentario enviado correctamente', 'success')
            return redirect(url_for('comentarios'))

    # Obtener comentarios existentes
    connection = get_db_connection()
    comentarios_list = []

    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM comentarios ORDER BY fecha DESC")
        comentarios_list = cursor.fetchall()
        cursor.close()
        connection.close()

    return render_template('comentarios.html', comentarios=comentarios_list)

@app.route('/admin')
def admin():
    """Panel administrativo"""
    if not session.get('logged_in') or session.get('rol') != 'administrador':
        flash('Acceso denegado. Se requieren privilegios de administrador.', 'danger')
        return redirect(url_for('login'))

    connection = get_db_connection()
    stats = {}

    if connection:
        cursor = connection.cursor(dictionary=True)

        # Estadísticas básicas
        cursor.execute("SELECT COUNT(*) as total FROM productos")
        stats['productos'] = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) as total FROM usuarios")
        stats['usuarios'] = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) as total FROM comentarios")
        stats['comentarios'] = cursor.fetchone()['total']

        cursor.close()
        connection.close()

    return render_template('admin.html', stats=stats)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Upload de archivos VULNERABLE"""
    if not session.get('logged_in'):
        flash('Debes iniciar sesión para subir archivos', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No se seleccionó ningún archivo', 'danger')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No se seleccionó ningún archivo', 'danger')
            return redirect(request.url)

        # ⚠️ VULNERABILIDAD: Sin validación de tipo de archivo
        if file:
            # Log upload TODO
            #app.logger.warning(f"Archivo subido: {file.filename} por {session.get('username')}")

            # Guardar archivo sin validación (VULNERABLE)
            filename = file.filename  # Sin secure_filename() intencionalmente
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Si el archivo es .py, ejecutarlo (VULNERABLE)
            if filename.endswith('.py'):
                try:
                    exec(open(file_path, encoding="utf-8").read())
                    flash(f'Archivo {filename} subido y ejecutado correctamente', 'success')
                except Exception as e:
                    flash(f'Error al ejecutar {filename}: {str(e)}', 'danger')
                    return redirect(url_for('upload_file'))
            else:
                flash(f'Archivo {filename} subido y no ejecutado correctamente', 'success')
            return redirect(url_for('upload_file'))

    # Listar archivos subidos
    uploaded_files = []
    upload_path = app.config['UPLOAD_FOLDER']
    if os.path.exists(upload_path):
        uploaded_files = os.listdir(upload_path)

    return render_template('upload.html', files=uploaded_files)

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    username = session.get('username', 'Desconocido')
    app.logger.info(f"Usuario {username} cerró sesión")

    session.clear()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('index'))

# ⚠️ ENDPOINT VULNERABLE PARA DEBUG
@app.route('/debug')
def debug():
    """Endpoint de debug que expone información sensible"""
    if not app.debug:  # Solo en modo debug
        return "Debug mode disabled", 404

    debug_info = {
        'session': dict(session),
        'db_config': DB_CONFIG,
        'app_config': dict(app.config),
        'environment': dict(os.environ)
    }

    return jsonify(debug_info)

if __name__ == '__main__':
    # Inicializar base de datos
    init_database()

    # Ejecutar aplicación
    print("🔨 Ferreterías Juan - Servidor iniciando...")
    print("⚠️  ATENCIÓN: Esta aplicación contiene vulnerabilidades INTENCIONALES")
    print("⚠️  SOLO para uso educativo en entorno de laboratorio")
    print("🌐 Acceso: http://localhost")
    print("🔗 Login admin: admin/admin123")

    app.run(host='0.0.0.0', port=80, debug=True)
