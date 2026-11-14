/**
 * CELL PHONE MODIFIER (CPM) - Frontend Logic v3.1
 * Conexión Real con la API de Python (Flask)
 * Las secciones 1 a 7 son el código original. La sección 8 es nueva.
 */

const consoleEl = document.getElementById('console-output');
const adbStatusEl = document.getElementById('adb-status');
const serverStatusEl = document.getElementById('server-status');

let currentSerial = null;

// ─── 1. RELOJ EN TIEMPO REAL ───
setInterval(() => {
    const clockEl = document.getElementById('clock');
    if(clockEl) clockEl.textContent = new Date().toLocaleTimeString('en-US', { hour12: false });
}, 1000);

// ─── 2. SISTEMA DE LOGS ───
function logToConsole(message, type = 'info') {
    const line = document.createElement('div');
    line.className = `log-line ${type}`;
    
    const now = new Date();
    const timestamp = `[${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}]`;
    const prefix = type === 'error' ? '[ERROR]' : type === 'success' ? '[OK]' : '[SYS]';
    
    line.innerHTML = `<span class="timestamp">${timestamp}</span> <span class="prefix">${prefix}</span> ${message}`;
    consoleEl.appendChild(line);
    consoleEl.scrollTo({ top: consoleEl.scrollHeight, behavior: 'smooth' });
}

function clearConsole() {
    consoleEl.innerHTML = '';
    logToConsole("Consola reiniciada.", "info");
}

function copyLog() {
    const text = consoleEl.innerText;
    navigator.clipboard.writeText(text).then(() => {
        logToConsole("Log copiado al portapapeles.", "success");
    }).catch(err => {
        logToConsole(`Error copiando log: ${err}`, "error");
    });
}

// ─── 3. ACTUALIZAR INTERFAZ ───
function updateTelemetry(cpu, ram, storage) {
    const cpuBar = document.getElementById('bar-cpu');
    const ramBar = document.getElementById('bar-ram');
    const strBar = document.getElementById('bar-storage');
    
    if (cpuBar) { cpuBar.style.width = `${cpu}%`; document.getElementById('val-cpu').textContent = `${cpu}%`; }
    if (ramBar) { ramBar.style.width = `${ram}%`; document.getElementById('val-ram').textContent = `${ram}%`; }
    if (strBar) { strBar.style.width = `${storage}%`; document.getElementById('val-storage').textContent = `${storage}%`; }
    
    const lastUpdate = document.getElementById('last-update');
    if (lastUpdate) {
        const now = new Date();
        lastUpdate.textContent = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')} hs`;
    }
}

function updateAdbStatus(status) {
    if (status === 'online') {
        adbStatusEl.innerHTML = `<span class="pulse-dot success"></span><span class="status-text">ADB: ONLINE</span>`;
        adbStatusEl.className = "status-pill";
    } else {
        adbStatusEl.innerHTML = `<span class="pulse-dot warning"></span><span class="status-text">ADB: OFFLINE</span>`;
        adbStatusEl.className = "status-pill warning";
    }
}

function actualizarPanel(d) {
    const setVal = (id, val) => { const el = document.getElementById(id); if(el) el.textContent = val; };
    
    setVal('dev-model', d.model || "Desconocido");
    setVal('dev-brand', d.brand || "Desconocida");
    setVal('dev-os', `${d.os_type} ${d.os_version}`);
    setVal('dev-arch', d.arch || "Desconocida");
    setVal('dev-ram', d.ram || "Desconocida");
    setVal('dev-serial', d.serial || "LOCAL");
    
    const rootEl = document.getElementById('dev-root');
    if (rootEl) {
        rootEl.textContent = d.is_rooted ? "ROOT DETECTADO" : "Sin Root";
        rootEl.style.color = d.is_rooted ? "var(--accent-red)" : "var(--text-muted)";
    }
}

