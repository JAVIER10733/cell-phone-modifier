module.exports = (io) => {
    io.on('connection', (socket) => {
        console.log(`[WS] Cliente conectado: ${socket.id}`);
        
        socket.on('disconnect', () => {
            console.log(`[WS] Cliente desconectado: ${socket.id}`);
        });
    });
};