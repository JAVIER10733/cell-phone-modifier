/**
 * Middleware de autenticación básica por API Key.
 */
const API_KEY = process.env.CPM_API_KEY || "cpm-secret-key";

function auth(req, res, next) {
    const clientKey = req.headers['x-api-key'];
    if (!clientKey || clientKey !== API_KEY) {
        return res.status(401).json({ status: "error", message: "No autorizado. Falta API Key válida." });
    }
    next();
}

module.exports = auth;