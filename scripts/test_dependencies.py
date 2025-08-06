#!/usr/bin/env python3
"""
Nokekoi App - Dependencies Test Script
Testa todas as dependências principais da aplicação
"""

import sys
import importlib
import subprocess
from pathlib import Path

# Colors for terminal output
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
NC = '\033[0m'  # No Color

def log_info(message):
    print(f"{GREEN}[INFO]{NC} {message}")

def log_warn(message):
    print(f"{YELLOW}[WARN]{NC} {message}")

def log_error(message):
    print(f"{RED}[ERROR]{NC} {message}")

def test_python_version():
    """Test Python version compatibility"""
    log_info("Testing Python version...")
    
    version = sys.version_info
    required_version = (3, 8)
    
    if version >= required_version:
        log_info(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        log_error(f"❌ Python {version.major}.{version.minor}.{version.micro} - Required: {required_version[0]}.{required_version[1]}+")
        return False

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, '__version__'):
            version = module.__version__
        else:
            version = "unknown"
        
        display_name = package_name or module_name
        log_info(f"✅ {display_name} ({version}) - OK")
        return True
    except ImportError as e:
        display_name = package_name or module_name
        log_error(f"❌ {display_name} - FAILED: {e}")
        return False

def test_core_dependencies():
    """Test core Python dependencies"""
    log_info("Testing core dependencies...")
    
    dependencies = [
        ("streamlit", "Streamlit"),
        ("pandas", "Pandas"),
        ("geopandas", "GeoPandas"),
        ("folium", "Folium"),
        ("streamlit_folium", "Streamlit-Folium"),
        ("requests", "Requests"),
        ("pytz", "PyTZ"),
        ("numpy", "NumPy"),
        ("shapely", "Shapely"),
        ("branca", "Branca"),
        ("rasterio", "Rasterio"),
        ("fiona", "Fiona"),
        ("dotenv", "Python-Dotenv"),
    ]
    
    results = []
    for module, name in dependencies:
        result = test_import(module, name)
        results.append(result)
    
    return all(results)

def test_optional_dependencies():
    """Test optional dependencies"""
    log_info("Testing optional dependencies...")
    
    optional_deps = [
        ("PIL", "Pillow"),
        ("dateutil", "Python-Dateutil"),
        ("streamlit_extras", "Streamlit-Extras"),
    ]
    
    results = []
    for module, name in optional_deps:
        result = test_import(module, name)
        results.append(result)
    
    return results

def test_environment_variables():
    """Test if required environment variables are available"""
    log_info("Testing environment variables...")
    
    import os
    from dotenv import load_dotenv
    
    # Load .env file if it exists
    if Path('.env').exists():
        load_dotenv()
        log_info("✅ .env file loaded")
    else:
        log_warn("⚠️  .env file not found")
    
    # Check critical environment variables
    ntr_token = os.getenv('NTR_TOKEN')
    if ntr_token and ntr_token != 'your_nasa_token_here':
        log_info("✅ NTR_TOKEN - Configured")
        return True
    else:
        log_warn("⚠️  NTR_TOKEN - Not configured or using default value")
        return False

def test_file_structure():
    """Test if required files and directories exist"""
    log_info("Testing file structure...")
    
    required_files = [
        "1_🔥_Foco_de_Calor.py",
        "requirements.txt",
        "env.example",
        "README.md",
    ]
    
    required_dirs = [
        "scripts",
        "img",
        ".streamlit",
    ]
    
    results = []
    
    # Test files
    for file_path in required_files:
        if Path(file_path).exists():
            log_info(f"✅ {file_path} - Found")
            results.append(True)
        else:
            log_error(f"❌ {file_path} - Missing")
            results.append(False)
    
    # Test directories
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            log_info(f"✅ {dir_path}/ - Found")
            results.append(True)
        else:
            log_error(f"❌ {dir_path}/ - Missing")
            results.append(False)
    
    return all(results)

def test_streamlit_config():
    """Test Streamlit configuration"""
    log_info("Testing Streamlit configuration...")
    
    config_file = Path(".streamlit/config.toml")
    if config_file.exists():
        log_info("✅ Streamlit config file found")
        return True
    else:
        log_warn("⚠️  Streamlit config file not found")
        return False

def test_nasa_api_connectivity():
    """Test NASA API connectivity (without making actual requests)"""
    log_info("Testing NASA API connectivity setup...")
    
    import os
    
    token = os.getenv('NTR_TOKEN')
    if not token or token == 'your_nasa_token_here':
        log_warn("⚠️  NASA token not configured - skipping connectivity test")
        return False
    
    # Test if requests module can handle HTTPS
    try:
        import requests
        import ssl
        log_info("✅ HTTPS/SSL support available")
        return True
    except Exception as e:
        log_error(f"❌ HTTPS/SSL test failed: {e}")
        return False

def run_security_checks():
    """Run basic security checks"""
    log_info("Running security checks...")
    
    checks_passed = []
    
    # Check if .env is in .gitignore
    gitignore = Path(".gitignore")
    if gitignore.exists():
        content = gitignore.read_text()
        if ".env" in content:
            log_info("✅ .env file is in .gitignore")
            checks_passed.append(True)
        else:
            log_warn("⚠️  .env file should be added to .gitignore")
            checks_passed.append(False)
    else:
        log_warn("⚠️  .gitignore file not found")
        checks_passed.append(False)
    
    # Check file permissions on scripts
    script_files = list(Path("scripts").glob("*.py")) if Path("scripts").exists() else []
    for script in script_files:
        if script.stat().st_mode & 0o777 == 0o755:
            log_info(f"✅ {script.name} has correct permissions")
        else:
            log_warn(f"⚠️  {script.name} may have incorrect permissions")
    
    return all(checks_passed)

def main():
    """Main test function"""
    print(f"{GREEN}🔥 Nokekoi App - Dependencies Test{NC}")
    print("=" * 50)
    
    test_results = []
    
    # Run all tests
    test_results.append(test_python_version())
    test_results.append(test_core_dependencies())
    test_optional_dependencies()  # Optional, don't fail on these
    test_results.append(test_environment_variables())
    test_results.append(test_file_structure())
    test_results.append(test_streamlit_config())
    test_results.append(test_nasa_api_connectivity())
    test_results.append(run_security_checks())
    
    # Summary
    print("\n" + "=" * 50)
    if all(test_results):
        log_info("🎉 All critical tests passed! Application should work correctly.")
        return 0
    else:
        failed_tests = len([r for r in test_results if not r])
        log_error(f"❌ {failed_tests} critical test(s) failed. Please fix the issues before running the application.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 