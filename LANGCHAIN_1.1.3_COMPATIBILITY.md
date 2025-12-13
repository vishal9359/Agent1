# LangChain 1.1.3 Compatibility Guide

This document explains the changes made to ensure compatibility with LangChain 1.1.3 and langchain-core 1.1.3.

## Import Changes

### Old (Pre-1.0) vs New (1.1.3+)

| Old Import | New Import | File |
|------------|------------|------|
| `from langchain.chains import RetrievalQA` | Use LCEL chains instead | agent.py |
| `from langchain.prompts import PromptTemplate` | `from langchain_core.prompts import PromptTemplate` | agent.py |
| `from langchain.text_splitter import RecursiveCharacterTextSplitter` | `from langchain_text_splitters import RecursiveCharacterTextSplitter` | rag_system.py |
| `from langchain.docstore.document import Document` | `from langchain_core.documents import Document` | rag_system.py |

## API Changes

### 1. RetrievalQA Chain → LCEL (LangChain Expression Language)

**Old way (deprecated):**
```python
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=False
)

result = qa_chain.invoke({"query": question})
answer = result['result']
```

**New way (LCEL):**
```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

qa_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

answer = qa_chain.invoke(question)  # Returns string directly
```

## Required Packages

### Minimum Requirements

```
langchain>=1.0.0
langchain-core>=1.1.3
langchain-community>=0.4.1
langchain-text-splitters>=1.0.0
langchain-ollama>=0.3.0
```

### Installation

```bash
pip install langchain
pip install langchain-ollama
pip install langchain-text-splitters  # If not auto-installed
```

## Module Structure in LangChain 1.1.3

```
langchain/                      # Main package (orchestration)
langchain_core/                 # Core abstractions
  ├── prompts/                  # Prompt templates
  ├── documents/                # Document classes
  ├── runnables/                # LCEL components
  └── output_parsers/           # Output parsers
langchain_community/            # Community integrations
  └── vectorstores/             # Vector stores (Chroma, etc.)
langchain_text_splitters/       # Text splitting utilities
langchain_ollama/               # Ollama integration
```

## Backward Compatibility

### What Changed
- ✅ Module reorganization (moved to `langchain_core`, `langchain_community`, etc.)
- ✅ Deprecated `langchain.chains` in favor of LCEL
- ✅ Text splitters moved to separate package
- ✅ Documents moved to `langchain_core`

### What Stayed the Same
- ✅ Core concepts (LLMs, prompts, chains)
- ✅ Vector store interfaces
- ✅ Retriever patterns
- ✅ Document structure

## Testing Compatibility

Run the verification script:

```bash
python3 verify_installation.py
```

This will check:
1. ✓ All required packages installed
2. ✓ Correct module imports
3. ✓ LangChain API compatibility
4. ✓ Ollama connection
5. ✓ All agent modules loadable

## Troubleshooting

### Error: "No module named 'langchain.chains'"

**Solution:** This is expected in LangChain 1.1.3. The code now uses LCEL chains instead.

### Error: "No module named 'langchain.text_splitter'"

**Solution:** 
```bash
pip install langchain-text-splitters
```

### Error: "No module named 'langchain.docstore'"

**Solution:** Import from `langchain_core.documents` instead.

### Error: "Cannot import RetrievalQA"

**Solution:** The code now uses LCEL. Pull the latest version:
```bash
git pull
```

## Migration Checklist

If you're updating from an older version:

- [ ] Install langchain 1.0+
- [ ] Install langchain-text-splitters
- [ ] Update imports in custom code
- [ ] Replace RetrievalQA with LCEL chains
- [ ] Test with `verify_installation.py`

## Benefits of LangChain 1.1.3

1. **More Modular** - Packages separated by concern
2. **Better Performance** - LCEL is faster
3. **More Flexible** - Easier to customize chains
4. **Better Type Hints** - Improved IDE support
5. **Cleaner API** - More consistent interfaces

## References

- [LangChain 1.0 Migration Guide](https://python.langchain.com/docs/versions/v0_2/)
- [LCEL Documentation](https://python.langchain.com/docs/expression_language/)
- [LangChain API Reference](https://api.python.langchain.com/)

---

**Last Updated:** December 2024
**LangChain Version:** 1.1.3
**Agent Version:** 1.0.0




