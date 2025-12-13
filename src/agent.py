"""
Main AI Agent for C++ Project Analysis
"""

from typing import Optional, Dict, Any, List
from pathlib import Path
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .config_loader import ConfigLoader
from .cpp_parser import CPPCodeParser
from .rag_system import RAGSystem
from .plantuml_generator import PlantUMLGenerator

console = Console()


class CPPAnalysisAgent:
    """AI Agent for analyzing C++ projects"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the agent
        
        Args:
            config_path: Path to configuration file
        """
        console.print(Panel.fit(
            "[bold cyan]C++ Analysis Agent[/bold cyan]\n"
            "Powered by LangChain + Ollama + ChromaDB",
            border_style="cyan"
        ))
        
        # Load configuration
        self.config_loader = ConfigLoader(config_path)
        
        # Get configs
        ollama_config = self.config_loader.get_ollama_config()
        vectordb_config = self.config_loader.get_vectordb_config()
        parsing_config = self.config_loader.get_parsing_config()
        flowchart_config = self.config_loader.get_flowchart_config()
        
        # Initialize components
        console.print("[blue]Initializing components...[/blue]")
        
        self.parser = CPPCodeParser(parsing_config)
        self.rag_system = RAGSystem(ollama_config, vectordb_config)
        self.diagram_generator = PlantUMLGenerator(flowchart_config)
        
        # Initialize LLM
        self.llm = ChatOllama(
            base_url=ollama_config['base_url'],
            model=ollama_config['llm_model'],
            temperature=ollama_config['temperature'],
        )
        
        # QA chain
        self.qa_chain: Optional[RetrievalQA] = None
        
        console.print("[green]✓ Agent initialized successfully[/green]")
    
    def analyze_project(self, project_path: str, force_reindex: bool = False) -> None:
        """
        Analyze a C++ project
        
        Args:
            project_path: Path to the C++ project
            force_reindex: Force re-indexing even if vector store exists
        """
        console.print(f"\n[bold cyan]Analyzing project: {project_path}[/bold cyan]\n")
        
        # Parse the project (always needed for statistics and flowcharts)
        console.print("[bold blue]Step 1: Parsing C++ code...[/bold blue]")
        self.parser.parse_project(project_path)
        
        if not self.parser.functions and not self.parser.classes:
            console.print("[red]No C++ code found. Check project path.[/red]")
            return
        
        # Check if vector store exists
        vectorstore_exists = self.rag_system.load_vectorstore()
        
        if vectorstore_exists and not force_reindex:
            console.print("\n[yellow]Using existing vector store. Use --force to re-index.[/yellow]")
        else:
            # Create vector store
            console.print("\n[bold blue]Step 2: Creating vector store...[/bold blue]")
            code_chunks = self.parser.get_code_chunks()
            
            if not code_chunks:
                console.print("[red]No code chunks found.[/red]")
                return
            
            self.rag_system.create_vectorstore(code_chunks)
        
        # Create QA chain
        console.print("\n[bold blue]Step 3: Setting up QA system...[/bold blue]")
        self._setup_qa_chain()
        
        # Generate summary
        console.print("\n[bold blue]Step 4: Generating project summary...[/bold blue]")
        self._generate_summary()
        
        console.print("\n[green]✓ Project analysis complete![/green]")
    
    def generate_flowchart(
        self,
        flowchart_type: str = "function_call",
        entry_point: Optional[str] = None,
        output_name: Optional[str] = None
    ) -> str:
        """
        Generate PlantUML diagram
        
        Args:
            flowchart_type: Type of diagram (function_call, class, module, function_flow)
            entry_point: Entry point for function call graph or specific function name
            output_name: Custom output name
            
        Returns:
            Path to generated PlantUML file
        """
        if not self.parser.functions and not self.parser.classes:
            console.print("[red]No parsed data. Run analyze_project first.[/red]")
            return ""
        
        output_name = output_name or flowchart_type
        
        if flowchart_type == "function_call":
            return self.diagram_generator.generate_function_call_graph(
                self.parser.functions,
                entry_point=entry_point,
                output_name=output_name
            )
        elif flowchart_type == "function_flow":
            # Generate detailed flow for a specific function
            if not entry_point:
                console.print("[yellow]No function specified. Generating flows for functions with control flow...[/yellow]")
                # Generate for functions with interesting control flow
                funcs_with_flow = [f for f in self.parser.functions if f.control_flow][:5]
                if not funcs_with_flow:
                    console.print("[red]No functions with control flow found.[/red]")
                    return ""
                
                paths = []
                for func in funcs_with_flow:
                    path = self.diagram_generator.generate_detailed_function_flow(func)
                    paths.append(path)
                
                console.print(f"[green]Generated {len(paths)} function flow diagrams[/green]")
                return paths[0] if paths else ""
            else:
                # Find specific function
                func = None
                for f in self.parser.functions:
                    if f.name == entry_point:
                        func = f
                        break
                
                if not func:
                    console.print(f"[red]Function '{entry_point}' not found.[/red]")
                    return ""
                
                return self.diagram_generator.generate_detailed_function_flow(func, output_name)
        elif flowchart_type == "class":
            return self.diagram_generator.generate_class_diagram(
                self.parser.classes,
                output_name=output_name
            )
        elif flowchart_type == "module":
            return self.diagram_generator.generate_module_structure(
                self.parser.files_content,
                output_name=output_name
            )
        else:
            console.print(f"[red]Unknown diagram type: {flowchart_type}[/red]")
            return ""
    
    def list_functions(self, limit: int = 20) -> List[str]:
        """
        List all functions in the project
        
        Args:
            limit: Maximum number of functions to display
            
        Returns:
            List of function names
        """
        if not self.parser.functions:
            console.print("[red]No functions found. Run analyze_project first.[/red]")
            return []
        
        console.print(f"\n[cyan]Found {len(self.parser.functions)} functions:[/cyan]\n")
        
        # Sort by control flow complexity (functions with control flow first)
        sorted_funcs = sorted(
            self.parser.functions,
            key=lambda f: len(f.control_flow) if f.control_flow else 0,
            reverse=True
        )
        
        table = Table(title="Functions")
        table.add_column("Name", style="cyan")
        table.add_column("Return Type", style="green")
        table.add_column("Control Flow", style="yellow")
        table.add_column("Calls", style="magenta")
        table.add_column("File", style="blue")
        
        func_names = []
        for func in sorted_funcs[:limit]:
            flow_count = len(func.control_flow) if func.control_flow else 0
            call_count = len(func.calls) if func.calls else 0
            file_name = Path(func.file_path).name
            
            table.add_row(
                func.name,
                func.return_type,
                str(flow_count),
                str(call_count),
                file_name
            )
            func_names.append(func.name)
        
        if len(sorted_funcs) > limit:
            console.print(f"\n[yellow]Showing {limit} of {len(sorted_funcs)} functions[/yellow]")
        
        console.print(table)
        return func_names
    
    def query(self, question: str) -> str:
        """
        Query the codebase
        
        Args:
            question: Question about the codebase
            
        Returns:
            Answer
        """
        if not self.qa_chain:
            console.print("[red]QA chain not initialized. Run analyze_project first.[/red]")
            return ""
        
        console.print(f"\n[cyan]Question:[/cyan] {question}")
        
        try:
            # With LCEL, the chain returns the answer directly as a string
            answer = self.qa_chain.invoke(question)
            
            console.print(f"[green]Answer:[/green] {answer}\n")
            return answer
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            return ""
    
    def search_code(self, search_query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for code snippets
        
        Args:
            search_query: Search query
            k: Number of results
            
        Returns:
            List of relevant code snippets
        """
        results = self.rag_system.query(search_query, k=k)
        
        console.print(f"\n[cyan]Search:[/cyan] {search_query}")
        console.print(f"[yellow]Found {len(results)} results:[/yellow]\n")
        
        formatted_results = []
        for i, doc in enumerate(results, 1):
            metadata = doc.metadata
            console.print(f"[bold cyan]Result {i}:[/bold cyan]")
            console.print(f"Type: {metadata.get('type', 'unknown')}")
            console.print(f"Name: {metadata.get('name', 'unknown')}")
            console.print(f"File: {metadata.get('file', 'unknown')}")
            console.print(f"Line: {metadata.get('line', 'unknown')}")
            console.print(f"Content preview: {doc.page_content[:200]}...\n")
            
            formatted_results.append({
                'metadata': metadata,
                'content': doc.page_content
            })
        
        return formatted_results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get project statistics"""
        if not self.parser.functions and not self.parser.classes:
            console.print("[red]No parsed data. Run analyze_project first.[/red]")
            return {}
        
        stats = self.diagram_generator.generate_summary_stats(
            self.parser.functions,
            self.parser.classes
        )
        
        # Display statistics
        table = Table(title="Project Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Functions", str(stats['total_functions']))
        table.add_row("Total Classes", str(stats['total_classes']))
        table.add_row("Total Methods", str(stats['total_methods']))
        table.add_row("Avg Methods/Class", f"{stats['avg_methods_per_class']:.2f}")
        table.add_row("Total Files", str(len(self.parser.files_content)))
        
        console.print(table)
        
        return stats
    
    def _setup_qa_chain(self) -> None:
        """Setup QA chain for querying"""
        console.print("[blue]Setting up QA chain...[/blue]")
        
        # Create prompt template
        prompt_template = """You are an expert C++ code analyst. Use the following code context to answer the question.
        
Context:
{context}

Question: {question}

Provide a detailed and technical answer based on the code context. If you don't know the answer, say so.

Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Create QA chain using LCEL (LangChain Expression Language)
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
    
    def _generate_summary(self) -> None:
        """Generate project summary"""
        stats = self.get_statistics()
        
        # Check if stats are available
        if not stats or 'total_functions' not in stats:
            console.print("[yellow]No statistics available to generate summary[/yellow]")
            return
        
        # Ask AI for high-level summary
        summary_query = (
            f"This C++ project has {stats['total_functions']} functions and "
            f"{stats['total_classes']} classes. Provide a brief architectural overview "
            "based on the code structure."
        )
        
        try:
            summary = self.query(summary_query)
        except Exception as e:
            console.print(f"[yellow]Could not generate AI summary: {e}[/yellow]")

