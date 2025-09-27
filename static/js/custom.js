// JavaScript personalizado para el Sistema de Servicio Técnico

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Inicializar popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts después de 5 segundos
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Confirmación para formularios de eliminación
    var deleteForms = document.querySelectorAll('form[action*="eliminar"]');
    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!confirm('¿Estás seguro de que deseas eliminar este elemento? Esta acción no se puede deshacer.')) {
                e.preventDefault();
            }
        });
    });

    // Validación de formularios
    var forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Búsqueda en tiempo real
    var searchInputs = document.querySelectorAll('input[name="search"]');
    searchInputs.forEach(function(input) {
        var timeout;
        input.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(function() {
                // Aquí se puede implementar búsqueda AJAX si es necesario
            }, 300);
        });
    });

    // Formateo automático de números
    var numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(function(input) {
        input.addEventListener('blur', function() {
            if (this.value && !isNaN(this.value)) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    });

    // Formateo automático de teléfonos
    var phoneInputs = document.querySelectorAll('input[name*="telefono"]');
    phoneInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            var value = this.value.replace(/\D/g, '');
            if (value.length >= 10) {
                value = value.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
            }
            this.value = value;
        });
    });

    // Formateo automático de RUC/CI
    var rucInputs = document.querySelectorAll('input[name*="ruc"]');
    rucInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            var value = this.value.replace(/\D/g, '');
            if (value.length > 10) {
                value = value.substring(0, 13);
            }
            this.value = value;
        });
    });

    // Cálculo automático de totales en facturas
    var subtotalInputs = document.querySelectorAll('input[name*="subtotal"]');
    var ivaInputs = document.querySelectorAll('input[name*="iva"]');
    var totalInputs = document.querySelectorAll('input[name*="total"]');

    function calculateTotal() {
        var subtotal = parseFloat(subtotalInputs[0]?.value || 0);
        var iva = parseFloat(ivaInputs[0]?.value || 0);
        var total = subtotal + iva;
        
        if (totalInputs[0]) {
            totalInputs[0].value = total.toFixed(2);
        }
    }

    subtotalInputs.forEach(function(input) {
        input.addEventListener('input', calculateTotal);
    });

    ivaInputs.forEach(function(input) {
        input.addEventListener('input', calculateTotal);
    });

    // Auto-generar códigos
    var codigoInputs = document.querySelectorAll('input[name*="codigo"]');
    codigoInputs.forEach(function(input) {
        if (!input.value) {
            var prefix = input.name.includes('cliente') ? 'CLI' : 
                        input.name.includes('equipo') ? 'EQ' : 
                        input.name.includes('ticket') ? 'TK' : 'COD';
            var timestamp = Date.now().toString().slice(-6);
            input.value = prefix + '-' + timestamp;
        }
    });

    // Validación de fechas
    var dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            var selectedDate = new Date(this.value);
            var today = new Date();
            
            if (selectedDate > today) {
                // Fecha futura - permitir para fechas prometidas
                if (!this.name.includes('prometida')) {
                    alert('La fecha no puede ser futura.');
                    this.value = '';
                }
            }
        });
    });

    // Carga de imágenes con preview
    var imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            var file = this.files[0];
            if (file) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    var preview = document.getElementById(input.name + '_preview');
                    if (preview) {
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // Toggle de visibilidad de contraseñas
    var passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(function(input) {
        var toggle = document.createElement('button');
        toggle.type = 'button';
        toggle.className = 'btn btn-outline-secondary';
        toggle.innerHTML = '<i class="bi bi-eye"></i>';
        toggle.style.position = 'absolute';
        toggle.style.right = '10px';
        toggle.style.top = '50%';
        toggle.style.transform = 'translateY(-50%)';
        toggle.style.border = 'none';
        toggle.style.background = 'transparent';
        
        input.parentElement.style.position = 'relative';
        input.style.paddingRight = '50px';
        input.parentElement.appendChild(toggle);
        
        toggle.addEventListener('click', function() {
            if (input.type === 'password') {
                input.type = 'text';
                this.innerHTML = '<i class="bi bi-eye-slash"></i>';
            } else {
                input.type = 'password';
                this.innerHTML = '<i class="bi bi-eye"></i>';
            }
        });
    });

    // Animación de carga para botones de envío
    var submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var originalText = this.innerHTML;
            this.innerHTML = '<span class="spinner"></span> Procesando...';
            this.disabled = true;
            
            // Re-habilitar después de 3 segundos como fallback
            setTimeout(function() {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 3000);
        });
    });

    // Smooth scroll para enlaces internos
    var internalLinks = document.querySelectorAll('a[href^="#"]');
    internalLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Auto-resize para textareas
    var textareas = document.querySelectorAll('textarea');
    textareas.forEach(function(textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });

    // Notificaciones toast personalizadas
    function showToast(message, type = 'info') {
        var toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toast-container';
            toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
            toastContainer.style.zIndex = '9999';
            document.body.appendChild(toastContainer);
        }

        var toast = document.createElement('div');
        toast.className = 'toast align-items-center text-white bg-' + type + ' border-0';
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

        toastContainer.appendChild(toast);
        var bsToast = new bootstrap.Toast(toast);
        bsToast.show();

        toast.addEventListener('hidden.bs.toast', function() {
            toast.remove();
        });
    }

    // Función global para mostrar notificaciones
    window.showToast = showToast;

    // Detectar cambios en formularios
    var forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        var originalData = new FormData(form);
        
        form.addEventListener('input', function() {
            var currentData = new FormData(form);
            var hasChanges = false;
            
            for (var [key, value] of originalData.entries()) {
                if (currentData.get(key) !== value) {
                    hasChanges = true;
                    break;
                }
            }
            
            var submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                if (hasChanges) {
                    submitButton.classList.remove('btn-secondary');
                    submitButton.classList.add('btn-primary');
                } else {
                    submitButton.classList.remove('btn-primary');
                    submitButton.classList.add('btn-secondary');
                }
            }
        });
    });
});

// Funciones utilitarias globales
window.utils = {
    // Formatear moneda
    formatCurrency: function(amount) {
        return new Intl.NumberFormat('es-EC', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    },

    // Formatear fecha
    formatDate: function(date) {
        return new Intl.DateTimeFormat('es-EC', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
        }).format(new Date(date));
    },

    // Formatear fecha y hora
    formatDateTime: function(date) {
        return new Intl.DateTimeFormat('es-EC', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        }).format(new Date(date));
    },

    // Validar email
    validateEmail: function(email) {
        var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },

    // Validar teléfono ecuatoriano
    validatePhone: function(phone) {
        var re = /^(\+593|0)[0-9]{9}$/;
        return re.test(phone.replace(/\D/g, ''));
    },

    // Validar RUC ecuatoriano
    validateRUC: function(ruc) {
        var re = /^[0-9]{13}$/;
        return re.test(ruc.replace(/\D/g, ''));
    },

    // Generar código único
    generateCode: function(prefix, length = 6) {
        var timestamp = Date.now().toString();
        var random = Math.random().toString(36).substring(2, 2 + length);
        return prefix + '-' + (timestamp + random).substring(0, length);
    }
};
