# New Agent Architecture - AST-Based Approach

## Design Principles

1. **AST-Based Chunking**: Use tree-sitter AST nodes directly for semantic chunking
2. **Simple PlantUML**: Generate diagrams from AST structure, not text manipulation
3. **Clean Separation**: Parser → Chunker → RAG → Diagram Generator
4. **Robust Error Handling**: Fail gracefully, always produce valid output

## Architecture

```
┌─────────────────┐
│   C++ Parser    │ → AST Nodes
│  (tree-sitter)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AST Chunker    │ → Semantic Chunks (function/class level)
│  (AST-based)    │
└────────┬────────┘
         │
         ├─────────────────┐
         │                 │
         ▼                 ▼
┌─────────────────┐  ┌──────────────┐
│   RAG System    │  │   Diagram    │
│   (ChromaDB)    │  │  Generator   │
│                 │  │  (PlantUML)  │
└─────────────────┘  └──────────────┘
```

## Key Improvements

1. **AST-Based Chunking**: Chunk at function/class boundaries (semantic units)
2. **Direct AST → PlantUML**: Convert AST nodes directly to PlantUML (no text parsing)
3. **Minimal Sanitization**: Only escape what's absolutely necessary
4. **Validation**: Always validate PlantUML before writing
