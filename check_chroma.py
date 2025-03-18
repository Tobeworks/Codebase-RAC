import chromadb

# Client erstellen
client = chromadb.HttpClient(host="localhost", port=8000)

# Alle verfügbaren Sammlungen anzeigen
collection_names = client.list_collections()
print("Verfügbare Sammlungen:")
for name in collection_names:
    print(f"- Name: {name}")

# Wenn Collections vorhanden sind, versuchen wir eine zu öffnen
if collection_names:
    # Erste Collection nehmen
    collection_name = collection_names[0]
    print(f"\nVersuche Collection zu öffnen: {collection_name}")
    
    try:
        # Collection öffnen
        coll = client.get_collection(name=collection_name)
        print(f"Collection erfolgreich geöffnet!")
        
        # Anzahl der Dokumente in der Collection anzeigen
        count = coll.count()
        print(f"Anzahl der Dokumente: {count}")
    except Exception as e:
        print(f"Fehler beim Öffnen der Collection: {e}")
else:
    print("\nKeine Collections gefunden! Wir müssen erst eine erstellen.")