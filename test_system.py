"""
Test Suite for ADGM Corporate Agent Pro
======================================

Simple tests to verify the application is working correctly.
Run this after setup to ensure all components are functional.

Author: Shreyas
"""

import sys
import os
import importlib.util

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python Version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Requires 3.9+")
        return False

def test_dependencies():
    """Test if required dependencies are installed"""
    print("📦 Testing Dependencies...")
    
    required_packages = [
        'streamlit',
        'pydantic',
        'pyyaml',
        'python_docx',
        'reportlab'
    ]
    
    failed = []
    
    for package in required_packages:
        try:
            if package == 'python_docx':
                import docx
            elif package == 'pyyaml':
                import yaml
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - Not installed")
            failed.append(package)
    
    if failed:
        print(f"\n   Install missing packages:")
        print(f"   pip install {' '.join(failed)}")
        return False
    
    return True

def test_file_structure():
    """Test if required files exist"""
    print("📁 Testing File Structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'src/core/classify.py',
        'src/core/validate.py',
        'src/core/report.py',
        'src/rag/retrieve.py',
        'references/adgm_courts_overview.txt'
    ]
    
    missing = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - Missing")
            missing.append(file_path)
    
    return len(missing) == 0

def test_imports():
    """Test if core modules can be imported"""
    print("🔧 Testing Module Imports...")
    
    modules = [
        ('src.core.classify', 'identify_doc_type'),
        ('src.core.validate', 'analyze_bundle'),
        ('src.core.report', 'build_summary_pdf'),
        ('src.rag.retrieve', 'cite_rules')
    ]
    
    failed = []
    
    for module_name, function_name in modules:
        try:
            # Add current directory to path
            if os.getcwd() not in sys.path:
                sys.path.insert(0, os.getcwd())
            
            module = importlib.import_module(module_name)
            if hasattr(module, function_name):
                print(f"   ✅ {module_name}.{function_name}")
            else:
                print(f"   ⚠️ {module_name}.{function_name} - Function not found")
                failed.append(f"{module_name}.{function_name}")
        except ImportError as e:
            print(f"   ❌ {module_name} - Import failed: {str(e)}")
            failed.append(module_name)
    
    return len(failed) == 0

def test_streamlit_config():
    """Test Streamlit configuration"""
    print("🌐 Testing Streamlit Configuration...")
    
    try:
        import streamlit as st
        print("   ✅ Streamlit imported successfully")
        
        # Test if app.py has required functions
        if os.path.exists('app.py'):
            with open('app.py', 'r', encoding='utf-8') as f:
                content = f.read()
                
            required_functions = ['create_navigation', 'page_analysis', 'main']
            for func in required_functions:
                if f'def {func}(' in content:
                    print(f"   ✅ Function {func} found")
                else:
                    print(f"   ⚠️ Function {func} not found")
        
        return True
    except ImportError:
        print("   ❌ Streamlit not installed")
        return False

def run_basic_functionality_test():
    """Test basic functionality"""
    print("⚡ Testing Basic Functionality...")
    
    try:
        # Test document classification
        sys.path.insert(0, os.getcwd())
        from src.core.classify import identify_doc_type
        
        sample_name = "articles_of_association.docx"
        sample_text = "ARTICLES OF ASSOCIATION\nThis document contains the articles of association."
        doc_type = identify_doc_type(sample_name, sample_text)
        
        if doc_type and doc_type != "Unknown":
            print(f"   ✅ Document classification working: {doc_type}")
        else:
            print("   ⚠️ Document classification returned unexpected results")
        
        # Test validation
        from src.core.validate import analyze_bundle
        print("   ✅ Validation module imported successfully")
        
        # Test report generation
        from src.core.report import build_summary_pdf
        print("   ✅ Report module imported successfully")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Functionality test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 ADGM Corporate Agent Pro - System Tests")
    print("=" * 45)
    print()
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("File Structure", test_file_structure),
        ("Module Imports", test_imports),
        ("Streamlit Config", test_streamlit_config),
        ("Basic Functionality", run_basic_functionality_test)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ Test failed with error: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 45)
    print("📊 Test Summary:")
    print("=" * 15)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your system is ready to use.")
        print("\nTo start the application:")
        print("   streamlit run app.py")
        print("\nThen open: http://localhost:8501")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please review the issues above.")
        print("\nCommon fixes:")
        print("   - Run: pip install -r requirements.txt")
        print("   - Ensure all files were copied correctly")
        print("   - Check Python version (3.9+ required)")

if __name__ == "__main__":
    main()
