/**
 * Terminal Component
 * Maneja el flujo de logs y la entrada de comandos.
 */

export function logMessage(message, type = 'info') {
    const consoleEl = document.getElementById('console-output');
    if (!consoleEl) return;

    const line = document.createElement('div');
    line.className = `log-line ${type}`;
    
    const now = new Date();
    const timestamp = `[${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}]`;
    
    line.innerHTML = `<span class="timestamp">${timestamp}</span> <span class="prefix">[${type.toUpperCase()}]</span> ${message}`;
    consoleEl.appendChild(line);
    consoleEl.scrollTo({ top: consoleEl.scrollHeight, behavior: 'smooth' });
}

export function clearTerminal() {
    const consoleEl = document.getElementById('console-output');
    if (consoleEl) {
        consoleEl.innerHTML = '';
        logMessage("Consola reiniciada.", "info");
    }
}