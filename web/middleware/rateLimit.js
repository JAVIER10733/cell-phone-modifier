/**
 * Rate Limiter básico en memoria.
 */
const requestCounts = new Map();
const LIMIT = 100; // Peticiones máximas
const WINDOW_MS = 60 * 1000; // Por minuto

function rateLimit(req, res, next) {
    const ip = req.ip || req.connection.remoteAddress;
    const now = Date.now();
    
    if (!requestCounts.has(ip)) {
        requestCounts.set(ip, { count: 1, startTime: now });
        return next();
    }

    const data = requestCounts.get(ip);
    if (now - data.startTime > WINDOW_MS) {
        data.count = 1;
        data.startTime = now;
        return next();
    }

    data.count++;
    if (data.count > LIMIT) {
        return res.status(429).json({ status: "error", message: "Demasiadas peticiones. Intenta más tarde." });
    }
    next();
}

module.exports = rateLimit;