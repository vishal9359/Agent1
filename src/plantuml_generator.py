"""
PlantUML Generator for C++ projects - FIXED VERSION
Handles real-world C++ code with proper sanitization
"""

from typing import List, Dict, Any, Set, Optional
from pathlib import Path
from dataclasses import dataclass
from rich.console import Console
import re

console = Console()


class PlantUMLGenerator:
    """Generate PlantUML diagrams from C++ code analysis - FIXED"""
    
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
    
    def _sanitize_for_plantuml(self, text: str, max_length: int = 50) -> str:
        """
        Properly sanitize text for PlantUML activity diagrams
        
        PlantUML special characters that need handling:
        - : (colon) - used for activity syntax
        - ; (semicolon) - statement terminator
        - | (pipe) - swimlane separator
        - [ ] - note syntax
        - ( ) - can cause issues in some contexts
        - < > - comparison operators and templates
        - " (quotes) - string delimiters
        
        Args:
            text: Text to sanitize
            max_length: Maximum length before truncation
            
        Returns:
            Sanitized text safe for PlantUML
        """
        if not text:
            return "condition"
        
        # Remove or replace problematic characters
        text = str(text).strip()
        
        # Remove newlines and carriage returns
        text = text.replace('\n', ' ').replace('\r', ' ')
        
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Handle parentheses - keep them but not in specific contexts
        # Remove outer parentheses if they wrap the entire expression
        if text.startswith('(') and text.endswith(')'):
            text = text[1:-1].strip()
        
        # Replace problematic characters
        replacements = {
            ';': '',  # Remove semicolons
            ':': ' ',  # Replace colons with space
            '|': ' or ',  # Replace pipe with 'or'
            '[': '(',  # Replace brackets with parentheses
            ']': ')',
            '{': '(',
            '}': ')',
            '"': "'",  # Replace double quotes with single
            '\\': '/',  # Replace backslash
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Handle comparison operators - ensure they're spaced
        text = re.sub(r'([<>=!]+)', r' \1 ', text)
        text = re.sub(r'\s+', ' ', text)  # Remove multiple spaces again
        
        # Truncate if too long
        if len(text) > max_length:
            text = text[:max_length - 3] + "..."
        
        text = text.strip()
        
        # Ensure we return something valid
        if not text or text.isspace():
            return "condition"
        
        return text
    
    def _sanitize_label(self, label: str, max_length: int = 60) -> str:
        """
        Sanitize labels for activity boxes
        
        Args:
            label: Label text
            max_length: Maximum length
            
        Returns:
            Sanitized label
        """
        if not label:
            return "statement"
        
        label = str(label).strip()
        
        # Remove newlines
        label = label.replace('\n', ' ').replace('\r', ' ')
        
        # Remove multiple spaces
        label = re.sub(r'\s+', ' ', label)
        
        # Keep more characters for labels, but escape special ones
        replacements = {
            ':': ' ',  # Colon breaks activity syntax
            ';': '',  # Remove semicolons
            '|': ' ',  # Pipe breaks syntax
        }
        
        for old, new in replacements.items():
            label = label.replace(old, new)
        
        # Truncate if needed
        if len(label) > max_length:
            label = label[:max_length - 3] + "..."
        
        label = label.strip()
        
        if not label or label.isspace():
            return "statement"
        
        return label
    
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
        plantuml.append(f"title Function Flow - {func.name}")
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
        
        # Function name - sanitize it
        func_label = self._sanitize_label(func.name, 40)
        plantuml.append(f":{func_label};")
        
        # Add note with details
        plantuml.append("note right")
        plantuml.append(f"  Return: {self._sanitize_label(func.return_type, 30)}")
        if func.parameters:
            param_count = len(func.parameters)
            plantuml.append(f"  Params: {param_count}")
        plantuml.append("end note")
        plantuml.append("")
        
        # Add control flow with error handling
        if func.control_flow:
            try:
                self._add_control_flow_nodes(func.control_flow, plantuml, indent="")
            except Exception as e:
                console.print(f"[yellow]Warning: Error in control flow generation: {e}[/yellow]")
                plantuml.append(":Function body;")
        else:
            # No control flow detected, show function calls or simple body
            if func.calls:
                plantuml.append(":Execute function body;")
                plantuml.append("")
                for call in func.calls[:5]:  # Limit to 5 calls
                    safe_call = self._sanitize_label(call, 50)
                    plantuml.append(f":{safe_call};")
            else:
                plantuml.append(":Execute function body;")
        
        plantuml.append("")
        plantuml.append("stop")
        plantuml.append("")
        plantuml.append("@enduml")
        
        # Write to file
        output_path = self.output_dir / f"{output_name}.puml"
        try:
            output_path.write_text('\n'.join(plantuml), encoding='utf-8')
            console.print(f"[green]✓ Function flow diagram saved to: {output_path}[/green]")
        except Exception as e:
            console.print(f"[red]✗ Error writing file: {e}[/red]")
            raise
        
        return str(output_path)
    
    def _add_control_flow_nodes(
        self,
        flow_nodes: List[Any],
        plantuml: List[str],
        indent: str = "",
        depth: int = 0,
        max_depth: int = 5
    ) -> None:
        """
        Add control flow nodes to PlantUML activity diagram
        
        Args:
            flow_nodes: List of ControlFlowNode objects
            plantuml: PlantUML lines list
            indent: Current indentation
            depth: Current recursion depth
            max_depth: Maximum recursion depth
        """
        if depth >= max_depth:
            plantuml.append(f"{indent}:... (max depth reached);")
            return
        
        if not flow_nodes:
            return
        
        for node in flow_nodes:
            try:
                if node.type == 'if':
                    # If statement with decision diamond
                    condition = self._sanitize_for_plantuml(node.condition) if node.condition else "condition"
                    plantuml.append(f"{indent}if ({condition}) then (yes)")
                    
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
                    condition = self._sanitize_for_plantuml(node.condition, 40) if node.condition else "loop"
                    plantuml.append(f"{indent}repeat")
                    
                    if node.body_nodes:
                        self._add_control_flow_nodes(node.body_nodes, plantuml, indent + "  ", depth + 1, max_depth)
                    else:
                        plantuml.append(f"{indent}  :loop body;")
                    
                    plantuml.append(f"{indent}repeat while ({condition})")
                
                elif node.type == 'while':
                    # While loop
                    condition = self._sanitize_for_plantuml(node.condition, 40) if node.condition else "condition"
                    plantuml.append(f"{indent}while ({condition}) is (true)")
                    
                    if node.body_nodes:
                        self._add_control_flow_nodes(node.body_nodes, plantuml, indent + "  ", depth + 1, max_depth)
                    else:
                        plantuml.append(f"{indent}  :loop body;")
                    
                    plantuml.append(f"{indent}endwhile (false)")
                
                elif node.type == 'switch':
                    # Switch statement
                    condition = self._sanitize_for_plantuml(node.condition, 30) if node.condition else "value"
                    plantuml.append(f"{indent}switch ({condition})")
                    
                    for case_node in node.body_nodes[:5]:  # Limit cases
                        if case_node.type == 'case':
                            case_label = self._sanitize_label(case_node.label, 20) if case_node.label else "case"
                            plantuml.append(f"{indent}case ( {case_label} )")
                            
                            if case_node.body_nodes:
                                self._add_control_flow_nodes(case_node.body_nodes, plantuml, indent + "  ", depth + 1, max_depth)
                            else:
                                plantuml.append(f"{indent}  :handle case;")
                    
                    plantuml.append(f"{indent}endswitch")
                
                elif node.type == 'return':
                    # Return statement
                    label = self._sanitize_label(node.label) if node.label else "return"
                    plantuml.append(f"{indent}:{label};")
                
                elif node.type == 'call':
                    # Function call
                    label = self._sanitize_label(node.label) if node.label else "function call"
                    plantuml.append(f"{indent}:{label};")
                
                elif node.type == 'statement':
                    # Generic statement
                    label = self._sanitize_label(node.label) if node.label else "statement"
                    plantuml.append(f"{indent}:{label};")
                    
            except Exception as e:
                # If any node fails, log and continue
                console.print(f"[yellow]Warning: Skipping node due to error: {e}[/yellow]")
                plantuml.append(f"{indent}:... (error in node);")
                continue
    
    def _sanitize_name(self, name: str) -> str:
        """Sanitize name for file names (remove special characters)"""
        # Replace special characters with underscores
        sanitized = str(name).replace('::', '_').replace('<', '_').replace('>', '_')
        sanitized = sanitized.replace(' ', '_').replace('(', '').replace(')', '')
        sanitized = sanitized.replace('[', '').replace(']', '').replace(',', '_')
        sanitized = sanitized.replace('.', '_').replace('/', '_').replace('\\', '_')
        sanitized = sanitized.replace('*', '').replace('&', '').replace('~', '')
        
        # Remove any remaining non-alphanumeric characters except underscore
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', sanitized)
        
        # Remove leading/trailing underscores
        sanitized = sanitized.strip('_')
        
        # Limit length
        if len(sanitized) > 50:
            sanitized = sanitized[:50]
        
        # Ensure it's not empty
        if not sanitized:
            sanitized = "function"
        
        return sanitized
    
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
            
            func_label = self._sanitize_label(entry_point, 40)
            plantuml.append(f":{func_label};")
            plantuml.append("note right")
            plantuml.append(f"  Return: {self._sanitize_label(func.return_type, 30)}")
            plantuml.append(f"  Params: {len(func.parameters)}")
            plantuml.append(f"  File: {Path(func.file_path).name}")
            plantuml.append("end note")
            plantuml.append("")
            
            # Add control flow
            if func.control_flow:
                try:
                    self._add_control_flow_nodes(func.control_flow, plantuml, indent="")
                except Exception as e:
                    console.print(f"[yellow]Warning in control flow: {e}[/yellow]")
                    for call in func.calls[:5]:
                        safe_call = self._sanitize_label(call, 50)
                        plantuml.append(f":{safe_call};")
            else:
                # Fallback to simple call list
                for call in func.calls[:5]:
                    safe_call = self._sanitize_label(call, 50)
                    plantuml.append(f":{safe_call};")
            
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
                    
                    func_label = self._sanitize_label(func.name, 40)
                    plantuml.append(f":{func_label};")
                    plantuml.append("note right")
                    plantuml.append(f"  Return: {self._sanitize_label(func.return_type, 30)}")
                    plantuml.append(f"  File: {Path(func.file_path).name}")
                    plantuml.append("end note")
                    
                    # Add control flow (limited)
                    if func.control_flow:
                        try:
                            self._add_control_flow_nodes(func.control_flow[:5], plantuml, indent="", max_depth=2)
                        except Exception as e:
                            console.print(f"[yellow]Warning: {e}[/yellow]")
                    
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
    
    def _print_view_instructions(self, file_path: Path) -> None:
        """Print instructions for viewing PlantUML files"""
        console.print("\n[cyan]To view this diagram:[/cyan]")
        console.print(f"  1. Online viewer: http://www.plantuml.com/plantuml/uml/")
        console.print(f"  2. VSCode: Install PlantUML extension")
        console.print(f"  3. View as text: cat {file_path.name}")
        console.print(f"  4. Generate PNG: plantuml {file_path.name}")
    
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
                return_type = self._sanitize_label(method.return_type, 20) if method.return_type else "void"
                params = ", ".join([self._sanitize_label(p, 15) for p in method.parameters[:3]])
                if len(method.parameters) > 3:
                    params += ", ..."
                method_name = self._sanitize_label(method.name, 30)
                plantuml.append(f"  +{method_name}({params}) {return_type}")
            
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
            safe_package = self._sanitize_label(package_name, 30)
            
            plantuml.append(f"partition \"{safe_package}\" {{")
            
            # Add files as activities within the partition
            for j, file_path in enumerate(sorted(files)[:5]):  # Limit to 5 files per dir
                file_name = Path(file_path).name
                safe_file = self._sanitize_label(file_name, 40)
                plantuml.append(f"  :{safe_file};")
                
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
        """Generate summary statistics"""
        stats = {
            'total_functions': len(functions),
            'total_classes': len(classes),
            'total_methods': sum(len(c.methods) for c in classes),
            'avg_methods_per_class': sum(len(c.methods) for c in classes) / len(classes) if classes else 0,
            'functions_by_file': {},
            'classes_by_file': {}
        }
        
        for func in functions:
            file_path = func.file_path
            stats['functions_by_file'][file_path] = stats['functions_by_file'].get(file_path, 0) + 1
        
        for cls in classes:
            file_path = cls.file_path
            stats['classes_by_file'][file_path] = stats['classes_by_file'].get(file_path, 0) + 1
        
        return stats
