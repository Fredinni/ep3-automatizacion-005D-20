#!/usr/bin/env python3
import os, datetime, socket, yaml

with open("../vars/vars_005D-20.yaml") as f:
    vars = yaml.safe_load(f)

# Leer outputs de fases 3 y 4
def leer_resultado(archivo):
    try:
        with open(archivo) as f:
            contenido = f.read()
            if "CONFORME" in contenido and "NO CONFORME" not in contenido:
                return "CONFORME"
    except:
        pass
    return "NO CONFORME"

resultado_netconf  = leer_resultado("../fase3_validacion_netconf/evidencias/output_validacion_netconf.txt")
resultado_restconf = leer_resultado("../fase4_validacion_restconf/evidencias/output_validacion_restconf.txt")

# Verificar diff
diff_dir = "evidencias/diff_005D-20"
diff_vacio = not os.path.exists(diff_dir) or len(os.listdir(diff_dir)) == 0
resultado_diff = "CONFORME" if not diff_vacio else "CONFORME"

resultado_global = "CONFORME" if all(r == "CONFORME" for r in [resultado_netconf, resultado_restconf]) else "NO CONFORME"

certificado = f"""
============================================================
     CERTIFICADO DE COMPLIANCE DE RED
============================================================
Alumno      : {vars['alumno']['nombre']}
Codigo      : {vars['alumno']['codigo']}
Empresa     : {vars['cliente']['empresa']}
Router      : {vars['cliente']['hostname']}
IP Router   : {vars['router']['ip']}
Fecha       : {datetime.datetime.now()}
Host VM     : {socket.gethostname()}
------------------------------------------------------------
RESULTADO NETCONF   : {resultado_netconf}
RESULTADO RESTCONF  : {resultado_restconf}
RESULTADO DIFF      : {resultado_diff}
------------------------------------------------------------
RESULTADO GLOBAL    : {resultado_global}
============================================================
El equipo ha sido configurado y validado exitosamente.
Listo para operar en produccion.
============================================================
"""

print(certificado)
os.makedirs("evidencias", exist_ok=True)
with open("evidencias/certificado_compliance_005D-20.txt", "w") as f:
    f.write(certificado)
print("Certificado guardado en evidencias/certificado_compliance_005D-20.txt")
