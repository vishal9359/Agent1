# Quick Start Guide

Get started with the C++ Analysis Agent in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:

- ✅ Ubuntu Server 24.04
- ✅ Python 3.11.14
- ✅ Ollama installed and running
- ✅ Required Ollama models pulled

## Step-by-Step Setup

### 1. Install Dependencies (2 minutes)

```bash
cd Agent1
chmod +x install.sh
./install.sh
```

This will:
- Install Graphviz
- Install Python packages
- Verify your environment

### 2. Verify Setup (1 minute)

```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it in another terminal:
ollama serve

# Check models are available
ollama list

# Should show:
# - qwen2.5 (or similar)
# - jina/jina-embeddings-v2-base-en (or similar)
```

### 3. Test the Agent (1 minute)

```bash
python test_agent.py
```

If all tests pass ✓, you're ready to go!

### 4. Analyze Your First Project (1 minute)

```bash
# Analyze your C++ project
python main.py analyze D:/git-project/poseidonos

# Or use a sample project
python main.py analyze /path/to/any/cpp/project
```

## Quick Commands

```bash
# Generate PlantUML diagrams
python main.py analyze /path/to/project --flowchart all

# View diagrams
python view_plantuml.py

# Ask questions
python main.py query "What is the main architecture?"

# Search code
python main.py search "memory management"

# View statistics
python main.py stats

# Interactive mode
python main.py interactive
```

## Example Session

```bash
# 1. Analyze project
python main.py analyze D:/git-project/poseidonos

# Output:
# Found 450 C++ files to parse
# Parsed 1234 functions and 156 classes
# Creating vector store with 1390 chunks...
# ✓ Project analysis complete!

# 2. View diagrams
python view_plantuml.py

# Output:
# ✓ HTML report generated: diagrams_report.html
# Download via MobaXterm and open in browser!

# 3. Ask a question
python main.py query "What are the main storage classes?"

# Output:
# Answer: The project has several storage-related classes including
# StorageManager, BufferManager, and BlockDevice...

# 4. Interactive exploration
python main.py interactive

# First analyze, then:
# > query How does initialization work?
# > stats
# > exit

# Note: For diagrams, use: python main.py analyze /path --flowchart all
```

## Common Issues

### "Ollama not responding"
```bash
# Start Ollama in another terminal
ollama serve
```

### "Model not found"
```bash
# Pull required models
ollama pull qwen2.5
ollama pull jina/jina-embeddings-v2-base-en
```

### "Cannot view diagrams"
```bash
# Generate HTML report
python view_plantuml.py
# Download diagrams_report.html and open in browser
```

## What's Next?

1. **Read the full guide**: [USAGE_GUIDE.md](USAGE_GUIDE.md)
2. **Customize settings**: Edit `config.yaml`
3. **Try different models**: Change models in config
4. **Generate documentation**: Create flowcharts and summaries

## Configuration (Optional)

Edit `config.yaml` to customize:

```yaml
ollama:
  llm_model: "qwen3-coder:latest"   # Best for C++ code analysis
  embedding_model: "jina/jina-embeddings-v2-base-en"

parsing:
  ignore_dirs: ["build", "test"]    # Add more dirs to ignore
  
flowchart:
  output_format: "puml"             # PlantUML text format
  output_dir: "./diagrams"          # Output directory
  max_depth: 5                      # Adjust call graph depth
```

## Need Help?

1. Run tests: `python test_agent.py`
2. Check logs for detailed errors
3. Verify Ollama: `ollama list`
4. See README.md for detailed documentation

---

**You're all set!** Start exploring your C++ projects with AI. 🚀

