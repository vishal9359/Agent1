"""
PlantUML Diagram Generator - AST-Based
Generates diagrams directly from AST structure
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
from rich.console import Console
from .ast_parser import FunctionAST, ClassAST, ASTChunk

console = Console()


class DiagramGenerator:
    """Generate PlantUML diagrams from AST"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.output_dir = Path(config.get('output_dir', './diagrams'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.max_depth = config.get('max_depth', 5)
    
    def generate_function_flow(self, func: FunctionAST, content: str = "", output_name: Optional[str] = None) -> str:
        """Generate function flow diagram from AST"""
        if output_name is None:
            output_name = f"flow_{self._safe_name(func.name)}"
        
        console.print(f"[blue]Generating flow for: {func.name}[/blue]")
        
        plantuml = [
            "@startuml",
            f"title Function Flow - {func.name}",
            "",
            "skinparam activity {",
            "  BackgroundColor #B4E7CE",
            "  BorderColor #2C5F2D",
            "}",
            "skinparam activityDiamond {",
            "  BackgroundColor #FFD966",
            "  BorderColor #CC9900",
            "}",
            "",
            "start",
            "",
            f":{self._safe_label(func.name)};",
            ""
        ]
        
        # Add note
        if func.return_type or func.parameters:
            plantuml.append("note right")
            if func.return_type:
                plantuml.append(f"  Returns {self._safe_label(func.return_type)}")
            if func.parameters:
                plantuml.append(f"  {len(func.parameters)} parameter(s)")
            plantuml.append("end note")
            plantuml.append("")
        
        # Generate flow from AST body
        if func.body_node and content:
            try:
                self._ast_to_plantuml(func.body_node, content, plantuml, depth=0)
            except Exception as e:
                console.print(f"[yellow]Warning: {e}[/yellow]")
                plantuml.append(":execute function body;")
        else:
            plantuml.append(":execute function body;")
        
        plantuml.extend([
            "",
            "stop",
            "",
            "@enduml"
        ])
        
        # Write file
        output_path = self.output_dir / f"{output_name}.puml"
        output_path.write_text('\n'.join(plantuml), encoding='utf-8')
        console.print(f"[green]✓ Saved: {output_path.name}[/green]")
        
        return str(output_path)
    
    def _ast_to_plantuml(self, node: Any, content: str, plantuml: List[str], depth: int = 0) -> None:
        """Convert AST node to PlantUML"""
        if depth >= self.max_depth or not node:
            return
        
        indent = "  " * depth
        
        # Handle different node types
        if node.type == 'if_statement':
            self._handle_if(node, content, plantuml, indent, depth)
        elif node.type == 'for_statement':
            self._handle_for(node, content, plantuml, indent, depth)
        elif node.type == 'while_statement':
            self._handle_while(node, content, plantuml, indent, depth)
        elif node.type == 'switch_statement':
            self._handle_switch(node, content, plantuml, indent, depth)
        elif node.type == 'return_statement':
            plantuml.append(f"{indent}:return;")
        elif node.type == 'call_expression':
            # Extract function name
            if node.children:
                func_name = self._get_node_text(node.children[0], content)
                if func_name:
                    plantuml.append(f"{indent}:{self._safe_label(func_name)};")
        elif node.type == 'compound_statement':
            # Process statements in body
            for child in node.children:
                if child.type != '{' and child.type != '}':
                    self._ast_to_plantuml(child, content, plantuml, depth)
        else:
            # Process children
            for child in node.children:
                self._ast_to_plantuml(child, content, plantuml, depth)
    
    def _handle_if(self, node: Any, content: str, plantuml: List[str], indent: str, depth: int) -> None:
        """Handle if statement"""
        condition = self._extract_condition(node, content)
        safe_cond = self._safe_condition(condition)
        
        plantuml.append(f"{indent}if ({safe_cond}) then (yes)")
        
        then_body = self._find_body(node)
        if then_body:
            self._ast_to_plantuml(then_body, content, plantuml, depth + 1)
        else:
            plantuml.append(f"{indent}  :process;")
        
        else_body = self._find_else(node)
        if else_body:
            plantuml.append(f"{indent}else (no)")
            self._ast_to_plantuml(else_body, content, plantuml, depth + 1)
        
        plantuml.append(f"{indent}endif")
    
    def _handle_for(self, node: Any, content: str, plantuml: List[str], indent: str, depth: int) -> None:
        """Handle for loop"""
        condition = self._extract_for_condition(node, content)
        safe_cond = self._safe_condition(condition)
        
        plantuml.append(f"{indent}repeat")
        
        body = self._find_body(node)
        if body:
            self._ast_to_plantuml(body, content, plantuml, depth + 1)
        else:
            plantuml.append(f"{indent}  :loop body;")
        
        plantuml.append(f"{indent}repeat while ({safe_cond})")
    
    def _handle_while(self, node: Any, content: str, plantuml: List[str], indent: str, depth: int) -> None:
        """Handle while loop"""
        condition = self._extract_condition(node, content)
        safe_cond = self._safe_condition(condition)
        
        plantuml.append(f"{indent}while ({safe_cond}) is (true)")
        
        body = self._find_body(node)
        if body:
            self._ast_to_plantuml(body, content, plantuml, depth + 1)
        else:
            plantuml.append(f"{indent}  :loop body;")
        
        plantuml.append(f"{indent}endwhile (false)")
    
    def _handle_switch(self, node: Any, content: str, plantuml: List[str], indent: str, depth: int) -> None:
        """Handle switch statement"""
        condition = self._extract_condition(node, content)
        safe_cond = self._safe_condition(condition)
        
        plantuml.append(f"{indent}switch ({safe_cond})")
        
        body = self._find_body(node)
        if body:
            for child in body.children:
                if child.type == 'case_statement':
                    case_label = self._get_case_label(child, content)
                    plantuml.append(f"{indent}case ({self._safe_label(case_label)})")
                    self._ast_to_plantuml(child, content, plantuml, depth + 1)
                elif child.type == 'default_statement':
                    plantuml.append(f"{indent}case (default)")
                    self._ast_to_plantuml(child, content, plantuml, depth + 1)
        
        plantuml.append(f"{indent}endswitch")
    
    def _extract_condition(self, node: Any, content: str) -> str:
        """Extract condition text from node"""
        for child in node.children:
            if child.type in ['condition_clause', 'parenthesized_expression']:
                if child.children:
                    return self._get_node_text(child.children[0], content)
        return "condition"
    
    def _extract_for_condition(self, node: Any, content: str) -> str:
        """Extract for loop condition"""
        for child in node.children:
            if child.type == 'for_range_loop':
                return "range loop"
            elif '(' in str(child.type):
                if len(child.children) > 1:
                    return self._get_node_text(child.children[1], content)
        return "loop"
    
    def _find_body(self, node: Any) -> Optional[Any]:
        """Find body of control structure"""
        for child in node.children:
            if child.type == 'compound_statement':
                return child
        return None
    
    def _find_else(self, node: Any) -> Optional[Any]:
        """Find else clause"""
        found_then = False
        for child in node.children:
            if child.type == 'compound_statement':
                found_then = True
            elif found_then and child.type in ['if_statement', 'compound_statement']:
                return child
        return None
    
    def _get_case_label(self, node: Any, content: str) -> str:
        """Get case label"""
        for child in node.children:
            if child.type in ['case', 'default']:
                if child.next_sibling:
                    return self._get_node_text(child.next_sibling, content)
        return "case"
    
    def _get_node_text(self, node: Any, content: str) -> str:
        """Get text from node using content"""
        try:
            return content[node.start_byte:node.end_byte].strip()
        except:
            return node.type.replace('_', ' ')
    
    def _safe_label(self, text: str) -> str:
        """Make label safe for PlantUML"""
        if not text:
            return "item"
        # Remove colons and semicolons
        text = str(text).replace(':', ' ').replace(';', '').strip()
        # Limit length
        if len(text) > 50:
            text = text[:47] + "..."
        return text or "item"
    
    def _safe_condition(self, text: str) -> str:
        """Make condition safe for PlantUML"""
        if not text:
            return "check"
        # More aggressive sanitization for conditions
        text = str(text).replace(':', ' ').replace(';', '').replace('|', ' or ')
        text = text.replace('[', '(').replace(']', ')')
        text = text.strip()
        if len(text) > 40:
            text = text[:37] + "..."
        return text or "check"
    
    def _safe_name(self, name: str) -> str:
        """Make name safe for filename"""
        import re
        safe = re.sub(r'[^a-zA-Z0-9_]', '_', str(name))
        return safe[:50] or "function"
    
    def generate_module_diagram(self, chunks: List[ASTChunk], output_name: str = "module_diagram") -> str:
        """Generate module structure diagram"""
        console.print("[blue]Generating module diagram...[/blue]")
        
        plantuml = [
            "@startuml",
            "title Module Structure",
            "",
            "skinparam activity {",
            "  BackgroundColor #E8F4F8",
            "  BorderColor #4A90E2",
            "}",
            "",
            "start",
            ""
        ]
        
        # Group by file
        files = {}
        for chunk in chunks:
            file_path = Path(chunk.file_path)
            dir_name = file_path.parent.name or "root"
            if dir_name not in files:
                files[dir_name] = []
            files[dir_name].append(chunk)
        
        # Add partitions
        for dir_name, dir_chunks in list(files.items())[:10]:
            plantuml.append(f'partition "{self._safe_label(dir_name)}" {{')
            for chunk in dir_chunks[:5]:
                plantuml.append(f"  :{self._safe_label(chunk.name)};")
            if len(dir_chunks) > 5:
                plantuml.append(f"  note right: {len(dir_chunks) - 5} more")
            plantuml.append("}")
            plantuml.append("")
        
        plantuml.extend([
            "stop",
            "",
            "@enduml"
        ])
        
        output_path = self.output_dir / f"{output_name}.puml"
        output_path.write_text('\n'.join(plantuml), encoding='utf-8')
        console.print(f"[green]✓ Saved: {output_path.name}[/green]")
        
        return str(output_path)
