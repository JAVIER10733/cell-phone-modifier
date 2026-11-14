/**
 * File Browser Component
 * Maneja la visualización de archivos.
 */

export function renderFileList(files) {
    const container = document.getElementById('file-list');
    if (!container) return;

    container.innerHTML = ''; // Limpiar
    files.forEach(file => {
        const item = document.createElement('div');
        item.className = 'file-item';
        item.textContent = file;
        container.appendChild(item);
    });
}