"""
RAG System using ChromaDB with AST-based chunks
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
from langchain_core.documents import Document
from rich.console import Console
from .ast_parser import ASTChunk

# Try different import paths for compatibility
try:
    from langchain_ollama import OllamaEmbeddings
except ImportError:
    try:
        from langchain_community.embeddings import OllamaEmbeddings
    except ImportError:
        from langchain.embeddings import OllamaEmbeddings

try:
    from langchain_chroma import Chroma
except ImportError:
    try:
        from langchain_community.vectorstores import Chroma
    except ImportError:
        from langchain.vectorstores import Chroma

console = Console()


class RAGSystem:
    """RAG system using ChromaDB and Ollama embeddings"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.ollama_config = config.get('ollama', {})
        self.vectordb_config = config.get('vectordb', {})
        
        # Initialize embeddings
        console.print("[blue]Initializing embeddings...[/blue]")
        self.embeddings = OllamaEmbeddings(
            model=self.ollama_config.get('embedding_model', 'jina/jina-embeddings-v2-base-en'),
            base_url=self.ollama_config.get('base_url', 'http://localhost:11434')
        )
        
        # Initialize ChromaDB
        persist_dir = self.vectordb_config.get('persist_directory', './chroma_db')
        collection_name = self.vectordb_config.get('collection_name', 'cpp_codebase')
        
        self.vectorstore: Optional[Chroma] = None
        self.persist_directory = Path(persist_dir)
        self.collection_name = collection_name
        
        console.print("[green]✓ RAG system initialized[/green]")
    
    def create_vectorstore_from_chunks(self, chunks: List[ASTChunk]) -> None:
        """Create vector store from AST chunks"""
        console.print(f"[blue]Creating vector store from {len(chunks)} chunks...[/blue]")
        
        # Convert chunks to LangChain documents
        documents = []
        for chunk in chunks:
            doc = Document(
                page_content=chunk.content,
                metadata={
                    'chunk_type': chunk.chunk_type,
                    'name': chunk.name,
                    'file_path': chunk.file_path,
                    'line_start': chunk.line_start,
                    'line_end': chunk.line_end,
                    **chunk.metadata
                }
            )
            documents.append(doc)
        
        # Create persist directory
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Create vectorstore
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name=self.collection_name,
            persist_directory=str(self.persist_directory)
        )
        
        # Persist
        self.vectorstore.persist()
        
        console.print(f"[green]✓ Vector store created with {len(chunks)} chunks[/green]")
    
    def load_vectorstore(self) -> bool:
        """Load existing vectorstore"""
        try:
            if not self.persist_directory.exists():
                return False
            
            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=str(self.persist_directory)
            )
            return True
        except Exception:
            return False
    
    def query(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Query the vector store"""
        if not self.vectorstore:
            return []
        
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                'content': doc.page_content,
                'metadata': doc.metadata,
                'score': score
            })
        
        return formatted_results
    
    def get_retriever(self, k: int = 5):
        """Get LangChain retriever"""
        if not self.vectorstore:
            raise ValueError("Vectorstore not initialized. Run create_vectorstore_from_chunks first.")
        return self.vectorstore.as_retriever(search_kwargs={"k": k})
