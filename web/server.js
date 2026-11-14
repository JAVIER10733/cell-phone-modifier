"""Servidor Flask del Dashboard CPM."""

from flask import Flask, send_from_directory, jsonify, request
from pathlib import Path
import platform
import subprocess
import psutil
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
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return jsonify({
        "status": "ok",
        "device": {
            "model": platform.node(),
            "brand": platform.processor() or "PC",
            "os_type": platform.system(),
            "os_version": platform.release(),
            "arch": platform.machine(),
            "ram": f"{psutil.virtual_memory().total / (1024**3):.1f} GB",
            "serial": "LOCAL_PC",
            "is_rooted": False,
            "telemetry": {"cpu": int(cpu), "ram": int(ram), "storage": int(disk)}
        }
    })

@app.route("/api/execute", methods=["POST"])
def execute():
    data = request.get_json()
    plugin = data.get("plugin")
    if plugin == "apps":
        out = run_cmd('powershell "Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName"')
        return jsonify({"status": "ok", "result": f"✅ Apps:\n{out[:500]}..."})
    elif plugin == "files":
        import os
        files = os.listdir(".")
        return jsonify({"status": "ok", "result": "✅ Archivos:\n" + "\n".join(files)})
    elif plugin == "network":
        out = run_cmd("ipconfig" if platform.system() == "Windows" else "ip addr")
        return jsonify({"status": "ok", "result": f"✅ Red:\n{out[:400]}..."})
    elif plugin == "battery":
        batt = psutil.sensors_battery()
        if batt:
            return jsonify({"status": "ok", "result": f"✅ Batería: {batt.percent}%"})
        return jsonify({"status": "ok", "result": "✅ Sin batería."})
    elif plugin in ["tweaks", "flash"]:
        return jsonify({"status": "ok", "result": "⚠️ Bloqueado por seguridad."})
    return jsonify({"status": "error", "message": "Plugin no encontrado"}), 404
