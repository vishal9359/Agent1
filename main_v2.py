#!/usr/bin/env python3
"""
Main entry point for Agent1 v2 - Clean AST-Based Implementation
"""

import sys
import argparse
from pathlib import Path

# Add src_v2 to path
sys.path.insert(0, str(Path(__file__).parent))

from src_v2.agent import CPPAnalysisAgent
from src_v2.config_loader import ConfigLoader
from rich.console import Console

console = Console()


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="C++ Analysis Agent v2 - AST-Based",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a project
  python main_v2.py analyze /path/to/cpp/project
  
  # Generate function flow diagrams
  python main_v2.py diagram --type function_flow
  
  # Generate for specific function
  python main_v2.py diagram --type function_flow --function ProcessEvent
  
  # Generate module diagram
  python main_v2.py diagram --type module
  
  # Query the codebase
  python main_v2.py query "How does the main function work?"
  
  # List functions
  python main_v2.py list-functions
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze C++ project')
    analyze_parser.add_argument('project_path', help='Path to C++ project')
    analyze_parser.add_argument('--config', default='config.yaml', help='Config file')
    
    # Diagram command
    diagram_parser = subparsers.add_parser('diagram', help='Generate diagrams')
    diagram_parser.add_argument('--type', choices=['function_flow', 'module'], 
                               default='function_flow', help='Diagram type')
    diagram_parser.add_argument('--function', help='Specific function name')
    diagram_parser.add_argument('--module', help='Module path filter')
    diagram_parser.add_argument('--config', default='config.yaml', help='Config file')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Query codebase')
    query_parser.add_argument('question', help='Question to ask')
    query_parser.add_argument('--config', default='config.yaml', help='Config file')
    
    # List functions
    list_parser = subparsers.add_parser('list-functions', help='List functions')
    list_parser.add_argument('--limit', type=int, default=20, help='Max functions to show')
    list_parser.add_argument('--config', default='config.yaml', help='Config file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        # Load config
        config_loader = ConfigLoader(getattr(args, 'config', 'config.yaml'))
        config = config_loader.get_config()
        
        # Initialize agent
        agent = CPPAnalysisAgent(config)
        
        # Execute command
        if args.command == 'analyze':
            agent.analyze_project(args.project_path)
        
        elif args.command == 'diagram':
            paths = agent.generate_diagrams(
                diagram_type=args.type,
                function_name=getattr(args, 'function', None),
                module_path=getattr(args, 'module', None)
            )
            if paths:
                console.print(f"\n[green]✓ Generated {len(paths)} diagram(s)[/green]")
                console.print(f"[cyan]View at: http://www.plantuml.com/plantuml/uml/[/cyan]")
        
        elif args.command == 'query':
            agent.query(args.question)
        
        elif args.command == 'list-functions':
            agent.list_functions(limit=args.limit)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