// ─── 4. ESCANEO DE HARDWARE ───
async function scanDevices() {
    logToConsole("Iniciando escaneo de hardware...", "info");
    const btnScan = document.getElementById('btn-scan');
    
    if(btnScan) {
        btnScan.disabled = true;
        btnScan.innerHTML = `<svg class="icon" style="animation: spin 1s linear infinite" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 1 1-6.219-8.56"></path></svg> Escaneando...`;
    }

    try {
        const res = await fetch('/api/hardware', { cache: 'no-store' });
        if (!res.ok) throw new Error("El servidor no responde.");

        const data = await res.json();

        if (data.status === "ok") {
            const d = data.device;
            actualizarPanel(d);
            
            if (d.telemetry) {
                updateTelemetry(d.telemetry.cpu, d.telemetry.ram, d.telemetry.storage);
            }

            currentSerial = d.serial;
            updateAdbStatus('online');
            logToConsole(`Hardware identificado: ${d.model}`, "success");
        } else {
            throw new Error(data.message || "No se pudo leer el hardware.");
        }
    } catch (e) {
        logToConsole(`Fallo en escaneo: ${e.message}`, "error");
        updateAdbStatus('offline');
    } finally {
        if(btnScan) {
            btnScan.disabled = false;
            btnScan.innerHTML = `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg> Iniciar Escaneo Profundo`;
        }
    }
}

// ─── 5. EJECUCIÓN DE MÓDULOS ───
async function execCommand(pluginName, btnElement) {
    if (!currentSerial) {
        logToConsole("⚠️ Escanea el hardware primero.", "warning");
        return;
    }

    let originalContent = "";
    if (btnElement) {
        originalContent = btnElement.innerHTML;
        btnElement.innerHTML = `<span class="loader"></span> PROCESANDO...`;
        btnElement.style.opacity = "0.7";
        btnElement.disabled = true;
    }

    logToConsole(`>> Inicializando módulo: ${pluginName.toUpperCase()}...`, "info");

    try {
        const res = await fetch('/api/execute', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            cache: 'no-store',
            body: JSON.stringify({ plugin: pluginName })
        });

        const data = await res.json();

        if (res.ok) {
            logToConsole(data.result, "success");
        } else {
            logToConsole(`[FALLÓ] ${data.message}`, "error");
        }
    } catch (e) {
        logToConsole(`Error de red: ${e.message}`, "error");
    } finally {
        if (btnElement) {
            btnElement.innerHTML = originalContent;
            btnElement.style.opacity = "1";
            btnElement.disabled = false;
        }
    }
}

// ─── 6. TERMINAL INTEGRADA ───
async function handleTerminalInput(event) {
    if (event.key === "Enter") {
        const input = event.target;
        const cmd = input.value.trim();
        if (!cmd) return;
        
        input.value = "";
        logToConsole(`root@cpm:~# ${cmd}`, "info");
        
        try {
            const res = await fetch('/api/execute', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ plugin: 'shell', command: cmd })
            });
            const data = await res.json();
            
            if (res.ok) {
                logToConsole(data.result, "success");
            } else {
                logToConsole(`[ERROR] ${data.message}`, "error");
            }
        } catch (e) {
            logToConsole(`Fallo de conexión: ${e.message}`, "error");
        }
    }
}

// ─── 7. INICIALIZACIÓN ───
document.addEventListener('DOMContentLoaded', () => {
    logToConsole("╔════════════════════════════════════════════╗", "info");
    logToConsole("║  CELL PHONE MODIFIER - TACTICAL DASHBOARD  ║", "success");
    logToConsole("╚════════════════════════════════════════════╝", "info");

    fetch('/api/status')
        .then(res => res.json())
        .then(data => {
            serverStatusEl.innerHTML = `<span class="pulse-dot success"></span><span class="status-text">SERVER: ONLINE</span>`;
            logToConsole(`Backend conectado. OS: ${data.os} | Versión: ${data.version}`, "success");
        })
        .catch(() => {
            serverStatusEl.innerHTML = `<span class="pulse-dot warning"></span><span class="status-text">SERVER: OFFLINE</span>`;
            logToConsole("Error crítico: No se pudo conectar con el servidor.", "error");
        });

    setTimeout(() => scanDevices(), 1000);
});

