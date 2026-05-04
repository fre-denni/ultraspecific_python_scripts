import pandas as pd
import re

# Carica i dati originali
df = pd.read_csv('dataset.csv')

# Dizionario dei pesi (Token Scoring System)
SCORES = {
    "Assignment 1": {"assignment 1": 3, "a1": 2, "chrono map": 3, "chrono-map": 3, "chronological": 2, "journey map": 3, "user journey": 3, "storyboard": 2, "time map": 2},
    "Assignment 2": {"assignment 2": 3, "a2": 2, "non-chrono": 3, "mental model": 3, "mind map": 2, "empathy map": 3, "non chronological": 3, "concept map": 3},
    "Assignment 3": {"assignment 3": 3, "a3": 2, "literature review": 3, "benchmark": 3, "benchmarking": 3, "ethnography": 3, "scraping": 3, "sentiment": 2, "zeeschuimer": 3, "research for design": 3, "research question": 2, "design hints": 2},
    "Assignment 4": {"assignment 4": 3, "a4": 2, "system map": 3, "stakeholder": 3, "service blueprint": 3, "concept creation": 3, "system analysis": 3, "concept": 2},
    "AI Usage": {"ai tools": 3, "artificial intelligence": 3, "chatgpt": 3, "gemini": 3, "perplexity": 3, "notebooklm": 3, "notebook lm": 3, "prompt": 3, "midjourney": 3, "ai usage": 3, "ai reflection": 3, "ai": 2}
}

refined_data = []

# Analizza il testo per ogni studente
for idx, row in df.iterrows():
    student_id = row['Student_ID']
    student_buckets = {k: [] for k in SCORES.keys()}
    student_buckets["Altro"] = []
    
    # Raccogli tutti i frammenti di testo
    all_chunks = []
    for col in df.columns:
        if col == 'Student_ID' or pd.isna(row[col]):
            continue
        chunks = str(row[col]).split('---')
        for chunk in chunks:
            clean_chunk = chunk.strip()
            if clean_chunk:
                all_chunks.append(clean_chunk)
                
    # Riassegna ogni frammento in base al punteggio più alto
    for chunk in all_chunks:
        chunk_lower = chunk.lower()
        best_category = "Altro"
        max_score = 0
        
        for category, keywords in SCORES.items():
            current_score = 0
            for kw, weight in keywords.items():
                # Regex per intercettare parole intere ed evitare falsi positivi
                pattern = r'\b' + re.escape(kw) + r'\b'
                matches = len(re.findall(pattern, chunk_lower))
                current_score += matches * weight
                
            if current_score > max_score:
                max_score = current_score
                best_category = category
                
        # Inserisci nel cluster vincente
        if max_score > 0:
            student_buckets[best_category].append(chunk)
        else:
            student_buckets["Altro"].append(chunk)
            
    # Ricomponi la riga
    row_data = {"Student_ID": student_id}
    for cat in student_buckets:
        row_data[cat] = "\n\n---\n\n".join(student_buckets[cat])
        
    refined_data.append(row_data)

# Salva il nuovo dataset
refined_df = pd.DataFrame(refined_data)
refined_df.to_csv('refined_dataset.csv', index=False)