// ProDig Architect Engine - Main Logic
import CONFIG from './config.js';

window.switchTab = switchTab;
window.sendMessage = sendMessage;
window.runHarvest = runHarvest;
window.generateProposal = generateProposal;
window.handleFileSelect = handleFileSelect;

async function switchTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = 'none';
    });
    const target = document.getElementById(tabId);
    if (target) {
        target.style.display = 'block';
    }

    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
        if (item.innerText.toLowerCase().includes(tabId)) {
            item.classList.add('active');
        }
    });

    if (tabId === 'explorer') {
        await loadAndRenderTech();
    }
}

async function loadAndRenderTech() {
    const grid = document.getElementById('tech-grid');
    grid.innerHTML = '<div class="message system">Consultando repositorio de tecnologías...</div>';
    try {
        const response = await fetch('/api/tech');
        const data = await response.json();
        
        grid.innerHTML = data.map(tech => `
            <div class="card fade-in">
                <h3>${tech['Tecnología']}</h3>
                <p class="text-dim" style="font-size: 0.8rem;">Proveedor: ${tech['Proveedor']}</p>
                <div style="margin-top: 1rem; color: var(--accent); font-size: 0.9rem;">
                    <strong>Aplicación:</strong> ${tech['Aplicación ProDig']}
                </div>
                ${tech['Handle Monitoreo'] !== 'n/a' ? `<div style="margin-top: 0.5rem;"><span class="tag">${tech['Handle Monitoreo']}</span></div>` : ''}
            </div>
        `).join('');
    } catch (e) {
        grid.innerHTML = '<div class="message system">Ocurrió un error al cargar las tecnologías.</div>';
        console.error(e);
    }
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const msg = input.value.trim();
    const chatMessages = document.getElementById('chat-messages');

    if (!msg) return;

    addMessage('user', msg);
    input.value = '';

    const loadingMsg = addMessage('system', 'Consultando con el cerebro de Groq y contexto de ProDig...');
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg })
        });
        const data = await response.json();
        
        // Remove loading message if we want, or just add new one
        if (data.response) {
            addMessage('system', data.response);
        } else if (data.error) {
            addMessage('system', 'Error: ' + data.error);
        }
    } catch (e) {
        addMessage('system', 'No se pudo conectar con el servicio de IA. ¿Está el servidor activo?');
        console.error(e);
    }
}

async function runHarvest() {
    addMessage('system', 'Iniciando "Knowledge Harvest" mediante Brave Search API...');
    
    try {
        const response = await fetch('/api/harvest', { method: 'POST' });
        const data = await response.json();
        
        if (data.results && data.results.length > 0) {
            addMessage('system', `He recolectado ${data.results.length} actualizaciones críticas:`);
            data.results.forEach(res => {
                addMessage('system', `📌 ${res.title}\n${res.description}\n[Ver más](${res.url})`);
            });
            addMessage('system', 'Datos listos para sincronización con NotebookLM "IA Tools 2".');
        } else {
            addMessage('system', 'No se encontraron actualizaciones nuevas en este ciclo.');
        }
    } catch (e) {
        addMessage('system', 'Error ejecutando la cosecha. Verifica la configuración de Brave API.');
    }
}

function addMessage(role, text) {
    const container = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.className = `message ${role}`;
    
    // Simple markdown link conversion for the display
    const formattedText = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" style="color:var(--accent)">$1</a>')
                               .replace(/\n/g, '<br>');
                               
    div.innerHTML = formattedText;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
    return div;
}

function handleFileSelect(input) {
    if (input.files && input.files[0]) {
        addMessage('user', `Archivo seleccionado para análisis: ${input.files[0].name}`);
    }
}

function generateProposal() {
    addMessage('system', 'Generando propuesta técnica basada en el mix seleccionado... (Función en desarrollo)');
}

// Initial state
window.addEventListener('DOMContentLoaded', () => {
    console.log('ProDig Architect Engine Initialized');
});