const style = document.createElement('style');
style.textContent = `@keyframes spin { 100% { transform: rotate(360deg); } } .loader { display: inline-block; width: 12px; height: 12px; border: 2px solid currentColor; border-radius: 50%; border-top-color: transparent; animation: spin 1s linear infinite; margin-right: 8px; }`;
document.head.appendChild(style);


// ═══════════════════════════════════════════════════════════════
// ─── 8. MEJORAS NUEVAS (no modifican nada de lo anterior) ───
// ═══════════════════════════════════════════════════════════════
(function cpmMejoras() {

    // 8.1 Los resultados con varias líneas se ven ordenados
    const extraStyle = document.createElement('style');
    extraStyle.textContent = `.log-line { white-space: pre-wrap; }`;
    document.head.appendChild(extraStyle);

    // 8.2 Historial de comandos con flechas arriba y abajo
    const input = document.getElementById('terminal-input');
    if (input) {
        let hist = [];
        try { hist = JSON.parse(localStorage.getItem('cpm_history') || '[]'); } catch (_) {}
        let idx = hist.length;
        let typed = '';

        input.addEventListener('input', () => { typed = input.value.trim(); });

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.isTrusted) {
                if (typed && hist[hist.length - 1] !== typed) {
                    hist.push(typed);
                    hist = hist.slice(-50);
                    try { localStorage.setItem('cpm_history', JSON.stringify(hist)); } catch (_) {}
                }
                typed = '';
                idx = hist.length;
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                if (idx > 0) { idx--; input.value = hist[idx]; }
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                if (idx < hist.length - 1) { idx++; input.value = hist[idx]; }
                else { idx = hist.length; input.value = ''; }
            } else if (e.key === 'Escape') {
                input.blur();
            }
        });

        // Atajos: "/" o Ctrl+K enfocan la terminal
        document.addEventListener('keydown', (e) => {
            const enCampo = /INPUT|TEXTAREA/.test(document.activeElement.tagName);
            if ((e.key === '/' && !enCampo) || ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k')) {
                e.preventDefault();
                input.focus();
            }
        });
    }

    // 8.3 Exportar el log como archivo de texto
    window.exportLog = function () {
        const blob = new Blob([consoleEl.innerText], { type: 'text/plain' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = `cpm-log-${new Date().toISOString().slice(0, 19).replace(/[:T]/g, '-')}.txt`;
        a.click();
        URL.revokeObjectURL(a.href);
        logToConsole('Log exportado.', 'success');
    };

    const actions = document.querySelector('.console-actions');
    if (actions) {
        const btn = document.createElement('button');
        btn.className = 'clear-btn';
        btn.textContent = 'EXPORTAR LOG';
        btn.onclick = window.exportLog;
        actions.appendChild(btn);
    }

    // 8.4 Telemetría que se actualiza sola cada 15 segundos
    async function refrescarTelemetria() {
        if (!currentSerial || document.hidden) return;
        try {
            const res = await fetch('/api/hardware', { cache: 'no-store' });
            const data = await res.json();
            if (data.status === 'ok' && data.device && data.device.telemetry) {
                const t = data.device.telemetry;
                updateTelemetry(t.cpu, t.ram, t.storage);
            }
        } catch (_) { /* si falla, no molesta con mensajes */ }
    }
    setInterval(refrescarTelemetria, 15000);

    // 8.5 Aviso si el servidor se cae o vuelve
    let servidorOnline = null;
    async function latido() {
        let ok = false;
        try {
            const res = await fetch('/api/status', { cache: 'no-store' });
            ok = res.ok;
        } catch (_) {}

        if (servidorOnline === ok) return;
        const primera = servidorOnline === null;
        servidorOnline = ok;
        if (primera) return;

        serverStatusEl.innerHTML = ok
            ? `<span class="pulse-dot success"></span><span class="status-text">SERVER: ONLINE</span>`
            : `<span class="pulse-dot warning"></span><span class="status-text">SERVER: OFFLINE</span>`;
        logToConsole(ok ? 'Servidor reconectado.' : 'Se perdió la conexión con el servidor.', ok ? 'success' : 'error');
    }
    latido();
    setInterval(latido, 20000);
})();
