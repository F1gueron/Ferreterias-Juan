#!/bin/bash

# Ferreterías Juan - Script de Instalación
# SOLO para entorno de laboratorio educativo

echo "🔨 Ferreterías Juan - Instalación"
echo "================================="
echo "⚠️  ATENCIÓN: Esta aplicación contiene vulnerabilidades INTENCIONALES"
echo "⚠️  SOLO para uso educativo en entorno de laboratorio"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para mostrar errores
error_exit() {
    echo -e "${RED}❌ Error: $1${NC}" >&2
    exit 1
}

# Función para mostrar éxito
success_msg() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Función para mostrar advertencias
warning_msg() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Verificar si se ejecuta como root para instalación de paquetes
if [ "$EUID" -eq 0 ]; then
    warning_msg "Ejecutándose como root. Se instalarán dependencias del sistema."
    INSTALL_SYSTEM_DEPS=true
else
    warning_msg "No se ejecuta como root. Saltando instalación de dependencias del sistema."
    INSTALL_SYSTEM_DEPS=false
fi

echo "1. Verificando dependencias del sistema..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    if [ "$INSTALL_SYSTEM_DEPS" = true ]; then
        echo "Instalando Python3..."
        apt update && apt install -y python3 python3-pip python3-venv
    else
        error_exit "Python3 no está instalado. Instala: sudo apt install python3 python3-pip python3-venv"
    fi
else
    success_msg "Python3 encontrado"
fi

# Verificar MySQL/MariaDB
if ! command -v mysql &> /dev/null; then
    if [ "$INSTALL_SYSTEM_DEPS" = true ]; then
        echo "Instalando MariaDB..."
        apt install -y mariadb-server mariadb-client
        systemctl start mariadb
        systemctl enable mariadb
        warning_msg "Ejecuta 'sudo mysql_secure_installation' después de la instalación"
    else
        error_exit "MySQL/MariaDB no está instalado. Instala: sudo apt install mariadb-server"
    fi
else
    success_msg "MySQL/MariaDB encontrado"
fi

echo ""
echo "2. Configurando entorno virtual Python..."

# Crear entorno virtual
if [ ! -d "venv" ]; then
    python3 -m venv venv
    success_msg "Entorno virtual creado"
else
    success_msg "Entorno virtual ya existe"
fi

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias Python
echo "3. Instalando dependencias Python..."
pip install --upgrade pip
pip install -r requirements.txt
success_msg "Dependencias Python instaladas"

echo ""
echo "4. Configurando base de datos MySQL..."

# Configuración de BD
DB_NAME="ferreteria_juan"
DB_USER="ferreteria_user"
DB_PASS="ferreteria_pass123"

# Crear base de datos y usuario
mysql -u root -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"
mysql -u root -e "CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';"
mysql -u root -e "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';"
mysql -u root -e "FLUSH PRIVILEGES;"

success_msg "Base de datos configurada: $DB_NAME"
success_msg "Usuario creado: $DB_USER"
warning_msg "Contraseña (DÉBIL INTENCIONAL): $DB_PASS"

echo ""
echo "5. Creando directorio de uploads..."
mkdir -p static/uploads
chmod 777 static/uploads  # Permiso vulnerable intencional
warning_msg "Directorio uploads creado con permisos 777 (VULNERABLE)"

echo ""
echo "6. Configurando logs..."
touch ferreteria_juan.log
chmod 666 ferreteria_juan.log
success_msg "Archivo de logs creado"

echo ""
echo "=========================="
echo "🎉 INSTALACIÓN COMPLETADA"
echo "=========================="
echo ""
echo "Para iniciar la aplicación:"
echo "  1. Activa el entorno virtual: source venv/bin/activate"
echo "  2. Ejecuta la aplicación: python app.py"
echo ""
echo "URLs de acceso:"
echo "  • Aplicación: http://localhost"
echo "  • Login admin: admin / admin123"
echo ""
echo "Puertos utilizados:"
echo "  • Flask: 80"
echo "  • MySQL: 3306"
echo ""
echo "⚠️  RECORDATORIO DE SEGURIDAD:"
echo "  • Esta aplicación es VULNERABLE por diseño"
echo "  • Solo usar en entorno de laboratorio AISLADO"
echo "  • NO exponer a Internet"
echo "  • Configurar firewall para bloquear acceso externo"
echo ""
