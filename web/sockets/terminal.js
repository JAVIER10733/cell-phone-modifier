module.exports = (io) => {
    io.on('connection', (socket) => {
        socket.on('terminal:input', (cmd) => {
            // Aquí iría la lógica real de ejecutar el comando
            socket.emit('terminal:output', `Comando recibido: ${cmd}`);
        });
    });
};