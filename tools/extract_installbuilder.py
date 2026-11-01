#!/usr/bin/env python3
"""
tools/extract_installbuilder.py
Extractor y ensamblador de binarios para BitRock InstallBuilder.
Reconstruye el binario Mach-O universal completo concatenando los bloques LZMA.
"""

import os
import sys
import lzma

PAYLOAD_PATH = "/tmp/ezdrummer_inspect/EZdrummer-3.1.1-osx-installer.app/Contents/Resources/installbuilder"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SANDBOX_DIR = os.path.join(BASE_DIR, "sandbox")
TARGET_SIZE = 43634288  # Tamaño exacto declarado en la cabecera Fat Mach-O (43.6 MB)

def reconstruct_binary():
    if not os.path.exists(PAYLOAD_PATH):
        print(f"[-] Error: {PAYLOAD_PATH} no existe. Verificá el montaje.")
        sys.exit(1)

    output_binary = os.path.join(SANDBOX_DIR, "EZdrummer_universal.bin")
    print(f"[+] Reconstruyendo binario universal en: {output_binary}")
    print(f"[+] Tamaño objetivo: {TARGET_SIZE} bytes ({TARGET_SIZE / (1024*1024):.2f} MB)")

    assembled_data = bytearray()
    file_size = os.path.getsize(PAYLOAD_PATH)

    with open(PAYLOAD_PATH, "rb") as f:
        # El chunk 0 fue el CodeResources (73.843 bytes comprimidos en offset 1)
        # El chunk 1 empieza en el byte 73844
        offset = 73844
        chunk_idx = 1

        while len(assembled_data) < TARGET_SIZE and offset < file_size:
            f.seek(offset)
            header = f.read(16)
            if not header:
                break

            lzma_offset = offset
            if header[0] == 0xff and header[1] == 0x5d:
                lzma_offset = offset + 1
            elif header[0] == 0x5d:
                lzma_offset = offset

            f.seek(lzma_offset)
            buffer = f.read(15 * 1024 * 1024)
            try:
                decompressor = lzma.LZMADecompressor(format=lzma.FORMAT_ALONE)
                decompressed = decompressor.decompress(buffer)
                consumed = len(buffer) - len(decompressor.unused_data)

                assembled_data.extend(decompressed)
                print(f"[+] Bloque #{chunk_idx}: +{len(decompressed)} bytes descomprimidos (Total acumulado: {len(assembled_data) / (1024*1024):.2f} MB)")

                offset = lzma_offset + consumed
                chunk_idx += 1

            except Exception as e:
                print(f"[-] Error descomprimiendo bloque #{chunk_idx} en offset {lzma_offset}: {e}")
                break

    # Recortar al tamaño exacto de la cabecera Mach-O
    final_data = assembled_data[:TARGET_SIZE]
    with open(output_binary, "wb") as out_f:
        out_f.write(final_data)

    print(f"\n[✓] ¡Binario reconstruido con éxito!")
    print(f"[+] Archivo final: {output_binary}")
    print(f"[+] Tamaño final: {len(final_data)} bytes")

if __name__ == "__main__":
    reconstruct_binary()
