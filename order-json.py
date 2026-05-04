import json
import csv
import re
import argparse
from pathlib import Path

def create_student_csv(json_path, csv_path):
    # Carichiamo il file JSON master che avevamo creato
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Errore nell'apertura del JSON: {e}")
        return

    students_data = {}

    # Navighiamo attraverso ogni cluster (Assignment 1, AI Usage, ecc.)
    for cluster_name, items in data.items():
        for item in items:
            source_file = item.get('source_file', '')
            text = item.get('text', '').strip()
            
            if not text:
                continue

            # Estraiamo l'ID studente dal nome del file (cerca i numeri)
            # es. "11114740.pdf.json" -> "11114740"
            match = re.search(r'\d+', source_file)
            if match:
                student_id = match.group()
            else:
                student_id = source_file # Fallback se non trova numeri

            # Se è un nuovo studente, creiamo la sua riga vuota
            if student_id not in students_data:
                students_data[student_id] = {'Student_ID': student_id}

            # Inseriamo il testo nella colonna corretta per questo studente
            if cluster_name in students_data[student_id]:
                # Se c'è già del testo in questo cluster per questo studente, li uniamo
                students_data[student_id][cluster_name] += "\n\n---\n\n" + text
            else:
                students_data[student_id][cluster_name] = text

    # Prepariamo le colonne per il CSV: ID + i nomi dei cluster
    fieldnames = ['Student_ID'] + list(data.keys())

    # Scriviamo il file CSV
    try:
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            # Scriviamo i dati riga per riga (studente per studente)
            for student_id, row in students_data.items():
                writer.writerow(row)
                
        print(f"Successo! Il CSV strutturato è stato salvato in: {csv_path}")
        print(f"Trovati {len(students_data)} studenti unici.")
        
    except Exception as e:
        print(f"Errore nel salvataggio del CSV: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converte il JSON master in un CSV raggruppato per studente.")
    parser.add_argument("-i", "--input", required=True, help="Percorso del file master_clusters.json")
    parser.add_argument("-o", "--output", default="dataset_studenti_finale.csv", help="Percorso di salvataggio del CSV")
    
    args = parser.parse_args()
    create_student_csv(args.input, args.output)