import requests
import getopt
import sys
import subprocess

# Función para mostrar ayuda
def mostrar_ayuda():
    print("Uso: python OUILookup.py --mac <mac> | --arp | [--help]")
    print(" --mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.")
    print(" --arp: muestra los fabricantes de los host disponibles en la tabla ARP.")
    print(" --help: muestra este mensaje y termina.")
    sys.exit()

# Función para verificar si una MAC es multicast o broadcast
def es_multicast_o_broadcast(mac):
    if mac.startswith("ff:ff:ff") or mac.startswith("01:00:5e"):
        return True
    return False

# Función para consultar fabricante usando una MAC
def consultar_fabricante(mac):
    url = f"https://api.maclookup.app/v2/macs/{mac}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Asegurar que el fabricante sea "Not Found" si no existe o si es una cadena vacía
            fabricante = data.get("company", "Not Found")
            if not fabricante:  # Si el valor está vacío o no es válido
                fabricante = "Not Found"
            tiempo_respuesta = response.elapsed.total_seconds()  # Obtener el tiempo de respuesta
            return fabricante, tiempo_respuesta
        else:
            return "Not Found", response.elapsed.total_seconds()
    except Exception as e:
        return f"Error: {e}", 0

# Función para obtener la tabla ARP en Windows y consultar el fabricante
def obtener_arp():
    try:
        output = subprocess.check_output("arp -a", shell=True).decode('cp1252')
        output = output.replace("din mico", "dinámico").replace("est tico", "estático")
        print("IP/MAC/Fabricante/Tipo:")
        for line in output.splitlines():
            if "incompl" not in line and "-" in line:
                parts = line.split()
                mac_address = parts[1].replace("-", ":")  # Convertir el formato MAC a formato con ":"
                tipo_direccion = parts[-1]  # Última palabra que indica si es dinámico o estático

                # Verificar si es multicast o broadcast
                if es_multicast_o_broadcast(mac_address):
                    fabricante = "N/A (Multicast/Broadcast)"
                else:
                    fabricante, _ = consultar_fabricante(mac_address)
                
                print(f"{parts[0]} / {mac_address} / {fabricante} / {tipo_direccion}")
    except Exception as e:
        print(f"Error al obtener la tabla ARP: {e}")

# Función principal para procesar los argumentos de línea de comandos
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["mac=", "arp", "help"])
    except getopt.GetoptError as err:
        print(str(err))
        mostrar_ayuda()

    if not opts:
        mostrar_ayuda()

    for opt, arg in opts:
        if opt == "--mac":
            fabricante, tiempo_respuesta = consultar_fabricante(arg)
            print(f"MAC address: {arg}")
            print(f"Fabricante: {fabricante}")
            print(f"Tiempo de respuesta: {tiempo_respuesta} segundos")
        elif opt == "--arp":
            obtener_arp()
        elif opt == "--help":
            mostrar_ayuda()
        else:
            mostrar_ayuda()

if __name__ == "__main__":
    main()
