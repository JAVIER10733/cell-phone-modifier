const express = require('express');
const router = express.Router();

router.get('/full', (req, res) => {
    res.json({ status: "ok", message: "Diagnóstico completo iniciado." });
});

module.exports = router;