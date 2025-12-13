"""
C++ Code Parser using tree-sitter
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser, Node
from rich.progress import Progress, SpinnerColumn, TextColumn


@dataclass
class ControlFlowNode:
    """Represents a control flow node"""
    type: str  # 'if', 'else', 'for', 'while', 'switch', 'case', 'return', 'call', 'statement'
    condition: Optional[str] = None
    body_nodes: List['ControlFlowNode'] = None
    else_nodes: List['ControlFlowNode'] = None
    label: Optional[str] = None
    
    def __post_init__(self):
        if self.body_nodes is None:
            self.body_nodes = []
        if self.else_nodes is None:
            self.else_nodes = []


@dataclass
class FunctionInfo:
    """Information about a C++ function"""
    name: str
    return_type: str
    parameters: List[str]
    body: str
    file_path: str
    line_number: int
    docstring: Optional[str] = None
    calls: List[str] = None  # Functions called by this function
    control_flow: List[ControlFlowNode] = None  # Control flow graph
    
    def __post_init__(self):
        if self.calls is None:
            self.calls = []
        if self.control_flow is None:
            self.control_flow = []


@dataclass
class ClassInfo:
    """Information about a C++ class"""
    name: str
    methods: List[FunctionInfo]
    file_path: str
    line_number: int
    base_classes: List[str] = None
    
    def __post_init__(self):
        if self.base_classes is None:
            self.base_classes = []


class CPPCodeParser:
    """Parse C++ code and extract information"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize C++ parser
        
        Args:
            config: Parser configuration
        """
        self.config = config
        self.file_extensions = config.get('file_extensions', ['.cpp', '.h', '.hpp'])
        self.ignore_dirs = config.get('ignore_dirs', [])
        self.max_file_size_mb = config.get('max_file_size_mb', 10)
        
        # Initialize tree-sitter parser
        self.parser = Parser()
        self.language = Language(tscpp.language())
        self.parser.language = self.language
        
        # Store parsed data
        self.functions: List[FunctionInfo] = []
        self.classes: List[ClassInfo] = []
        self.files_content: Dict[str, str] = {}
        
    def parse_project(self, project_path: str) -> None:
        """
        Parse entire C++ project
        
        Args:
            project_path: Root path of the project
        """
        project_path = Path(project_path)
        
        if not project_path.exists():
            raise FileNotFoundError(f"Project path not found: {project_path}")
        
        # Find all C++ files
        cpp_files = self._find_cpp_files(project_path)
        
        print(f"Found {len(cpp_files)} C++ files to parse")
        
        # Parse each file
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task("Parsing C++ files...", total=len(cpp_files))
            
            for file_path in cpp_files:
                try:
                    self._parse_file(file_path)
                    progress.update(task, advance=1)
                except Exception as e:
                    print(f"Error parsing {file_path}: {e}")
                    progress.update(task, advance=1)
        
        print(f"Parsed {len(self.functions)} functions and {len(self.classes)} classes")
    
    def _find_cpp_files(self, root_path: Path) -> List[Path]:
        """Find all C++ files in the project"""
        cpp_files = []
        
        for file_path in root_path.rglob('*'):
            # Skip ignored directories
            if any(ignored in file_path.parts for ignored in self.ignore_dirs):
                continue
            
            # Check file extension
            if file_path.suffix in self.file_extensions:
                # Check file size
                if file_path.is_file():
                    size_mb = file_path.stat().st_size / (1024 * 1024)
                    if size_mb <= self.max_file_size_mb:
                        cpp_files.append(file_path)
        
        return cpp_files
    
    def _parse_file(self, file_path: Path) -> None:
        """Parse a single C++ file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return
        
        # Store file content
        self.files_content[str(file_path)] = content
        
        # Parse with tree-sitter
        tree = self.parser.parse(bytes(content, 'utf8'))
        root_node = tree.root_node
        
        # Extract functions and classes
        self._extract_functions(root_node, content, str(file_path))
        self._extract_classes(root_node, content, str(file_path))
    
    def _extract_functions(self, node: Node, content: str, file_path: str) -> None:
        """Extract function definitions from AST"""
        if node.type == 'function_definition':
            func_info = self._parse_function_node(node, content, file_path)
            if func_info:
                self.functions.append(func_info)
        
        # Recursively process children
        for child in node.children:
            self._extract_functions(child, content, file_path)
    
    def _extract_classes(self, node: Node, content: str, file_path: str) -> None:
        """Extract class definitions from AST"""
        if node.type in ['class_specifier', 'struct_specifier']:
            class_info = self._parse_class_node(node, content, file_path)
            if class_info:
                self.classes.append(class_info)
        
        # Recursively process children
        for child in node.children:
            self._extract_classes(child, content, file_path)
    
    def _parse_function_node(self, node: Node, content: str, file_path: str) -> Optional[FunctionInfo]:
        """Parse a function node"""
        try:
            # Get function name
            declarator = self._find_child_by_type(node, 'function_declarator')
            if not declarator:
                return None
            
            identifier = self._find_child_by_type(declarator, 'identifier')
            if not identifier:
                # Try field_identifier for member functions
                identifier = self._find_child_by_type(declarator, 'field_identifier')
            
            if not identifier:
                return None
            
            func_name = content[identifier.start_byte:identifier.end_byte]
            
            # Get return type
            return_type = self._get_return_type(node, content)
            
            # Get parameters
            parameters = self._get_parameters(declarator, content)
            
            # Get function body
            body_node = self._find_child_by_type(node, 'compound_statement')
            body = content[body_node.start_byte:body_node.end_byte] if body_node else ""
            
            # Get function calls
            calls = self._extract_function_calls(body_node, content) if body_node else []
            
            # Extract control flow
            control_flow = self._extract_control_flow(body_node, content) if body_node else []
            
            return FunctionInfo(
                name=func_name,
                return_type=return_type,
                parameters=parameters,
                body=body,
                file_path=file_path,
                line_number=node.start_point[0] + 1,
                calls=calls,
                control_flow=control_flow
            )
        except Exception as e:
            return None
    
    def _parse_class_node(self, node: Node, content: str, file_path: str) -> Optional[ClassInfo]:
        """Parse a class node"""
        try:
            # Get class name
            name_node = self._find_child_by_type(node, 'type_identifier')
            if not name_node:
                return None
            
            class_name = content[name_node.start_byte:name_node.end_byte]
            
            # Get base classes
            base_classes = self._get_base_classes(node, content)
            
            # Get member functions
            body_node = self._find_child_by_type(node, 'field_declaration_list')
            methods = []
            if body_node:
                for child in body_node.children:
                    if child.type == 'function_definition':
                        method = self._parse_function_node(child, content, file_path)
                        if method:
                            methods.append(method)
            
            return ClassInfo(
                name=class_name,
                methods=methods,
                file_path=file_path,
                line_number=node.start_point[0] + 1,
                base_classes=base_classes
            )
        except Exception:
            return None
    
    def _find_child_by_type(self, node: Node, type_name: str) -> Optional[Node]:
        """Find first child node with given type"""
        for child in node.children:
            if child.type == type_name:
                return child
        return None
    
    def _get_return_type(self, node: Node, content: str) -> str:
        """Get function return type"""
        for child in node.children:
            if child.type in ['primitive_type', 'type_identifier', 'qualified_identifier']:
                return content[child.start_byte:child.end_byte]
        return "void"
    
    def _get_parameters(self, declarator: Node, content: str) -> List[str]:
        """Get function parameters"""
        params = []
        param_list = self._find_child_by_type(declarator, 'parameter_list')
        if param_list:
            for child in param_list.children:
                if child.type == 'parameter_declaration':
                    param_text = content[child.start_byte:child.end_byte]
                    params.append(param_text)
        return params
    
    def _get_base_classes(self, node: Node, content: str) -> List[str]:
        """Get class base classes"""
        base_classes = []
        base_clause = self._find_child_by_type(node, 'base_class_clause')
        if base_clause:
            for child in base_clause.children:
                if child.type in ['type_identifier', 'qualified_identifier']:
                    base_classes.append(content[child.start_byte:child.end_byte])
        return base_classes
    
    def _extract_function_calls(self, node: Node, content: str) -> List[str]:
        """Extract function calls from a node"""
        calls = []
        
        if node.type == 'call_expression':
            func_node = node.children[0] if node.children else None
            if func_node:
                call_name = content[func_node.start_byte:func_node.end_byte]
                calls.append(call_name)
        
        for child in node.children:
            calls.extend(self._extract_function_calls(child, content))
        
        return calls
    
    def _extract_control_flow(self, node: Node, content: str, depth: int = 0) -> List[ControlFlowNode]:
        """Extract control flow structures from a node"""
        flow_nodes = []
        
        if not node:
            return flow_nodes
        
        # Limit recursion depth
        if depth > 10:
            return flow_nodes
        
        for child in node.children:
            if child.type == 'if_statement':
                flow_node = self._parse_if_statement(child, content, depth)
                if flow_node:
                    flow_nodes.append(flow_node)
            
            elif child.type == 'for_statement':
                flow_node = self._parse_for_statement(child, content, depth)
                if flow_node:
                    flow_nodes.append(flow_node)
            
            elif child.type == 'while_statement':
                flow_node = self._parse_while_statement(child, content, depth)
                if flow_node:
                    flow_nodes.append(flow_node)
            
            elif child.type == 'switch_statement':
                flow_node = self._parse_switch_statement(child, content, depth)
                if flow_node:
                    flow_nodes.append(flow_node)
            
            elif child.type == 'return_statement':
                return_expr = content[child.start_byte:child.end_byte].strip()
                flow_nodes.append(ControlFlowNode(
                    type='return',
                    label=return_expr[:50]  # Limit length
                ))
            
            elif child.type == 'call_expression':
                call_name = self._get_call_name(child, content)
                if call_name:
                    flow_nodes.append(ControlFlowNode(
                        type='call',
                        label=call_name
                    ))
            
            elif child.type == 'expression_statement':
                # Check if it contains a call
                call_expr = self._find_child_by_type(child, 'call_expression')
                if call_expr:
                    call_name = self._get_call_name(call_expr, content)
                    if call_name:
                        flow_nodes.append(ControlFlowNode(
                            type='call',
                            label=call_name
                        ))
                else:
                    # Generic statement
                    stmt = content[child.start_byte:child.end_byte].strip()
                    if stmt and len(stmt) < 100:
                        flow_nodes.append(ControlFlowNode(
                            type='statement',
                            label=stmt[:50]
                        ))
        
        return flow_nodes
    
    def _parse_if_statement(self, node: Node, content: str, depth: int) -> Optional[ControlFlowNode]:
        """Parse if statement"""
        try:
            # Get condition
            condition_node = self._find_child_by_type(node, 'condition_clause')
            if not condition_node:
                condition_node = self._find_child_by_type(node, 'parenthesized_expression')
            
            condition = "condition"
            if condition_node:
                condition = content[condition_node.start_byte:condition_node.end_byte]
                # Simplify condition
                condition = condition.replace('\n', ' ').strip()
                if len(condition) > 50:
                    condition = condition[:47] + "..."
            
            # Get then body
            then_body = None
            else_body = None
            
            for child in node.children:
                if child.type == 'compound_statement' and not then_body:
                    then_body = child
                elif child.type in ['if_statement', 'compound_statement'] and then_body:
                    else_body = child
                    break
            
            # Extract flow from bodies
            then_nodes = []
            if then_body:
                then_nodes = self._extract_control_flow(then_body, content, depth + 1)
            
            else_nodes = []
            if else_body:
                else_nodes = self._extract_control_flow(else_body, content, depth + 1)
            
            return ControlFlowNode(
                type='if',
                condition=condition,
                body_nodes=then_nodes,
                else_nodes=else_nodes
            )
        except Exception:
            return None
    
    def _parse_for_statement(self, node: Node, content: str, depth: int) -> Optional[ControlFlowNode]:
        """Parse for loop"""
        try:
            # Get condition/init
            condition = "loop"
            for child in node.children:
                if '(' in content[child.start_byte:child.end_byte]:
                    condition_text = content[child.start_byte:child.end_byte]
                    condition = condition_text.replace('\n', ' ').strip()
                    if len(condition) > 50:
                        condition = "for loop"
                    break
            
            # Get body
            body_node = self._find_child_by_type(node, 'compound_statement')
            body_nodes = []
            if body_node:
                body_nodes = self._extract_control_flow(body_node, content, depth + 1)
            
            return ControlFlowNode(
                type='for',
                condition=condition,
                body_nodes=body_nodes
            )
        except Exception:
            return None
    
    def _parse_while_statement(self, node: Node, content: str, depth: int) -> Optional[ControlFlowNode]:
        """Parse while loop"""
        try:
            # Get condition
            condition_node = self._find_child_by_type(node, 'condition_clause')
            if not condition_node:
                condition_node = self._find_child_by_type(node, 'parenthesized_expression')
            
            condition = "loop"
            if condition_node:
                condition = content[condition_node.start_byte:condition_node.end_byte]
                condition = condition.replace('\n', ' ').strip()
                if len(condition) > 50:
                    condition = "while loop"
            
            # Get body
            body_node = self._find_child_by_type(node, 'compound_statement')
            body_nodes = []
            if body_node:
                body_nodes = self._extract_control_flow(body_node, content, depth + 1)
            
            return ControlFlowNode(
                type='while',
                condition=condition,
                body_nodes=body_nodes
            )
        except Exception:
            return None
    
    def _parse_switch_statement(self, node: Node, content: str, depth: int) -> Optional[ControlFlowNode]:
        """Parse switch statement"""
        try:
            # Get condition
            condition_node = self._find_child_by_type(node, 'condition_clause')
            if not condition_node:
                condition_node = self._find_child_by_type(node, 'parenthesized_expression')
            
            condition = "switch"
            if condition_node:
                condition = content[condition_node.start_byte:condition_node.end_byte]
                condition = condition.replace('\n', ' ').strip()
                if len(condition) > 50:
                    condition = "switch"
            
            # Get cases
            body_node = self._find_child_by_type(node, 'compound_statement')
            body_nodes = []
            if body_node:
                for child in body_node.children:
                    if child.type in ['case_statement', 'default_statement']:
                        case_label = content[child.start_byte:child.start_byte + 30].strip()
                        case_nodes = self._extract_control_flow(child, content, depth + 1)
                        body_nodes.append(ControlFlowNode(
                            type='case',
                            label=case_label,
                            body_nodes=case_nodes
                        ))
            
            return ControlFlowNode(
                type='switch',
                condition=condition,
                body_nodes=body_nodes
            )
        except Exception:
            return None
    
    def _get_call_name(self, node: Node, content: str) -> Optional[str]:
        """Get function call name from call_expression"""
        if not node or node.type != 'call_expression':
            return None
        
        func_node = node.children[0] if node.children else None
        if func_node:
            call_name = content[func_node.start_byte:func_node.end_byte]
            # Simplify nested calls
            if len(call_name) > 50:
                call_name = call_name[:47] + "..."
            return call_name
        return None
    
    def get_code_chunks(self) -> List[Dict[str, str]]:
        """
        Get code chunks for RAG
        
        Returns:
            List of code chunks with metadata
        """
        chunks = []
        
        # Add function chunks
        for func in self.functions:
            chunk = {
                'content': f"Function: {func.name}\n"
                          f"Return Type: {func.return_type}\n"
                          f"Parameters: {', '.join(func.parameters)}\n"
                          f"File: {func.file_path}\n"
                          f"Line: {func.line_number}\n\n"
                          f"{func.body}",
                'metadata': {
                    'type': 'function',
                    'name': func.name,
                    'file': func.file_path,
                    'line': func.line_number
                }
            }
            chunks.append(chunk)
        
        # Add class chunks
        for cls in self.classes:
            methods_text = '\n'.join([f"  - {m.name}({', '.join(m.parameters)})" for m in cls.methods])
            chunk = {
                'content': f"Class: {cls.name}\n"
                          f"Base Classes: {', '.join(cls.base_classes) if cls.base_classes else 'None'}\n"
                          f"File: {cls.file_path}\n"
                          f"Line: {cls.line_number}\n"
                          f"Methods:\n{methods_text}",
                'metadata': {
                    'type': 'class',
                    'name': cls.name,
                    'file': cls.file_path,
                    'line': cls.line_number
                }
            }
            chunks.append(chunk)
        
        return chunks

