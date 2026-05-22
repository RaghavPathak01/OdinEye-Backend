import pandas as pd
import chromadb

# Database connection
client = chromadb.PersistentClient(path="./veriguard_db")
# Collection name 'knowledge_vault' rakhein jo Raghav ke wide data ko suit kare
collection = client.get_or_create_collection(name="knowledge_vault")

def load_raghavs_data(file_path):
    # CSV read karein
    df = pd.read_csv(file_path)
    
    # Purana data delete karein taaki duplication na ho (Optional but recommended)
    # collection.delete(where={}) 

    # Bulk mein data add karein
    collection.add(
        documents=df['Content'].tolist(),
        ids=df['ID'].astype(str).tolist(),
        metadatas=[{"source": row['Source'], "domain": row['Domain']} for index, row in df.iterrows()]
    )
    print(f"--- SUCCESS: {len(df)} records from Raghav's file loaded into Knowledge Vault ---")

def verify_from_db(query_text):
    results = collection.query(
        query_texts=[query_text],
        n_results=1
    )
    return results

# Is line se command run karte hi file load ho jayegi
if __name__ == "__main__":
    load_raghavs_data("knowledge_base.csv")