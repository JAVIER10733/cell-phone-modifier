"""
Comandos de conexión ADB (USB y WiFi).
"""

from typing import Optional

from cli.colors import print_error, print_info, print_success, print_warning
from cli.ui import get_input, get_int_input, pause, show_table
from core.adb_wrapper import ADBWrapper
from core.validators import validate_ip, validate_port


class ConnectCommands:
    """Comandos de conexión ADB."""
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        self.adb = adb or ADBWrapper()
    
    def connect_usb(self) -> None:
        """Conecta dispositivo por USB."""
        print_info("Conectando dispositivo por USB...")
        print_info("Asegúrate de:")
        print("  1. Depuración USB activada en el dispositivo")
        print("  2. Cable USB conectado")
        print("  3. Aceptar solicitud de depuración en el dispositivo")
        
        # Iniciar servidor ADB
        try:
            self.adb._execute(["start-server"], check=False)
            print_success("Servidor ADB iniciado")
        except Exception as e:
            print_warning(f"No se pudo iniciar servidor ADB: {e}")
        
        # Listar dispositivos
        devices = self.adb.get_devices()
        
        if not devices:
            print_warning("No se detectaron dispositivos")
            print_info("Verifica la conexión y los drivers")
            return
        
        unauthorized = [d for d in devices if d.get("state") == "unauthorized"]
        if unauthorized:
            print_warning("Hay dispositivos no autorizados")
            print_info("Acepta la solicitud de depuración USB en el dispositivo")
        
        self._show_connected_devices()
    
    def connect_wifi_pair(self) -> None:
    """Conecta dispositivo por WiFi usando pairing (Android 11+)."""
        print_info("Conexión WiFi con pairing (Android 11+)")
        print_info("En el dispositivo:")
        print("  1. Activa 'Depuración inalámbrica' en Opciones de desarrollador")
        print("  2. Toca 'Emparejar dispositivo con código'")
        print("  3. Anota el código y la IP:puerto")
        
        ip = get_input("IP del dispositivo (ej: 192.168.1.100)")
        if not ip:
            return
        
        valid, msg = validate_ip(ip)
        if not valid:
            print_error(f"IP inválida: {msg}")
            return
        
        port = get_int_input("Puerto de pairing", min_val=1, max_val=65535)
        if port is None:
            return
        
        code = get_input("Código de pairing")
        if not code:
            return
        
        print_info(f"Emparejando con {ip}:{port}...")
        
        try:
            result = self.adb._execute(["pair", f"{ip}:{port}", code], check=False)
            
            if result.returncode == 0:
                print_success("Emparejamiento exitoso")
                print_info("Ahora conecta con la IP y puerto de 'Depuración inalámbrica'")
            else:
                print_error(f"Error: {result.stderr}")
        except Exception as e:
            print_error(f"Error: {e}")
    
    def connect_wifi_direct(self) -> None:
        """Conecta dispositivo por WiFi directamente (Android 10 o inferior)."""
        print_info("Conexión WiFi directa (Android 10 o inferior)")
        print_info("En el dispositivo:")
        print("  1. Conecta el dispositivo por USB primero")
        print("  2. Ejecuta: adb tcpip 5555")
        print("  3. Desconecta el USB")
        print("  4. Anota la IP del dispositivo")
        
        ip = get_input("IP del dispositivo (ej: 192.168.1.100)")
        if not ip:
            return
        
        valid, msg = validate_ip(ip)
        if not valid:
            print_error(f"IP inválida: {msg}")
            return
        
        port = get_int_input("Puerto", default=5555, min_val=1, max_val=65535)
        if port is None:
            return
        
        print_info(f"Conectando a {ip}:{port}...")
        
        try:
            result = self.adb._execute(["connect", f"{ip}:{port}"], check=False)
            
            if "connected" in result.stdout.lower():
                print_success(f"Conectado a {ip}:{port}")
                self.adb.set_serial(f"{ip}:{port}")
            else:
                print_error(f"Error: {result.stdout}")
        except Exception as e:
            print_error(f"Error: {e}")
    
    def disconnect_device(self) -> None:
        """Desconecta dispositivo."""
        if not self.adb.serial:
            print_warning("No hay dispositivo seleccionado")
            return
        
        print_info(f"Desconectando {self.adb.serial}...")
        
        try:
            result = self.adb._execute(["disconnect", self.adb.serial], check=False)
            print_success(f"Desconectado: {result.stdout}")
            self.adb.serial = None
        except Exception as e:
            print_error(f"Error: {e}")
    
    def _show_connected_devices(self) -> None:
        """Muestra dispositivos conectados."""
        devices = self.adb.get_devices()
        
        if not devices:
            print_info("No hay dispositivos conectados")
            return
        
        headers = ["Serial", "Estado", "Seleccionado"]
        rows = []
        
        for device in devices:
            serial = device.get("serial", "N/A")
            state = device.get("state", "N/A")
            selected = "✅" if serial == self.adb.serial else ""
            rows.append([serial, state, selected])
        
        show_table("Dispositivos Conectados", headers, rows)
    
    def select_device(self) -> None:
        """Selecciona un dispositivo de la lista."""
        devices = self.adb.get_devices()
        
        if not devices:
            print_warning("No hay dispositivos conectados")
            return
        
        connected = [d for d in devices if d.get("state") == "device"]
        
        if not connected:
            print_warning("No hay dispositivos autorizados")
            return
        
        if len(connected) == 1:
            self.adb.set_serial(connected[0]["serial"])
            print_success(f"Dispositivo seleccionado: {connected[0]['serial']}")
            return
        
        print("\nDispositivos disponibles:")
        for i, device in enumerate(connected, 1):
            serial = device.get("serial", "N/A")
            model = device.get("model", "N/A")
            print(f"  {i}. {serial} ({model})")
        
        choice = get_int_input("Selecciona dispositivo", min_val=1, max_val=len(connected))
        
        if choice is not None:
            self.adb.set_serial(connected[choice - 1]["serial"])
            print_success(f"Dispositivo seleccionado: {connected[choice - 1]['serial']}")
    
    def run(self) -> None:
        """Menú de comandos de conexión."""
        while True:
            print("\n=== Conexión ===")
            print("1. Conectar por USB")
            print("2. Conectar por WiFi (pairing - Android 11+)")
            print("3. Conectar por WiFi (directo - Android 10-)")
            print("4. Seleccionar dispositivo")
            print("5. Desconectar dispositivo")
            print("6. Listar dispositivos")
            print("0. Volver")
            
            choice = get_int_input("Tu elección", min_val=0, max_val=6)
            
            if choice is None or choice == 0:
                break
            
            if choice == 1:
                self.connect_usb()
            elif choice == 2:
                self.connect_wifi_pair()
            elif choice == 3:
                self.connect_wifi_direct()
            elif choice == 4:
                self.select_device()
            elif choice == 5:
                self.disconnect_device()
            elif choice == 6:
                self._show_connected_devices()
            
            pause()