# Code-RAG: Chroma-Vektordatenbank mit Anything LLM

Dieses Repository enthält Anleitungen zur Erstellung eines Code-Retrieval-Augmented-Generation (RAG) Systems mit Chroma und Anything LLM.

## 📋 Inhaltsverzeichnis

- [Überblick](#überblick)
- [Installation](#installation)
- [Indexierung von Code](#indexierung-von-code)
- [Starten des Chroma-Servers](#starten-des-chroma-servers)
- [Einrichtung von Anything LLM](#einrichtung-von-anything-llm)
- [Fehlerbehebung](#fehlerbehebung)

## 🔍 Überblick

Dieses System ermöglicht es, eigene Codebasen zu indexieren und mit Hilfe von LLMs (Large Language Models) intelligente Anfragen dazu zu stellen. Die wichtigsten Komponenten sind:

1. **Chroma**: Eine Vektordatenbank zur Speicherung von Code-Embeddings
2. **Anything LLM**: Eine benutzerfreundliche Chat-Oberfläche zum Abfragen der Codebasen
3. **LangChain**: Framework zur Integration von Vektordatenbanken mit LLMs

## 🛠️ Installation

### Voraussetzungen

- Python 3.8+ und pip
- OpenAI API-Schlüssel (für Embeddings und optional auch für das LLM)
- Optional: Anthropic API-Schlüssel (für Claude-Modelle)

### Pakete installieren

```bash
# Erstelle eine virtuelle Umgebung (empfohlen)
python -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate

# Installiere die benötigten Pakete
pip install chromadb langchain langchain-community langchain-openai python-dotenv
```

### .env-Datei erstellen

Erstelle eine `.env`-Datei im Projektverzeichnis mit API-Schlüsseln:

```
OPENAI_API_KEY=dein-openai-api-key-hier
ANTHROPIC_API_KEY=dein-anthropic-api-key-hier  # Optional
```

## 📚 Indexierung von Code

Verwende das `chroma_indexer.py`-Skript, um deine Codebasen zu indexieren. Die wichtigsten Optionen:

### Neue Codebase indexieren

```bash
python chroma_indexer.py --path /pfad/zu/deiner/codebase --collection meine_collection
```

### Weitere Codebase zur selben Collection hinzufügen

```bash
python chroma_indexer.py --path /pfad/zu/weiterer/codebase --collection meine_collection --add
```

### Anpassung der zu indexierenden Dateitypen

```bash
python chroma_indexer.py --path /pfad/zur/codebase --collection meine_collection --extensions .py,.js,.html,.ts,.jsx
```

### Anpassung des Speicherorts der Datenbank

```bash
python chroma_indexer.py --path /pfad/zur/codebase --collection meine_collection --persist-dir /pfad/zur/chroma_db
```

## 🖥️ Starten des Chroma-Servers

Nach der Indexierung musst du den Chroma-Server starten, um auf die Vektordatenbank zugreifen zu können:

```bash
chroma run --path /pfad/zur/chroma_db --host 0.0.0.0 --port 8000
```

Der Server ist dann unter http://localhost:8000 erreichbar.

## 🤖 Einrichtung von Anything LLM

[Anything LLM](https://anythingllm.com/) ist eine benutzerfreundliche Chat-Oberfläche, die mit deinem Chroma-Index arbeiten kann.

### Installation von Anything LLM

1. Lade Anything LLM von https://anythingllm.com/ herunter
2. Installiere es gemäß der Anleitung
3. Starte Anything LLM

### Konfiguration von Anything LLM

1. Öffne Anything LLM
2. Erstelle einen neuen Workspace oder wähle einen bestehenden
3. Navigiere zu den Workspace-Einstellungen

4. Konfiguriere die Vektordatenbank:
   - Wähle "Chroma" als Vektordatenbank-Typ
   - Server URL: zB `http://localhost:8000`
   - **SEHR WICHTIG**: Collection Name: Der Name deiner Collection (z.B. `meine_collection`) muss IMMER genauso heißen wie der Arbeitsbereich in Anything!

5. Konfiguriere den Embedding-Provider:
   - Wähle "OpenAI" als Embedding-Provider
   - Gib deinen OpenAI API-Schlüssel ein
   - **WICHTIG**: Verwende **denselben** Embedding-Provider wie bei der Indexierung!

6. Konfiguriere das LLM:
   - Wähle einen LLM-Provider (OpenAI, Anthropic, etc.)
   - Wähle ein Modell (GPT-4, Claude 3, etc.)
   - Gib den entsprechenden API-Schlüssel ein

7. Speichere die Einstellungen

## ❓ Fehlerbehebung

### Collection nicht gefunden

Wenn die Fehlermeldung "Collection XYZ does not exist" erscheint:

1. Überprüfe die verfügbaren Collections:
   ```python
   import chromadb
   client = chromadb.HttpClient(host="localhost", port=8000)
   print(client.list_collections())
   ```

2. Stelle sicher, dass der Collection-Name in Anything LLM exakt mit dem tatsächlichen Collection-Namen übereinstimmt (Groß-/Kleinschreibung beachten)

3. Überprüfe ob der Arbeitsbereich genauso heißt wie deine Collection. Anders kann Aynthing LLM nicht auf deinen Collection zugreifen.

### Dimensionsfehler bei Embeddings

Wenn Fehler mit "Embedding dimension X does not match collection dimensionality Y" auftreten:

1. Stelle sicher, dass du in Anything LLM denselben Embedding-Provider verwendest wie bei der Indexierung (hier OpenAI)
2. Überprüfe, ob das korrekte Embedding-Modell ausgewählt ist (OpenAI verwendet 1536 Dimensionen)

### Andere Probleme

- Stelle sicher, dass der Chroma-Server läuft und erreichbar ist und keien Consolen Fehler wirft
- Überprüfe, ob die API-Schlüssel korrekt und gültig sind
- Bei Problemen mit bestehenden Collections, erstelle gegebenenfalls eine neue Collection