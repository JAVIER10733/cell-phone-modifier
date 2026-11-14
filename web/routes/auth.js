const express = require('express');
const router = express.Router();

router.post('/login', (req, res) => {
    // Aquí iría la lógica real de login
    res.status(501).json({ status: "error", message: "Login aún no implementado." });
});

module.exports = router;