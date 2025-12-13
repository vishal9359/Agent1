#!/usr/bin/env python3
"""
Main entry point for C++ Analysis Agent
"""

import sys
import argparse
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agent import CPPAnalysisAgent

console = Console()


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="AI Agent for C++ Project Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a project
  python main.py analyze /path/to/cpp/project
  
  # Force re-indexing
  python main.py analyze /path/to/cpp/project --force
  
  # Generate flowcharts
  python main.py flowchart --type function_call
  python main.py flowchart --type class
  python main.py flowchart --type module
  python main.py flowchart --type function_flow --entry-point main
  
  # List functions
  python main.py list-functions
  
  # Query the codebase
  python main.py query "How does the main function work?"
  
  # Search code
  python main.py search "memory allocation"
  
  # Get statistics
  python main.py stats
  
  # Interactive mode
  python main.py interactive
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze C++ project')
    analyze_parser.add_argument('project_path', help='Path to C++ project')
    analyze_parser.add_argument('--force', action='store_true', help='Force re-indexing')
    analyze_parser.add_argument('--flowchart', nargs='*', choices=['function_call', 'class', 'module', 'all'],
                                help='Generate flowcharts after analysis (e.g., --flowchart function_call class)')
    analyze_parser.add_argument('--config', default='config.yaml', help='Config file path')
    
    # Flowchart command
    flowchart_parser = subparsers.add_parser('flowchart', help='Generate flowchart')
    flowchart_parser.add_argument('--type', choices=['function_call', 'class', 'module', 'function_flow'],
                                  default='function_call', help='Flowchart type')
    flowchart_parser.add_argument('--entry-point', help='Entry point or specific function name')
    flowchart_parser.add_argument('--output', help='Output file name')
    flowchart_parser.add_argument('--config', default='config.yaml', help='Config file path')
    
    # List functions command
    list_funcs_parser = subparsers.add_parser('list-functions', help='List all functions')
    list_funcs_parser.add_argument('--limit', type=int, default=20, help='Maximum functions to display')
    list_funcs_parser.add_argument('--config', default='config.yaml', help='Config file path')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Query the codebase')
    query_parser.add_argument('question', help='Question to ask')
    query_parser.add_argument('--config', default='config.yaml', help='Config file path')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search code')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--limit', type=int, default=5, help='Number of results')
    search_parser.add_argument('--config', default='config.yaml', help='Config file path')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show project statistics')
    stats_parser.add_argument('--config', default='config.yaml', help='Config file path')
    
    # Interactive command
    interactive_parser = subparsers.add_parser('interactive', help='Interactive mode')
    interactive_parser.add_argument('--config', default='config.yaml', help='Config file path')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        # Initialize agent
        config_path = getattr(args, 'config', 'config.yaml')
        agent = CPPAnalysisAgent(config_path)
        
        # Execute command
        if args.command == 'analyze':
            agent.analyze_project(args.project_path, force_reindex=args.force)
            
            # Generate flowcharts if requested
            if hasattr(args, 'flowchart') and args.flowchart is not None:
                if len(args.flowchart) == 0 or 'all' in args.flowchart:
                    # Generate all flowcharts
                    console.print("\n[bold cyan]Generating all flowcharts...[/bold cyan]")
                    agent.generate_flowchart('function_call')
                    agent.generate_flowchart('class')
                    agent.generate_flowchart('module')
                else:
                    # Generate specified flowcharts
                    for ftype in args.flowchart:
                        agent.generate_flowchart(ftype)
            
        elif args.command == 'flowchart':
            agent.generate_flowchart(
                flowchart_type=args.type,
                entry_point=args.entry_point,
                output_name=args.output
            )
            
        elif args.command == 'query':
            agent.query(args.question)
            
        elif args.command == 'search':
            agent.search_code(args.query, k=args.limit)
            
        elif args.command == 'stats':
            agent.get_statistics()
        
        elif args.command == 'list-functions':
            agent.list_functions(limit=args.limit)
            
        elif args.command == 'interactive':
            interactive_mode(agent)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def interactive_mode(agent: CPPAnalysisAgent):
    """Interactive mode for the agent"""
    console.print(Panel.fit(
        "[bold green]Interactive Mode[/bold green]\n"
        "Commands: query, search, flowchart, stats, help, exit",
        border_style="green"
    ))
    
    while True:
        try:
            user_input = console.input("\n[cyan]>[/cyan] ").strip()
            
            if not user_input:
                continue
            
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            
            if command == 'exit' or command == 'quit':
                console.print("[yellow]Goodbye![/yellow]")
                break
                
            elif command == 'help':
                console.print("""
[cyan]Available commands:[/cyan]
  query <question>       - Ask a question about the codebase
  search <query>         - Search for code snippets
  flowchart <type>       - Generate flowchart (function_call/class/module/function_flow)
  flow <function_name>   - Generate detailed flow for a function
  list                   - List all functions
  stats                  - Show project statistics
  help                   - Show this help
  exit                   - Exit interactive mode
                """)
                
            elif command == 'query':
                if len(parts) < 2:
                    console.print("[red]Usage: query <question>[/red]")
                else:
                    agent.query(parts[1])
                    
            elif command == 'search':
                if len(parts) < 2:
                    console.print("[red]Usage: search <query>[/red]")
                else:
                    agent.search_code(parts[1])
                    
            elif command == 'flowchart':
                flowchart_type = parts[1] if len(parts) > 1 else 'function_call'
                agent.generate_flowchart(flowchart_type=flowchart_type)
            
            elif command == 'flow':
                if len(parts) < 2:
                    console.print("[yellow]Generating flows for interesting functions...[/yellow]")
                    agent.generate_flowchart(flowchart_type='function_flow')
                else:
                    agent.generate_flowchart(flowchart_type='function_flow', entry_point=parts[1])
            
            elif command == 'list':
                agent.list_functions()
                
            elif command == 'stats':
                agent.get_statistics()
                
            else:
                console.print(f"[red]Unknown command: {command}[/red]")
                console.print("[yellow]Type 'help' for available commands[/yellow]")
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Type 'exit' to quit[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == '__main__':
    main()

