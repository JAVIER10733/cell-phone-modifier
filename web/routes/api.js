const express = require('express');
const router = express.Router();
const { execFile } = require('child_process');
const path = require('path');

// Hardware
router.get('/hardware', (req, res, next) => {
    const script = path.join(__dirname, '..', '..', 'core', 'hardware_reader.py');
    execFile('python', [script], (err, stdout, stderr) => {
        if (err) return next(new Error(stderr || err.message));
        try {
            res.json(JSON.parse(stdout));
        } catch (e) {
            next(new Error("Error parseando JSON"));
        }
    });
});

// Ejecutar Plugin
router.post('/execute', (req, res, next) => {
    const { plugin } = req.body;
    const script = path.join(__dirname, '..', '..', 'core', 'plugin_runner.py');
    execFile('python', [script, plugin], (err, stdout, stderr) => {
        if (err) return next(new Error(stderr || err.message));
        try {
            res.json(JSON.parse(stdout));
        } catch (e) {
            next(new Error("Error parseando JSON del plugin"));
        }
    });
});

module.exports = router;