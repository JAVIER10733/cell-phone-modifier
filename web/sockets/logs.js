module.exports = (io) => {
    setInterval(() => {
        // Emitir logs reales (simulados por ahora)
        io.emit('log', { 
            timestamp: new Date().toISOString(), 
            message: "Latido de logs (Log heartbeat)" 
        });
    }, 5000);
};