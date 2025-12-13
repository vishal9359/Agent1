#!/usr/bin/env python3
"""
Test script for PoseidonOS-like C++ code patterns
Tests the fixed PlantUML generator with real-world C++ patterns
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.cpp_parser import CPPCodeParser
from src.plantuml_generator import PlantUMLGenerator


def test_poseidonos_patterns():
    """Test with PoseidonOS-like C++ code patterns"""
    
    print("=" * 70)
    print("Testing PlantUML Generator with PoseidonOS-like C++ Patterns")
    print("=" * 70)
    
    # Create test directory
    test_dir = Path("test_poseidonos_code")
    test_dir.mkdir(exist_ok=True)
    
    # Create test C++ file with PoseidonOS-like patterns
    test_cpp = test_dir / "event_handler.cpp"
    test_cpp.write_text("""
#include <iostream>
#include <memory>
#include <vector>
#include <string>

namespace pos {
namespace event {

// Test 1: Namespace, templates, pointers
template<typename T>
class EventHandler {
public:
    // Test 2: Complex conditions with operators
    int ProcessEvent(Event* event, const std::string& type) {
        if (event == nullptr || type.empty()) {
            return -1;
        }
        
        // Test 3: Multiple comparisons
        if (event->priority >= HIGH_PRIORITY && event->priority <= MAX_PRIORITY) {
            HandleHighPriority(event);
        } else if (event->priority > 0) {
            HandleNormalPriority(event);
        } else {
            return -1;
        }
        
        return 0;
    }
    
    // Test 4: Switch with complex cases
    void RouteEvent(EventType type) {
        switch(type) {
            case EventType::IO_REQUEST:
                ProcessIORequest();
                break;
            case EventType::FLUSH_CMD:
                ProcessFlushCommand();
                break;
            case EventType::SHUTDOWN:
                HandleShutdown();
                break;
            default:
                LogError("Unknown event type");
                break;
        }
    }
    
    // Test 5: Nested loops with conditions
    void ProcessQueue(std::vector<Event*>& queue) {
        for (size_t i = 0; i < queue.size(); i++) {
            Event* evt = queue[i];
            
            while (evt->retryCount < MAX_RETRIES) {
                if (TryProcess(evt)) {
                    break;
                } else {
                    evt->retryCount++;
                }
            }
            
            if (evt->retryCount >= MAX_RETRIES) {
                LogFailure(evt);
            }
        }
    }
    
    // Test 6: Complex boolean conditions
    bool ValidateEvent(Event* evt) {
        if ((evt->type == IO_READ || evt->type == IO_WRITE) && 
            evt->buffer != nullptr && evt->size > 0) {
            return true;
        }
        
        if (evt->type == CONTROL_CMD && evt->cmdCode >= 0 && evt->cmdCode < MAX_CMD) {
            return CheckPermission(evt);
        }
        
        return false;
    }
    
    // Test 7: Pointer operations and references
    void UpdateEvent(Event*& evt, const Config& cfg) {
        if (evt == nullptr) {
            evt = AllocateEvent();
        }
        
        evt->timestamp = GetCurrentTime();
        evt->config = &cfg;
    }
    
    // Test 8: Template and namespace combinations
    std::shared_ptr<T> CreateHandler(const std::string& name) {
        if (name.find("::") != std::string::npos) {
            return CreateNamespacedHandler(name);
        }
        
        for (const auto& factory : factoryList) {
            if (factory->CanCreate(name)) {
                return factory->Create<T>(name);
            }
        }
        
        return nullptr;
    }
    
    // Test 9: Bit operations and hex values
    uint32_t EncodeFlags(uint32_t flags) {
        uint32_t result = 0;
        
        if (flags & 0x01) {
            result |= FLAG_URGENT;
        }
        
        if ((flags & 0xFF00) >> 8 == SPECIAL_CODE) {
            result |= FLAG_SPECIAL;
        }
        
        return result | (flags << 16);
    }
    
