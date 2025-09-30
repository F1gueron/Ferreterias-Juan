#!/bin/bash

# Script para iniciar Ferreterías Juan como www-data
echo "🔨 Iniciando Ferreterías Juan como www-data..."

# Verificar si el usuario actual es www-data o si podemos cambiar a www-data
if [ "$(whoami)" != "www-data" ]; then
    if [ "$EUID" -eq 0 ]; then
        echo "📋 Cambiando a usuario www-data..."
        exec sudo -u www-data "$0" "$@"
    else
        echo "❌ Error: Se requieren privilegios para cambiar a www-data"
        echo "Ejecuta: sudo $0"
        exit 1
    fi
fi

echo "✅ Ejecutándose como usuario www-data"

# Verificar si estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: No se encuentra app.py"
    echo "Ejecuta este script desde el directorio ferreteria_juan"
    exit 1
fi

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo "📦 Activando entorno virtual..."
    source venv/bin/activate
fi

# Verificar conexión a base de datos
echo "🔍 Verificando conexión a base de datos..."
mysql -u ferreteria_user -pferreteria_pass123 -e "USE ferreteria_juan; SHOW TABLES;" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Conexión a base de datos OK"
else
    echo "⚠️  Error conectando a base de datos"
    echo "Ejecuta primero: ./install.sh"
fi

# Crear el directorio de uploads si no existe
UPLOADS_DIR="static/uploads"
if [ ! -d "$UPLOADS_DIR" ]; then
    echo "📁 Creando directorio de uploads en $UPLOADS_DIR..."
    mkdir -p "$UPLOADS_DIR"
fi

# Asegurar permisos correctos para www-data
echo "🔐 Configurando permisos para www-data..."
chown -R www-data:www-data static/uploads 2>/dev/null || true
chmod -R 755 static/uploads 2>/dev/null || true

# Mostrar información importante
echo ""
echo "🚀 Iniciando servidor Flask como www-data..."
echo ""
echo "⚠️  IMPORTANTE:"
echo "  • Esta aplicación contiene vulnerabilidades INTENCIONALES"
echo "  • Solo para uso educativo en laboratorio"
echo "  • Ejecutándose como www-data para mayor seguridad"
echo ""
echo "📱 URLs de acceso:"
echo "  • Principal: http://localhost:8080"
echo "  • Login: http://localhost:8080/login (admin/admin123)"
echo ""
echo "🔧 Para detener: Ctrl+C"
echo ""

# Iniciar aplicación en puerto 8080 (www-data no puede usar puerto 80)
python3 app.py