# Function Flow Diagram Examples

This document shows examples of the improved function flow diagrams with actual PlantUML code.

## Example 1: Simple If-Else Function

### C++ Code
```cpp
int calculateSum(int a, int b) {
    if (a > 0) {
        return a + b;
    } else {
        return b;
    }
}
```

### Generated PlantUML
```plantuml
@startuml
title Function Flow: calculateSum

skinparam activity {
  BackgroundColor #B4E7CE
  BorderColor #2C5F2D
  FontSize 11
}
skinparam activityDiamond {
  BackgroundColor #FFD966
  BorderColor #CC9900
}
skinparam activityStart {
  BackgroundColor #4A90E2
}
skinparam activityEnd {
  BackgroundColor #E74C3C
}

start

:calculateSum(|
  int a
  int b
);
note right: Returns int

if ((a > 0)?) then (yes)
  :return a + b;
else (no)
  :return b;
endif

stop

@enduml
```

### Visual Result
```
    [Start]
       ↓
[calculateSum()]
       ↓
   ◇ a > 0?
   /       \
 yes       no
  ↓         ↓
return    return
 a+b        b
  \        /
    [Stop]
```

---

## Example 2: For Loop with Nested If

### C++ Code
```cpp
void processData(int* data, int size) {
    for (int i = 0; i < size; i++) {
        if (data[i] > 0) {
            data[i] = data[i] * 2;
        }
    }
}
```

### Generated PlantUML
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
skinparam activityStart {
  BackgroundColor #4A90E2
}
skinparam activityEnd {
  BackgroundColor #E74C3C
}

start

:processData(|
  int* data
  int size
);
note right: Returns void

repeat
  if ((data[i] > 0)?) then (yes)
    :data[i] = data[i] * 2;
  endif
repeat while ((i < size)?)

stop

@enduml
```

### Visual Result
```
     [Start]
        ↓
 [processData()]
        ↓
     ┌──→─┐
     │    │
     │ ◇ data[i] > 0?
     │  /      \
     │ yes     no
     │  ↓      │
     │ double  │
     │  data   │
     │  \     /
     └←──┘
        ↓
     [Stop]
```

---

## Example 3: Switch Statement

### C++ Code
```cpp
int checkValue(int x) {
    switch(x) {
        case 1:
            return 10;
        case 2:
            return 20;
        default:
            return 0;
    }
}
```

### Generated PlantUML
```plantuml
@startuml
title Function Flow: checkValue

skinparam activity {
  BackgroundColor #B4E7CE
  BorderColor #2C5F2D
  FontSize 11
}
skinparam activityDiamond {
  BackgroundColor #FFD966
  BorderColor #CC9900
}
skinparam activityStart {
  BackgroundColor #4A90E2
}
skinparam activityEnd {
  BackgroundColor #E74C3C
}

start

:checkValue(|
  int x
);
note right: Returns int

switch ((x)?)
case (case 1:)
  :return 10;
case (case 2:)
  :return 20;
case (default:)
  :return 0;
endswitch

stop

@enduml
```

### Visual Result
```
    [Start]
       ↓
 [checkValue()]
       ↓
    ◇ x ?
   /  |  \
  1   2  default
  ↓   ↓   ↓
 ret ret ret
  10  20  0
   \  |  /
    [Stop]
```

---

## Example 4: While Loop with Function Calls

### C++ Code
```cpp
void printLoop(int n) {
    while (n > 0) {
        printf("%d", n);
        n--;
    }
}
```

### Generated PlantUML
```plantuml
@startuml
title Function Flow: printLoop

skinparam activity {
  BackgroundColor #B4E7CE
  BorderColor #2C5F2D
  FontSize 11
}
skinparam activityDiamond {
  BackgroundColor #FFD966
  BorderColor #CC9900
}
skinparam activityStart {
  BackgroundColor #4A90E2
}
skinparam activityEnd {
  BackgroundColor #E74C3C
}

start

:printLoop(|
  int n
);
note right: Returns void

while ((n > 0)?) is (true)
  :printf;
  :n--;
endwhile (false)

stop

@enduml
```

### Visual Result
```
     [Start]
        ↓
   [printLoop()]
        ↓
  while n > 0?
     /      \
   true    false
    ↓        ↓
  [printf]   │
    ↓        │
   [n--]     │
    ↓        │
    └───→←───┘
        ↓
     [Stop]