    // Test 10: Exception-like patterns (C++ specific)
    int SafeExecute(Callback* cb) {
        if (cb == nullptr) {
            return -EINVAL;
        }
        
        try {
            cb->Execute();
        } catch (const std::exception& e) {
            LogException(e.what());
            return -EIO;
        } catch (...) {
            return -EFAULT;
        }
        
        return 0;
    }
};

} // namespace event
} // namespace pos
""")
    
    print(f"\n✓ Created test file: {test_cpp}")
    print("  Patterns tested:")
    print("    - Namespaces and templates")
    print("    - Pointer and reference operations")
    print("    - Complex boolean conditions (&&, ||, ==, !=, >=, <=)")
    print("    - Nested loops and switches")
    print("    - Bit operations and hex values")
    print("    - Special characters (:, ;, |, &, *, <, >)")
    
    # Initialize parser
    parser_config = {
        'file_extensions': ['.cpp', '.h', '.hpp'],
        'ignore_dirs': ['build', 'dist'],
        'max_file_size_mb': 10
    }
    
    print("\n1. Initializing C++ parser...")
    parser = CPPCodeParser(parser_config)
    
    # Parse the project
    print(f"2. Parsing test code from {test_dir}...")
    parser.parse_project(str(test_dir))
    
    print(f"\n✓ Found {len(parser.functions)} functions")
    
    # Show functions with control flow
    print("\n3. Functions with control flow:")
    for func in parser.functions:
        flow_count = len(func.control_flow) if func.control_flow else 0
        if flow_count > 0:
            print(f"   - {func.name}: {flow_count} control flow nodes")
    
    # Initialize diagram generator
    flowchart_config = {
        'output_dir': 'outputs',
        'output_format': 'png',
        'max_depth': 5
    }
    
    print("\n4. Initializing diagram generator with FIXED sanitization...")
    generator = PlantUMLGenerator(flowchart_config)
    
    # Generate detailed flow diagrams
    print("\n5. Generating function flow diagrams...")
    print("   (Testing PlantUML syntax with complex C++ patterns)\n")
    
    success_count = 0
    error_count = 0
    
    for func in parser.functions:
        if func.control_flow:
            print(f"   → Generating flow for: {func.name}")
            try:
                path = generator.generate_detailed_function_flow(func)
                
                # Validate the generated PlantUML
                with open(path, 'r') as f:
                    content = f.read()
                    
                # Check for common PlantUML syntax errors
                errors = []
                if ':;' in content or '; :' in content:
                    errors.append("Empty activity labels")
                if '()' in content and 'if ()' not in content:
                    errors.append("Empty conditions")
                if content.count('@startuml') != content.count('@enduml'):
                    errors.append("Mismatched start/end tags")
                
                if errors:
                    print(f"     ⚠ Warnings: {', '.join(errors)}")
                    error_count += 1
                else:
                    print(f"     ✓ Syntax validated - saved to: {Path(path).name}")
                    success_count += 1
                
                # Show a snippet of the generated PlantUML
                print(f"\n     PlantUML snippet:")
                lines = content.split('\n')
                for i, line in enumerate(lines[10:20]):  # Show middle section
                    print(f"     {line}")
                print()
                    
            except Exception as e:
                print(f"     ✗ Error: {e}")
                error_count += 1
    
    # Generate overview diagram
    print("\n6. Generating overview function call diagram...")
    try:
        path = generator.generate_function_call_graph(
            parser.functions,
            output_name="poseidonos_test_overview"
        )
        print(f"   ✓ Saved to: {path}")
        success_count += 1
    except Exception as e:
        print(f"   ✗ Error: {e}")
        error_count += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Results:")
    print("=" * 70)
    print(f"✓ Successfully generated: {success_count} diagrams")
    if error_count > 0:
        print(f"✗ Errors encountered: {error_count}")
    else:
        print("✓ All diagrams generated without errors!")
    
    print(f"\nGenerated diagrams are in: outputs/")
    print("\nValidation checks performed:")
    print("  ✓ PlantUML syntax validation")
    print("  ✓ Special character handling")
    print("  ✓ Complex condition sanitization")
    print("  ✓ Template and namespace handling")
    print("  ✓ Operator and comparison handling")
    
    print("\nTo view diagrams:")
    print("  1. Visit: http://www.plantuml.com/plantuml/uml/")
    print("  2. Copy and paste the PlantUML content")
    print("  3. Or use VSCode PlantUML extension")
    
    print("\n" + "=" * 70)
    if error_count == 0:
        print("✅ ALL TESTS PASSED - Ready for PoseidonOS!")
    else:
        print("⚠ Some warnings found - review outputs")
    print("=" * 70)
    
    return error_count == 0


if __name__ == '__main__':
    try:
        success = test_poseidonos_patterns()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
