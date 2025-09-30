/* Ferreterías Juan - JavaScript */

// Configuración global
const FerreteriaJuan = {
    API_BASE: 'http://localhost',
    DEBUG: true,

    // Logging para el Blue Team
    log: function(action, data) {
        if (this.DEBUG) {
            const logEntry = {
                timestamp: new Date().toISOString(),
                action: action,
                data: data,
                userAgent: navigator.userAgent,
                url: window.location.href
            };
            console.log('[FERRETERIA_JUAN]', logEntry);

            // Enviar log al servidor (simulado)
            if (typeof sendLogToServer === 'function') {
                sendLogToServer(logEntry);
            }
        }
    },

    // Inicializar aplicación
    init: function() {
        console.log('🔨 Ferreterías Juan - Aplicación iniciada');
        console.log('⚠️ ATENCIÓN: Esta aplicación contiene vulnerabilidades INTENCIONALES');

        this.setupEventListeners();
        this.setupTooltips();
        this.logPageView();
    },

    // Event listeners
    setupEventListeners: function() {
        // Log de clics en enlaces
        document.addEventListener('click', (e) => {
            if (e.target.tagName === 'A') {
                this.log('LINK_CLICK', {
                    href: e.target.href,
                    text: e.target.innerText
                });
            }
        });

        // Log de envío de formularios
        document.addEventListener('submit', (e) => {
            const form = e.target;
            const formData = new FormData(form);
            const data = {};

            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }

            this.log('FORM_SUBMIT', {
                action: form.action,
                method: form.method,
                fields: Object.keys(data)
            });
        });

        // Log de búsquedas (posibles SQL injection)
        const searchInputs = document.querySelectorAll('input[name="search"], input[name="producto"]');
        searchInputs.forEach(input => {
            input.addEventListener('input', (e) => {
                const value = e.target.value;

                // Detectar posibles payloads SQL
                const sqlPatterns = [
                    /'/gi,
                    /union/gi,
                    /select/gi,
                    /drop/gi,
                    /insert/gi,
                    /delete/gi,
                    /--/gi,
                    /;/gi
                ];

                const suspiciousPatterns = sqlPatterns.filter(pattern => pattern.test(value));

                if (suspiciousPatterns.length > 0) {
                    this.log('POSSIBLE_SQL_INJECTION', {
                        input: e.target.name,
                        value: value,
                        patterns: suspiciousPatterns.length
                    });
                }
            });
        });

        // Log de inputs XSS
        const textAreas = document.querySelectorAll('textarea');
        textAreas.forEach(textarea => {
            textarea.addEventListener('input', (e) => {
                const value = e.target.value;

                // Detectar posibles payloads XSS
                const xssPatterns = [
                    /<script/gi,
                    /javascript:/gi,
                    /onerror=/gi,
                    /onload=/gi,
                    /alert\(/gi,
                    /<img/gi,
                    /<iframe/gi,
                    /<svg/gi
                ];

                const suspiciousPatterns = xssPatterns.filter(pattern => pattern.test(value));

                if (suspiciousPatterns.length > 0) {
                    this.log('POSSIBLE_XSS', {
                        field: e.target.name,
                        patterns: suspiciousPatterns.length,
                        length: value.length
                    });
                }
            });
        });
    },

    // Setup tooltips
    setupTooltips: function() {
        // Inicializar tooltips de Bootstrap si están disponibles
        if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(function(tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }
    },

    // Log de vista de página
    logPageView: function() {
        this.log('PAGE_VIEW', {
            path: window.location.pathname,
            referrer: document.referrer,
            timestamp: new Date().toISOString()
        });
    }
};

// Funciones de utilidad
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    const container = document.querySelector('main .container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
    }

    // Auto-remove after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Función para simular ataques (para testing)
function simulateXSSAttack() {
    const payload = '<script>alert("XSS Test - Ferreterías Juan")</script>';
    const commentField = document.querySelector('textarea[name="comentario"]');

    if (commentField) {
        commentField.value = payload;
        showAlert('Payload XSS insertado en el campo comentario', 'warning');
        FerreteriaJuan.log('XSS_SIMULATION', { payload: payload });
    }
}

function simulateSQLInjection() {
    const payload = "' OR 1=1 --";
    const searchField = document.querySelector('input[name="search"], input[name="producto"]');

    if (searchField) {
        searchField.value = payload;
        showAlert('Payload SQL Injection insertado en búsqueda', 'warning');
        FerreteriaJuan.log('SQLI_SIMULATION', { payload: payload });
    }
}

// Función para mostrar información de debug
function showDebugInfo() {
    const debugInfo = {
        userAgent: navigator.userAgent,
        url: window.location.href,
        cookies: document.cookie,
        localStorage: Object.keys(localStorage),
        sessionStorage: Object.keys(sessionStorage),
        referrer: document.referrer
    };

    console.table(debugInfo);
    FerreteriaJuan.log('DEBUG_INFO_ACCESSED', debugInfo);

    return debugInfo;
}

// Funciones para el panel admin
function loadStats() {
    // Simular carga de estadísticas
    showAlert('Estadísticas actualizadas', 'success');
}

function exportLogs() {
    const logs = [
        '[2024-01-20 10:30:15] INFO - Usuario admin inició sesión desde 192.168.1.100',
        '[2024-01-20 10:31:02] WARNING - Búsqueda SQL: \' OR 1=1 -- desde 192.168.1.100',
        '[2024-01-20 10:31:45] ERROR - SQL Injection detectada: UNION SELECT',
        '[2024-01-20 10:32:12] INFO - Archivo shell.php subido por admin',
        '[2024-01-20 10:32:30] CRITICAL - Ejecución de comando: whoami'
    ];

    const logContent = logs.join('\n');
    const blob = new Blob([logContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'ferreteria_juan_logs.txt';
    a.click();

    URL.revokeObjectURL(url);
    showAlert('Logs exportados', 'info');
}

// Upload de archivos con preview
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        const fileName = file.name;
        const fileSize = (file.size / 1024 / 1024).toFixed(2);
        const fileType = file.type;

        // Log del archivo seleccionado
        FerreteriaJuan.log('FILE_SELECTED', {
            name: fileName,
            size: fileSize + ' MB',
            type: fileType
        });

        // Mostrar información del archivo
        showAlert(`Archivo seleccionado: ${fileName} (${fileSize} MB)`, 'info');

        // Detectar archivos potencialmente peligrosos
        const dangerousExtensions = ['.php', '.py', '.js', '.exe', '.bat', '.sh'];
        const isDangerous = dangerousExtensions.some(ext => fileName.toLowerCase().endsWith(ext));

        if (isDangerous) {
            showAlert(`⚠️ ATENCIÓN: Archivo potencialmente peligroso detectado: ${fileName}`, 'warning');
            FerreteriaJuan.log('DANGEROUS_FILE_UPLOAD_ATTEMPT', {
                filename: fileName,
                type: fileType
            });
        }
    }
}

// Funciones de desarrollo/debug
if (FerreteriaJuan.DEBUG) {
    window.FerreteriaJuan = FerreteriaJuan;
    window.simulateXSSAttack = simulateXSSAttack;
    window.simulateSQLInjection = simulateSQLInjection;
    window.showDebugInfo = showDebugInfo;
    window.exportLogs = exportLogs;
}

// Inicializar aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    FerreteriaJuan.init();

    // Setup file upload handler
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', handleFileSelect);
    });
});

// Interceptar errores JavaScript
window.addEventListener('error', function(e) {
    FerreteriaJuan.log('JS_ERROR', {
        message: e.message,
        filename: e.filename,
        lineno: e.lineno,
        colno: e.colno
    });
});

// Detectar herramientas de desarrollador
let devtools = {
    open: false,
    orientation: null
};

setInterval(function() {
    if (window.outerHeight - window.innerHeight > 200 || window.outerWidth - window.innerWidth > 200) {
        if (!devtools.open) {
            devtools.open = true;
            FerreteriaJuan.log('DEVTOOLS_OPENED', {
                timestamp: new Date().toISOString()
            });
            console.log('🔍 DevTools detectado - Blue Team, aquí tienes información útil:');
            console.log('📊 Llamadas AJAX interceptadas');
            console.log('🔒 Cookies y storage monitorizados');
            console.log('⚠️ Vulnerabilidades activas en esta página');
        }
    } else {
        devtools.open = false;
    }
}, 500);