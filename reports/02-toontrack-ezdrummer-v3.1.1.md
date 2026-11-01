# Reporte Forense: Toontrack EZdrummer v3.1.1 U2B (.dmg)

- **Archivo:** `Toontrack EZdrummer v3.1.1.dmg`
- **Hash SHA-256:** `6c74d53f20f1e4013e1270ca84c19d48ea55458899ca435d6be55045bcc8408b`
- **Hash MD5:** `19a4ef0aef3f7b44ae1737380e5fb05f`
- **Tamaño comprimido:** 733 MB (768.606.208 bytes)
- **Tamaño descomprimido:** 942.6 MB (942.669.824 bytes)
- **Formato:** ULFO (`lzfse encoded, lzvn compressed`)
- **Firma digital (`codesign`):** `code object is not signed at all`
- **Grupo de distribución:** Team V.R (`VR.nfo`)
- **Motor de empaquetado:** BitRock InstallBuilder
- **Veredicto:** 🔴 **RIESGO ALTO / NO CONFIABLE**

---

## Hallazgos de la Inspección en Modo Solo Lectura

1. **Estructura del instalador:**
   * Contiene `EZdrummer-3.1.1-osx-installer.app` con identificador `com.installbuilder.appinstaller`.
   * El ejecutable principal es un script `installbuilder.sh` que detecta la arquitectura (`arm64` vs `x86_64`).
2. **Elevación de privilegios de Administrador:**
   * Utiliza un binario intermediario `EZdrummer` con strings de `system.privilege.admin` (`AuthorizationServices`).
   * Su único rol es solicitar la contraseña de administrador (`root`) de macOS.
3. **Carga útil hermética (LZMA):**
   * El archivo de 720 MB `Contents/Resources/installbuilder` posee cabecera LZMA (`5d 00 00 00`). Contiene todos los plugins modificados y componentes de instalación comprimidos en bloque.
4. **Análisis de red:**
   * No se encontraron llamadas a sockets ni URLs hardcodeadas en el binario inicial de arranque (`osx-arm64`), descartando que actúe como un dropper de primera etapa.
