# Reporte Forense: Arturia Analog Lab V Pro v5.10.2 (Infección AMOS Stealer)

- **Archivo DMG:** `Arturia Analog Lab V Pro v5.10.2.4741.dmg`
- **Hash SHA-256 (DMG):** `56a963386a216593ce856bc544f3f27c7ed5c4a8a47f962afd11f5c2a624b14f`
- **Hash MD5 (DMG):** `293a85ea32a33001db60695f15fe6d12`
- **Veredicto:** 🚨 **CRÍTICO: TROYANO DE ROBO DE DATOS ACTIVO (ATOMIC MACOS STEALER - AMOS)**

---

## 🚨 Hallazgo Crítico de Seguridad

Al inspeccionar estáticamente la imagen montada en solo lectura (`/tmp/arturia_inspect`), se identificó una campaña de señuelo (*Trojan Horse / Malvertising*) combinada con un instalador legítimo:

```text
/tmp/arturia_inspect/
├── Analog_Lab_V__5_10_2_4741.pkg   (4.95 GB - Instalador oficial legítimo firmado por Arturia)
├── Extra/
│   ├── Analog Lab V.command         (Script Perl para parchear opcodes de licencia)
│   └── info.txt
├── Open Gatekeeper friendly         🚨 TROYANO AMOS (Atomic macOS Stealer) 🚨
└── info.txt
```

---

## 🔬 Análisis Forense de la Carga Maliciosa: "Open Gatekeeper friendly"

- **Hash SHA-256:** `b32cca8b57c79409887fe4e5cdbabdf7687a993fb3f82e5f736f2b3bf058bdcc`
- **Hash MD5:** `e45071579d5b58f7e05d7fefdd49f868`
- **Familia de Malware:** **Atomic macOS Stealer (AMOS)**
- **Servidor C2 (Comando y Control):** `http://79.137.192.4/p2p` (Red AS216246 Aeza Group, San Petersburgo, Rusia).

### Modo de Operación de la Amenaza:
El archivo simula ser una utilidad inofensiva para "ayudar al usuario a saltarse Gatekeeper". Al abrirse, ejecuta un script codificado en Base64/AppleScript que realiza una recolección masiva de credenciales y datos privados en milisegundos:

1. **Robo de Llavero de macOS:**
   * Extrae directamente el archivo de contraseñas del sistema: `/Library/Keychains/login.keychain-db`.
2. **Robo de Navegadores Web (Cookies y Sesiones):**
   * Google Chrome, Brave Browser, Microsoft Edge, Vivaldi, Opera, OperaGX, Chromium, Firefox, Waterfox, Pale Moon y Safari (`Cookies.binarycookies`).
3. **Robo de Billeteras Cripto (Wallets):**
   * Electrum, Coinomi, Exodus, Atomic Wallet, Wasabi, Ledger Live, Monero, Bitcoin Core, Litecoin Core, Dash Core, Guarda, Dogecoin Core, Trezor Suite, Binance y TonKeeper.
4. **Robo de Notas de Apple y Documentos Personales:**
   * Base de datos completa de Apple Notes (`NoteStore.sqlite`).
   * Búsqueda automática en las carpetas `Desktop` y `Documents` de archivos con extensiones `.txt`, `.rtf`, `.key`, `.wallet`, `.doc`, `.docx` y `.kdbx` (KeePass).
5. **Empaquetado y Exfiltración:**
   * Comprime todo el botín en `/tmp/out.zip` usando la herramienta del sistema `ditto`.
   * Realiza un envío inmediato vía `curl -X POST` hacia el servidor C2 ruso: `http://79.137.192.4/p2p`.
   * Borra las carpetas temporales (`/tmp/xuyna`, `/tmp/photos`, `/tmp/out.zip`) para eliminar evidencia forense.

---

## 📦 Análisis del Paquete PKG: ¿Trae las librerías de sonido?

* **Nombre:** `Analog_Lab_V__5_10_2_4741.pkg` (4.95 GB).
* **Firma oficial:** `Developer ID Installer: Arturia (T53ZHSF36C)`.
* **Notarización de Apple:** `trusted by the Apple notary service`.
* **Conclusión:** El archivo PKG es el instalador **100% original, oficial e íntegro de Arturia**, el cual **SÍ contiene todas las librerías de sonido de fábrica, motores de síntesis y presets (4.95 GB)**. Los atacantes utilizaron el instalador real como cebo para engañar al usuario y hacer que ejecute el troyano `Open Gatekeeper friendly`.

---

## 🛡️ Indicadores de Compromiso (IoCs)

| Indicador | Tipo | Valor |
| :--- | :--- | :--- |
| **AMOS Binary** | SHA-256 | `b32cca8b57c79409887fe4e5cdbabdf7687a993fb3f82e5f736f2b3bf058bdcc` |
| **AMOS Binary** | MD5 | `e45071579d5b58f7e05d7fefdd49f868` |
| **C2 Server** | IP / URL | `http://79.137.192.4/p2p` |
| **C2 Provider** | ASN / Org | AS216246 (Aeza Group / Rusia) |
| **Directorio temporal** | Path | `/tmp/xuyna/` |
