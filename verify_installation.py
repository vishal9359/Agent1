#!/usr/bin/env python3
"""
Comprehensive installation verification script
Tests all imports and dependencies for LangChain 1.1.3 compatibility
"""

import sys
from pathlib import Path

print("=" * 70)
print("C++ Analysis Agent - Installation Verification")
print("=" * 70)
print()

# Track errors
errors = []
warnings = []

# 1. Check Python version
print("1. Checking Python version...")
if sys.version_info >= (3, 11):
    print(f"   ✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
else:
    errors.append(f"Python 3.11+ required, found {sys.version_info.major}.{sys.version_info.minor}")
    print(f"   ✗ Python {sys.version_info.major}.{sys.version_info.minor} (3.11+ required)")

# 2. Check core imports
print("\n2. Checking core imports...")
try:
    import yaml
    print("   ✓ pyyaml")
except ImportError as e:
    errors.append(f"pyyaml: {e}")
    print("   ✗ pyyaml")

try:
    from rich.console import Console
    print("   ✓ rich")
except ImportError as e:
    errors.append(f"rich: {e}")
    print("   ✗ rich")

try:
    from dotenv import load_dotenv
    print("   ✓ python-dotenv")
except ImportError as e:
    errors.append(f"python-dotenv: {e}")
    print("   ✗ python-dotenv")

# 3. Check LangChain packages
print("\n3. Checking LangChain packages...")
try:
    import langchain
    version = getattr(langchain, '__version__', 'unknown')
    print(f"   ✓ langchain ({version})")
except ImportError as e:
    errors.append(f"langchain: {e}")
    print("   ✗ langchain (REQUIRED)")

try:
    import langchain_core
    version = getattr(langchain_core, '__version__', 'unknown')
    print(f"   ✓ langchain-core ({version})")
except ImportError as e:
    errors.append(f"langchain-core: {e}")
    print("   ✗ langchain-core")

try:
    import langchain_community
    version = getattr(langchain_community, '__version__', 'unknown')
    print(f"   ✓ langchain-community ({version})")
except ImportError as e:
    errors.append(f"langchain-community: {e}")
    print("   ✗ langchain-community")

try:
    import langchain_text_splitters
    print("   ✓ langchain-text-splitters")
except ImportError as e:
    errors.append(f"langchain-text-splitters: {e}")
    print("   ✗ langchain-text-splitters")

try:
    import langchain_ollama
    print("   ✓ langchain-ollama")
except ImportError as e:
    errors.append(f"langchain-ollama: {e}")
    print("   ✗ langchain-ollama (REQUIRED)")

# 4. Check specific LangChain imports
print("\n4. Checking LangChain module structure...")
try:
    from langchain_core.prompts import PromptTemplate
    print("   ✓ langchain_core.prompts")
except ImportError as e:
    errors.append(f"langchain_core.prompts: {e}")
    print("   ✗ langchain_core.prompts")

try:
    from langchain_core.documents import Document
    print("   ✓ langchain_core.documents")
except ImportError as e:
    errors.append(f"langchain_core.documents: {e}")
    print("   ✗ langchain_core.documents")

try:
    from langchain_core.runnables import RunnablePassthrough
    print("   ✓ langchain_core.runnables")
except ImportError as e:
    errors.append(f"langchain_core.runnables: {e}")
    print("   ✗ langchain_core.runnables")

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    print("   ✓ langchain_text_splitters.RecursiveCharacterTextSplitter")
except ImportError as e:
    errors.append(f"RecursiveCharacterTextSplitter: {e}")
    print("   ✗ langchain_text_splitters.RecursiveCharacterTextSplitter")

# 5. Check ChromaDB
print("\n5. Checking vector database...")
try:
    import chromadb
    version = getattr(chromadb, '__version__', 'unknown')
    print(f"   ✓ chromadb ({version})")
except ImportError as e:
    errors.append(f"chromadb: {e}")
    print("   ✗ chromadb (REQUIRED)")

try:
    from langchain_chroma import Chroma
    print("   ✓ langchain-chroma (Chroma vectorstore)")
except ImportError as e:
    errors.append(f"langchain-chroma: {e}")
    print("   ✗ langchain-chroma (REQUIRED)")
    print("      Install with: pip install langchain-chroma")

# 6. Check tree-sitter
print("\n6. Checking code parser...")
try:
    import tree_sitter
    version = getattr(tree_sitter, '__version__', 'unknown')
    print(f"   ✓ tree-sitter ({version})")
except ImportError as e:
    errors.append(f"tree-sitter: {e}")
    print("   ✗ tree-sitter")

try:
    import tree_sitter_cpp
    print("   ✓ tree-sitter-cpp")
except ImportError as e:
    errors.append(f"tree-sitter-cpp: {e}")
    print("   ✗ tree-sitter-cpp (REQUIRED)")

try:
    from tree_sitter import Language, Parser
    print("   ✓ tree-sitter API")
except ImportError as e:
    errors.append(f"tree-sitter API: {e}")
    print("   ✗ tree-sitter API")

# 7. Check visualization
print("\n7. Checking visualization tools...")
try:
    import graphviz
    version = getattr(graphviz, '__version__', 'unknown')
    print(f"   ✓ graphviz ({version})")
except ImportError as e:
    errors.append(f"graphviz: {e}")
    print("   ✗ graphviz (REQUIRED for flowcharts)")

try:
    from PIL import Image
    import PIL
    version = getattr(PIL, '__version__', 'unknown')
    print(f"   ✓ pillow ({version})")
except ImportError as e:
    warnings.append(f"pillow: {e}")
    print("   ⚠ pillow (optional)")

# 8. Check Ollama integration
print("\n8. Checking Ollama integration...")
try:
    from langchain_ollama import ChatOllama, OllamaEmbeddings
    print("   ✓ ChatOllama")
    print("   ✓ OllamaEmbeddings")
except ImportError as e:
    errors.append(f"Ollama integration: {e}")
    print("   ✗ Ollama integration")

# 9. Test Ollama connection
print("\n9. Testing Ollama connection...")
try:
    import requests
    response = requests.get('http://localhost:11434/api/tags', timeout=2)
    if response.status_code == 200:
        print("   ✓ Ollama server is running")
        data = response.json()
        models = data.get('models', [])
        print(f"   ✓ Found {len(models)} models")
        
        # Check for required models
        model_names = [m.get('name', '') for m in models]
        if any('qwen' in name for name in model_names):
            print("   ✓ Qwen model available")
        else:
            warnings.append("No Qwen model found")
            print("   ⚠ No Qwen model found")
            
        if any('jina' in name or 'embed' in name for name in model_names):
            print("   ✓ Embedding model available")
        else:
            warnings.append("No embedding model found")
            print("   ⚠ No embedding model found")
    else:
        warnings.append("Ollama server not responding properly")
        print("   ⚠ Ollama server not responding properly")
except Exception as e:
    warnings.append(f"Cannot connect to Ollama: {e}")
    print(f"   ⚠ Cannot connect to Ollama: {e}")
    print("   Note: Make sure Ollama is running (ollama serve)")

# 10. Test agent imports
print("\n10. Testing agent modules...")
sys.path.insert(0, str(Path(__file__).parent))

try:
    from src.config_loader import ConfigLoader
    print("   ✓ ConfigLoader")
except ImportError as e:
    errors.append(f"ConfigLoader: {e}")
    print(f"   ✗ ConfigLoader: {e}")

try:
    from src.cpp_parser import CPPCodeParser
    print("   ✓ CPPCodeParser")
except ImportError as e:
    errors.append(f"CPPCodeParser: {e}")
    print(f"   ✗ CPPCodeParser: {e}")

try:
    from src.rag_system import RAGSystem
    print("   ✓ RAGSystem")
except ImportError as e:
    errors.append(f"RAGSystem: {e}")
    print(f"   ✗ RAGSystem: {e}")

try:
    from src.flowchart_generator import FlowchartGenerator
    print("   ✓ FlowchartGenerator")
except ImportError as e:
    errors.append(f"FlowchartGenerator: {e}")
    print(f"   ✗ FlowchartGenerator: {e}")

try:
    from src.agent import CPPAnalysisAgent
    print("   ✓ CPPAnalysisAgent")
except ImportError as e:
    errors.append(f"CPPAnalysisAgent: {e}")
    print(f"   ✗ CPPAnalysisAgent: {e}")

# Summary
print("\n" + "=" * 70)
print("VERIFICATION SUMMARY")
print("=" * 70)

if not errors and not warnings:
    print("✓ ALL CHECKS PASSED!")
    print("\nYour installation is complete and ready to use.")
    print("\nNext steps:")
    print("  1. python3 main.py analyze /path/to/cpp/project")
    print("  2. python3 main.py flowchart --type function_call")
    print("  3. python3 main.py query 'Your question'")
    sys.exit(0)
elif not errors:
    print(f"✓ PASSED with {len(warnings)} warning(s)")
    print("\nWarnings:")
    for w in warnings:
        print(f"  ⚠ {w}")
    print("\nYour installation should work, but some features may be limited.")
    sys.exit(0)
else:
    print(f"✗ FAILED with {len(errors)} error(s)")
    print("\nErrors:")
    for e in errors:
        print(f"  ✗ {e}")
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  ⚠ {w}")
    print("\nPlease fix the errors above before using the agent.")
    print("\nTo install missing packages:")
    print("  pip install -r requirements.txt")
    sys.exit(1)

