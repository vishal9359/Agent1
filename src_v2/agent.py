"""
Main Agent - Clean Implementation
"""

from typing import Optional, Dict, Any, List
from pathlib import Path
try:
    from langchain_ollama import ChatOllama
except ImportError:
    from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .ast_parser import ASTParser
from .rag_system import RAGSystem
from .diagram_generator import DiagramGenerator

console = Console()


class CPPAnalysisAgent:
    """AI Agent for analyzing C++ projects"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize agent"""
        console.print(Panel.fit(
            "[bold cyan]C++ Analysis Agent v2[/bold cyan]\n"
            "AST-Based Architecture",
            border_style="cyan"
        ))
        
        # Initialize components
        console.print("[blue]Initializing components...[/blue]")
        
        self.parser = ASTParser(config.get('parsing', {}))
        self.rag_system = RAGSystem(config)
        self.diagram_generator = DiagramGenerator(config.get('flowchart', {}))
        
        # Initialize LLM
        ollama_config = config.get('ollama', {})
        self.llm = ChatOllama(
            base_url=ollama_config.get('base_url', 'http://localhost:11434'),
            model=ollama_config.get('llm_model', 'qwen2.5:latest'),
            temperature=ollama_config.get('temperature', 0.3),
        )
        
        self.qa_chain = None
        
        console.print("[green]✓ Agent initialized[/green]")
    
    def analyze_project(self, project_path: str, force_reindex: bool = False) -> None:
        """Analyze C++ project"""
        console.print(f"\n[bold cyan]Analyzing: {project_path}[/bold cyan]\n")
        
        # Parse project
        console.print("[bold blue]Step 1: Parsing C++ code...[/bold blue]")
        self.parser.parse_project(project_path)
        
        if not self.parser.chunks:
            console.print("[red]No code found. Check project path.[/red]")
            return
        
        # Create vector store
        console.print("\n[bold blue]Step 2: Creating vector store...[/bold blue]")
        chunks = self.parser.get_ast_chunks()
        self.rag_system.create_vectorstore_from_chunks(chunks)
        
        # Setup QA chain
        console.print("\n[bold blue]Step 3: Setting up QA system...[/bold blue]")
        self._setup_qa_chain()
        
        console.print("\n[green]✓ Analysis complete![/green]")
        console.print(f"[cyan]Found {len(self.parser.get_functions())} functions, {len(self.parser.get_classes())} classes[/cyan]")
    
    def generate_diagrams(
        self,
        diagram_type: str = "function_flow",
        function_name: Optional[str] = None,
        module_path: Optional[str] = None
    ) -> List[str]:
        """Generate diagrams"""
        output_paths = []
        
        if diagram_type == "function_flow":
            if function_name:
                # Generate for specific function
                funcs = [f for f in self.parser.get_functions() if f.name == function_name]
                if funcs:
                    func = funcs[0]
                    content = self.parser.files_content.get(func.file_path, "")
                    path = self.diagram_generator.generate_function_flow(func, content)
                    output_paths.append(path)
                else:
                    console.print(f"[red]Function '{function_name}' not found[/red]")
            else:
                # Generate for all functions with bodies
                funcs = [f for f in self.parser.get_functions() if f.body_node]
                console.print(f"[blue]Generating flows for {len(funcs)} functions...[/blue]")
                for func in funcs[:20]:  # Limit to 20
                    try:
                        content = self.parser.files_content.get(func.file_path, "")
                        path = self.diagram_generator.generate_function_flow(func, content)
                        output_paths.append(path)
                    except Exception as e:
                        console.print(f"[yellow]Warning: {func.name}: {e}[/yellow]")
        
        elif diagram_type == "module":
            chunks = self.parser.get_ast_chunks()
            if module_path:
                # Filter by module path
                chunks = [c for c in chunks if module_path in c.file_path]
            path = self.diagram_generator.generate_module_diagram(chunks)
            output_paths.append(path)
        
        return output_paths
    
    def query(self, question: str) -> str:
        """Query the codebase"""
        if not self.qa_chain:
            console.print("[red]QA chain not initialized. Run analyze_project first.[/red]")
            return ""
        
        console.print(f"\n[cyan]Question:[/cyan] {question}")
        
        try:
            answer = self.qa_chain.invoke(question)
            console.print(f"[green]Answer:[/green] {answer}\n")
            return answer
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            return ""
    
    def list_functions(self, limit: int = 20) -> None:
        """List all functions"""
        funcs = self.parser.get_functions()
        
        table = Table(title="Functions")
        table.add_column("Name", style="cyan")
        table.add_column("Return", style="green")
        table.add_column("File", style="blue")
        table.add_column("Line", style="yellow")
        
        for func in funcs[:limit]:
            file_name = Path(func.file_path).name
            table.add_row(
                func.name,
                func.return_type,
                file_name,
                str(func.line_number)
            )
        
        console.print(table)
    
    def _setup_qa_chain(self) -> None:
        """Setup QA chain"""
        prompt_template = """You are an expert C++ code analyst. Use the following code context to answer the question.

Context:
{context}

Question: {question}

Provide a detailed and technical answer based on the code context.

Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        retriever = self.rag_system.get_retriever(k=5)
        
        self.qa_chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough()
            }
            | PROMPT
            | self.llm
            | StrOutputParser()
        )
        
        console.print("[green]✓ QA chain ready[/green]")
