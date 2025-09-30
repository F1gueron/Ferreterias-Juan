// Ferreterías Juan - JavaScript

const FerreteriaJuan = {
    API_BASE: 'http://localhost',
    DEBUG: true,

    init: function() {
        this.setupTooltips();
    },

    setupTooltips: function() {
        if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(function(tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }
    }
};

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

    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        const fileName = file.name;
        const fileSize = (file.size / 1024 / 1024).toFixed(2);

        showAlert(`Archivo seleccionado: ${fileName} (${fileSize} MB)`, 'info');

        const dangerousExtensions = ['.php', '.py', '.js', '.exe', '.bat', '.sh'];
        const isDangerous = dangerousExtensions.some(ext => fileName.toLowerCase().endsWith(ext));

        if (isDangerous) {
            showAlert(`⚠️ ATENCIÓN: Archivo potencialmente peligroso detectado: ${fileName}`, 'warning');
        }
    }
}

if (FerreteriaJuan.DEBUG) {
    window.FerreteriaJuan = FerreteriaJuan;
}

document.addEventListener('DOMContentLoaded', function() {
    FerreteriaJuan.init();

    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', handleFileSelect);
    });
});