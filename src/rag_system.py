"""
RAG System using ChromaDB and Ollama embeddings
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import chromadb
from chromadb.config import Settings
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from rich.console import Console

console = Console()


class RAGSystem:
    """RAG system for C++ code analysis"""
    
    def __init__(self, ollama_config: Dict[str, Any], vectordb_config: Dict[str, Any]):
        """
        Initialize RAG system
        
        Args:
            ollama_config: Ollama configuration
            vectordb_config: Vector database configuration
        """
        self.ollama_config = ollama_config
        self.vectordb_config = vectordb_config
        
        # Initialize embeddings
        console.print("[blue]Initializing embeddings...[/blue]")
        self.embeddings = OllamaEmbeddings(
            base_url=ollama_config['base_url'],
            model=ollama_config['embedding_model']
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=vectordb_config['chunk_size'],
            chunk_overlap=vectordb_config['chunk_overlap'],
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Vector store
        self.vectorstore: Optional[Chroma] = None
        self.persist_directory = Path(vectordb_config['persist_directory'])
        self.collection_name = vectordb_config['collection_name']
        
    def create_vectorstore(self, code_chunks: List[Dict[str, Any]]) -> None:
        """
        Create vector store from code chunks
        
        Args:
            code_chunks: List of code chunks with content and metadata
        """
        console.print(f"[blue]Creating vector store with {len(code_chunks)} chunks...[/blue]")
        
        # Convert to LangChain documents
        documents = []
        for chunk in code_chunks:
            doc = Document(
                page_content=chunk['content'],
                metadata=chunk['metadata']
            )
            documents.append(doc)
        
        # Split documents if needed
        split_docs = self.text_splitter.split_documents(documents)
        console.print(f"[blue]Split into {len(split_docs)} document chunks[/blue]")
        
        # Create persist directory
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=split_docs,
            embedding=self.embeddings,
            collection_name=self.collection_name,
            persist_directory=str(self.persist_directory)
        )
        
        console.print("[green]✓ Vector store created successfully[/green]")
    
    def load_vectorstore(self) -> bool:
        """
        Load existing vector store
        
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            if not self.persist_directory.exists():
                return False
            
            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=str(self.persist_directory)
            )
            
            # Check if collection has documents
            collection = self.vectorstore._collection
            if collection.count() == 0:
                return False
            
            console.print("[green]✓ Vector store loaded successfully[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Error loading vector store: {e}[/red]")
            return False
    
    def query(self, query_text: str, k: int = 5) -> List[Document]:
        """
        Query the vector store
        
        Args:
            query_text: Query text
            k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        if not self.vectorstore:
            raise ValueError("Vector store not initialized. Create or load first.")
        
        results = self.vectorstore.similarity_search(query_text, k=k)
        return results
    
    def query_with_score(self, query_text: str, k: int = 5) -> List[tuple]:
        """
        Query with similarity scores
        
        Args:
            query_text: Query text
            k: Number of results to return
            
        Returns:
            List of (document, score) tuples
        """
        if not self.vectorstore:
            raise ValueError("Vector store not initialized. Create or load first.")
        
        results = self.vectorstore.similarity_search_with_score(query_text, k=k)
        return results
    
    def delete_collection(self) -> None:
        """Delete the vector store collection"""
        try:
            if self.vectorstore:
                self.vectorstore._client.delete_collection(self.collection_name)
                console.print("[yellow]Collection deleted[/yellow]")
        except Exception as e:
            console.print(f"[red]Error deleting collection: {e}[/red]")
    
    def get_retriever(self, k: int = 5):
        """
        Get a retriever for LangChain
        
        Args:
            k: Number of documents to retrieve
            
        Returns:
            LangChain retriever
        """
        if not self.vectorstore:
            raise ValueError("Vector store not initialized. Create or load first.")
        
        return self.vectorstore.as_retriever(search_kwargs={"k": k})

