const express = require('express');
const router = express.Router();

router.post('/run', (req, res) => {
    res.json({ status: "ok", message: "Automatización iniciada." });
});

module.exports = router;