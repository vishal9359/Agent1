# Usage Guide - C++ Analysis Agent

This guide provides detailed examples and use cases for the C++ Analysis Agent.

## Table of Contents
- [Getting Started](#getting-started)
- [Analyzing Projects](#analyzing-projects)
- [Generating Flowcharts](#generating-flowcharts)
- [Querying Codebase](#querying-codebase)
- [Advanced Features](#advanced-features)

## Getting Started

### 1. First Time Setup

```bash
# Navigate to Agent1 directory
cd Agent1

# Run installation script
chmod +x install.sh
./install.sh

# Verify Ollama is running
curl http://localhost:11434/api/tags
```

### 2. Configuration

Edit `config.yaml` to customize:

```yaml
ollama:
  llm_model: "qwen2.5"  # Change to your preferred model
  embedding_model: "jina/jina-embeddings-v2-base-en"
```

## Analyzing Projects

### Basic Analysis

```bash
# Analyze a C++ project
python main.py analyze /path/to/project

# Example: Analyze PoseidonOS
python main.py analyze D:/git-project/poseidonos
```

**What happens during analysis:**
1. Scans all C++ files (.cpp, .h, .hpp, etc.)
2. Parses code using tree-sitter
3. Extracts functions, classes, and relationships
4. Creates embeddings for RAG
5. Stores in ChromaDB vector database

### Force Re-indexing

If you've made changes to the project:

```bash
python main.py analyze /path/to/project --force
```

### Analyzing Specific Modules

To analyze just a specific module:

```bash
# Option 1: Analyze subdirectory
python main.py analyze /path/to/project/src/module_name

# Option 2: Create custom config
cp config.yaml config_module.yaml
# Edit config_module.yaml to adjust ignore_dirs
python main.py analyze /path/to/project --config config_module.yaml
```

## Generating Flowcharts

### Function Call Graph

Shows how functions call each other:

```bash
# Full function call graph
python main.py flowchart --type function_call

# From specific entry point (e.g., main function)
python main.py flowchart --type function_call --entry-point main

# With custom output name
python main.py flowchart --type function_call --output my_analysis
```

**Output:** `flowcharts/function_call_graph.png`

### Class Diagram

Shows class relationships and inheritance:

```bash
python main.py flowchart --type class
```

**Output:** `flowcharts/class_diagram.png`

Shows:
- Class names
- Methods (up to 5 per class)
- Inheritance relationships

### Module Structure

Shows directory and file organization:

```bash
python main.py flowchart --type module
```

**Output:** `flowcharts/module_structure.png`

### Customizing Flowcharts

Edit `config.yaml`:

```yaml
flowchart:
  output_format: "svg"  # or "pdf", "png"
  max_depth: 10         # Maximum call depth
  output_dir: "./my_flowcharts"
```

## Querying Codebase

### Basic Queries

```bash
# Architecture questions
python main.py query "What is the overall architecture?"
python main.py query "What design patterns are used?"

# Specific functionality
python main.py query "How does memory allocation work?"
python main.py query "Explain the error handling approach"

# Code understanding
python main.py query "What does the Storage class do?"
python main.py query "How are buffers managed?"
```

### Complex Queries

```bash
# Multi-part questions
python main.py query "What are the main components and how do they interact?"

# Performance analysis
python main.py query "Are there any potential performance bottlenecks?"

# Code quality
python main.py query "What are the dependencies between modules?"
```

### Search Code

Direct code search (not AI-based):

```bash
# Search for specific patterns
python main.py search "memory allocation"
python main.py search "mutex lock"
python main.py search "error handling"

# Limit results
python main.py search "class definition" --limit 10
```

## Advanced Features

### Interactive Mode

For exploratory analysis:

```bash
python main.py interactive
```

In interactive mode:
```
> query What is the main entry point?
> search buffer management
> flowchart function_call
> stats
> help
> exit
```

### Project Statistics

Get overview statistics:

```bash
python main.py stats
```

**Output:**
- Total functions
- Total classes
- Methods per class
- Files analyzed
- Code distribution

### Batch Analysis

Analyze multiple projects:

```bash
#!/bin/bash
# analyze_all.sh

projects=(
    "/path/to/project1"
    "/path/to/project2"
    "/path/to/project3"
)

for project in "${projects[@]}"; do
    echo "Analyzing $project..."
    python main.py analyze "$project" --force
    
    # Generate flowcharts
    python main.py flowchart --type function_call --output "${project##*/}_funcs"
    python main.py flowchart --type class --output "${project##*/}_classes"
    
    # Export stats
    python main.py stats > "${project##*/}_stats.txt"
done
```

## Real-World Use Cases

### Use Case 1: Understanding New Codebase

```bash
# Step 1: Analyze
python main.py analyze /path/to/new/project

# Step 2: Get overview
python main.py stats
python main.py query "What is the main purpose of this project?"

# Step 3: Understand structure
python main.py flowchart --type module
python main.py flowchart --type class

# Step 4: Deep dive
python main.py query "What are the core components?"
python main.py search "main functionality"
```

### Use Case 2: Code Review

```bash
# Analyze the code
python main.py analyze /path/to/code

# Check architecture
python main.py query "Are there any architectural issues?"
python main.py query "How is separation of concerns handled?"

# Check specific aspects
python main.py query "Are there memory leaks?"
python main.py query "Is error handling consistent?"
```

### Use Case 3: Documentation

```bash
# Generate all diagrams
python main.py flowchart --type function_call --output docs_funcs
python main.py flowchart --type class --output docs_classes
python main.py flowchart --type module --output docs_modules

# Extract information
python main.py stats > project_stats.txt
python main.py query "Summarize each major component" > components.txt
```

### Use Case 4: Refactoring Planning

```bash
# Understand current structure
python main.py analyze /path/to/project
python main.py flowchart --type function_call --entry-point target_function

# Identify dependencies
python main.py query "What depends on the TargetClass?"
python main.py query "What are all the callers of this function?"

# Plan changes
python main.py search "TargetClass" --limit 20
```

## Tips and Best Practices

### Performance Optimization

1. **For Large Projects:**
   - Analyze incrementally (module by module)
   - Increase `chunk_size` in config for faster indexing
   - Use specific entry points for flowcharts

2. **Memory Management:**
   - Reduce `max_file_size_mb` if running out of memory
   - Close unused applications
   - Use lighter models (gemma:2b instead of gemma:7b)

### Query Optimization

1. **Be Specific:**
   - ✗ "Tell me about this code"
   - ✓ "How does the Storage class handle write operations?"

2. **Break Down Complex Questions:**
   - Instead of: "How does everything work?"
   - Use: Multiple specific queries about components

3. **Use Context:**
   - Reference specific classes/functions in queries
   - Use code search first to find relevant parts

### Workflow Recommendations

1. **Initial Analysis:**
   ```bash
   python main.py analyze /path/to/project
   python main.py stats
   python main.py flowchart --type module
   ```

2. **Detailed Exploration:**
   ```bash
   python main.py interactive
   > query What are the main components?
   > flowchart class
   > search [component name]
   ```

3. **Documentation Generation:**
   ```bash
   # Generate all artifacts
   ./generate_docs.sh
   ```

## Troubleshooting Common Issues

### Issue: Slow Analysis

**Solution:**
- Reduce project size by excluding test directories
- Adjust `ignore_dirs` in config.yaml
- Use faster model (qwen2.5 is good balance)

### Issue: Poor Query Results

**Solution:**
- Ensure project is fully analyzed
- Try re-indexing with --force
- Be more specific in queries
- Check if vector database has data

### Issue: Flowchart Too Complex

**Solution:**
- Use entry points to limit scope
- Reduce `max_depth` in config
- Generate multiple focused flowcharts

### Issue: Out of Memory

**Solution:**
- Analyze smaller portions
- Reduce `chunk_size`
- Use smaller embedding model
- Close other applications

## Next Steps

1. **Explore Your Project:**
   ```bash
   python main.py interactive
   ```

2. **Generate Documentation:**
   - Create flowcharts
   - Export statistics
   - Query for summaries

3. **Customize:**
   - Modify config.yaml for your needs
   - Experiment with different models
   - Adjust parsing settings

For more details, see [README.md](README.md)

