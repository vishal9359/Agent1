# C++ Project Analysis Agent

An AI-powered agent for analyzing C++ projects using LangChain, Ollama, and ChromaDB. This agent can understand complete C++ projects, perform RAG (Retrieval-Augmented Generation) queries, and generate flowchart diagrams.

## Features

- 🔍 **Code Understanding**: Parse and understand complete C++ projects using tree-sitter
- 🤖 **RAG System**: Query codebase using natural language with ChromaDB vector database
- 📊 **Flowchart Generation**: Generate function call graphs, class diagrams, and module structures
- 🔓 **Open Source**: Uses only open-source LLM models via Ollama
- 🎯 **Modular Design**: Works with any C++ project

## Requirements

- **OS**: Ubuntu Server 24.04 (or compatible Linux)
- **Python**: 3.11.14
- **Ollama**: Installed with models (qwen2.5, jina/jina-embeddings-v2-base-en, etc.)
- **Graphviz**: For flowchart generation

### Pre-installed Python Packages
- langchain-classic 1.0.0
- langchain-community 0.4.1
- langchain-core 1.1.3
- langchain-text-splitters 1.0.0
- tree-sitter 0.25.2

## Installation

### 1. Install Graphviz (for flowcharts)

```bash
sudo apt update
sudo apt install graphviz
```

### 2. Install Python Dependencies

```bash
cd Agent1
pip install -r requirements.txt
```

### 3. Verify Ollama Models

Make sure you have the required models pulled:

```bash
ollama list
```

You should see at least:
- qwen2.5 (or another LLM model)
- jina/jina-embeddings-v2-base-en (or another embedding model)

If not, pull them:

```bash
ollama pull qwen2.5
ollama pull jina/jina-embeddings-v2-base-en
```

### 4. Configure the Agent

Edit `config.yaml` to match your setup:

```yaml
ollama:
  base_url: "http://localhost:11434"
  llm_model: "qwen2.5"
  embedding_model: "jina/jina-embeddings-v2-base-en"
```

## Usage

### Analyze a C++ Project

```bash
# First time analysis (will parse and index the project)
python main.py analyze /path/to/cpp/project

# Example with your project
python main.py analyze D:/git-project/poseidonos

# Force re-indexing
python main.py analyze /path/to/cpp/project --force
```

### Generate Flowcharts

```bash
# Function call graph
python main.py flowchart --type function_call

# Class diagram
python main.py flowchart --type class

# Module structure
python main.py flowchart --type module

# Function call graph from specific entry point
python main.py flowchart --type function_call --entry-point main
```

Flowcharts are saved in the `./flowcharts/` directory as PNG files by default.

### Query the Codebase

```bash
# Ask questions about the code
python main.py query "How does the main function work?"
python main.py query "What are the main classes in this project?"
python main.py query "Explain the memory management approach"
```

### Search for Code

```bash
# Search for specific code patterns
python main.py search "memory allocation"
python main.py search "error handling"
python main.py search "class definition" --limit 10
```

### View Project Statistics

```bash
python main.py stats
```

### Interactive Mode

```bash
python main.py interactive
```

In interactive mode, you can use these commands:
- `query <question>` - Ask questions
- `search <query>` - Search code
- `flowchart <type>` - Generate flowcharts
- `stats` - Show statistics
- `help` - Show help
- `exit` - Exit

## Project Structure

```
Agent1/
├── main.py                    # Main entry point
├── config.yaml                # Configuration file
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── src/
│   ├── __init__.py
│   ├── agent.py              # Main agent orchestrator
│   ├── config_loader.py      # Configuration management
│   ├── cpp_parser.py         # C++ code parser (tree-sitter)
│   ├── rag_system.py         # RAG system (ChromaDB)
│   └── flowchart_generator.py # Flowchart generation (graphviz)
├── chroma_db/                # Vector database (created automatically)
└── flowcharts/               # Generated flowcharts (created automatically)
```

## Configuration

### config.yaml

```yaml
# Ollama Settings
ollama:
  base_url: "http://localhost:11434"
  llm_model: "qwen2.5"
  embedding_model: "jina/jina-embeddings-v2-base-en"
  temperature: 0.3
  max_tokens: 4096

# Vector Database
vectordb:
  persist_directory: "./chroma_db"
  collection_name: "cpp_codebase"
  chunk_size: 1000
  chunk_overlap: 200

# Code Parsing
parsing:
  file_extensions: [".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx"]
  max_file_size_mb: 10
  ignore_dirs: ["build", "bin", "obj", ".git", "node_modules", "test", "tests"]

# Flowchart Settings
flowchart:
  output_format: "png"
  output_dir: "./flowcharts"
  max_depth: 5
  include_comments: true
```

## Example Workflow

```bash
# 1. Analyze your C++ project
python main.py analyze D:/git-project/poseidonos

# 2. Generate function call graph
python main.py flowchart --type function_call

# 3. Generate class diagram
python main.py flowchart --type class

# 4. Ask questions
python main.py query "What is the main architecture of this project?"
python main.py query "How does the storage layer work?"

# 5. Search for specific code
python main.py search "buffer management"

# 6. View statistics
python main.py stats
```

## Supported Ollama Models

The agent works with any Ollama model. Recommended models:

**LLM Models** (for analysis):
- qwen2.5 (recommended)
- llama3.2
- gemma:7b
- mistral

**Embedding Models** (for RAG):
- jina/jina-embeddings-v2-base-en (recommended)
- nomic-embed-text
- mxbai-embed-large

To use a different model, update `config.yaml`:

```yaml
ollama:
  llm_model: "llama3.2"
  embedding_model: "nomic-embed-text"
```

## Troubleshooting

### Issue: "Ollama not responding"

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve
```

### Issue: "Model not found"

```bash
# Pull the model
ollama pull qwen2.5
ollama pull jina/jina-embeddings-v2-base-en
```

### Issue: "Graphviz not found"

```bash
# Install graphviz
sudo apt install graphviz
```

### Issue: "Out of memory"

- Reduce `chunk_size` in `config.yaml`
- Use a smaller model (e.g., gemma:2b)
- Process smaller portions of the codebase

## Advanced Usage

### Analyzing Specific Modules

If you want to analyze specific modules instead of the entire project, you can:

1. Create a custom `config.yaml` with specific paths
2. Or copy the module to a separate directory and analyze it

### Custom Flowcharts

To generate flowcharts for specific functions:

```bash
python main.py flowchart --type function_call --entry-point YourFunctionName
```

### Batch Processing

Create a script to analyze multiple projects:

```bash
#!/bin/bash
for project in /path/to/projects/*; do
    python main.py analyze "$project"
    python main.py flowchart --type class --output "${project##*/}_classes"
done
```

## Performance Tips

1. **First Run**: The first analysis takes time as it parses all files and creates embeddings
2. **Subsequent Runs**: Much faster as the vector database is cached
3. **Large Projects**: Consider analyzing specific modules separately
4. **Memory**: Monitor memory usage with large codebases

## Contributing

This agent is designed to be modular and extensible. You can:

- Add new code parsers for other languages
- Implement additional flowchart types
- Extend the RAG system with more features
- Add custom analysis tools

## License

This project uses open-source components:
- LangChain (MIT License)
- Ollama (MIT License)
- ChromaDB (Apache 2.0)
- tree-sitter (MIT License)
- Graphviz (EPL)

## Support

For issues or questions:
1. Check the configuration in `config.yaml`
2. Verify Ollama is running and models are available
3. Check the console output for detailed error messages

---

**Note**: This agent is designed for Ubuntu Server 24.04 with your specific Python environment. Make sure all dependencies are installed correctly.

