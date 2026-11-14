const express = require('express');
const router = express.Router();
const fs = require('fs');
const path = require('path');

router.get('/', (req, res) => {
    const dir = req.query.path || process.cwd();
    try {
        const files = fs.readdirSync(dir);
        res.json({ status: "ok", files });
    } catch (e) {
        res.status(500).json({ status: "error", message: e.message });
    }
});

module.exports = router;