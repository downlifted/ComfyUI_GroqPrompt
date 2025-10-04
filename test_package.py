#!/usr/bin/env python3
"""
Test script for ComfyUI_GroqPrompt package
Verifies that all components can be imported and basic functionality works
"""

import sys
import os


def test_imports():
    """Test that all package components can be imported"""
    try:
        from ComfyUI_GroqPrompt.nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
        print("✅ Package imports successful")

        # Check node classes
        found_nodes = list(NODE_CLASS_MAPPINGS.keys())

        print(f"✅ Found {len(found_nodes)} node classes:")
        for node in found_nodes:
            print(f"   - {node}")

        # Verify categories
        categories_found = set()
        for node_class in NODE_CLASS_MAPPINGS.values():
            if hasattr(node_class, 'CATEGORY'):
                categories_found.add(node_class.CATEGORY)

        print("✅ Node categories:")
        for category in sorted(categories_found):
            print(f"   - {category}")

        return True

    except Exception as e:
        print(f"❌ Import error: {e}")
        return False


def test_dependencies():
    """Test that required dependencies are available"""
    required_modules = ['groq', 'torch', 'numpy', 'PIL']

    print("🔍 Checking dependencies...")
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} - Available")
        except ImportError:
            print(f"❌ {module} - Missing")
            return False

    return True


def test_node_structure():
    """Test that nodes have required methods"""
    try:
        from ComfyUI_GroqPrompt.nodes import NODE_CLASS_MAPPINGS

        print("🔍 Testing node structure...")

        for node_name, node_class in NODE_CLASS_MAPPINGS.items():
            # Check for required class methods
            if not hasattr(node_class, 'INPUT_TYPES'):
                print(f"❌ {node_name} missing INPUT_TYPES")
                return False

            if not hasattr(node_class, 'RETURN_TYPES'):
                print(f"❌ {node_name} missing RETURN_TYPES")
                return False

            if not hasattr(node_class, 'FUNCTION'):
                print(f"❌ {node_name} missing FUNCTION")
                return False

            if not hasattr(node_class, 'CATEGORY'):
                print(f"❌ {node_name} missing CATEGORY")
                return False

            print(f"✅ {node_name} - Valid structure")

        return True

    except Exception as e:
        print(f"❌ Structure test error: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 ComfyUI_GroqPrompt Package Test Suite")
    print("=" * 50)

    tests = [
        ("Package Imports", test_imports),
        ("Dependencies", test_dependencies),
        ("Node Structure", test_node_structure)
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n🔧 Running {test_name}...")
        result = test_func()
        results.append(result)

    print("\n" + "=" * 50)
    print("📊 Test Results:")

    all_passed = all(results)
    if all_passed:
        print("✅ All tests PASSED! Package is ready for GitHub distribution.")
    else:
        print("❌ Some tests FAILED. Please fix issues before uploading to GitHub.")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

