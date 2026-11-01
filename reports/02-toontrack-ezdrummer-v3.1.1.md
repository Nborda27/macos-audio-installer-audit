# Reporte Forense e Ingeniería Inversa: Toontrack EZdrummer v3.1.1 U2B

- **Archivo:** `Toontrack EZdrummer v3.1.1.dmg`
- **Hash SHA-256:** `6c74d53f20f1e4013e1270ca84c19d48ea55458899ca435d6be55045bcc8408b`
- **Hash MD5:** `19a4ef0aef3f7b44ae1737380e5fb05f`
- **Grupo de distribución:** Team V.R (`VR.nfo`)
- **Motor del instalador:** BitRock InstallBuilder con compresión LZMA por bloques
- **Veredicto Técnico:** 🟡 **CRACK LIMPIO / SIN MALWARE ACTIVO DETECTADO (CON RIESGOS DE INSTALADOR)**

---

## 🔬 Metodología de Ingeniería Inversa Aplicada

1. **Montaje aislado en modo solo lectura:**
   Montado mediante `hdiutil attach -readonly -nobrowse -noautoopen -mountpoint /tmp/ezdrummer_inspect` sin permisos `root`.
2. **Descifrado del contenedor InstallBuilder:**
   Se desarrolló el script [`tools/extract_installbuilder.py`](../tools/extract_installbuilder.py) en Python. Se descubrió que la carga útil de 720 MB está dividida en **bloques LZMA continuos de 2.500.000 bytes (2.5 MB)** con prefijo `0xff`.
3. **Reconstrucción del binario universal:**
   Se concatenaron y descomprimieron 18 bloques LZMA consecutivos hasta reconstruir con precisión quirúrgica el binario ejecutable universal Fat Mach-O de **43.634.288 bytes (~43.6 MB)** en `sandbox/EZdrummer_universal.bin`.

---

## 📊 Hallazgos del Análisis Binario (Mach-O)

### 1. Arquitectura e Integridad (`lipo`)
* Binario Fat Mach-O con soporte universal dual:
  * **Intel x86_64:** slice de 22.6 MB (offset `0x4000`).
  * **Apple Silicon ARM64:** slice de 20.9 MB (offset `0x015a8000`).
* Ambas arquitecturas se encuentran íntegras y validadas por el sistema.

### 2. Auditoría de Librerías Dinámicas (`otool -L`)
* **Sin Dylib Hijacking:** El binario **únicamente** enlaza frameworks oficiales del sistema macOS ubicados en `/System/Library/Frameworks/` y `/usr/lib/`.
* No se detectó ninguna librería dinámica inyectada ni rutas relativas (`@rpath`) dirigidas a carpetas temporales o de terceros.
* Framework de audio identificado: desarrollado sobre **JUCE** (`https://juce.com`).

### 3. Estado de la Firma de Código (`codesign`)
* **Identifier:** `com.toontrack.ezdrummer3.app`
* **Signature:** `adhoc` (`flags=0x2(adhoc)`)
* **TeamIdentifier:** `not set`
* **CDHash:** `8a0e64db05a172817842d2bd8dc2b35122dc1541`
* **Diagnóstico del crack:** Team V.R eliminó el certificado oficial de Toontrack AB, parcheó las rutinas de validación de licencia en ensamblador y re-firmó el binario con firma ad-hoc local para permitir su ejecución en Apple Silicon sin que el kernel de macOS lo cierre con `SIGKILL`.

### 4. Auditoría de Red y Procesos (`nm` y `strings`)
* **Sin C2 / Sin Spyware:** Todas las URLs embebidas pertenecen exclusivamente a dominios oficiales:
  * `http://www.toontrack.com` (soporte, registro y manuales).
  * `https://juce.com` (framework de desarrollo).
  * `http://www.w3.org` (esquemas XML).
  * No hay conexiones a servidores externos no autorizados ni direcciones IP sospechosas.
* **Sin intérpretes de comandos:** No se importan ni llaman funciones de ejecución de procesos (`_system`, `_popen`, `_posix_spawn`). Tampoco contiene referencias a intérpretes `/bin/sh`, `/bin/bash` u `osascript`.

---

## 🛡️ Evaluación de Riesgo Final

* **El ejecutable `EZdrummer`:** Es un crack técnico limpio de Team V.R (modificación estricta de la protección de licencia sin adición de troyanos ni *info-stealers* en el código de audio).
* **El instalador `InstallBuilder`:** El riesgo residual reside en que el instalador solicita permisos de administrador (`root`) durante la fase inicial para escribir en `/Library/Audio/Plug-Ins/`. Aunque no se detectaron scripts destructivos, cualquier instalador empaquetado por terceros requiere precaución operativa.
