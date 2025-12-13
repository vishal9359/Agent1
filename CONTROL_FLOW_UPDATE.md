# Control Flow Diagram Update

## Summary

I've fixed the Agent1 to generate **proper function flow diagrams** with actual control flow structures (if/else, loops, switches) instead of just styling code.

## What Was Fixed

### 1. **Enhanced C++ Parser** (`src/cpp_parser.py`)

Added a new `ControlFlowNode` dataclass to represent control flow structures:
- **If/Else statements** with decision diamonds
- **For loops** with proper repeat structures
- **While loops** with condition checking
- **Switch/Case statements** with multiple branches
- **Function calls** and statements
- **Return statements**

The parser now analyzes the AST to extract:
- Conditions for if/while/for/switch
- Then/Else branches
- Loop bodies
- Case statements
- Nested control structures (up to 10 levels deep)

### 2. **Improved PlantUML Generator** (`src/plantuml_generator.py`)

Added new method `generate_detailed_function_flow()` that creates:
- **Activity diagrams** with proper PlantUML syntax
- **Decision diamonds** for if/else (`if (condition?) then (yes) ... else (no) ... endif`)
- **Loop structures** (`repeat ... repeat while (condition?)` for for-loops)
- **While loops** (`while (condition?) is (true) ... endwhile (false)`)
- **Switch statements** (`switch (value?) case (x) ... endswitch`)
- **Colorful styling** matching your reference images:
  - Green boxes for activities
  - Yellow diamonds for decisions
  - Blue start/end nodes
  - Red stop nodes

### 3. **Enhanced Agent** (`src/agent.py`)

Added new methods:
- `generate_flowchart(flowchart_type='function_flow')` - Generate detailed function flow diagrams
- `list_functions()` - List all functions sorted by control flow complexity

### 4. **Updated CLI** (`main.py`)

Added new commands:
- `python main.py flowchart --type function_flow --entry-point <function_name>`
- `python main.py list-functions` - List all functions
- Interactive mode commands: `flow <function_name>`, `list`

## Before vs After

### Before ❌
```plantuml
@startuml
skinparam sequence {
  ArrowColor DeepSkyBlue
  ActorBorderColor DeepSkyBlue
  LifeLineBorderColor Blue
  ParticipantBorderColor DeepSkyBlue
  ParticipantBackgroundColor LightSkyBlue
}
@enduml
```
*Only styling, no actual flowchart content*

### After ✅
```plantuml
@startuml
title Function Flow: processData

skinparam activity {
  BackgroundColor #B4E7CE
  BorderColor #2C5F2D
  FontSize 11
}
skinparam activityDiamond {
  BackgroundColor #FFD966
  BorderColor #CC9900
}

start

:processData(|
  int* data
  int size
);
note right: Returns void

repeat
  if (data[i] > 0?) then (yes)
    :data[i] = data[i] * 2;
  endif
repeat while (i < size?)

stop

@enduml
```
*Complete flowchart with decision diamonds, loops, and proper flow*

## How to Use

### Install Dependencies

```bash
cd "C:\Users\Vishal shakya\cursor-workspace\Agent1"
pip install -r requirements.txt
```

### Analyze the PoseidonOS Trace Module

```bash
# Clone or download the trace module
git clone https://github.com/poseidonos/poseidonos.git
cd "C:\Users\Vishal shakya\cursor-workspace\Agent1"

# Analyze the project
python main.py analyze "poseidonos\src\trace"

# List all functions (sorted by control flow complexity)
python main.py list-functions --limit 30

# Generate detailed flow for a specific function
python main.py flowchart --type function_flow --entry-point <function_name>

# Generate all function flows (for functions with control flow)
python main.py flowchart --type function_flow
```

### Interactive Mode

```bash
python main.py interactive

# Then use these commands:
> list                          # List all functions
> flow <function_name>          # Generate flow for specific function
> flow                          # Generate flows for interesting functions
> flowchart function_call       # Generate overview call graph
> flowchart module              # Generate module structure
> stats                         # Show statistics
```

### View Generated Diagrams

The PlantUML files (`.puml`) are saved in the `outputs/` directory.

**Option 1: Online Viewer**
1. Visit http://www.plantuml.com/plantuml/uml/
2. Copy the content from the `.puml` file
3. Paste it into the web editor

**Option 2: VSCode Extension**
1. Install "PlantUML" extension in VSCode
2. Open the `.puml` file
3. Press `Alt+D` to preview

**Option 3: Command Line**
```bash
# Install PlantUML (requires Java)
pip install plantuml

# Generate PNG
plantuml outputs/flow_function_name.puml

# Or using Java directly
java -jar plantuml.jar outputs/flow_function_name.puml
```

## Example Output

For a function like this:

