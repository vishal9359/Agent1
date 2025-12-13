#!/usr/bin/env python3
"""
Test script to demonstrate the improved PlantUML diagram generation
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.cpp_parser import CPPCodeParser, FunctionInfo
from src.plantuml_generator import PlantUMLGenerator
from rich.console import Console

console = Console()


def create_sample_trace_functions():
    """Create sample functions mimicking the poseidonos trace module structure"""
    
    functions = [
        # Main trace functions
        FunctionInfo(
            name="TraceManager::Initialize",
            return_type="void",
            parameters=["const TraceConfig& config"],
            body="{ /* initialization code */ }",
            file_path="trace/trace_manager.cpp",
            line_number=10,
            calls=["TraceBuffer::Allocate", "TraceWriter::Setup", "ConfigLoader::Load"]
        ),
        FunctionInfo(
            name="TraceBuffer::Allocate",
            return_type="bool",
            parameters=["size_t buffer_size"],
            body="{ /* buffer allocation */ }",
            file_path="trace/trace_buffer.cpp",
            line_number=25,
            calls=["MemoryAllocator::Allocate", "Logger::Info"]
        ),
        FunctionInfo(
            name="TraceWriter::Setup",
            return_type="void",
            parameters=["const std::string& output_path"],
            body="{ /* writer setup */ }",
            file_path="trace/trace_writer.cpp",
            line_number=15,
            calls=["FileSystem::CreatePath", "FileHandle::Open"]
        ),
        FunctionInfo(
            name="ConfigLoader::Load",
            return_type="TraceConfig",
            parameters=["const std::string& config_file"],
            body="{ /* config loading */ }",
            file_path="trace/config_loader.cpp",
            line_number=30,
            calls=["JsonParser::Parse", "Validator::Validate"]
        ),
        FunctionInfo(
            name="MemoryAllocator::Allocate",
            return_type="void*",
            parameters=["size_t size"],
            body="{ /* memory allocation */ }",
            file_path="trace/memory_allocator.cpp",
            line_number=40,
            calls=[]
        ),
        FunctionInfo(
            name="Logger::Info",
            return_type="void",
            parameters=["const std::string& message"],
            body="{ /* logging */ }",
            file_path="trace/logger.cpp",
            line_number=50,
            calls=["LogWriter::Write"]
        ),
        FunctionInfo(
            name="FileSystem::CreatePath",
            return_type="bool",
            parameters=["const std::string& path"],
            body="{ /* path creation */ }",
            file_path="trace/filesystem.cpp",
            line_number=20,
            calls=[]
        ),
        FunctionInfo(
            name="FileHandle::Open",
            return_type="bool",
            parameters=["const std::string& filename", "OpenMode mode"],
            body="{ /* file open */ }",
            file_path="trace/file_handle.cpp",
            line_number=35,
            calls=["ErrorHandler::Check"]
        ),
        FunctionInfo(
            name="JsonParser::Parse",
            return_type="JsonObject",
            parameters=["const std::string& json_string"],
            body="{ /* JSON parsing */ }",
            file_path="trace/json_parser.cpp",
            line_number=45,
            calls=[]
        ),
        FunctionInfo(
            name="Validator::Validate",
            return_type="bool",
            parameters=["const JsonObject& config"],
            body="{ /* validation */ }",
            file_path="trace/validator.cpp",
            line_number=55,
            calls=[]
        ),
        FunctionInfo(
            name="LogWriter::Write",
            return_type="void",
            parameters=["const std::string& message"],
            body="{ /* write to log */ }",
            file_path="trace/log_writer.cpp",
            line_number=60,
            calls=[]
        ),
        FunctionInfo(
            name="ErrorHandler::Check",
            return_type="bool",
            parameters=["int error_code"],
            body="{ /* error checking */ }",
            file_path="trace/error_handler.cpp",
            line_number=70,
            calls=[]
        ),
        # Additional trace recording functions
        FunctionInfo(
            name="TraceRecorder::Record",
            return_type="void",
            parameters=["const TraceEvent& event"],
            body="{ /* record event */ }",
            file_path="trace/trace_recorder.cpp",
            line_number=80,
            calls=["TraceBuffer::Write", "EventSerializer::Serialize"]
        ),
        FunctionInfo(
            name="TraceBuffer::Write",
            return_type="bool",
            parameters=["const void* data", "size_t size"],
            body="{ /* write to buffer */ }",
            file_path="trace/trace_buffer.cpp",
            line_number=90,
            calls=[]
        ),
        FunctionInfo(
            name="EventSerializer::Serialize",
            return_type="std::string",
            parameters=["const TraceEvent& event"],
            body="{ /* serialize event */ }",
            file_path="trace/event_serializer.cpp",
            line_number=100,
            calls=[]
        ),
    ]
    
    return functions


def main():
    """Main test function"""
    console.print("\n[bold cyan]Testing Improved PlantUML Diagram Generation[/bold cyan]\n")
    
    # Configuration for diagram generation
    config = {
        'output_dir': 'test_output',
        'output_format': 'png',
        'max_depth': 3
    }
    
    # Create output directory
    Path(config['output_dir']).mkdir(exist_ok=True)
    
    # Initialize generator
    generator = PlantUMLGenerator(config)
    
    # Create sample functions
    console.print("[blue]Creating sample trace module functions...[/blue]")
    functions = create_sample_trace_functions()
    console.print(f"[green]✓ Created {len(functions)} sample functions[/green]\n")
    
    # Test 1: Generate function call graph with entry point
    console.print("[bold yellow]Test 1: Function Call Graph with Entry Point[/bold yellow]")
    console.print("Generating diagram from 'TraceManager::Initialize' entry point...\n")
    
    output1 = generator.generate_function_call_graph(
        functions,
        entry_point="TraceManager::Initialize",
        output_name="trace_flow_with_entry_point"
    )
    console.print(f"[green]✓ Generated: {output1}[/green]\n")
    
    # Test 2: Generate function call graph without entry point
    console.print("[bold yellow]Test 2: Function Call Graph without Entry Point[/bold yellow]")
    console.print("Generating diagram with auto-detected entry points...\n")
    
    output2 = generator.generate_function_call_graph(
        functions,
        entry_point=None,
        output_name="trace_flow_auto_entry"
    )
    console.print(f"[green]✓ Generated: {output2}[/green]\n")
    
    # Test 3: Generate module structure
    console.print("[bold yellow]Test 3: Module Structure Diagram[/bold yellow]")
    console.print("Generating module structure flow...\n")
    
    files_info = {
        "trace/trace_manager.cpp": {},
        "trace/trace_buffer.cpp": {},
        "trace/trace_writer.cpp": {},
        "trace/config_loader.cpp": {},
        "trace/memory_allocator.cpp": {},
        "trace/logger.cpp": {},
        "trace/filesystem.cpp": {},
        "trace/file_handle.cpp": {},
    }
    
    output3 = generator.generate_module_structure(
        files_info,
        output_name="trace_module_structure"
    )
    console.print(f"[green]✓ Generated: {output3}[/green]\n")
    
    # Display summary
    console.print("\n[bold green]✓ All tests completed![/bold green]\n")
    console.print("[cyan]Generated files:[/cyan]")
    console.print(f"  1. {output1}")
    console.print(f"  2. {output2}")
    console.print(f"  3. {output3}")
    
    console.print("\n[yellow]To view these diagrams:[/yellow]")
    console.print("  1. Online: Visit http://www.plantuml.com/plantuml/uml/")
    console.print("  2. VSCode: Install PlantUML extension")
    console.print("  3. Command line: plantuml <filename>.puml")
    console.print("\n[cyan]Key improvements:[/cyan]")
    console.print("  ✓ Colorful activity diagrams with proper flow")
    console.print("  ✓ Decision diamonds for multiple function calls")
    console.print("  ✓ Boxes with colors (green for activities, yellow for decisions)")
    console.print("  ✓ Notes showing function details (return type, file)")
    console.print("  ✓ Better module structure with partitions")
    console.print("  ✓ Proper start/stop nodes")
    
    # Display sample PlantUML code
    console.print("\n[bold cyan]Sample PlantUML Code Preview:[/bold cyan]")
    sample_file = Path(config['output_dir']) / "trace_flow_with_entry_point.puml"
    if sample_file.exists():
        content = sample_file.read_text(encoding='utf-8')
        console.print("\n[dim]" + content[:500] + "...[/dim]\n")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)
