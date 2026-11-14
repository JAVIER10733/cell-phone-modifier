const express = require('express');
const router = express.Router();

router.post('/create', (req, res) => {
    res.json({ status: "ok", message: "Backup iniciado. (Lógica en core/modules/backup.py)" });
});

module.exports = router;