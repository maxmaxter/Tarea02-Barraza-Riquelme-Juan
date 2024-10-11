# Tarea 2 - OUILookup

## Integrantes
- Juan Barraza
 juan.barraza@alumnos.uv.cl
-Walter Castillo
 walter.castillo@alumnos.uv.cl


## Descripción

Este proyecto implementa una herramienta de línea de comandos en Python llamada **OUILookup**, que permite consultar el fabricante de una tarjeta de red a partir de su dirección MAC utilizando una API REST pública.

## Requisitos

- Python 3.8 o superior
- Librería `getopt` para procesar parámetros
- Conexión a Internet (para hacer consultas a la API REST)

## Uso

Ejecutar el programa en la línea de comandos de la siguiente manera:

### En Linux:
   ```bash
   ./OUILookup --mac <mac> | --arp | [--help]
```
### En Windows
 ```bash
 python3 OUILookup.py --mac <mac> | --arp | [--help]
```

## Ejemplos de Uso 

1. Consultar fabricante de una MAC:

```bash
$ python3 OUILookup.py --mac 98:06:3c:92:ff:c5
```
```bash
MAC address : 98:06:3c:92:ff:c5
Fabricante  : Samsung Electronics Co.,Ltd
Tiempo de respuesta: 17ms
```