```cpp
void processData(int* data, int size) {
    for (int i = 0; i < size; i++) {
        if (data[i] > 0) {
            data[i] = data[i] * 2;
        }
    }
}
```

The generated diagram will show:
- **Start node** (blue circle)
- **Function name** with parameters (green box)
- **For loop** with repeat structure (yellow diamond)
- **If condition** inside loop (yellow diamond with yes/no branches)
- **Assignment statement** in the "yes" branch (green box)
- **Stop node** (red circle)

## Features

✅ **Decision diamonds** for if/else statements
✅ **Loop structures** for for/while loops
✅ **Switch/case** statements with multiple branches
✅ **Nested control flow** (up to 10 levels)
✅ **Function calls** clearly marked
✅ **Return statements** displayed
✅ **Color coding** matching reference images
✅ **Automatic detection** of interesting functions
✅ **Batch generation** for multiple functions

## Diagram Types

### 1. Function Flow (NEW!)
**Command**: `python main.py flowchart --type function_flow --entry-point <name>`

Shows the **detailed control flow inside a function**:
- Decision points (if/else)
- Loops (for/while)
- Switch statements
- Function calls
- Returns

### 2. Function Call Graph
**Command**: `python main.py flowchart --type function_call`

Shows **which functions call which** (inter-function relationships).

### 3. Class Diagram
**Command**: `python main.py flowchart --type class`

Shows **class relationships** and inheritance.

### 4. Module Structure
**Command**: `python main.py flowchart --type module`

Shows **file and directory organization**.

## Testing

I've created test scripts to verify the functionality:

### Simple Test (No External Dependencies)
```bash
python test_simple_flow.py
```

This will:
1. Create a test C++ file with various control structures
2. Parse it to extract control flow
3. Generate PlantUML diagrams
4. Display the PlantUML code in the console

### Full Test (With Agent)
```bash
python test_control_flow.py
```

This tests the complete agent functionality.

## Technical Details

### Control Flow Node Types
- `if` - If/else statement
- `for` - For loop
- `while` - While loop  
- `switch` - Switch statement
- `case` - Case in switch
- `call` - Function call
- `statement` - Generic statement
- `return` - Return statement

### PlantUML Mapping
- If/Else → `if (condition?) then (yes) ... else (no) ... endif`
- For Loop → `repeat ... repeat while (condition?)`
- While Loop → `while (condition?) is (true) ... endwhile (false)`
- Switch → `switch (value?) case (x) ... endswitch`
- Activity → `:label;`

### Parser Algorithm
1. Parse C++ file with tree-sitter
2. For each function, traverse the AST
3. Identify control flow nodes (if_statement, for_statement, etc.)
4. Extract conditions, bodies, and branches
5. Build a tree of ControlFlowNode objects
6. Store in FunctionInfo.control_flow

### Generator Algorithm
1. Receive FunctionInfo with control_flow
2. Start PlantUML activity diagram
3. Recursively traverse control flow nodes
4. Map each node type to PlantUML syntax
5. Handle nesting with indentation
6. Add colors and styling
7. Output .puml file

## Troubleshooting

### No Control Flow Detected
- The function may be too simple (no if/loops)
- Try with more complex functions
- Check that the C++ file parses correctly

### Diagram Looks Wrong
- Open the `.puml` file and check the syntax
- Try viewing with different PlantUML viewers
- Report specific issues with the function name

### Module Not Found
- Install dependencies: `pip install -r requirements.txt`
- Ensure you're in the Agent1 directory
- Check Python version (3.8+recommended)

## Next Steps

To use with the PoseidonOS trace module:

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Download the source**:
   ```bash
   git clone https://github.com/poseidonos/poseidonos.git
   ```

3. **Analyze**:
   ```bash
   python main.py analyze "poseidonos/src/trace" --flowchart function_flow
   ```

4. **Review outputs**:
   ```bash
   ls outputs/
   ```

5. **View diagrams** using one of the methods above

## Files Modified

1. `src/cpp_parser.py` - Added ControlFlowNode and control flow extraction
2. `src/plantuml_generator.py` - Added detailed flow generation with proper activity diagram syntax
3. `src/agent.py` - Added function_flow type and list_functions method
4. `main.py` - Added new CLI commands

## Comparison with Reference Images

Your reference images show:
- ✅ Rounded rectangles for processes
- ✅ Diamond shapes for decisions
- ✅ Clear arrows showing flow direction
- ✅ Labels on decision branches (yes/no, conditions)
- ✅ Different colors for different elements
- ✅ Start/end nodes
- ✅ Nested structures

All of these are now implemented in the PlantUML output!

---

**Author**: AI Assistant  
**Date**: December 13, 2025  
**Status**: ✅ Ready to Use
