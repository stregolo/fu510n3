import requests
import re
import os

def delete_file_if_exists(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f'File {file_path} deleted.')

def fetch_m3u8_data(url):
    """Scarica il contenuto del file .m3u8 da un URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Errore durante il download del file .m3u8 da {url}: {e}")
        return ""


def remove_extm3u_from_second_file(m3u8_data):
    """Rimuove la riga #EXTM3U all'inizio del secondo file m3u8."""
    lines = m3u8_data.splitlines()
    if lines and lines[0] == "#EXTM3U":
        lines.pop(0)  # Rimuove la prima riga (#EXTM3U)
    return "\n".join(lines)


def save_m3u8(merged_data):
    """Salva i contenuti uniti in un file M3U8."""
    if os.path.exists(output_file):
        os.remove(output_file)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(merged_data)

# URL dei file m3u8 da cui scaricare i dati
M3U8_URLS = [
    "https://raw.githubusercontent.com/stregolo/eventi/refs/heads/main/out_tivimate.m3u8",  # URL del primo file m3u8
    "https://raw.githubusercontent.com/stregolo/vavooita/refs/heads/main/vavooIta.m3u8"  # URL del secondo file m3u8
]

output_file = os.path.join(os.path.dirname(os.path.dirname(__file__)),  'merged.m3u8')


def main():
    merged_data = ""  
    delete_file_if_exists(output_file)


    # Uniamo il contenuto dei file m3u8
    for i, url in enumerate(M3U8_URLS):
        m3u8_data = fetch_m3u8_data(url)
        if m3u8_data:
            # Se è il secondo file o più, rimuoviamo la riga #EXTM3U
            if i > 0:
                m3u8_data = remove_extm3u_from_second_file(m3u8_data)
            merged_data += m3u8_data + "\n"  # Aggiungi il contenuto di ogni file separato da una nuova riga

    # Salvataggio nel file M3U8
    save_m3u8(merged_data)

    print(f"File {output_file} creato con successo!")


if __name__ == "__main__":
    main()
