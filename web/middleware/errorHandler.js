/**
 * Manejador global de errores para Express.
 */
function errorHandler(err, req, res, next) {
    console.error(`[ERROR] ${new Date().toISOString()} - ${err.message}`);
    res.status(err.status || 500).json({
        status: "error",
        message: err.message || "Error interno del servidor.",
        timestamp: new Date().toISOString()
    });
}

module.exports = errorHandler;