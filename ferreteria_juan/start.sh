#!/bin/bash

# Script para iniciar Ferreterías Juan
echo "🔨 Iniciando Ferreterías Juan..."

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

# Mostrar información importante
echo ""
echo "🚀 Iniciando servidor Flask..."
echo ""
echo "⚠️  IMPORTANTE:"
echo "  • Esta aplicación contiene vulnerabilidades INTENCIONALES"
echo "  • Solo para uso educativo en laboratorio"
echo "  • Puerto 80 (requiere privilegios root o usar puerto >1024)"
echo ""
echo "📱 URLs de acceso:"
echo "  • Principal: http://localhost"
echo "  • Login: http://localhost/login (admin/admin123)"
echo ""
echo "🔧 Para detener: Ctrl+C"
echo ""

# Verificar puerto 80
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  Advertencia: No tienes privilegios root."
    echo "La aplicación intentará usar puerto 80 y puede fallar."
    echo "Alternativas:"
    echo "  1. Ejecutar como root: sudo ./start.sh"
    echo "  2. Cambiar puerto en app.py (línea final) a 5000 o 8080"
    echo ""
fi

# Iniciar aplicación
python app.py
