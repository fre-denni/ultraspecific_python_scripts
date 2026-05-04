import json
import os
import argparse
from pathlib import Path

# Definiamo i cluster semantici
CLUSTERS = {
    "Assignment 1": ["assignment 1", "a1", "chrono map", "chrono-maps", "user journey map", "chrono maps", "time", "chronological maps", "storyboard"],
    "Assignment 2": ["assignment 2", "a2", "non-chrono maps", "non chronological map", "mental model", "mind map", "concept map", "mindset"],
    "Assignment 3": ["assignment 3", "a3", "literature review", "benchmark", "digital ethnography", "sentiment analysis", "client", "bibliography"],
    "Assignment 4": ["assignment 4", "a4", "system map", "system", "app", "solution", "service"],
    "AI Usage" : ["ai assignment", "personal reflections", "artificial intelligence", "tools", "ai use", "ai tools", "chatgpt", "gemini", "prompt"],
}

def aggregate_and_recluster(input_folder, output_file):
    # Inizializziamo il dizionario globale con liste vuote per ogni cluster
    aggregated_data = {key: [] for key in CLUSTERS.keys()}
    aggregated_data["Altro"] = []
    
    json_files = list(Path(input_folder).glob("*.json"))
    
    if not json_files:
        print(f"Nessun file JSON trovato in: {input_folder}")
        return

    print(f"Trovati {len(json_files)} file JSON. Inizio l'aggregazione...")
    
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"Errore nella lettura di {json_file.name}. Salto il file.")
                continue
        
        # Iteriamo sulle sezioni originarie del singolo file
        for original_section, content in data.items():
            if not content.strip():
                continue # Ignoriamo i blocchi di testo completamente vuoti
                
            content_lower = content.lower()
            assigned = False
            
            # Controlliamo a quale cluster appartiene
            for cluster, keywords in CLUSTERS.items():
                # Cerchiamo le keyword sia nel titolo originale che nel contenuto
                if any(kw in content_lower for kw in keywords) or any(kw in original_section.lower() for kw in keywords):
                    # Creiamo un record strutturato invece di unire stringhe
                    entry = {
                        "source_file": json_file.name,
                        "original_section": original_section,
                        "text": content.strip()
                    }
                    aggregated_data[cluster].append(entry)
                    assigned = True
                    break # Interrompe il ciclo per non assegnare il testo a più di un cluster
            
            # Se non matcha nessuna keyword, finisce in "Altro"
            if not assigned:
                aggregated_data["Altro"].append({
                    "source_file": json_file.name,
                    "original_section": original_section,
                    "text": content.strip()
                })
                
    # Salviamo il tutto in un unico grande file master
    # Assicuriamoci che la cartella di destinazione esista
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(aggregated_data, f, indent=4, ensure_ascii=False)
        
    print(f"\nOperazione completata!")
    print(f"Tutti i testi sono stati raggruppati correttamente in: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aggrega e riclassifica i file JSON dei logbook.")
    parser.add_argument("-i", "--input", required=True, help="Percorso della cartella contenente i JSON da pulire")
    parser.add_argument("-o", "--output", default="./risultato_finale/master_clusters.json", help="Percorso e nome del file JSON di output (es. ./out/master.json)")
    
    args = parser.parse_args()
    
    aggregate_and_recluster(args.input, args.output)