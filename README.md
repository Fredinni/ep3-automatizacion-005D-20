# EP3 — Implementación de Automatización de Red con Compliance Auditado

**Alumno:** Vasquez Cortes Freddy  
**Código:** 005D-20  
**Empresa cliente:** Supermercados Cord Ltda  
**Fecha:** 2026-06-26  

---

## 1. Objetivo del proyecto

Se implementó la automatización completa del ciclo de incorporación de un nuevo router para la empresa Supermercados Cord Ltda. El objetivo fue configurar el equipo con los estándares corporativos de la empresa, verificar su correcta aplicación mediante protocolos de gestión de red, y dejar evidencia auditable de todo el proceso en un repositorio GitHub.

---

## 2. Alcance

**Configurado:**
- Hostname corporativo (RTR-SUPCORD)
- Interfaz Loopback10 con IP de gestión (10.5.20.1/24)
- Descripción de interfaz WAN (Enlace-WAN-San-Antonio)
- Banner de acceso corporativo
- Servidor NTP (208.67.222.222)
- Habilitación de NETCONF y RESTCONF para gestión automatizada

**Fuera del alcance:**
- Configuración de protocolos de enrutamiento dinámico
- Configuración de VLANs o interfaces adicionales
- Hardening de seguridad avanzado

**Herramientas utilizadas:** pyATS/Genie, Ansible, ncclient (NETCONF), Python requests (RESTCONF)

---

## 3. Infraestructura utilizada

| Componente | Detalle |
|---|---|
| Router | Cisco CSR1000V — IOS-XE 16.9.5 |
| IP del router | 192.168.56.103 |
| Estación de trabajo | DEVASC VM — Ubuntu / labvm |
| Sistema operativo VM | Ubuntu Linux |
| Python | 3.8 |
| pyATS / Genie | 20.5 |
| Ansible | 2.9 |
| ncclient | Última versión disponible |

---

## 4. Tecnologías empleadas y justificación

**pyATS / Genie:** Se usó en la Fase 1 para capturar el estado inicial del router antes de cualquier cambio (baseline), y en la Fase 5 para capturar el estado final y comparar diferencias. Se eligió porque permite documentar el estado del dispositivo vía SSH sin requerir NETCONF habilitado.

**Ansible:** Se usó en la Fase 2 para aplicar toda la configuración corporativa de forma automatizada e idempotente. Se eligió porque permite declarar el estado deseado del dispositivo y aplicarlo de forma reproducible sin intervención manual.

**NETCONF (ncclient):** Se usó en la Fase 3 para validar de forma independiente que la configuración fue aplicada correctamente. Se eligió porque entrega el árbol de configuración completo en XML estructurado, permitiendo verificación precisa campo por campo.

**RESTCONF (Python requests):** Se usó en la Fase 4 para una segunda validación independiente usando endpoints REST. Se eligió porque permite consultar recursos específicos de configuración en formato JSON mediante HTTP, complementando la validación NETCONF.

---

## 5. Configuración aplicada

| Parámetro | Valor configurado |
|---|---|
| Hostname corporativo | RTR-SUPCORD |
| IP Loopback10 | 10.5.20.1 |
| Máscara Loopback10 | 255.255.255.0 |
| Descripción interfaz WAN | Enlace-WAN-San-Antonio |
| Banner de acceso | ACCESO RESTRINGIDO - SUPCORD |
| Servidor NTP | 208.67.222.222 |
| NETCONF | Habilitado (puerto 830) |
| RESTCONF | Habilitado (HTTPS) |
| HTTP seguro | Habilitado |

---

## 6. Resultados de validación

| Criterio | NETCONF | RESTCONF |
|---|---|---|
| Hostname corporativo (RTR-SUPCORD) | CONFORME | CONFORME |
| IP Loopback (10.5.20.1) | CONFORME | CONFORME |
| Máscara Loopback (255.255.255.0) | CONFORME | — |
| Descripción WAN (Enlace-WAN-San-Antonio) | CONFORME | CONFORME |
| Servidor NTP (208.67.222.222) | CONFORME | CONFORME |
| **Resultado global** | **CONFORME** | **CONFORME** |

---

## 7. Conclusiones

El router fue incorporado exitosamente a la red corporativa de Supermercados Cord Ltda con toda la configuración estándar aplicada y validada. Las validaciones independientes mediante NETCONF y RESTCONF confirmaron que los 5 criterios de compliance se encuentran correctamente configurados. El equipo fue entregado a operaciones en estado CONFORME y listo para operar en producción. Todo el proceso quedó registrado y auditable en el historial de commits del repositorio GitHub.
