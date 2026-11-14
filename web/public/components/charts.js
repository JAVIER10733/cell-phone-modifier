/**
 * Charts Component
 * Maneja las barras de progreso y telemetría.
 */

export function updateTelemetryBars(cpu, ram, storage) {
    const barCpu = document.getElementById('bar-cpu');
    const barRam = document.getElementById('bar-ram');
    const barStorage = document.getElementById('bar-storage');

    const valCpu = document.getElementById('val-cpu');
    const valRam = document.getElementById('val-ram');
    const valStorage = document.getElementById('val-storage');

    if (barCpu && valCpu) {
        barCpu.style.width = `${cpu}%`;
        valCpu.textContent = `${cpu}%`;
    }
    if (barRam && valRam) {
        barRam.style.width = `${ram}%`;
        valRam.textContent = `${ram}%`;
    }
    if (barStorage && valStorage) {
        barStorage.style.width = `${storage}%`;
        valStorage.textContent = `${storage}%`;
    }
}