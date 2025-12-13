# Quick Start Guide - Agent1 v2

## Fresh Start - Clean Implementation

This is a **completely new** implementation with AST-based architecture.

## Installation

```bash
# Make sure you're in Agent1 directory
cd "C:\Users\Vishal shakya\cursor-workspace\Agent1"

# Install dependencies (if not already)
pip install -r requirements.txt

# Verify Ollama is running
ollama list
```

## Usage

### Step 1: Analyze Your C++ Project

```bash
# For PoseidonOS event module
python main_v2.py analyze "D:/git-project/poseidonos/src/event"

# Or any other C++ project
python main_v2.py analyze "/path/to/your/cpp/project"
```

This will:
- Parse all C++ files using tree-sitter
- Extract functions and classes from AST
- Create semantic chunks
- Build ChromaDB vector store

### Step 2: Generate Function Flow Diagrams

```bash
# Generate for all functions
python main_v2.py diagram --type function_flow

# Generate for specific function
python main_v2.py diagram --type function_flow --function ProcessEvent

# Generate module structure
python main_v2.py diagram --type module
```

### Step 3: View Diagrams

1. Open `diagrams/flow_*.puml` files
2. Visit: http://www.plantuml.com/plantuml/uml/
3. Copy/paste the PlantUML content
4. View the rendered diagram

### Step 4: Query the Codebase

```bash
python main_v2.py query "How does event processing work?"
```

### Step 5: List Functions

```bash
python main_v2.py list-functions --limit 30
```

## What's Different in v2?

1. **AST-Based**: Uses tree-sitter AST directly, not text parsing
2. **Cleaner Code**: Simpler, more maintainable
3. **Better Chunking**: Semantic chunks at function/class level
4. **Reliable PlantUML**: Direct AST conversion, minimal sanitization

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "Ollama connection error"
Make sure Ollama is running:
```bash
ollama serve
```

### "No functions found"
Check that your project path is correct and contains C++ files.

## Files Generated

- `chroma_db/` - Vector database
- `diagrams/flow_*.puml` - Function flow diagrams
- `diagrams/module_diagram.puml` - Module structure

## Next Steps

1. Test with PoseidonOS event module
2. Generate diagrams
3. Verify PlantUML renders correctly
4. Report any issues
