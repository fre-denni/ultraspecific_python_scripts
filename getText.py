"""
usage: python getText.py -i ./logbooks_pdf -o ./risultati_json
"""
import fitz  # PyMuPDF
import os
import argparse
import json
from pathlib import Path
from unidecode import unidecode

# Definiamo le sezioni chiave da cercare nei titoli (tutto minuscolo per facilitare il match)
# Puoi espandere questa lista in base ai titoli che noti più spesso nei logbook.
SECTION_KEYWORDS = [
    "assignment 1", "assignment 2", "assignment 3", "assignment 4",
    "a1", "a2", "a3", "a4","personal reflection", "personal reflections", 
    "reflection", "ai tools", "artificial intelligence", "use of ai", "ai usage",
    "literature review", "digital ethnography", "benchmarking", "conclusion"
]

def extract_sections(text):
    """Semplice funzione per dividere il testo in sezioni basate su parole chiave."""
    lines = text.split('\n')
    current_section = "General/Intro"
    structured_data = {current_section: []}

    for line in lines:
        clean_line = line.strip().lower()
        
        # Logica euristica per i titoli: una riga corta (es. < 60 caratteri) 
        # che contiene una delle nostre keyword viene considerata un titolo di sezione.
        if len(clean_line) > 0 and len(clean_line) < 60:
            for keyword in SECTION_KEYWORDS:
                if keyword in clean_line:
                    current_section = keyword.title()
                    if current_section not in structured_data:
                        structured_data[current_section] = []
                    break # Trovata la sezione, passa alla riga successiva
        
        # Aggiungi la riga pulita alla sezione corrente (evitando righe totalmente vuote)
        if line.strip():
            structured_data[current_section].append(line.strip())

    # Uniamo le liste di righe in un unico grande blocco di testo per ogni sezione
    for section in structured_data:
        structured_data[section] = ' '.join(structured_data[section])
        
    return structured_data

def getTextfromFolders(folder_path, output_dir):
    # Assicurati che la cartella di output esista, altrimenti creala
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Prendi tutti i file pdf dalla cartella
    pdf_files = list(Path(folder_path).glob("*.pdf"))
    
    if not pdf_files:
        print(f"Nessun file PDF trovato in: {folder_path}")
        return

    print(f"Trovati {len(pdf_files)} file PDF. Inizio l'estrazione...")
    
    for pdf_path in pdf_files:
        print(f"Elaborazione in corso: {pdf_path.name}")
        try:
            # Apri il documento PDF
            doc = fitz.open(pdf_path)
            full_text = ""
            
            # Estrai il testo pagina per pagina
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                full_text += page.get_text("text") + "\n"
            
            # Pulisci il testo rimuovendo accenti o caratteri strani che potrebbero rompere l'analisi
            full_text = unidecode(full_text)
            
            # Dividi il testo in sezioni
            sections_data = extract_sections(full_text)
            
            # Salva il risultato in un file JSON con lo stesso nome del PDF
            output_file = Path(output_dir) / f"{pdf_path.stem}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(sections_data, f, indent=4, ensure_ascii=False)
                
        except Exception as e:
            print(f"Errore durante l'elaborazione di {pdf_path.name}: {e}")
            
    print(f"\nEstrazione completata! I file JSON sono salvati in: {output_dir}")

if __name__ == "__main__":
    # Setup di argparse per passare le cartelle da linea di comando
    parser = argparse.ArgumentParser(description="Estrai testo e identifica le sezioni dai logbook in PDF.")
    
    # Argomento obbligatorio: cartella di input
    parser.add_argument("-i", "--input_folder", required=True, 
                        help="Percorso della cartella contenente i file PDF (es. ./logbooks)")
    
    # Argomento opzionale: cartella di output
    parser.add_argument("-o", "--output_folder", default="./extracted_data", 
                        help="Percorso dove salvare i JSON estratti (default: ./extracted_data)")
    
    args = parser.parse_args()
    
    # Avvia la funzione principale
    getTextfromFolders(args.input_folder, args.output_folder)