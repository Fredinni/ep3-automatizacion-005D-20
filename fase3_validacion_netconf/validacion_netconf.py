#!/usr/bin/env python3
import os, datetime, socket, yaml
from ncclient import manager
from lxml import etree

# Metadatos
print("=" * 60)
print(f"Script      : validacion_netconf.py")
print(f"Fecha/Hora  : {datetime.datetime.now()}")
print(f"Host VM     : {socket.gethostname()}")
print("=" * 60)

# Cargar variables
with open("../vars/vars_005D-20.yaml") as f:
    vars = yaml.safe_load(f)

# Filtro XML
filtro = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname/>
    <interface>
      <GigabitEthernet>
        <name>1</name>
        <description/>
      </GigabitEthernet>
      <Loopback>
        <name>10</name>
        <ip/>
      </Loopback>
    </interface>
    <ntp>
      <server xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ntp"/>
    </ntp>
  </native>
</filter>
"""

# Conectar
print("\nConectando via NETCONF...")
with manager.connect(
    host=vars["router"]["ip"],
    port=830,
    username=vars["router"]["usuario"],
    password=vars["router"]["password"],
    hostkey_verify=False,
    allow_agent=False,
    look_for_keys=False
) as m:
    reply = m.get_config(source="running", filter=filtro)

# Guardar XML crudo
os.makedirs("evidencias", exist_ok=True)
with open("evidencias/rpc_reply_raw.xml", "w") as f:
    f.write(str(reply))
print("XML guardado en evidencias/rpc_reply_raw.xml")

# Parsear
root = etree.fromstring(str(reply).encode())
ns_native = {"ios": "http://cisco.com/ns/yang/Cisco-IOS-XE-native"}
ns_ntp    = {"ntp": "http://cisco.com/ns/yang/Cisco-IOS-XE-ntp"}

def get_text(element, xpath, ns):
    try:
        result = element.find(xpath, ns)
        return result.text if result is not None else None
    except:
        return None

hostname      = get_text(root, ".//ios:native/ios:hostname", ns_native)
desc_wan      = get_text(root, ".//ios:native/ios:interface/ios:GigabitEthernet/ios:description", ns_native)
loopback_ip   = get_text(root, ".//ios:native/ios:interface/ios:Loopback/ios:ip/ios:address/ios:primary/ios:address", ns_native)
loopback_mask = get_text(root, ".//ios:native/ios:interface/ios:Loopback/ios:ip/ios:address/ios:primary/ios:mask", ns_native)
ntp_server    = get_text(root, ".//ntp:server/ntp:server-list/ntp:ip-address", ns_ntp)

# Comparar
print("\n--- REPORTE DE VALIDACION NETCONF ---")
resultados = []

checks = [
    ("Hostname corporativo", hostname,      vars["cliente"]["hostname"]),
    ("Descripcion WAN",      desc_wan,      vars["router"]["descripcion_wan"]),
    ("IP Loopback",          loopback_ip,   vars["router"]["loopback_ip"]),
    ("Mascara Loopback",     loopback_mask, vars["router"]["loopback_mask"]),
    ("Servidor NTP",         ntp_server,    vars["router"]["ntp_server"]),
]

for nombre, obtenido, esperado in checks:
    ok = obtenido == esperado
    estado = "[OK]" if ok else "[FAIL]"
    print(f"{estado} {nombre}: esperado='{esperado}' obtenido='{obtenido}'")
    resultados.append(ok)

print("\n--- RESULTADO GLOBAL ---")
if all(resultados):
    print("CONFORME — 5/5 criterios validados correctamente")
else:
    print(f"NO CONFORME — {sum(resultados)}/5 criterios validados")
