from PIL import Image
import os

# Cartelle base
PNG_DIR = "png"
WEBP_DIR = "webp"

# Crea le cartelle base se non esistono
os.makedirs(PNG_DIR, exist_ok=True)
os.makedirs(WEBP_DIR, exist_ok=True)

def convert_image(src_path, dst_path):
    """Converte un'immagine PNG in WebP e la salva nel percorso di destinazione."""
    im = Image.open(src_path).convert("RGBA")
    im.save(dst_path, "webp")
    print(f"  ✓ {src_path} → {dst_path}")

def convert_all():
    converted = 0
    skipped = 0

    # Ricorre ricorsivamente nella cartella png
    for root, dirs, files in os.walk(PNG_DIR):
        png_files = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg"))]

        if not png_files:
            continue

        # Calcola la sottocartella relativa (es. "png/jobs" → "jobs")
        relative = os.path.relpath(root, PNG_DIR)

        # Cartella di destinazione corrispondente in webp/
        dst_dir = os.path.join(WEBP_DIR, relative)
        os.makedirs(dst_dir, exist_ok=True)

        for filename in png_files:
            src_path = os.path.join(root, filename)
            dst_filename = os.path.splitext(filename)[0] + ".webp"
            dst_path = os.path.join(dst_dir, dst_filename)

            try:
                convert_image(src_path, dst_path)
                converted += 1
            except Exception as e:
                print(f"  ✗ Errore su {src_path}: {e}")
                skipped += 1

    print(f"\nDone! {converted} file convertiti, {skipped} errori.")

if __name__ == "__main__":
    convert_all()
