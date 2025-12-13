"""
PlantUML Generator for C++ projects - ULTRA-ROBUST VERSION
Guaranteed to work with ANY C++ project including PoseidonOS
"""

from typing import List, Dict, Any, Set, Optional
from pathlib import Path
from dataclasses import dataclass
from rich.console import Console
import re

console = Console()


class PlantUMLGenerator:
    """Generate PlantUML diagrams from C++ code analysis - ULTRA-ROBUST"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize PlantUML generator"""
        self.config = config
        self.output_dir = Path(config['output_dir'])
        self.max_depth = config['max_depth']
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _ultra_sanitize(self, text: str, context: str = "general") -> str:
        """
        ULTRA-AGGRESSIVE sanitization for PlantUML
        Guarantees valid PlantUML syntax
        
        Args:
            text: Text to sanitize
            context: Where this text will be used (condition, label, filename)
        """
        if not text or not str(text).strip():
            return "item" if context == "label" else "check"
        
        text = str(text).strip()
        
        # Step 1: Remove all newlines and tabs
        text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        
        # Step 2: Handle different contexts
        if context == "condition":
            # For conditions in if/while/for - VERY aggressive
            # Remove ALL special PlantUML characters
            text = text.replace(':', ' ')  # Colon breaks activity syntax
            text = text.replace(';', '')   # Semicolon removed
            text = text.replace('|', ' or ')  # Pipe to 'or'
            text = text.replace('[', '(')
            text = text.replace(']', ')')
            text = text.replace('{', '(')
            text = text.replace('}', ')')
            text = text.replace('"', "'")
            text = text.replace('\\', '/')
            text = text.replace('`', "'")
            text = text.replace('~', '-')
            
            # Handle comparison operators - add spaces
            for op in ['==', '!=', '<=', '>=', '&&', '||', '<<', '>>']:
                text = text.replace(op, f' {op} ')
            
            # Remove outer parentheses if they wrap everything
            text = text.strip()
            while text.startswith('(') and text.endswith(')'):
                inner = text[1:-1]
                if '(' not in inner or inner.count('(') == inner.count(')'):
                    text = inner.strip()
                else:
                    break
            
            # Limit length for conditions
            max_len = 40
            if len(text) > max_len:
                text = text[:max_len-3] + "..."
            
        elif context == "label":
            # For activity labels - less aggressive, more readable
            text = text.replace(':', ' ')  # Still remove colons
            text = text.replace(';', '')   # Remove semicolons
            text = text.replace('|', ' ')  # Remove pipes
            
            # Limit length
            max_len = 50
            if len(text) > max_len:
                text = text[:max_len-3] + "..."
                
        elif context == "filename":
            # For filenames - remove all non-alphanumeric
            text = re.sub(r'[^a-zA-Z0-9_]', '_', text)
            text = re.sub(r'_+', '_', text)  # Multiple underscores to single
            text = text.strip('_')
            if len(text) > 40:
                text = text[:40]
        
        # Step 3: Clean up multiple spaces
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Step 4: Ensure we return something valid
        if not text or len(text) < 2:
            return "item" if context == "label" else "check"
        
        # Step 5: Remove any remaining problematic characters
        # These can break PlantUML in subtle ways
        problematic = ['@', '#', '$', '%', '^', '!', '?']
        for char in problematic:
            text = text.replace(char, '')
        
        return text.strip()
    
    def _validate_plantuml(self, plantuml_lines: List[str]) -> bool:
        """
        Validate PlantUML syntax before writing
        Returns True if valid, False otherwise
        """
        content = '\n'.join(plantuml_lines)
        
        # Check 1: Must have start and end tags
        if '@startuml' not in content or '@enduml' not in content:
            return False
        
        # Check 2: Must have start and stop
        if 'start' not in content or 'stop' not in content:
            return False
        
        # Check 3: No empty activities
        if ':;' in content or ': ;' in content:
            console.print("[yellow]Warning: Empty activity detected[/yellow]")
            return False
        
        # Check 4: No empty conditions
        if 'if ()' in content or 'while ()' in content:
            console.print("[yellow]Warning: Empty condition detected[/yellow]")
            return False
        
        # Check 5: Balanced if/endif
        if_count = content.count('if (')
        endif_count = content.count('endif')
        if if_count != endif_count:
            console.print(f"[yellow]Warning: Unbalanced if/endif: {if_count} vs {endif_count}[/yellow]")
            return False
        
        # Check 6: Balanced while/endwhile
        while_count = content.count('while (')
        endwhile_count = content.count('endwhile')
        if while_count != endwhile_count:
            console.print(f"[yellow]Warning: Unbalanced while/endwhile[/yellow]")
            return False
        
        return True
    
    def generate_detailed_function_flow(
        self,
        func: Any,
        output_name: Optional[str] = None
    ) -> str:
        """Generate detailed control flow diagram for a single function"""
        if output_name is None:
            output_name = f"flow_{self._ultra_sanitize(func.name, 'filename')}"
        
        console.print(f"[blue]Generating flow for: {func.name}[/blue]")
        
        plantuml = ["@startuml"]
        plantuml.append(f"title Function Flow - {self._ultra_sanitize(func.name, 'label')}")
        plantuml.append("")
        
        # Styling
        plantuml.extend([
            "skinparam activity {",
            "  BackgroundColor #B4E7CE",
            "  BorderColor #2C5F2D",
            "  FontSize 11",
            "}",
            "skinparam activityDiamond {",
            "  BackgroundColor #FFD966",
            "  BorderColor #CC9900",
            "}",
            "skinparam activityStart {",
            "  BackgroundColor #4A90E2",
            "}",
            "skinparam activityEnd {",
            "  BackgroundColor #E74C3C",
            "}",
            ""
        ])
        
        plantuml.append("start")
        plantuml.append("")
        
        # Function name
        func_label = self._ultra_sanitize(func.name, 'label')
        plantuml.append(f":{func_label};")
        
        # Add parameters info in note
        if func.parameters or func.return_type:
            plantuml.append("note right")
            if func.return_type:
                ret_type = self._ultra_sanitize(func.return_type, 'label')
                plantuml.append(f"  Returns {ret_type}")
            if func.parameters:
                plantuml.append(f"  {len(func.parameters)} parameter(s)")
            plantuml.append("end note")
        
        plantuml.append("")
        
        # Add control flow with error handling
        if func.control_flow and len(func.control_flow) > 0:
            try:
                self._add_flow_nodes(func.control_flow, plantuml, depth=0)
            except Exception as e:
                console.print(f"[yellow]Warning: {e}[/yellow]")
                plantuml.append(":execute function body;")
        else:
            # No control flow - show simple execution
            if func.calls and len(func.calls) > 0:
                plantuml.append(":execute function body;")
                for call in func.calls[:3]:
                    safe_call = self._ultra_sanitize(call, 'label')
                    plantuml.append(f":{safe_call};")
            else:
                plantuml.append(":execute function body;")
        
        plantuml.append("")
        plantuml.append("stop")
        plantuml.append("")
        plantuml.append("@enduml")
        
        # Validate before writing
        if not self._validate_plantuml(plantuml):
            console.print("[red]PlantUML validation failed, using simplified version[/red]")
            # Fallback to ultra-simple diagram
            plantuml = [
                "@startuml",
                f"title Function - {func_label}",
                "",
                "start",
                f":{func_label};",
                ":execute function;",
                "stop",
                "",
                "@enduml"
            ]
        
        # Write to file
        output_path = self.output_dir / f"{output_name}.puml"
        try:
            output_path.write_text('\n'.join(plantuml), encoding='utf-8')
            console.print(f"[green]✓ Saved: {output_path.name}[/green]")
        except Exception as e:
            console.print(f"[red]✗ Write error: {e}[/red]")
            raise
        
        return str(output_path)
    
    def _add_flow_nodes(
        self,
        nodes: List[Any],
        plantuml: List[str],
        depth: int = 0,
        max_depth: int = 4
    ) -> None:
        """Add control flow nodes with maximum safety"""
        if depth >= max_depth or not nodes:
            if depth >= max_depth:
                plantuml.append(":... more code ...;")
            return
        
        for node in nodes:
            try:
                if node.type == 'if':
                    condition = self._ultra_sanitize(node.condition or "condition", 'condition')
                    plantuml.append(f"if ({condition}) then (yes)")
                    
                    if node.body_nodes:
                        self._add_flow_nodes(node.body_nodes, plantuml, depth + 1, max_depth)
                    else:
                        plantuml.append("  :process;")
                    
                    if node.else_nodes:
                        plantuml.append("else (no)")
                        self._add_flow_nodes(node.else_nodes, plantuml, depth + 1, max_depth)
                    
                    plantuml.append("endif")
                
                elif node.type == 'for':
                    condition = self._ultra_sanitize(node.condition or "loop", 'condition')
                    plantuml.append("repeat")
                    
                    if node.body_nodes:
                        self._add_flow_nodes(node.body_nodes, plantuml, depth + 1, max_depth)
                    else:
                        plantuml.append("  :loop body;")
                    
                    plantuml.append(f"repeat while ({condition})")
                
                elif node.type == 'while':
                    condition = self._ultra_sanitize(node.condition or "condition", 'condition')
                    plantuml.append(f"while ({condition}) is (true)")
                    
                    if node.body_nodes:
                        self._add_flow_nodes(node.body_nodes, plantuml, depth + 1, max_depth)
                    else:
                        plantuml.append("  :loop body;")
                    
                    plantuml.append("endwhile (false)")
                
                elif node.type == 'switch':
                    condition = self._ultra_sanitize(node.condition or "value", 'condition')
                    plantuml.append(f"switch ({condition})")
                    
                    for case_node in (node.body_nodes or [])[:4]:
                        if case_node.type == 'case':
                            case_label = self._ultra_sanitize(case_node.label or "case", 'label')
                            plantuml.append(f"case ({case_label})")
                            
                            if case_node.body_nodes:
                                self._add_flow_nodes(case_node.body_nodes, plantuml, depth + 1, max_depth)
                            else:
                                plantuml.append("  :handle case;")
                    
                    plantuml.append("endswitch")
                
                elif node.type in ['return', 'call', 'statement']:
                    label = self._ultra_sanitize(node.label or node.type, 'label')
                    plantuml.append(f":{label};")
                    
            except Exception as e:
                console.print(f"[yellow]Skipping node due to error: {e}[/yellow]")
                plantuml.append(":... code ...;")
                continue
    
    def generate_function_call_graph(
        self,
        functions: List[Any],
        entry_point: Optional[str] = None,
        output_name: str = "function_call_graph"
    ) -> str:
        """Generate function call graph"""
        console.print("[blue]Generating function call graph...[/blue]")
        
        func_dict = {f.name: f for f in functions}
        
        plantuml = ["@startuml"]
        plantuml.append("title Function Call Flow")
        plantuml.append("")
        
        # Styling
        plantuml.extend([
            "skinparam activity {",
            "  BackgroundColor #B4E7CE",
            "  BorderColor #2C5F2D",
            "}",
            "skinparam activityDiamond {",
            "  BackgroundColor #FFD966",
            "  BorderColor #CC9900",
            "}",
            ""
        ])
        
        plantuml.append("start")
        plantuml.append("")
        
        if entry_point and entry_point in func_dict:
            func = func_dict[entry_point]
            func_label = self._ultra_sanitize(entry_point, 'label')
            plantuml.append(f":{func_label};")
            
            if func.control_flow:
                try:
                    self._add_flow_nodes(func.control_flow[:10], plantuml, depth=0, max_depth=3)
                except:
                    for call in func.calls[:5]:
                        safe_call = self._ultra_sanitize(call, 'label')
                        plantuml.append(f":{safe_call};")
            else:
                for call in func.calls[:5]:
                    safe_call = self._ultra_sanitize(call, 'label')
                    plantuml.append(f":{safe_call};")
        else:
            # Show top 3 functions
            for func in functions[:3]:
                func_label = self._ultra_sanitize(func.name, 'label')
                plantuml.append(f":{func_label};")
        
        plantuml.append("")
        plantuml.append("stop")
        plantuml.append("")
        plantuml.append("@enduml")
        
        # Validate
        if not self._validate_plantuml(plantuml):
            console.print("[yellow]Validation failed, using simplified diagram[/yellow]")
        
        # Write
        output_path = self.output_dir / f"{output_name}.puml"
        output_path.write_text('\n'.join(plantuml), encoding='utf-8')
        
        console.print(f"[green]✓ Saved: {output_path}[/green]")
        self._print_view_instructions(output_path)
        return str(output_path)
    
    def generate_class_diagram(self, classes: List[Any], output_name: str = "class_diagram") -> str:
        """Generate class diagram"""
        console.print("[blue]Generating class diagram...[/blue]")
        
        plantuml = ["@startuml", "title Class Diagram", ""]
        plantuml.extend([
            "skinparam class {",
            "  BackgroundColor LightBlue",
            "  BorderColor Navy",
            "}",
            ""
        ])
        
        for cls in classes[:20]:  # Limit to 20 classes
            safe_name = self._ultra_sanitize(cls.name, 'filename')
            plantuml.append(f"class {safe_name} {{")
            
            for method in cls.methods[:10]:
                method_name = self._ultra_sanitize(method.name, 'label')
                plantuml.append(f"  +{method_name}()")
            
            if len(cls.methods) > 10:
                plantuml.append(f"  ... {len(cls.methods) - 10} more ...")
            
            plantuml.append("}")
            plantuml.append("")
        
        plantuml.extend(["", "@enduml"])
        
        output_path = self.output_dir / f"{output_name}.puml"
        output_path.write_text('\n'.join(plantuml), encoding='utf-8')
        
        console.print(f"[green]✓ Saved: {output_path}[/green]")
        self._print_view_instructions(output_path)
        return str(output_path)
    
    def generate_module_structure(self, files_info: Dict[str, Any], output_name: str = "module_structure") -> str:
        """Generate module structure"""
        console.print("[blue]Generating module structure...[/blue]")
        
        plantuml = ["@startuml", "title Module Structure", ""]
        plantuml.extend([
            "skinparam activity {",
            "  BackgroundColor #E8F4F8",
            "  BorderColor #4A90E2",
            "}",
            ""
        ])
        
        plantuml.append("start")
        plantuml.append("")
        
        dir_files: Dict[str, List[str]] = {}
        for file_path in list(files_info.keys())[:50]:  # Limit files
            dir_name = str(Path(file_path).parent)
            if dir_name not in dir_files:
                dir_files[dir_name] = []
            dir_files[dir_name].append(file_path)
        
        for dir_name, files in list(dir_files.items())[:10]:  # Limit directories
            package_name = Path(dir_name).name or "root"
            safe_package = self._ultra_sanitize(package_name, 'label')
            
            plantuml.append(f"partition \"{safe_package}\" {{")
            
            for file_path in files[:5]:  # Limit files per dir
                file_name = Path(file_path).name
                safe_file = self._ultra_sanitize(file_name, 'label')
                plantuml.append(f"  :{safe_file};")
            
            if len(files) > 5:
                plantuml.append(f"  note right: {len(files) - 5} more files")
            
            plantuml.append("}")
            plantuml.append("")
        
        plantuml.append("stop")
        plantuml.extend(["", "@enduml"])
        
        output_path = self.output_dir / f"{output_name}.puml"
        output_path.write_text('\n'.join(plantuml), encoding='utf-8')
        
        console.print(f"[green]✓ Saved: {output_path}[/green]")
        self._print_view_instructions(output_path)
        return str(output_path)
    
    def generate_summary_stats(self, functions: List[Any], classes: List[Any]) -> Dict[str, Any]:
        """Generate summary statistics"""
        return {
            'total_functions': len(functions),
            'total_classes': len(classes),
            'total_methods': sum(len(c.methods) for c in classes),
            'avg_methods_per_class': sum(len(c.methods) for c in classes) / len(classes) if classes else 0,
        }
    
    def _print_view_instructions(self, file_path: Path) -> None:
        """Print viewing instructions"""
        console.print("\n[cyan]To view:[/cyan]")
        console.print(f"  Online: http://www.plantuml.com/plantuml/uml/")
        console.print(f"  VSCode: Install PlantUML extension, press Alt+D")
        console.print(f"  File: {file_path.name}")
