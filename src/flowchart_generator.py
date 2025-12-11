"""
Flowchart Generator for C++ projects
"""

from typing import List, Dict, Any, Set, Optional
from pathlib import Path
import graphviz
from dataclasses import dataclass
from rich.console import Console

console = Console()


@dataclass
class FlowNode:
    """Represents a node in the flowchart"""
    id: str
    label: str
    node_type: str  # function, class, file, module
    shape: str = "box"
    color: str = "lightblue"


@dataclass
class FlowEdge:
    """Represents an edge in the flowchart"""
    source: str
    target: str
    label: str = ""


class FlowchartGenerator:
    """Generate flowcharts from C++ code analysis"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize flowchart generator
        
        Args:
            config: Flowchart configuration
        """
        self.config = config
        self.output_dir = Path(config['output_dir'])
        self.output_format = config['output_format']
        self.max_depth = config['max_depth']
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Graph elements
        self.nodes: Dict[str, FlowNode] = {}
        self.edges: List[FlowEdge] = []
    
    def generate_function_call_graph(
        self,
        functions: List[Any],
        entry_point: Optional[str] = None,
        output_name: str = "function_call_graph"
    ) -> str:
        """
        Generate function call graph
        
        Args:
            functions: List of FunctionInfo objects
            entry_point: Entry point function name (optional)
            output_name: Output file name
            
        Returns:
            Path to generated flowchart
        """
        console.print("[blue]Generating function call graph...[/blue]")
        
        # Create function lookup
        func_dict = {f.name: f for f in functions}
        
        # Build graph
        self.nodes.clear()
        self.edges.clear()
        
        if entry_point and entry_point in func_dict:
            # Build from entry point
            self._build_call_graph_from_function(entry_point, func_dict, depth=0)
        else:
            # Build full graph
            for func in functions:
                self._add_function_node(func)
                for call in func.calls:
                    if call in func_dict:
                        self._add_call_edge(func.name, call)
        
        # Generate flowchart
        output_path = self._render_graph(output_name, "Function Call Graph")
        console.print(f"[green]✓ Flowchart saved to: {output_path}[/green]")
        return output_path
    
    def generate_class_diagram(
        self,
        classes: List[Any],
        output_name: str = "class_diagram"
    ) -> str:
        """
        Generate class diagram
        
        Args:
            classes: List of ClassInfo objects
            output_name: Output file name
            
        Returns:
            Path to generated flowchart
        """
        console.print("[blue]Generating class diagram...[/blue]")
        
        self.nodes.clear()
        self.edges.clear()
        
        # Create class lookup
        class_dict = {c.name: c for c in classes}
        
        # Add class nodes
        for cls in classes:
            methods_str = "\\n".join([f"+ {m.name}()" for m in cls.methods[:5]])  # Limit to 5
            if len(cls.methods) > 5:
                methods_str += f"\\n... ({len(cls.methods) - 5} more)"
            
            label = f"{cls.name}|{methods_str}"
            
            node = FlowNode(
                id=cls.name,
                label=label,
                node_type="class",
                shape="record",
                color="lightgreen"
            )
            self.nodes[cls.name] = node
            
            # Add inheritance edges
            for base_class in cls.base_classes:
                if base_class in class_dict:
                    edge = FlowEdge(base_class, cls.name, "inherits")
                    self.edges.append(edge)
        
        # Generate flowchart
        output_path = self._render_graph(output_name, "Class Diagram")
        console.print(f"[green]✓ Class diagram saved to: {output_path}[/green]")
        return output_path
    
    def generate_module_structure(
        self,
        files_info: Dict[str, Any],
        output_name: str = "module_structure"
    ) -> str:
        """
        Generate module structure diagram
        
        Args:
            files_info: Dictionary of file paths and their info
            output_name: Output file name
            
        Returns:
            Path to generated flowchart
        """
        console.print("[blue]Generating module structure...[/blue]")
        
        self.nodes.clear()
        self.edges.clear()
        
        # Group by directory
        dir_files: Dict[str, List[str]] = {}
        for file_path in files_info.keys():
            dir_name = str(Path(file_path).parent)
            if dir_name not in dir_files:
                dir_files[dir_name] = []
            dir_files[dir_name].append(file_path)
        
        # Add directory nodes
        for dir_name, files in dir_files.items():
            node = FlowNode(
                id=dir_name,
                label=f"{Path(dir_name).name}\\n({len(files)} files)",
                node_type="directory",
                shape="folder",
                color="lightyellow"
            )
            self.nodes[dir_name] = node
        
        # Add file nodes
        for file_path in files_info.keys():
            dir_name = str(Path(file_path).parent)
            file_name = Path(file_path).name
            
            node = FlowNode(
                id=file_path,
                label=file_name,
                node_type="file",
                shape="note",
                color="white"
            )
            self.nodes[file_path] = node
            
            # Add edge from directory to file
            edge = FlowEdge(dir_name, file_path)
            self.edges.append(edge)
        
        # Generate flowchart
        output_path = self._render_graph(output_name, "Module Structure", rankdir="TB")
        console.print(f"[green]✓ Module structure saved to: {output_path}[/green]")
        return output_path
    
    def _build_call_graph_from_function(
        self,
        func_name: str,
        func_dict: Dict[str, Any],
        depth: int,
        visited: Optional[Set[str]] = None
    ) -> None:
        """Build call graph starting from a function"""
        if visited is None:
            visited = set()
        
        if depth > self.max_depth or func_name in visited:
            return
        
        visited.add(func_name)
        
        if func_name not in func_dict:
            return
        
        func = func_dict[func_name]
        self._add_function_node(func)
        
        # Process calls
        for call in func.calls:
            if call in func_dict:
                self._add_function_node(func_dict[call])
                self._add_call_edge(func_name, call)
                self._build_call_graph_from_function(call, func_dict, depth + 1, visited)
    
    def _add_function_node(self, func: Any) -> None:
        """Add a function node"""
        if func.name not in self.nodes:
            label = f"{func.name}\\n{func.return_type}"
            node = FlowNode(
                id=func.name,
                label=label,
                node_type="function",
                shape="box",
                color="lightblue"
            )
            self.nodes[func.name] = node
    
    def _add_call_edge(self, source: str, target: str) -> None:
        """Add a function call edge"""
        edge = FlowEdge(source, target, "calls")
        # Avoid duplicate edges
        if not any(e.source == source and e.target == target for e in self.edges):
            self.edges.append(edge)
    
    def _render_graph(self, name: str, title: str, rankdir: str = "LR") -> str:
        """
        Render graph using graphviz
        
        Args:
            name: Output file name
            title: Graph title
            rankdir: Graph direction (LR, TB, etc.)
            
        Returns:
            Path to output file
        """
        # Create digraph
        dot = graphviz.Digraph(comment=title)
        dot.attr(rankdir=rankdir)
        dot.attr('node', style='filled')
        dot.attr(label=title, labelloc='t', fontsize='20')
        
        # Add nodes
        for node in self.nodes.values():
            dot.node(
                node.id,
                label=node.label,
                shape=node.shape,
                fillcolor=node.color
            )
        
        # Add edges
        for edge in self.edges:
            dot.edge(edge.source, edge.target, label=edge.label)
        
        # Render
        output_path = self.output_dir / name
        dot.render(str(output_path), format=self.output_format, cleanup=True)
        
        return f"{output_path}.{self.output_format}"
    
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

