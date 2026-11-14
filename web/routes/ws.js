const express = require('express');
const router = express.Router();

router.get('/ws', (req, res) => {
    res.json({ status: "ok", message: "WebSocket endpoint." });
});

module.exports = router;