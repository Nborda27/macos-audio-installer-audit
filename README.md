# macOS Audio Installer Audit & Reverse Engineering

Repositorio de investigación en ciberseguridad, análisis forense estático e ingeniería inversa aplicada a instaladores no oficiales de plugins de audio y DAWs en macOS.

---

## 🎯 Objetivo

Establecer un marco metodológico estricto, reproducible y seguro para analizar imágenes de disco (`.dmg`) e instaladores de software de audio sin comprometer la seguridad del equipo anfitrión:
- **Cero ejecución:** No se ejecutan binarios desconocidos ni se abren archivos ejecutables.
- **Aislamiento:** Inspección en modo solo lectura (`-readonly -nobrowse -noautoopen`).
- **Triage de amenazas:** Detección de *info-stealers* (como Atomic Stealer / AMOS), droppers de red y scripts maliciosos de post-instalación.

---

## 📂 Estructura del Repositorio

```text
macos-audio-installer-audit/
├── .gitignore              # Protección OPSEC contra subida de binarios maliciosos
├── README.md               # Metodología y documentación general
├── reports/                # Informes forenses individuales
│   ├── 01-logic-pro-v11.0.1.md
│   ├── 02-toontrack-ezdrummer-v3.1.1.md
│   └── 03-arturia-analog-lab-v5.10.2.md
├── tools/                  # Scripts en Python/Bash para extracción y análisis estático
└── ioc/                    # Indicadores de Compromiso (Hashes SHA-256 / MD5)
    └── hashes.json
```

---

## 🔬 Muestras Analizadas

| Muestra | Tamaño | Hash SHA-256 | Firma | Riesgo |
| :--- | :--- | :--- | :--- | :--- |
| **Logic Pro v11.0.1** | 1.2 GB | `8588439d0c251a22893259371eb74fa815e501abf9d072de99cd3815ed1b542d` | ❌ Sin firma | 🔴 Alto |
| **Toontrack EZdrummer v3.1.1** | 733 MB | `6c74d53f20f1e4013e1270ca84c19d48ea55458899ca435d6be55045bcc8408b` | ❌ Sin firma | 🔴 Alto |
| **Arturia Analog Lab V Pro** | 4.6 GB | `56a963386a216593ce856bc544f3f27c7ed5c4a8a47f962afd11f5c2a624b14f` | ❌ Sin firma | 🔴 Alto |

---

## ⚖️ Aviso Legal y Ético

Este repositorio tiene fines exclusivamente educativos y de investigación en ciberseguridad defensiva. No se distribuyen cracks, números de serie, llaves de activación ni binarios protegidos por derechos de autor.
