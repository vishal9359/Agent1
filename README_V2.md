# Agent1 v2 - Clean AST-Based Implementation

## Overview

This is a **completely rewritten** version of Agent1 with a clean, AST-based architecture. It's designed to work reliably with ANY C++ project.

## Key Improvements

1. **AST-Based Chunking**: Uses tree-sitter AST nodes directly for semantic chunking
2. **Clean Architecture**: Clear separation of concerns
3. **Robust PlantUML**: Generates diagrams from AST structure, not text manipulation
4. **Better Error Handling**: Graceful failures, always produces valid output

## Architecture

```
AST Parser → AST Chunks → RAG System (ChromaDB)
                      ↓
              Diagram Generator (PlantUML)
```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Make sure Ollama is running
ollama serve
```

## Usage

### 1. Analyze Project

```bash
python main_v2.py analyze /path/to/poseidonos/src/event
```

### 2. Generate Diagrams

```bash
# All function flows
python main_v2.py diagram --type function_flow

# Specific function
python main_v2.py diagram --type function_flow --function ProcessEvent

# Module structure
python main_v2.py diagram --type module
```

### 3. Query Codebase

```bash
python main_v2.py query "How does event processing work?"
```

### 4. List Functions

```bash
python main_v2.py list-functions --limit 30
```

## Viewing Diagrams

1. Open generated `.puml` files in `diagrams/` directory
2. Visit: http://www.plantuml.com/plantuml/uml/
3. Copy/paste the PlantUML content
4. View the rendered diagram

## Configuration

Edit `config.yaml`:

```yaml
ollama:
  base_url: "http://localhost:11434"
  llm_model: "qwen2.5:latest"
  embedding_model: "jina/jina-embeddings-v2-base-en"

vectordb:
  persist_directory: "./chroma_db"
  collection_name: "cpp_codebase"

parsing:
  file_extensions: [".cpp", ".h", ".hpp"]
  ignore_dirs: ["build", "bin", ".git"]

flowchart:
  output_dir: "./diagrams"
  max_depth: 5
```

## Differences from v1

- **Cleaner code**: Less complexity, easier to maintain
- **AST-based**: Better semantic understanding
- **More reliable**: Better error handling
- **Simpler PlantUML**: Direct AST conversion, less sanitization needed

## Status

✅ **Ready for testing with PoseidonOS**
