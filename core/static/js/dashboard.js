// Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar gráfico de inventario
    initInventoryChart();
    
    // Configurar chat
    setupChat();
    
    // Configurar búsqueda
    setupSearch();
});

function initInventoryChart() {
    const ctx = document.getElementById('inventoryChart');
    if (!ctx) return;
    
    // Datos de ejemplo - en producción vendrían del servidor
    const fechas = [];
    const valoresActuales = [];
    const valoresPredichos = [];
    
    // Generar datos de ejemplo para últimos 30 días
    for (let i = 30; i >= 0; i--) {
        const fecha = new Date();
        fecha.setDate(fecha.getDate() - i);
        fechas.push(fecha.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit' }));
        // Simular datos con variación
        valoresActuales.push(50 + Math.random() * 20);
    }
    
    // Generar predicción para próximos 30 días
    for (let i = 1; i <= 30; i++) {
        const fecha = new Date();
        fecha.setDate(fecha.getDate() + i);
        fechas.push(fecha.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit' }));
        // Predicción basada en tendencia
        valoresPredichos.push(40 + Math.random() * 15);
    }
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: fechas,
            datasets: [
                {
                    label: 'Stock Actual',
                    data: [...valoresActuales, ...Array(30).fill(null)],
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    tension: 0.4,
                    borderWidth: 2
                },
                {
                    label: 'Predicción',
                    data: [...Array(31).fill(null), ...valoresPredichos],
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    borderDash: [5, 5],
                    tension: 0.4,
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 20
                    }
                },
                x: {
                    ticks: {
                        maxTicksLimit: 10
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

function setupChat() {
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-chat');
    const chatMessages = document.getElementById('chat-messages');
    
    if (!chatInput || !sendButton || !chatMessages) return;
    
    function sendMessage() {
        const mensaje = chatInput.value.trim();
        if (!mensaje) return;
        
        // Agregar mensaje del usuario
        addMessage(mensaje, 'user');
        chatInput.value = '';
        
        // Mostrar indicador de carga
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message mb-2';
        loadingDiv.id = 'loading-message';
        loadingDiv.innerHTML = '<div class="answer-badge bg-light p-2 rounded border"><small class="text-muted">Pensando...</small></div>';
        chatMessages.appendChild(loadingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Enviar al servidor
        fetch('/ia/chatbot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ mensaje: mensaje })
        })
        .then(response => response.json())
        .then(data => {
            // Remover indicador de carga
            const loadingMsg = document.getElementById('loading-message');
            if (loadingMsg) loadingMsg.remove();
            
            if (data.respuesta_ia) {
                addMessage(data.respuesta_ia, 'ai');
            } else if (data.error) {
                addMessage('Error: ' + data.error, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            const loadingMsg = document.getElementById('loading-message');
            if (loadingMsg) loadingMsg.remove();
            addMessage('Error al conectar con el servidor. Por favor, intenta nuevamente.', 'error');
        });
    }
    
    sendButton.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
}

function addMessage(texto, tipo) {
    const chatMessages = document.getElementById('chat-messages');
    if (!chatMessages) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message mb-2';
    
    // Convertir saltos de línea a <br>
    texto = texto.replace(/\n/g, '<br>');
    
    if (tipo === 'user') {
        messageDiv.innerHTML = `<div class="question-badge bg-primary text-white p-2 rounded mb-2">${texto}</div>`;
    } else if (tipo === 'ai') {
        messageDiv.innerHTML = `<div class="answer-badge bg-light p-2 rounded border">${texto}</div>`;
    } else {
        messageDiv.innerHTML = `<div class="answer-badge bg-danger text-white p-2 rounded">${texto}</div>`;
    }
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setupSearch() {
    const searchInput = document.getElementById('search-input');
    if (!searchInput) return;
    
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const query = this.value.trim();
            if (query) {
                // Redirigir a búsqueda de tickets
                window.location.href = `/tickets/?search=${encodeURIComponent(query)}`;
            }
        }
    });
}