```

---

## Example 5: Complex Nested Control Flow

### C++ Code
```cpp
int complexFunction(int x, int y) {
    int result = 0;
    
    if (x > 0) {
        for (int i = 0; i < y; i++) {
            if (i % 2 == 0) {
                result += i;
            } else {
                result -= i;
            }
        }
    } else {
        while (y > 0) {
            result += calculate(y);
            y--;
        }
    }
    
    return result;
}
```

### Generated PlantUML
```plantuml
@startuml
title Function Flow: complexFunction

skinparam activity {
  BackgroundColor #B4E7CE
  BorderColor #2C5F2D
  FontSize 11
}
skinparam activityDiamond {
  BackgroundColor #FFD966
  BorderColor #CC9900
}
skinparam activityStart {
  BackgroundColor #4A90E2
}
skinparam activityEnd {
  BackgroundColor #E74C3C
}

start

:complexFunction(|
  int x
  int y
);
note right: Returns int

:result = 0;

if ((x > 0)?) then (yes)
  repeat
    if ((i % 2 == 0)?) then (yes)
      :result += i;
    else (no)
      :result -= i;
    endif
  repeat while ((i < y)?)
else (no)
  while ((y > 0)?) is (true)
    :calculate(y);
    :y--;
  endwhile (false)
endif

:return result;

stop

@enduml
```

### Visual Result
```
        [Start]
           ↓
   [complexFunction()]
           ↓
      result = 0
           ↓
       ◇ x > 0?
      /        \
    yes        no
     ↓          ↓
   ┌──→─┐    while y > 0?
   │    │     /      \
   │ ◇ i%2=0? true   false
   │ /    \   ↓       ↓
   │yes   no  calc    │
   │ ↓    ↓   y--     │
   │+=   -=   └→←─────┘
   └←──┘        ↓
       ↓     return result
   [Stop]
```

---

## Comparison: Before vs After

### ❌ BEFORE (Just Styling)
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

**Problem**: No actual diagram content! Just empty styling that doesn't show any flow.

### ✅ AFTER (Complete Flow Diagram)
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
  if ((data[i] > 0)?) then (yes)
    :data[i] = data[i] * 2;
  endif
repeat while ((i < size)?)

stop

@enduml
```

**Result**: Complete activity diagram with:
- ✅ Start/stop nodes
- ✅ Function name and parameters
- ✅ Decision diamonds for conditionals
- ✅ Loop structures
- ✅ Clear flow arrows
- ✅ Proper colors matching reference images

---

## Color Scheme

The diagrams use a professional color scheme matching your reference images:

| Element | Color | PlantUML |
|---------|-------|----------|
| Activity boxes | Light green | `#B4E7CE` |
| Activity borders | Dark green | `#2C5F2D` |
| Decision diamonds | Yellow | `#FFD966` |
| Diamond borders | Gold | `#CC9900` |
| Start node | Blue | `#4A90E2` |
| End node | Red | `#E74C3C` |
| Arrows | Dark green | `#2C5F2D` |

---

## How to View These Diagrams

### Online Viewer (Easiest)
1. Go to http://www.plantuml.com/plantuml/uml/
2. Copy any PlantUML code from above
3. Paste it into the text area
4. See the rendered diagram instantly!

### VSCode Extension
1. Install "PlantUML" extension
2. Create a new file `example.puml`
3. Paste the PlantUML code
4. Press `Alt+D` to preview

### Command Line
```bash
# Install PlantUML
npm install -g node-plantuml

# Generate image
puml generate example.puml -o example.png
```

---

## Tips for Best Results

### 1. Focus on Functions with Control Flow
Functions with if/else, loops, and switches generate the most interesting diagrams.

### 2. Use the list-functions Command
```bash
python main.py list-functions
```
This shows functions sorted by control flow complexity.

### 3. Generate for Specific Functions
```bash
python main.py flowchart --type function_flow --entry-point functionName
```

### 4. Batch Generate
```bash
python main.py flowchart --type function_flow
```
This generates diagrams for all functions with control flow.

### 5. Check the Output Directory
All diagrams are saved to `outputs/` with names like:
- `flow_functionName.puml`
- `test_overview.puml`
- `module_structure.puml`

---

## Real World Example: Trace Module

For the PoseidonOS trace module at:
https://github.com/poseidonos/poseidonos/tree/main/src/trace

The generated diagrams will show:
- Trace initialization flow
- Event handling logic
- Buffer management decisions
- Memory allocation patterns
- Error handling paths

Example command:
```bash
python main.py analyze "path/to/poseidonos/src/trace"
python main.py list-functions --limit 30
python main.py flowchart --type function_flow --entry-point TraceInit
```

This will generate detailed flowcharts showing exactly how the trace module works internally!

---

**Created**: December 13, 2025  
**Status**: ✅ Ready to Use
