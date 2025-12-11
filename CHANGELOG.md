# Changelog

All notable changes to the C++ Analysis Agent project.

## [2.0.0] - 2024-12-12

### 🎉 Major Changes

#### PlantUML Diagram Generation
- **BREAKING CHANGE**: Replaced Graphviz with PlantUML for diagram generation
- Diagrams now generated as text-based `.puml` files instead of binary images
- Output directory changed from `flowcharts/` to `diagrams/`

**Benefits:**
- ✅ Text-based diagrams (easy to view over SSH)
- ✅ Lightweight files (no binary images)
- ✅ Editable in any text editor
- ✅ Version control friendly
- ✅ Multiple viewing options (online, VSCode, local tools)
- ✅ Perfect for MobaXterm/SSH users

**Migration:**
- Old: `python main.py flowchart --type class` (doesn't work standalone)
- New: `python main.py analyze /path --flowchart all` (recommended)
- View: `python view_plantuml.py` (generates HTML report)

#### Model Updates
- Default LLM changed from `qwen2.5` to `qwen3-coder:latest`
- Better code-specialized model for C++ analysis

### ✨ Added

- `src/plantuml_generator.py` - PlantUML diagram generator
- `view_plantuml.py` - HTML report generator for diagrams
- `README_PLANTUML.md` - Complete PlantUML usage guide
- `--flowchart` option for analyze command (generate diagrams during analysis)
- HTML report generation with embedded diagram viewers
- Online viewing support (planttext.com, plantuml.com)

### 🔧 Changed

- Updated `config.yaml` - PlantUML settings
- Updated `requirements.txt` - Removed graphviz, pillow
- Updated all documentation for PlantUML
- Improved analyze workflow (always parse, optionally re-index)

### 🐛 Fixed

- **KeyError: 'total_functions'** when using existing vector store
- Separate flowchart command now requires fresh analysis
- Chroma deprecation warning (using `langchain-chroma`)
- LangChain 1.1.3 compatibility (LCEL chains)
- tree-sitter-cpp version (0.23.4)

### 📚 Documentation

- Updated `README.md` - PlantUML instructions
- Updated `QUICK_START.md` - New workflow
- Updated `install.sh` - No Graphviz needed
- Added `README_PLANTUML.md` - Comprehensive guide
- Added `FIXES_SUMMARY.md` - All bug fixes
- Added `LANGCHAIN_1.1.3_COMPATIBILITY.md` - Migration guide

---

## [1.0.0] - 2024-12-11

### 🎉 Initial Release

#### Core Features
- C++ code parsing using tree-sitter
- RAG system with ChromaDB and Ollama embeddings
- Graphviz-based flowchart generation (replaced in 2.0.0)
- LangChain integration with Ollama LLMs
- CLI interface with multiple commands
- Interactive mode

#### Components
- `src/agent.py` - Main agent orchestrator
- `src/cpp_parser.py` - C++ code parser
- `src/rag_system.py` - RAG implementation
- `src/flowchart_generator.py` - Graphviz flowcharts (replaced in 2.0.0)
- `src/config_loader.py` - Configuration management

#### Commands
- `analyze` - Analyze C++ project
- `flowchart` - Generate flowcharts
- `query` - Query codebase
- `search` - Search code
- `stats` - Project statistics
- `interactive` - Interactive mode

#### Documentation
- `README.md` - Main documentation
- `QUICK_START.md` - Quick start guide
- `USAGE_GUIDE.md` - Detailed usage
- `PROJECT_SUMMARY.md` - Architecture overview

---

## Version History

| Version | Date | Major Changes |
|---------|------|---------------|
| 2.0.0 | 2024-12-12 | PlantUML diagrams, bug fixes, LangChain 1.1.3 |
| 1.0.0 | 2024-12-11 | Initial release |

---

## Breaking Changes

### v2.0.0

1. **Diagram Format Changed**
   - Old: PNG/SVG images via Graphviz
   - New: .puml text files via PlantUML
   - Action: Use `view_plantuml.py` to generate HTML reports

2. **Output Directory Changed**
   - Old: `./flowcharts/`
   - New: `./diagrams/`
   - Action: Update any scripts referencing old directory

3. **Flowchart Command Workflow**
   - Old: `python main.py flowchart --type class` (worked standalone)
   - New: Must analyze first or use `--flowchart` option with analyze
   - Action: Use `python main.py analyze /path --flowchart all`

4. **Dependencies Removed**
   - Removed: graphviz, pillow
   - Added: langchain-chroma
   - Action: `pip install -r requirements.txt`

5. **Configuration Keys**
   - Old: `flowchart.output_format: "png"`
   - New: `flowchart.output_format: "puml"`
   - Action: Update config.yaml or use default

---

## Upgrade Guide

### From v1.0.0 to v2.0.0

```bash
# 1. Pull latest code
git pull

# 2. Update dependencies
pip install -r requirements.txt

# 3. Update config (optional)
# Edit config.yaml:
#   flowchart.output_format: "puml"
#   flowchart.output_dir: "./diagrams"

# 4. Use new workflow
python main.py analyze /path/to/project --flowchart all
python view_plantuml.py

# 5. Clean up old files (optional)
rm -rf flowcharts/
rm -rf chroma_db/  # Force re-index
```

---

## Future Plans

### Planned Features
- [ ] Support for more languages (Python, Java, Go)
- [ ] Web UI interface
- [ ] Incremental indexing (only changed files)
- [ ] Call graph analysis with metrics
- [ ] Code quality suggestions
- [ ] Automated documentation generation
- [ ] Git integration (analyze commits/diffs)
- [ ] Multi-project analysis

### Under Consideration
- [ ] C# support
- [ ] Docker containerization
- [ ] REST API
- [ ] Jupyter notebook integration
- [ ] Real-time code analysis
- [ ] IDE plugins

---

## Contributors

- Initial development and PlantUML migration: December 2024

## License

Open Source - See repository for details

---

**For detailed changes, see individual commit messages on GitHub.**

