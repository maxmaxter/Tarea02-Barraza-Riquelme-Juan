import sys
import time
import requests
import re
import subprocess
import platform

# Mensaje de ayuda que se muestra al usuario
MENSAJE_AYUDA = '''Uso: python OUILookup.py --mac <mac> | --arp | [--help]
--mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.
--arp: muestra los fabricantes de los hosts disponibles en la tabla ARP.
--help: muestra este mensaje y termina.
'''

def obtener_fabricante(direccion_mac):
    # Normalizar la dirección MAC eliminando caracteres que no sean hexadecimales
    mac_limpia = re.sub('[^A-Fa-fA-F0-9]', '', direccion_mac)
    # Verificar que la dirección MAC tenga al menos 6 caracteres (3 bytes)
    if len(mac_limpia) < 6:
        print("Dirección MAC inválida:", direccion_mac)
        return "Dirección MAC inválida", 0
    # Construir la URL para consultar el fabricante en la API
    url = f'https://api.maclookup.app/v2/macs/{direccion_mac}'
    tiempo_inicio = time.time()
    try:
        # Realizar la solicitud HTTP a la API
        respuesta = requests.get(url)
        # Calcular el tiempo de respuesta en milisegundos
        tiempo_respuesta = int((time.time() - tiempo_inicio) * 1000)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            if datos.get('found'):
                # Obtener el nombre del fabricante
                fabricante = datos.get('company', 'No encontrado')
            else:
                fabricante = 'No encontrado'
        else:
            fabricante = 'No encontrado'
    except Exception as e:
        # En caso de error, asignar 'No encontrado' y calcular el tiempo de respuesta
        fabricante = 'No encontrado'
        tiempo_respuesta = int((time.time() - tiempo_inicio) * 1000)
    return fabricante, tiempo_respuesta

def obtener_tabla_arp():
    # Determinar el sistema operativo
    tipo_os = platform.system()
    cmd = ['arp', '-a']
    try:
        if tipo_os == 'Windows':
            # En Windows, usar codificación 'mbcs'
            salida = subprocess.check_output(cmd, encoding='mbcs', errors='ignore')
        else:
            # En otros sistemas, usar codificación 'utf-8'
            salida = subprocess.check_output(cmd, encoding='utf-8', errors='ignore')
    except Exception as e:
        print("Error ejecutando el comando arp:", e)
        return []
    # Analizar la salida del comando ARP
    entradas = []
    if tipo_os == 'Windows':
        entradas = analizar_arp_windows(salida)
    else:
        entradas = analizar_arp_linux(salida)
    return entradas

def analizar_arp_windows(salida):
    entradas = []
    # Dividir la salida en líneas
    lineas = salida.split('\n')
    for linea in lineas:
        linea = linea.strip()
        # Ignorar líneas que no contienen información relevante
        if linea.startswith('Interface:') or linea.startswith('Interfaz:'):
            continue
        if ('Internet Address' in linea or 'Dirección de Internet' in linea or
            'Physical Address' in linea or 'Dirección física' in linea or
            'Type' in linea or 'Tipo' in linea):
            continue
        if linea:
            # Dividir la línea en partes
            partes = linea.split()
            if len(partes) >= 2:
                ip = partes[0]
                # Reemplazar guiones por dos puntos en la dirección MAC
                mac = partes[1].replace('-', ':')
                entradas.append((ip, mac))
    return entradas

def analizar_arp_linux(salida):
    entradas = []
    # Dividir la salida en líneas
    lineas = salida.split('\n')
    for linea in lineas:
        # Utilizar expresión regular para extraer IP y MAC
        match = re.match(r'.*\(([\d\.]+)\) at ([0-9a-fA-F:]+) ', linea)
        if match:
            ip = match.group(1)
            mac = match.group(2)
            entradas.append((ip, mac))
    return entradas

def mostrar_ayuda():
    # Imprimir el mensaje de ayuda al usuario
    print(MENSAJE_AYUDA)

def main():
    # Si no hay argumentos o se solicita ayuda, mostrar el mensaje de ayuda
    if len(sys.argv) <= 1 or '--help' in sys.argv:
        mostrar_ayuda()
        return
    if '--mac' in sys.argv:
        # Obtener el índice del argumento '--mac'
        idx = sys.argv.index('--mac')
        if idx + 1 >= len(sys.argv):
            # Si no se proporciona una dirección MAC después de '--mac'
            print("Dirección MAC no proporcionada.")
            mostrar_ayuda()
            return
        direccion_mac = sys.argv[idx + 1]
        # Obtener el fabricante y el tiempo de respuesta
        fabricante, tiempo_respuesta = obtener_fabricante(direccion_mac)
        # Mostrar los resultados
        print(f"Dirección MAC : {direccion_mac}")
        print(f"Fabricante : {fabricante}")
        print(f"Tiempo de respuesta: {tiempo_respuesta}ms")
    elif '--arp' in sys.argv:
        # Obtener las entradas de la tabla ARP
        entradas = obtener_tabla_arp()
        # Mostrar encabezado
        print("IP / MAC / Fabricante / Tiempo de respuesta:")
        for ip, mac in entradas:
            # Obtener el fabricante y el tiempo de respuesta para cada entrada
            fabricante, tiempo_respuesta = obtener_fabricante(mac)
            # Mostrar los resultados
            print(f"{ip} / {mac} / {fabricante} / {tiempo_respuesta}ms")
    else:
        # Si se proporcionan argumentos no reconocidos, mostrar ayuda
        mostrar_ayuda()

if __name__ == '__main__':
    main()
