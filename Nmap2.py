import nmap

# Crear un objeto de escaneo Nmap
port_scan = nmap.PortScanner()

# Solicitar al usuario que ingrese los hosts
hosts = input("Ingresa uno o varios hosts separados por comas: ")

# Dividir los hosts ingresados por comas y eliminar los espacios en blanco
hosts_list = [host.strip() for host in hosts.split(',')]

# Solicitar al usuario que ingrese los puertos
ports_input = input("Ingresa los puertos a escanear (puedes usar una lista separada por comas o un rango en formato inicio-fin): ")

# Verificar si los puertos son un rango o una lista
if '-' in ports_input:
    # Dividir el rango de puertos en inicio y fin
    start_port, end_port = map(int, ports_input.split('-'))
    
    # Generar la lista de puertos entre el inicio y el fin del rango
    ports_list = list(range(start_port, end_port + 1))
else:
    # Dividir los puertos ingresados por comas y eliminar los espacios en blanco
    ports_list = [int(port.strip()) for port in ports_input.split(',')]

# Solicitar al usuario que ingrese los argumentos
print("Algunos ejemplos de argumentos son -sS -sT -sU -sY -sN -sA -sW -sM")
arguments = input("Ingresa los argumentos para el escaneo (opcional): ")

# Solicitar al usuario que elija si desea utilizar sudo
sudo_input = input("¿Deseas utilizar sudo para privilegios de superusuario? (TRUE/FALSE): ")
sudo = sudo_input.lower() == 'true'

# Imprimir el formato del CSV
print("Formato de los resultados:")
print("host;hostname;hostname_type;protocol;port;name;state;product;extrainfo;reason;version;conf;cpe")

# Realizar el escaneo en cada host para cada puerto
for host in hosts_list:
    print("\n")  # Agregar un salto de línea antes de imprimir los resultados para el host
    print(f"Resultados para el host {host}:")
    for port in ports_list:
        try:
            # Realizar un escaneo en el host en el puerto especificado con los argumentos ingresados y sudo
            port_scan.scan(hosts=host, ports=str(port), arguments=arguments, sudo=sudo)
            
            # Obtener la salida en formato CSV
            csv_output = port_scan.csv()
            
            # Dividir la salida en líneas
            lines = csv_output.split('\n')
            
            # Imprimir solo las líneas que contienen información sobre el puerto escaneado
            for line in lines:
                if line.strip() and not line.startswith("host;"):
                    print(f"{host};{line}")
        except Exception as e:
            print(f"Error: {e}. Es posible que el escaneo necesite permisos de superusuario.")
