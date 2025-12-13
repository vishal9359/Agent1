"""
AST-Based C++ Parser - Clean Implementation
Uses tree-sitter to parse C++ and extract semantic units
"""

from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field
import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser, Node
from rich.console import Console

console = Console()


@dataclass
class ASTChunk:
    """Represents a semantic chunk from AST"""
    chunk_type: str  # 'function', 'class', 'namespace'
    name: str
    content: str  # Full source code
    ast_node: Any  # tree-sitter Node reference
    file_path: str
    line_start: int
    line_end: int
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FunctionAST:
    """Function extracted from AST"""
    name: str
    return_type: str
    parameters: List[str]
    body_node: Optional[Node] = None
    file_path: str = ""
    line_number: int = 0
    namespace: str = ""
    class_name: str = ""
    is_method: bool = False


@dataclass
class ClassAST:
    """Class extracted from AST"""
    name: str
    methods: List[FunctionAST] = field(default_factory=list)
    base_classes: List[str] = field(default_factory=list)
    file_path: str = ""
    line_number: int = 0
    namespace: str = ""


class ASTParser:
    """Parse C++ code using tree-sitter AST"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.file_extensions = config.get('file_extensions', ['.cpp', '.h', '.hpp'])
        self.ignore_dirs = config.get('ignore_dirs', [])
        self.max_file_size_mb = config.get('max_file_size_mb', 10)
        
        # Initialize parser
        self.parser = Parser()
        self.language = Language(tscpp.language())
        self.parser.language = self.language
        
        # Storage
        self.functions: List[FunctionAST] = []
        self.classes: List[ClassAST] = []
        self.chunks: List[ASTChunk] = []
        self.files_content: Dict[str, str] = {}
    
    def parse_project(self, project_path: str) -> None:
        """Parse entire C++ project"""
        project_path = Path(project_path)
        if not project_path.exists():
            raise FileNotFoundError(f"Project path not found: {project_path}")
        
        cpp_files = self._find_cpp_files(project_path)
        console.print(f"[blue]Found {len(cpp_files)} C++ files[/blue]")
        
        for file_path in cpp_files:
            try:
                self._parse_file(file_path)
            except Exception as e:
                console.print(f"[yellow]Warning: Error parsing {file_path}: {e}[/yellow]")
        
        console.print(f"[green]✓ Parsed {len(self.functions)} functions, {len(self.classes)} classes[/green]")
    
    def _find_cpp_files(self, root_path: Path) -> List[Path]:
        """Find all C++ files"""
        cpp_files = []
        for file_path in root_path.rglob('*'):
            if any(ignored in file_path.parts for ignored in self.ignore_dirs):
                continue
            if file_path.suffix in self.file_extensions and file_path.is_file():
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
            console.print(f"[red]Error reading {file_path}: {e}[/red]")
            return
        
        self.files_content[str(file_path)] = content
        
        # Parse AST
        tree = self.parser.parse(bytes(content, 'utf8'))
        root_node = tree.root_node
        
        # Extract semantic units
        self._extract_from_ast(root_node, content, str(file_path), "")
    
    def _extract_from_ast(self, node: Node, content: str, file_path: str, namespace: str) -> None:
        """Recursively extract functions and classes from AST"""
        if node.type == 'function_definition':
            func = self._parse_function(node, content, file_path, namespace)
            if func:
                self.functions.append(func)
                # Create chunk
                chunk = ASTChunk(
                    chunk_type='function',
                    name=func.name,
                    content=content[node.start_byte:node.end_byte],
                    ast_node=node,
                    file_path=file_path,
                    line_start=node.start_point[0] + 1,
                    line_end=node.end_point[0] + 1,
                    metadata={
                        'return_type': func.return_type,
                        'parameters': func.parameters,
                        'namespace': func.namespace,
                        'class_name': func.class_name,
                        'is_method': func.is_method
                    }
                )
                self.chunks.append(chunk)
        
        elif node.type in ['class_specifier', 'struct_specifier']:
            cls = self._parse_class(node, content, file_path, namespace)
            if cls:
                self.classes.append(cls)
                # Create chunk
                chunk = ASTChunk(
                    chunk_type='class',
                    name=cls.name,
                    content=content[node.start_byte:node.end_byte],
                    ast_node=node,
                    file_path=file_path,
                    line_start=node.start_point[0] + 1,
                    line_end=node.end_point[0] + 1,
                    metadata={
                        'base_classes': cls.base_classes,
                        'namespace': cls.namespace,
                        'method_count': len(cls.methods)
                    }
                )
                self.chunks.append(chunk)
        
        elif node.type == 'namespace_definition':
            # Extract namespace name and recurse
            name_node = self._find_child(node, 'namespace')
            if name_node and name_node.next_sibling:
                ns_name = content[name_node.next_sibling.start_byte:name_node.next_sibling.end_byte]
                new_namespace = f"{namespace}::{ns_name}" if namespace else ns_name
            else:
                new_namespace = namespace
            
            # Recurse into namespace body
            body = self._find_child(node, 'declaration_list') or self._find_child(node, 'compound_statement')
            if body:
                for child in body.children:
                    self._extract_from_ast(child, content, file_path, new_namespace)
            return
        
        # Recurse into children
        for child in node.children:
            self._extract_from_ast(child, content, file_path, namespace)
    
    def _parse_function(self, node: Node, content: str, file_path: str, namespace: str) -> Optional[FunctionAST]:
        """Parse function from AST node"""
        try:
            # Get function declarator
            declarator = self._find_child(node, 'function_declarator')
            if not declarator:
                return None
            
            # Get function name
            identifier = self._find_child(declarator, 'identifier') or self._find_child(declarator, 'field_identifier')
            if not identifier:
                return None
            
            name = content[identifier.start_byte:identifier.end_byte]
            
            # Get return type
            return_type = "void"
            for child in node.children:
                if child.type in ['primitive_type', 'type_identifier', 'qualified_identifier']:
                    return_type = content[child.start_byte:child.end_byte]
                    break
            
            # Get parameters
            params = []
            param_list = self._find_child(declarator, 'parameter_list')
            if param_list:
                for child in param_list.children:
                    if child.type == 'parameter_declaration':
                        params.append(content[child.start_byte:child.end_byte])
            
            # Get body
            body_node = self._find_child(node, 'compound_statement')
            
            # Check if it's a method (inside a class)
            class_name = ""
            is_method = False
            parent = node.parent
            while parent:
                if parent.type in ['class_specifier', 'struct_specifier']:
                    class_node = self._find_child(parent, 'type_identifier')
                    if class_node:
                        class_name = content[class_node.start_byte:class_node.end_byte]
                        is_method = True
                    break
                parent = parent.parent
            
            return FunctionAST(
                name=name,
                return_type=return_type,
                parameters=params,
                body_node=body_node,
                file_path=file_path,
                line_number=node.start_point[0] + 1,
                namespace=namespace,
                class_name=class_name,
                is_method=is_method
            )
        except Exception:
            return None
    
    def _parse_class(self, node: Node, content: str, file_path: str, namespace: str) -> Optional[ClassAST]:
        """Parse class from AST node"""
        try:
            name_node = self._find_child(node, 'type_identifier')
            if not name_node:
                return None
            
            name = content[name_node.start_byte:name_node.end_byte]
            
            # Get base classes
            base_classes = []
            base_clause = self._find_child(node, 'base_class_clause')
            if base_clause:
                for child in base_clause.children:
                    if child.type in ['type_identifier', 'qualified_identifier']:
                        base_classes.append(content[child.start_byte:child.end_byte])
            
            # Get methods
            methods = []
            body = self._find_child(node, 'field_declaration_list')
            if body:
                for child in body.children:
                    if child.type == 'function_definition':
                        method = self._parse_function(child, content, file_path, namespace)
                        if method:
                            method.class_name = name
                            method.is_method = True
                            methods.append(method)
            
            return ClassAST(
                name=name,
                methods=methods,
                base_classes=base_classes,
                file_path=file_path,
                line_number=node.start_point[0] + 1,
                namespace=namespace
            )
        except Exception:
            return None
    
    def _find_child(self, node: Node, type_name: str) -> Optional[Node]:
        """Find first child with given type"""
        for child in node.children:
            if child.type == type_name:
                return child
        return None
    
    def get_ast_chunks(self) -> List[ASTChunk]:
        """Get all AST-based chunks for RAG"""
        return self.chunks
    
    def get_functions(self) -> List[FunctionAST]:
        """Get all functions"""
        return self.functions
    
    def get_classes(self) -> List[ClassAST]:
        """Get all classes"""
        return self.classes
