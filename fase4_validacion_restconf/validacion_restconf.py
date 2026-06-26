#!/usr/bin/env python3
import requests, json, os, datetime, socket, yaml
import urllib3
urllib3.disable_warnings()

# Metadatos
print("=" * 60)
print(f"Script      : validacion_restconf.py")
print(f"Fecha/Hora  : {datetime.datetime.now()}")
print(f"Host VM     : {socket.gethostname()}")
print("=" * 60)

# Cargar variables
with open("../vars/vars_005D-20.yaml") as f:
    vars = yaml.safe_load(f)

base_url = f"https://{vars['router']['ip']}/restconf/data"
auth = (vars["router"]["usuario"], vars["router"]["password"])
headers = {"Accept": "application/yang-data+json"}
os.makedirs("evidencias/responses", exist_ok=True)

def get_endpoint(url, archivo):
    r = requests.get(url, auth=auth, headers=headers, verify=False)
    data = r.json()
    with open(f"evidencias/responses/{archivo}", "w") as f:
        json.dump(data, f, indent=2)
    return data

print("\nConsultando endpoints RESTCONF...")

data_hostname   = get_endpoint(f"{base_url}/Cisco-IOS-XE-native:native/hostname", "get_hostname.json")
data_loopback   = get_endpoint(f"{base_url}/ietf-interfaces:interfaces/interface=Loopback{vars['router']['loopback_id']}", "get_loopback.json")
data_interfaces = get_endpoint(f"{base_url}/ietf-interfaces:interfaces/interface=GigabitEthernet1", "get_interfaces.json")
data_ntp        = get_endpoint(f"{base_url}/Cisco-IOS-XE-native:native/ntp", "get_ntp.json")

# Extraer valores con la estructura real
hostname    = data_hostname.get("Cisco-IOS-XE-native:hostname", "")

iface_loop  = data_loopback.get("ietf-interfaces:interface", {})
loopback_ip = iface_loop.get("ietf-ip:ipv4", {}).get("address", [{}])[0].get("ip", "")

iface_wan   = data_interfaces.get("ietf-interfaces:interface", {})
desc_wan    = iface_wan.get("description", "")

ntp_server  = ""
try:
    ntp_server = data_ntp["Cisco-IOS-XE-native:ntp"]["Cisco-IOS-XE-ntp:server"]["server-list"][0]["ip-address"]
except:
    pass

# Comparar
print("\n--- REPORTE DE VALIDACION RESTCONF ---")
resultados = []

checks = [
    ("Hostname corporativo", hostname,    vars["cliente"]["hostname"]),
    ("IP Loopback",          loopback_ip, vars["router"]["loopback_ip"]),
    ("Descripcion WAN",      desc_wan,    vars["router"]["descripcion_wan"]),
    ("Servidor NTP",         ntp_server,  vars["router"]["ntp_server"]),
]

for nombre, obtenido, esperado in checks:
    ok = obtenido == esperado
    estado = "[OK]" if ok else "[FAIL]"
    print(f"{estado} {nombre}: esperado='{esperado}' obtenido='{obtenido}'")
    resultados.append(ok)

print("\n--- RESULTADO GLOBAL ---")
if all(resultados):
    print("CONFORME — 4/4 criterios validados correctamente")
else:
    print(f"NO CONFORME — {sum(resultados)}/4 criterios validados")
