/**
 * Device Card Component
 * Se encarga de actualizar el DOM con los datos del hardware.
 */

export function updateDeviceCard(data) {
    const elModel = document.getElementById('dev-model');
    const elSerial = document.getElementById('dev-serial');
    const elOs = document.getElementById('dev-os');
    const elArch = document.getElementById('dev-arch');
    const elRoot = document.getElementById('dev-root');

    if (elModel) elModel.textContent = data.model || "Desconocido";
    if (elSerial) elSerial.textContent = data.serial || "-";
    if (elOs) elOs.textContent = `${data.os_type} ${data.os_version}` || "-";
    if (elArch) elArch.textContent = `${data.ram} RAM | ${data.arch}` || "-";
    
    if (elRoot) {
        elRoot.textContent = data.is_rooted ? "ROOT DETECTADO" : "Sin Root";
        elRoot.style.color = data.is_rooted ? "var(--accent-red)" : "var(--text-muted)";
    }
}