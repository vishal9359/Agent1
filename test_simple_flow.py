#!/usr/bin/env python3
"""
Simple test script for control flow diagram generation (no dependencies)
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.cpp_parser import CPPCodeParser
from src.plantuml_generator import PlantUMLGenerator


def test_control_flow():
    """Test control flow diagram generation"""
    
    print("=" * 60)
    print("Testing Control Flow Diagram Generation")
    print("=" * 60)
    
    # Create test directory
    test_dir = Path("test_code")
    test_dir.mkdir(exist_ok=True)
    
    # Create test C++ file with control flow
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
    
    print(f"\n✓ Created test file: {test_cpp}")
    
    # Initialize parser
    parser_config = {
        'file_extensions': ['.cpp', '.h', '.hpp'],
        'ignore_dirs': ['build', 'dist'],
        'max_file_size_mb': 10
    }
    
    print("\n1. Initializing C++ parser...")
    parser = CPPCodeParser(parser_config)
    
    # Parse the project
    print(f"2. Parsing test code from {test_dir}...")
    parser.parse_project(str(test_dir))
    
    print(f"\n✓ Found {len(parser.functions)} functions")
    
    # Show functions with control flow
    print("\n3. Functions with control flow:")
    for func in parser.functions:
        flow_count = len(func.control_flow) if func.control_flow else 0
        print(f"   - {func.name}: {flow_count} control flow nodes")
        if func.control_flow:
            for node in func.control_flow[:3]:  # Show first 3 nodes
                print(f"      • {node.type}: {node.label or node.condition or ''}")
    
    # Initialize diagram generator
    flowchart_config = {
        'output_dir': 'outputs',
        'output_format': 'png',
        'max_depth': 5
    }
    
    print("\n4. Initializing diagram generator...")
    generator = PlantUMLGenerator(flowchart_config)
    
    # Generate detailed flow diagrams
    print("\n5. Generating function flow diagrams...")
    
    for func in parser.functions:
        if func.control_flow:
            print(f"\n   Generating flow for: {func.name}")
            path = generator.generate_detailed_function_flow(func)
            print(f"   ✓ Saved to: {path}")
            
            # Show the PlantUML content
            print(f"\n   PlantUML content for {func.name}:")
            print("   " + "-" * 50)
            with open(path, 'r') as f:
                for line in f:
                    print(f"   {line}", end='')
            print("   " + "-" * 50)
    
    # Generate overview diagram
    print("\n6. Generating overview function call diagram...")
    path = generator.generate_function_call_graph(
        parser.functions,
        output_name="test_overview"
    )
    print(f"   ✓ Saved to: {path}")
    
    print("\n" + "=" * 60)
    print("✓ Test complete!")
    print("=" * 60)
    print(f"\nGenerated diagrams are in: outputs/")
    print("\nTo view diagrams:")
    print("  1. Visit: http://www.plantuml.com/plantuml/uml/")
    print("  2. Copy and paste the PlantUML content from above")
    print("  3. Or use VSCode PlantUML extension")
    print("  4. Or install PlantUML and run: plantuml <filename>.puml")


if __name__ == '__main__':
    try:
        test_control_flow()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
