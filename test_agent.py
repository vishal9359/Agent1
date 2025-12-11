#!/usr/bin/env python3
"""
Test script for C++ Analysis Agent
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agent import CPPAnalysisAgent
from rich.console import Console

console = Console()


def test_agent():
    """Test the agent with a sample project"""
    
    console.print("[bold cyan]Testing C++ Analysis Agent[/bold cyan]\n")
    
    try:
        # Initialize agent
        console.print("[blue]1. Initializing agent...[/blue]")
        agent = CPPAnalysisAgent("config.yaml")
        console.print("[green]✓ Agent initialized[/green]\n")
        
        # Test configuration
        console.print("[blue]2. Testing configuration...[/blue]")
        config = agent.config_loader.get_ollama_config()
        console.print(f"   LLM Model: {config['llm_model']}")
        console.print(f"   Embedding Model: {config['embedding_model']}")
        console.print(f"   Base URL: {config['base_url']}")
        console.print("[green]✓ Configuration loaded[/green]\n")
        
        # Test LLM connection
        console.print("[blue]3. Testing LLM connection...[/blue]")
        try:
            response = agent.llm.invoke("Say 'Hello'")
            console.print(f"   LLM Response: {response.content[:50]}...")
            console.print("[green]✓ LLM connection working[/green]\n")
        except Exception as e:
            console.print(f"[red]✗ LLM connection failed: {e}[/red]\n")
            console.print("[yellow]Make sure Ollama is running: ollama serve[/yellow]\n")
            return False
        
        # Test embeddings
        console.print("[blue]4. Testing embeddings...[/blue]")
        try:
            test_text = "This is a test"
            embeddings = agent.rag_system.embeddings.embed_query(test_text)
            console.print(f"   Embedding dimension: {len(embeddings)}")
            console.print("[green]✓ Embeddings working[/green]\n")
        except Exception as e:
            console.print(f"[red]✗ Embeddings failed: {e}[/red]\n")
            return False
        
        console.print("[bold green]All tests passed! ✓[/bold green]\n")
        console.print("The agent is ready to use.\n")
        console.print("Try analyzing a project:")
        console.print("  python main.py analyze /path/to/cpp/project\n")
        
        return True
        
    except Exception as e:
        console.print(f"[red]Error during testing: {e}[/red]")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_agent()
    sys.exit(0 if success else 1)

