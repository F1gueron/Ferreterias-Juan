#!/bin/bash

# Script para resetear la base de datos y logs
echo "🔄 Reseteando Ferreterías Juan..."

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

warning_msg() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

success_msg() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Confirmar reset
read -p "¿Estás seguro de que quieres resetear la base de datos? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Operación cancelada."
    exit 0
fi

echo "🗄️ Reseteando base de datos..."

# Variables de BD
DB_NAME="ferreteria_juan"
DB_USER="ferreteria_user"
DB_PASS="ferreteria_pass123"

# Limpiar tablas
mysql -u $DB_USER -p$DB_PASS $DB_NAME -e "DROP TABLE IF EXISTS productos, usuarios, comentarios;"
success_msg "Tablas eliminadas"

# Limpiar logs
> ferreteria_juan.log
success_msg "Logs limpiados"

# Limpiar uploads
rm -rf static/uploads/*
success_msg "Archivos subidos eliminados"

# Recrear estructura de uploads
mkdir -p static/uploads
chmod 777 static/uploads

echo ""
warning_msg "Base de datos reseteada completamente"
warning_msg "La próxima vez que inicies la aplicación se recrearán las tablas"
echo ""
echo "Para reiniciar con datos frescos:"
echo "  ./start.sh"
