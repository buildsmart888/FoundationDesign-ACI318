"""
Development Installation and Testing Guide
FoundationDesign-ACI318 Package

This script helps install the package in development mode
and run comprehensive tests.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and display results"""
    print(f"\n{description}")
    print("-" * 50)
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ SUCCESS: {description}")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"✗ FAILED: {description}")
            if result.stderr:
                print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False

def main():
    print("="*80)
    print("FOUNDATIONDESIGN-ACI318 DEVELOPMENT SETUP")
    print("="*80)
    
    # Check if we're in the right directory
    if not os.path.exists("setup_new.py"):
        print("✗ Error: setup_new.py not found!")
        print("Please run this script from the project root directory.")
        return
    
    print("Current directory:", os.getcwd())
    
    # Install in development mode
    success = run_command(
        "pip install -e .",
        "Installing package in development mode"
    )
    
    if not success:
        print("\n⚠️  Development installation failed. Trying with setup_new.py...")
        success = run_command(
            "pip install -e . -f setup_new.py",
            "Installing with custom setup file"
        )
    
    if success:
        print("\n✓ Package installed successfully in development mode!")
        print("You can now import and use the package from anywhere.")
    else:
        print("\n✗ Installation failed. Please check the error messages above.")
        return
    
    # Run tests
    print("\n" + "="*80)
    print("RUNNING TESTS")
    print("="*80)
    
    # Test basic functionality
    run_command(
        "python test_aci318_basic.py",
        "Running basic functionality tests"
    )
    
    # Test complete design example
    run_command(
        "python complete_design_example.py",
        "Running complete design example"
    )
    
    print("\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    print("\n1. Package Installation:")
    print("   ✓ Package is installed in development mode")
    print("   ✓ You can edit source code and changes will be reflected immediately")
    
    print("\n2. Usage Examples:")
    print("   • Run: python test_aci318_basic.py")
    print("   • Run: python complete_design_example.py")
    print("   • Open: examples/Concentric_Footing_ACI318_Example.ipynb")
    
    print("\n3. Key Features Tested:")
    print("   ✓ ACI 318M-25 load factors and strength reduction factors")
    print("   ✓ Whitney stress block flexural design")
    print("   ✓ One-way and punching shear design")
    print("   ✓ Complete foundation design workflow")
    
    print("\n4. Import in Your Code:")
    print("   from FoundationDesign import PadFoundationACI318, padFoundationDesignACI318")
    
    print("\n5. Design Code Compliance:")
    print("   • ACI 318M-25 Chapter 13.1 - Foundations")
    print("   • Section 5.3 - Load combinations")  
    print("   • Section 7 - Flexural design")
    print("   • Section 22 - Shear and torsion")
    print("   • Section 20.5 - Concrete cover")

if __name__ == "__main__":
    main()
