"""Servidor Flask del Dashboard CPM."""

from flask import Flask, send_from_directory, jsonify, request
from pathlib import Path
import platform
import subprocess
import psutil
import os
import sys
import json
from core.platform_utils import get_os, is_termux
from core.logger import get_logger

log = get_logger(__name__)

base_dir = Path(__file__).resolve().parent
public_dir = base_dir / "public"

app = Flask(__name__, static_folder=str(public_dir), static_url_path="")

def run_cmd(cmd: str) -> str:
    try:
        kwargs = {}
        if platform.system() == "Windows":
            kwargs["creationflags"] = 0x08000000
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10, shell=True, **kwargs)
        return res.stdout.strip() if res.stdout.strip() else "Completado."
    except Exception as e:
        return f"Error: {e}"

@app.route("/")
def index():
    return send_from_directory(str(public_dir), "index.html")

@app.route("/api/status")
def status():
    return jsonify({"status": "ok", "os": get_os(), "version": "1.0.0", "is_termux": is_termux()})

@app.route("/api/hardware")
def hardware():
    try:
        try:
            cpu = psutil.cpu_percent(interval=0.5)
        except Exception:
            cpu = 0
        try:
            ram = psutil.virtual_memory().percent
        except Exception:
            ram = 0
        try:
            disk = psutil.disk_usage('/').percent
        except Exception:
            disk = 0

        return jsonify({
            "status": "ok",
            "device": {
                "model": platform.node(),
                "brand": platform.processor() or "PC",
                "os_type": platform.system(),
                "os_version": platform.release(),
                "arch": platform.machine(),
                "ram": f"{psutil.virtual_memory().total / (1024**3):.1f} GB" if hasattr(psutil, "virtual_memory") else "Desconocida",
                "serial": "LOCAL_PC",
                "is_rooted": False,
                "telemetry": {
                    "cpu": int(cpu),
                    "ram": int(ram),
                    "storage": int(disk)
                }
            }
        })
    except Exception as e:
        log.error(f"Error en /api/hardware: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/execute", methods=["POST"])
def execute():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Faltan datos."}), 400

    plugin = data.get("plugin")
    if not plugin:
        return jsonify({"status": "error", "message": "Falta el nombre del plugin."}), 400

    if plugin == "shell":
        cmd = data.get("command")
        if not cmd:
            return jsonify({"status": "error", "message": "Comando vacío."}), 400
        
        peligrosos = ["rm -rf /", "mkfs", "dd if=", "shutdown", "reboot", "format"]
        if any(p in cmd.lower() for p in peligrosos):
            return jsonify({"status": "error", "message": "Comando bloqueado por seguridad."}), 403
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, shell=True)
            return jsonify({"status": "ok", "result": result.stdout.strip() or result.stderr.strip()}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    try:
        script_path = base_dir.parent / "core" / "plugin_runner.py"
        result = subprocess.run(
            [sys.executable, str(script_path), plugin],
            capture_output=True, text=True, timeout=30
        )
        try:
            response_data = json.loads(result.stdout)
            return jsonify(response_data), 200
        except json.JSONDecodeError:
            return jsonify({
                "status": "error", 
                "message": f"Error parseando JSON: {result.stdout[:200]} | STDERR: {result.stderr[:200]}"
            }), 500
    except subprocess.TimeoutExpired:
        return jsonify({"status": "error", "message": "El comando tardó demasiado."}), 504
    except Exception as e:
        log.error(f"Error en /api/execute: {e}")
        return jsonify({"status": "error", "message": f"Error interno: {str(e)}"}), 500
