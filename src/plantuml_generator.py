"""
PlantUML Generator for C++ projects
Generates PlantUML diagrams that are text-based and easy to view/share
"""

from typing import List, Dict, Any, Set, Optional
from pathlib import Path
from dataclasses import dataclass
from rich.console import Console

console = Console()


class PlantUMLGenerator:
    """Generate PlantUML diagrams from C++ code analysis"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize PlantUML generator
        
        Args:
            config: Flowchart configuration
        """
        self.config = config
        self.output_dir = Path(config['output_dir'])
        self.max_depth = config['max_depth']
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_function_call_graph(
        self,
        functions: List[Any],
        entry_point: Optional[str] = None,
        output_name: str = "function_call_graph"
    ) -> str:
        """
        Generate function call graph using PlantUML activity diagram
        
        Args:
            functions: List of FunctionInfo objects
            entry_point: Entry point function name (optional)
            output_name: Output file name
            
        Returns:
            Path to generated PlantUML file
        """
        console.print("[blue]Generating PlantUML function call graph...[/blue]")
        
        # Create function lookup
        func_dict = {f.name: f for f in functions}
        
        plantuml = ["@startuml"]
        plantuml.append("title Function Call Graph")
        plantuml.append("")
        plantuml.append("skinparam defaultFontSize 10")
        plantuml.append("skinparam backgroundColor #FEFEFE")
        plantuml.append("")
        
        # Track visited functions to avoid infinite loops
        visited = set()
        
        if entry_point and entry_point in func_dict:
            # Build from entry point
            plantuml.append(f"start")
            plantuml.append(f":{entry_point}()|")
            self._add_function_calls(func_dict[entry_point], func_dict, plantuml, visited, depth=0)
            plantuml.append("stop")
        else:
            # Build call graph using sequence diagram for better visualization
            plantuml = ["@startuml"]
            plantuml.append("title Function Call Graph")
            plantuml.append("")
            plantuml.append("skinparam sequence {")
            plantuml.append("  ArrowColor DeepSkyBlue")
            plantuml.append("  ActorBorderColor DeepSkyBlue")
            plantuml.append("  LifeLineBorderColor Blue")
            plantuml.append("  ParticipantBorderColor DeepSkyBlue")
            plantuml.append("  ParticipantBackgroundColor LightSkyBlue")
            plantuml.append("}")
            plantuml.append("")
            
            # Add functions as participants
            added_funcs = set()
            for func in functions[:20]:  # Limit to first 20 for readability
                if func.name not in added_funcs:
                    plantuml.append(f'participant "{func.name}" as {self._sanitize_name(func.name)}')
                    added_funcs.add(func.name)
            
            plantuml.append("")
            
            # Add function calls
            for func in functions[:20]:
                for call in func.calls[:5]:  # Limit calls per function
                    if call in func_dict and call in added_funcs:
                        sanitized_caller = self._sanitize_name(func.name)
                        sanitized_callee = self._sanitize_name(call)
                        plantuml.append(f"{sanitized_caller} -> {sanitized_callee}: call")
        
        plantuml.append("")
        plantuml.append("@enduml")
        
        # Write to file
        output_path = self.output_dir / f"{output_name}.puml"
        output_path.write_text('\n'.join(plantuml), encoding='utf-8')
        
        console.print(f"[green]✓ PlantUML diagram saved to: {output_path}[/green]")
        self._print_view_instructions(output_path)
        return str(output_path)
    
    def generate_class_diagram(
        self,
        classes: List[Any],
        output_name: str = "class_diagram"
    ) -> str:
        """
        Generate class diagram using PlantUML
        
        Args:
            classes: List of ClassInfo objects
            output_name: Output file name
            
        Returns:
            Path to generated PlantUML file
        """
        console.print("[blue]Generating PlantUML class diagram...[/blue]")
        
        plantuml = ["@startuml"]
        plantuml.append("title Class Diagram")
        plantuml.append("")
        plantuml.append("skinparam class {")
        plantuml.append("  BackgroundColor LightBlue")
        plantuml.append("  BorderColor Navy")
        plantuml.append("  ArrowColor Navy")
        plantuml.append("}")
        plantuml.append("")
        
        # Add classes
        for cls in classes:
            sanitized_name = self._sanitize_name(cls.name)
            plantuml.append(f"class {sanitized_name} {{")
            
            # Add methods (limit to first 10 for readability)
            for method in cls.methods[:10]:
                return_type = method.return_type if method.return_type else "void"
                params = ", ".join(method.parameters[:3])  # Limit params shown
                if len(method.parameters) > 3:
                    params += ", ..."
                plantuml.append(f"  +{method.name}({params}): {return_type}")
            
            if len(cls.methods) > 10:
                plantuml.append(f"  .. {len(cls.methods) - 10} more methods ..")
            
            plantuml.append("}")
            plantuml.append("")
        
        # Add inheritance relationships
        class_dict = {c.name: c for c in classes}
        for cls in classes:
            sanitized_child = self._sanitize_name(cls.name)
            for base_class in cls.base_classes:
                if base_class in class_dict:
                    sanitized_parent = self._sanitize_name(base_class)
                    plantuml.append(f"{sanitized_parent} <|-- {sanitized_child}")
        
        plantuml.append("")
        plantuml.append("@enduml")
        
        # Write to file
        output_path = self.output_dir / f"{output_name}.puml"
        output_path.write_text('\n'.join(plantuml), encoding='utf-8')
        
        console.print(f"[green]✓ PlantUML diagram saved to: {output_path}[/green]")
        self._print_view_instructions(output_path)
        return str(output_path)
    
    def generate_module_structure(
        self,
        files_info: Dict[str, Any],
        output_name: str = "module_structure"
    ) -> str:
        """
        Generate module structure diagram using PlantUML component diagram
        
        Args:
            files_info: Dictionary of file paths and their info
            output_name: Output file name
            
        Returns:
            Path to generated PlantUML file
        """
        console.print("[blue]Generating PlantUML module structure...[/blue]")
        
        plantuml = ["@startuml"]
        plantuml.append("title Module Structure")
        plantuml.append("")
        plantuml.append("skinparam component {")
        plantuml.append("  BackgroundColor LightYellow")
        plantuml.append("  BorderColor Orange")
        plantuml.append("}")
        plantuml.append("skinparam package {")
        plantuml.append("  BackgroundColor LightGray")
        plantuml.append("  BorderColor DarkGray")
        plantuml.append("}")
        plantuml.append("")
        
        # Group by directory
        dir_files: Dict[str, List[str]] = {}
        for file_path in files_info.keys():
            dir_name = str(Path(file_path).parent)
            if dir_name not in dir_files:
                dir_files[dir_name] = []
            dir_files[dir_name].append(file_path)
        
        # Add packages (directories) and components (files)
        for dir_name, files in sorted(dir_files.items()):
            package_name = Path(dir_name).name or "root"
            sanitized_package = self._sanitize_name(package_name)
            
            plantuml.append(f"package \"{package_name}\" as {sanitized_package} {{")
            
            # Add files as components
            for file_path in sorted(files):
                file_name = Path(file_path).name
                sanitized_file = self._sanitize_name(file_name)
                plantuml.append(f"  [{file_name}] as {sanitized_file}")
            
            plantuml.append("}")
            plantuml.append("")
        
        plantuml.append("@enduml")
        
        # Write to file
        output_path = self.output_dir / f"{output_name}.puml"
        output_path.write_text('\n'.join(plantuml), encoding='utf-8')
        
        console.print(f"[green]✓ PlantUML diagram saved to: {output_path}[/green]")
        self._print_view_instructions(output_path)
        return str(output_path)
    
    def generate_summary_stats(
        self,
        functions: List[Any],
        classes: List[Any]
    ) -> Dict[str, Any]:
        """
        Generate summary statistics
        
        Args:
            functions: List of functions
            classes: List of classes
            
        Returns:
            Dictionary of statistics
        """
        stats = {
            'total_functions': len(functions),
            'total_classes': len(classes),
            'total_methods': sum(len(c.methods) for c in classes),
            'avg_methods_per_class': sum(len(c.methods) for c in classes) / len(classes) if classes else 0,
            'functions_by_file': {},
            'classes_by_file': {}
        }
        
        # Count by file
        for func in functions:
            file_path = func.file_path
            stats['functions_by_file'][file_path] = stats['functions_by_file'].get(file_path, 0) + 1
        
        for cls in classes:
            file_path = cls.file_path
            stats['classes_by_file'][file_path] = stats['classes_by_file'].get(file_path, 0) + 1
        
        return stats
    
    def _add_function_calls(
        self,
        func: Any,
        func_dict: Dict[str, Any],
        plantuml: List[str],
        visited: Set[str],
        depth: int
    ) -> None:
        """Recursively add function calls to activity diagram"""
        if depth >= self.max_depth or func.name in visited:
            return
        
        visited.add(func.name)
        
        for call in func.calls[:3]:  # Limit to 3 calls per function for readability
            if call in func_dict:
                plantuml.append(f":{call}()|")
                self._add_function_calls(func_dict[call], func_dict, plantuml, visited, depth + 1)
    
    def _sanitize_name(self, name: str) -> str:
        """Sanitize name for PlantUML (remove special characters)"""
        # Replace special characters with underscores
        sanitized = name.replace('::', '_').replace('<', '_').replace('>', '_')
        sanitized = sanitized.replace(' ', '_').replace('(', '').replace(')', '')
        sanitized = sanitized.replace('[', '').replace(']', '').replace(',', '_')
        sanitized = sanitized.replace('.', '_').replace('/', '_').replace('\\', '_')
        return sanitized
    
    def _print_view_instructions(self, file_path: Path) -> None:
        """Print instructions for viewing PlantUML files"""
        console.print("\n[cyan]To view this diagram:[/cyan]")
        console.print(f"  1. Download: scp user@server:{file_path.absolute()} .")
        console.print(f"  2. Online viewer: http://www.plantuml.com/plantuml/uml/")
        console.print(f"  3. VSCode: Install PlantUML extension")
        console.print(f"  4. View as text: cat {file_path.name}")
        console.print(f"  5. Generate PNG: plantuml {file_path.name}")

