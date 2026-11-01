# Reporte Forense: Arturia Analog Lab V Pro v5.10.2.4741 (.dmg)

- **Archivo:** `Arturia Analog Lab V Pro v5.10.2.4741.dmg`
- **Hash SHA-256:** `56a963386a216593ce856bc544f3f27c7ed5c4a8a47f962afd11f5c2a624b14f`
- **Hash MD5:** `293a85ea32a33001db60695f15fe6d12`
- **Tamaño comprimido:** 4.6 GB (4.939.214.848 bytes)
- **Tamaño descomprimido:** 5.39 GB (5.387.772.928 bytes)
- **Formato:** UDZO (`zlib compressed data`)
- **Firma digital (`codesign`):** `code object is not signed at all`
- **Atributos extendidos:** `com.apple.quarantine` registrado por Safari
- **Veredicto:** 🔴 **RIESGO ALTO / NO CONFIABLE**

---

## Hallazgos Clave

1. **Ausencia total de firma:** Arturia firma todos sus instaladores oficiales con `Developer ID Installer: Arturia (Team ID: 99SF484AH8)`. Este archivo carece de cualquier firma válida.
2. **Distribución vulnerada:** Arturia distribuye sus instrumentos exclusivamente mediante paquetes `.pkg` firmados individualmente y gestionados por el software **Arturia Software Center (ASC)**.
3. **Peligro para el usuario:** Los cracks de Arturia suelen parchear frameworks compartidos en `/Library/Arturia/` que exigen privilegios de administrador, lo que suele ser aprovechado por actores maliciosos para introducir persistencia en `LaunchAgents`.
