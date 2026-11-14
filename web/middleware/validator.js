/**
 * Validador de payloads básico.
 */
function validateRequest(requiredFields) {
    return (req, res, next) => {
        const missing = requiredFields.filter(field => !req.body[field]);
        if (missing.length > 0) {
            return res.status(400).json({ 
                status: "error", 
                message: `Campos requeridos faltantes: ${missing.join(', ')}` 
            });
        }
        next();
    };
}

module.exports = validateRequest;