const express = require('express');
const router = express.Router();
const { execFile } = require('child_process');

router.get('/', (req, res, next) => {
    execFile('adb', ['devices', '-l'], (err, stdout) => {
        if (err) return res.json({ status: "ok", devices: [], message: "ADB no instalado" });
        
        const lines = stdout.split('\n').slice(1).filter(l => l.trim() !== '');
        const devices = lines.map(line => {
            const parts = line.trim().split(/\s+/);
            return { serial: parts[0], state: parts[1], model: "Unknown" };
        });
        res.json({ status: "ok", devices });
    });
});

module.exports = router;