import fitz  # PyMuPDF
import csv
import re
import argparse
from pathlib import Path
from unidecode import unidecode
import sys

# ==========================================
# 1. SISTEMA DI PESI PERSONALIZZABILE
# ==========================================
# Puoi modificare le parole chiave o il loro "peso" (punteggio) qui.
# Se un blocco di testo contiene una parola chiave, guadagna i punti indicati.
# Il blocco viene assegnato alla categoria con il punteggio totale più alto.
# Se il punteggio è 0, finisce in "Altro".

SCORES = {
    "Assignment 1": {
        "assignment 1": 3, "a1": 3, "chrono map": 3, "chrono-map": 3,
        "Assignment 01": 3, "a01": 3,  
        "chronological": 2, "journey map": 3, "user journey": 3, 
        "storyboard": 2, "time map": 2
    },
    "Assignment 2": {
        "assignment 2": 3, "a2": 2, "non-chrono": 3, "mental model": 3, 
        "Assignment 02": 3, "a02": 3,  
        "mind map": 2, "empathy map": 3, "non chronological": 3, "concept map": 3,
        "affinity map": 2, "mental model map": 3, "empathy": 2
    },
    "Assignment 3": {
        "assignment 3": 3, "a3": 2, "literature review": 3, "benchmark": 3, 
        "Assignment 03": 3, "a03": 3, "bibliography": 3, "literature": 2, "paper": 2,
        "benchmarking": 3, "ethnography": 3, "scraping": 3, "sentiment": 2, 
        "zeeschuimer": 3, "research for design": 3, "research question": 2, "design hints": 2
    },
    "Assignment 4": {
        "assignment 4": 3, "a4": 2, "system map": 3, "stakeholder": 3,
        "Assignment 04": 3, "a04": 3,  "app": 2, "service map": 2,
        "service blueprint": 3, "concept creation": 3, "system analysis": 3, "concept": 2
    },
    "AI Usage": {
        "ai tools": 3, "artificial intelligence": 3, "chatgpt": 3, "gemini": 3, 
        "perplexity": 3, "notebooklm": 3, "notebook lm": 3, "prompt": 3, "claude": 3,
        "midjourney": 3, "ai usage": 3, "ai reflection": 3, "use of ai": 3
    }
}

# ==========================================
# 2. LOGICA DI CLASSIFICAZIONE
# ==========================================
def classify_chunk(text):
    chunk_lower = text.lower()
    best_category = "Altro"
    max_score = 0
    
    for category, keywords in SCORES.items():
        current_score = 0
        for kw, weight in keywords.items():
            pattern = r'\b' + re.escape(kw) + r'\b'
            matches = len(re.findall(pattern, chunk_lower))
            current_score += matches * weight
            
        if current_score > max_score:
            max_score = current_score
            best_category = category
            
    return best_category

# ==========================================
# 3. ESTRAZIONE E LIVE UPDATE
# ==========================================
def process_logbooks_live(input_folder, output_csv):
    pdf_files = list(Path(input_folder).glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ Nessun file PDF trovato in: {input_folder}")
        return

    print(f"🚀 Trovati {len(pdf_files)} file PDF. Inizio elaborazione live...")
    
    fieldnames = ['Student_ID'] + list(SCORES.keys()) + ['Altro']
    output_path = Path(output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Apriamo il file CSV in modalità "append" (scrittura continua)
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for idx, pdf_path in enumerate(pdf_files):
            student_id = pdf_path.stem 
            student_buckets = {cat: [] for cat in fieldnames if cat != 'Student_ID'}
            
            # Print status aggiornato
            sys.stdout.write(f"[{idx + 1}/{len(pdf_files)}] Parsing {student_id}... ")
            sys.stdout.flush()
            
            text_found = False # Per controllare se il PDF è un'immagine
            
            try:
                doc = fitz.open(pdf_path)
                
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    # Estraiamo tutto il testo della pagina
                    page_text = page.get_text("text")
                    
                    if page_text.strip():
                        text_found = True
                        
                        # Miglioramento Precisione: Dividiamo il testo in paragrafi logici
                        # usando i doppi a capo invece dei "blocchi" rigidi di PyMuPDF
                        paragraphs = [p.strip() for p in page_text.split('\n\n') if p.strip()]
                        
                        for chunk in paragraphs:
                            clean_chunk = unidecode(chunk) # Pulizia accenti
                            # Evitiamo di classificare frammenti troppo corti (< 3 parole)
                            if len(clean_chunk.split()) < 3:
                                student_buckets["Altro"].append(clean_chunk)
                                continue
                                
                            category = classify_chunk(clean_chunk)
                            student_buckets[category].append(clean_chunk)
                            
            except Exception as e:
                print(f"\n   ❌ Errore nella lettura: {e}")
                continue

            # Avviso visivo se il PDF è un'immagine rasterizzata
            if not text_found:
                print("⚠️  WARNING: Nessun testo trovato! (Probabilmente salvato come immagine)")
            else:
                print("✅ Fatto.")

            # Prepariamo la riga
            row_data = {'Student_ID': student_id}
            for cat in student_buckets:
                if student_buckets[cat]:
                    row_data[cat] = "\n\n---\n\n".join(student_buckets[cat])
                else:
                    row_data[cat] = ""
                    
            # SALVIAMO IMMEDIATAMENTE NEL CSV
            writer.writerow(row_data)
            f.flush() # Forza il sistema operativo a scrivere su disco all'istante

    print(f"\n🎉 Processo completato! Dati salvati progressivamente in: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Estrai e classifica testi con salvataggio live su CSV.")
    parser.add_argument("-i", "--input", required=True, help="Cartella con i PDF")
    parser.add_argument("-o", "--output", default="dataset_logbooks.csv", help="Percorso del file CSV di output")
    
    args = parser.parse_args()
    process_logbooks_live(args.input, args.output)