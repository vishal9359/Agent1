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
        Generate function call graph using PlantUML activity diagram with control flow
        
        Args:
            functions: List of FunctionInfo objects
            entry_point: Entry point function name (optional)
            output_name: Output file name
            
        Returns:
            Path to generated PlantUML file
        """
        console.print("[blue]Generating PlantUML function flow diagram with control flow...[/blue]")
        
        # Create function lookup
        func_dict = {f.name: f for f in functions}
        
        plantuml = ["@startuml"]
        plantuml.append("title Function Call Flow Diagram")
        plantuml.append("")
        
        # Add styling for a colorful flowchart
        plantuml.append("skinparam activity {")
        plantuml.append("  BackgroundColor #B4E7CE")
        plantuml.append("  BorderColor #2C5F2D")
        plantuml.append("  FontSize 11")
        plantuml.append("}")
        plantuml.append("skinparam activityDiamond {")
        plantuml.append("  BackgroundColor #FFD966")
        plantuml.append("  BorderColor #CC9900")
        plantuml.append("}")
        plantuml.append("skinparam activityStart {")
        plantuml.append("  BackgroundColor #4A90E2")
        plantuml.append("  BorderColor #2E5C8A")
        plantuml.append("}")
        plantuml.append("skinparam activityEnd {")
        plantuml.append("  BackgroundColor #E74C3C")
        plantuml.append("  BorderColor #C0392B")
        plantuml.append("}")
        plantuml.append("skinparam ArrowColor #2C5F2D")
        plantuml.append("")
        
        if entry_point and entry_point in func_dict:
            # Generate detailed flow for specific function
            func = func_dict[entry_point]
            plantuml.append("start")
            plantuml.append("")
            plantuml.append(f":{entry_point}();")
            plantuml.append("note right")
            plantuml.append(f"  Return: {func.return_type}")
            plantuml.append(f"  Params: {len(func.parameters)}")
            plantuml.append(f"  File: {Path(func.file_path).name}")
            plantuml.append("end note")
            plantuml.append("")
            
            # Add control flow
            if func.control_flow:
                self._add_control_flow_nodes(func.control_flow, plantuml, indent="")
            else:
                # Fallback to simple call list
                for call in func.calls[:5]:
                    plantuml.append(f":{call}();")
            
            plantuml.append("")
            plantuml.append("stop")
        else:
            # Generate overview with multiple functions
            plantuml.append("start")
            plantuml.append("")
            
            # Find functions with control flow to showcase
            interesting_funcs = [f for f in functions if f.control_flow][:3]
            
            if not interesting_funcs:
                # Fallback to any functions
                interesting_funcs = functions[:3]
            
            if len(interesting_funcs) == 0:
                plantuml.append(":No functions found;")
            else:
                console.print(f"[yellow]Generating flow for {len(interesting_funcs)} functions[/yellow]")
                
                for i, func in enumerate(interesting_funcs):
                    if i > 0:
                        plantuml.append("")
                        plantuml.append("fork")
                        plantuml.append("")
                    
                    plantuml.append(f":{func.name}();")
                    plantuml.append("note right")
                    plantuml.append(f"  Return: {func.return_type}")
                    plantuml.append(f"  File: {Path(func.file_path).name}")
                    plantuml.append("end note")
                    
                    # Add control flow (limited)
                    if func.control_flow:
                        self._add_control_flow_nodes(func.control_flow[:5], plantuml, indent="", max_depth=2)
                    
                    if i < len(interesting_funcs) - 1:
                        plantuml.append("")
                        plantuml.append("fork again")
                
                if len(interesting_funcs) > 1:
                    plantuml.append("")
                    plantuml.append("end fork")
            
            plantuml.append("")
            plantuml.append("stop")
        
        plantuml.append("")
        plantuml.append("@enduml")
        
        # Write to file
        output_path = self.output_dir / f"{output_name}.puml"
        output_path.write_text('\n'.join(plantuml), encoding='utf-8')
        
        console.print(f"[green]✓ PlantUML diagram saved to: {output_path}[/green]")
        self._print_view_instructions(output_path)
        return str(output_path)
    
    def generate_detailed_function_flow(
        self,
        func: Any,
        output_name: Optional[str] = None
    ) -> str:
        """
        Generate detailed control flow diagram for a single function
        
        Args:
            func: FunctionInfo object
            output_name: Output file name (optional, uses function name by default)
            
        Returns:
            Path to generated PlantUML file
        """
        if output_name is None:
            output_name = f"flow_{self._sanitize_name(func.name)}"
        
        console.print(f"[blue]Generating detailed flow for function: {func.name}[/blue]")
        
        plantuml = ["@startuml"]
        plantuml.append(f"title Function Flow: {func.name}")
        plantuml.append("")
        
        # Enhanced styling
        plantuml.append("skinparam activity {")
        plantuml.append("  BackgroundColor #B4E7CE")
        plantuml.append("  BorderColor #2C5F2D")
        plantuml.append("  FontSize 11")
        plantuml.append("}")
        plantuml.append("skinparam activityDiamond {")
        plantuml.append("  BackgroundColor #FFD966")
        plantuml.append("  BorderColor #CC9900")
        plantuml.append("}")
        plantuml.append("skinparam activityStart {")
        plantuml.append("  BackgroundColor #4A90E2")
        plantuml.append("}")
        plantuml.append("skinparam activityEnd {")
        plantuml.append("  BackgroundColor #E74C3C")
        plantuml.append("}")
        plantuml.append("")
        
        plantuml.append("start")
        plantuml.append("")
        plantuml.append(f":{func.name}(|")
        
        # Add parameters
        if func.parameters:
            for param in func.parameters[:3]:
                plantuml.append(f"  {self._sanitize_text(param)}")
            if len(func.parameters) > 3:
                plantuml.append(f"  ... {len(func.parameters) - 3} more params")
        plantuml.append(");")
        
        plantuml.append(f"note right: Returns {func.return_type}")
        plantuml.append("")
        
        # Add control flow
        if func.control_flow:
            self._add_control_flow_nodes(func.control_flow, plantuml, indent="")
        else:
            # No control flow detected, show function calls
            if func.calls:
                plantuml.append(":Execute function body;")
                plantuml.append("")
                for call in func.calls[:10]:
                    plantuml.append(f":{call}();")
            else:
                plantuml.append(":Execute function body;")
        
        plantuml.append("")
        plantuml.append("stop")
        plantuml.append("")
        plantuml.append("@enduml")
        
        # Write to file
        output_path = self.output_dir / f"{output_name}.puml"
        output_path.write_text('\n'.join(plantuml), encoding='utf-8')
        
        console.print(f"[green]✓ Function flow diagram saved to: {output_path}[/green]")
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
        Generate module structure diagram using PlantUML activity diagram showing flow
        
        Args:
            files_info: Dictionary of file paths and their info
            output_name: Output file name
            
        Returns:
            Path to generated PlantUML file
        """
        console.print("[blue]Generating PlantUML module structure...[/blue]")
        
        plantuml = ["@startuml"]
        plantuml.append("title Module Structure Flow")
        plantuml.append("")
        
        # Use activity diagram style for better flow visualization
        plantuml.append("skinparam activity {")
        plantuml.append("  BackgroundColor #E8F4F8")
        plantuml.append("  BorderColor #4A90E2")
        plantuml.append("  FontSize 11")
        plantuml.append("}")
        plantuml.append("skinparam activityDiamond {")
        plantuml.append("  BackgroundColor #FFE5B4")
        plantuml.append("  BorderColor #E6A23C")
        plantuml.append("}")
        plantuml.append("skinparam partition {")
        plantuml.append("  BackgroundColor #F0F0F0")
        plantuml.append("  BorderColor #606060")
        plantuml.append("}")
        plantuml.append("")
        
        # Group by directory
        dir_files: Dict[str, List[str]] = {}
        for file_path in files_info.keys():
            dir_name = str(Path(file_path).parent)
            if dir_name not in dir_files:
                dir_files[dir_name] = []
            dir_files[dir_name].append(file_path)
        
        plantuml.append("start")
        plantuml.append("")
        
        # Add partitions for each directory showing files as activities
        for i, (dir_name, files) in enumerate(sorted(dir_files.items())):
            package_name = Path(dir_name).name or "root"
            
            plantuml.append(f"partition \"{package_name}\" {{")
            
            # Add files as activities within the partition
            for j, file_path in enumerate(sorted(files)[:5]):  # Limit to 5 files per dir
                file_name = Path(file_path).name
                plantuml.append(f"  :{file_name};")
                
                # Add separator between files
                if j < len(files) - 1 and j < 4:
                    plantuml.append("  -[hidden]->")
            
            # Show count if more files
            if len(files) > 5:
                plantuml.append(f"  note right")
                plantuml.append(f"    ... {len(files) - 5} more files")
                plantuml.append(f"  end note")
            
            plantuml.append("}")
            
            # Add flow between directories
            if i < len(dir_files) - 1:
                plantuml.append("")
                plantuml.append("->")
                plantuml.append("")
        
        plantuml.append("")
        plantuml.append("stop")
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
    
    def _add_control_flow_nodes(
        self,
        flow_nodes: List[Any],
        plantuml: List[str],
        indent: str = "",
        depth: int = 0,
        max_depth: int = 5
    ) -> None:
        """Add control flow nodes to PlantUML activity diagram"""
        if depth >= max_depth:
            return
        
        for node in flow_nodes:
            if node.type == 'if':
                # If statement with decision diamond
                condition = self._sanitize_text(node.condition) if node.condition else "condition"
                plantuml.append(f"{indent}if ({condition}?) then (yes)")
                
                # Then branch
                if node.body_nodes:
                    self._add_control_flow_nodes(node.body_nodes, plantuml, indent + "  ", depth + 1, max_depth)
                else:
                    plantuml.append(f"{indent}  :process;")
                
                # Else branch
                if node.else_nodes:
                    plantuml.append(f"{indent}else (no)")
                    self._add_control_flow_nodes(node.else_nodes, plantuml, indent + "  ", depth + 1, max_depth)
                
                plantuml.append(f"{indent}endif")
            
            elif node.type == 'for':
                # For loop
                condition = self._sanitize_text(node.condition) if node.condition else "loop"
                plantuml.append(f"{indent}repeat")
                
                if node.body_nodes:
                    self._add_control_flow_nodes(node.body_nodes, plantuml, indent + "  ", depth + 1, max_depth)
                else:
                    plantuml.append(f"{indent}  :loop body;")
                
                plantuml.append(f"{indent}repeat while ({condition}?)")
            
            elif node.type == 'while':
                # While loop
                condition = self._sanitize_text(node.condition) if node.condition else "condition"
                plantuml.append(f"{indent}while ({condition}?) is (true)")
                
                if node.body_nodes:
                    self._add_control_flow_nodes(node.body_nodes, plantuml, indent + "  ", depth + 1, max_depth)
                else:
                    plantuml.append(f"{indent}  :loop body;")
                
                plantuml.append(f"{indent}endwhile (false)")
            
            elif node.type == 'switch':
                # Switch statement
                condition = self._sanitize_text(node.condition) if node.condition else "value"
                plantuml.append(f"{indent}switch ({condition}?)")
                
                for case_node in node.body_nodes[:5]:  # Limit cases
                    if case_node.type == 'case':
                        case_label = self._sanitize_text(case_node.label) if case_node.label else "case"
                        plantuml.append(f"{indent}case ({case_label})")
                        
                        if case_node.body_nodes:
                            self._add_control_flow_nodes(case_node.body_nodes, plantuml, indent + "  ", depth + 1, max_depth)
                        else:
                            plantuml.append(f"{indent}  :handle case;")
                
                plantuml.append(f"{indent}endswitch")
            
            elif node.type == 'return':
                # Return statement
                label = self._sanitize_text(node.label) if node.label else "return"
                plantuml.append(f"{indent}:{label};")
            
            elif node.type == 'call':
                # Function call
                label = self._sanitize_text(node.label) if node.label else "function call"
                plantuml.append(f"{indent}:{label};")
            
            elif node.type == 'statement':
                # Generic statement
                label = self._sanitize_text(node.label) if node.label else "statement"
                plantuml.append(f"{indent}:{label};")
    
    def _sanitize_text(self, text: str) -> str:
        """Sanitize text for PlantUML"""
        if not text:
            return ""
        
        # Remove problematic characters
        text = text.replace('\n', ' ').replace('\r', '')
        text = text.replace(';', ',')
        text = text.strip()
        
        # Limit length
        if len(text) > 60:
            text = text[:57] + "..."
        
        return text
    
    def _add_function_calls(
        self,
        func: Any,
        func_dict: Dict[str, Any],
        plantuml: List[str],
        visited: Set[str],
        depth: int
    ) -> None:
        """Recursively add function calls to activity diagram (legacy method)"""
        if depth >= self.max_depth or func.name in visited:
            return
        
        visited.add(func.name)
        
        # Check if function has multiple calls (use decision diamond)
        valid_calls = [call for call in func.calls[:5] if call in func_dict]
        
        if len(valid_calls) == 0:
            return
        elif len(valid_calls) == 1:
            # Single call - direct flow
            call = valid_calls[0]
            called_func = func_dict[call]
            plantuml.append("")
            plantuml.append(f":{call}();")
            plantuml.append("note right")
            plantuml.append(f"  Return: {called_func.return_type}")
            plantuml.append("end note")
            self._add_function_calls(called_func, func_dict, plantuml, visited, depth + 1)
        else:
            # Multiple calls - use decision or fork
            plantuml.append("")
            plantuml.append("if (Has multiple calls?) then (yes)")
            
            for i, call in enumerate(valid_calls[:3]):  # Limit to 3 for readability
                called_func = func_dict[call]
                if i > 0:
                    plantuml.append("else")
                plantuml.append(f"  :{call}();")
                plantuml.append("  note right")
                plantuml.append(f"    Return: {called_func.return_type}")
                plantuml.append("  end note")
                
                # Add one level of nested calls
                if called_func.calls and depth < self.max_depth - 1:
                    for nested_call in called_func.calls[:2]:
                        if nested_call in func_dict and nested_call not in visited:
                            plantuml.append(f"    :{nested_call}();")
            
            plantuml.append("endif")
            plantuml.append("")
    
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




