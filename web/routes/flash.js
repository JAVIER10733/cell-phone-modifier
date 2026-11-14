const express = require('express');
const router = express.Router();

router.post('/flash', (req, res) => {
    res.status(403).json({ status: "error", message: "PELIGRO: Flasheo bloqueado desde web. Usa la CLI." });
});

module.exports = router;