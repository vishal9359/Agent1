#!/usr/bin/env python3
"""
Test script for control flow diagram generation
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agent import CPPAnalysisAgent
from rich.console import Console

console = Console()


def test_control_flow_diagrams():
    """Test control flow diagram generation"""
    
    console.print("[bold cyan]Testing Control Flow Diagram Generation[/bold cyan]\n")
    
    # Initialize agent
    console.print("[blue]1. Initializing agent...[/blue]")
    agent = CPPAnalysisAgent('config.yaml')
    
    # For testing, create a simple C++ file
    test_dir = Path("test_code")
    test_dir.mkdir(exist_ok=True)
    
    test_cpp = test_dir / "test.cpp"
    test_cpp.write_text("""
#include <iostream>

int calculateSum(int a, int b) {
    if (a > 0) {
        return a + b;
    } else {
        return b;
    }
}

void processData(int* data, int size) {
    for (int i = 0; i < size; i++) {
        if (data[i] > 0) {
            data[i] = data[i] * 2;
        }
    }
}

int checkValue(int x) {
    switch(x) {
        case 1:
            return 10;
        case 2:
            return 20;
        default:
            return 0;
    }
}

int main() {
    int result = calculateSum(5, 3);
    
    int data[] = {1, 2, 3, 4, 5};
    processData(data, 5);
    
    int value = checkValue(2);
    
    while (value > 0) {
        value--;
        std::cout << value << std::endl;
    }
    
    return 0;
}
""")
    
    # Parse the project
    console.print(f"[blue]2. Parsing test code from {test_dir}...[/blue]")
    agent.parser.parse_project(str(test_dir))
    
    console.print(f"[green]Found {len(agent.parser.functions)} functions[/green]\n")
    
    # List functions with control flow
    console.print("[blue]3. Functions with control flow:[/blue]")
    for func in agent.parser.functions:
        if func.control_flow:
            console.print(f"  - {func.name}: {len(func.control_flow)} flow nodes")
    
    # Generate flowcharts
    console.print("\n[blue]4. Generating function flow diagrams...[/blue]")
    
    # Generate detailed flow for each function
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    for func in agent.parser.functions:
        if func.control_flow:
            console.print(f"\n[cyan]Generating flow for: {func.name}[/cyan]")
            path = agent.diagram_generator.generate_detailed_function_flow(func)
            console.print(f"[green]✓ Saved to: {path}[/green]")
            
            # Display the PlantUML content
            console.print("\n[yellow]PlantUML Content:[/yellow]")
            with open(path, 'r') as f:
                content = f.read()
                console.print(content)
    
    # Generate overview diagram
    console.print("\n[blue]5. Generating overview diagram...[/blue]")
    path = agent.diagram_generator.generate_function_call_graph(
        agent.parser.functions,
        output_name="test_overview"
    )
    
    console.print("\n[bold green]✓ Test complete![/bold green]")
    console.print(f"\n[cyan]Generated diagrams are in: {output_dir}[/cyan]")
    console.print("\n[yellow]To view diagrams:[/yellow]")
    console.print("  1. Visit: http://www.plantuml.com/plantuml/uml/")
    console.print("  2. Copy and paste the PlantUML content")
    console.print("  3. Or use VSCode PlantUML extension")


if __name__ == '__main__':
    try:
        test_control_flow_diagrams()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)
