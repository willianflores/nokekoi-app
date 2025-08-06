#!/usr/bin/env python3
"""
Nokekoi App - NASA API Test Script
Testa conectividade e autenticação com a NASA FIRMS API
"""

import os
import sys
import requests
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

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

def load_environment():
    """Load environment variables"""
    if Path('.env').exists():
        load_dotenv()
        log_info("✅ Environment variables loaded from .env")
    else:
        log_warn("⚠️  .env file not found, using system environment")

def get_nasa_token():
    """Get NASA token from environment"""
    token = os.getenv('NTR_TOKEN')
    
    if not token:
        log_error("❌ NTR_TOKEN environment variable not found")
        return None
    
    if token == 'your_nasa_token_here':
        log_error("❌ NTR_TOKEN is still using default value")
        return None
    
    log_info("✅ NASA token found in environment")
    return token

def test_api_connectivity():
    """Test basic API connectivity without authentication"""
    log_info("Testing basic API connectivity...")
    
    base_url = "https://nrt4.modaps.eosdis.nasa.gov"
    
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code in [200, 301, 302]:
            log_info("✅ NASA FIRMS API endpoint is reachable")
            return True
        else:
            log_warn(f"⚠️  NASA FIRMS API returned status: {response.status_code}")
            return False
    except requests.ConnectionError:
        log_error("❌ Cannot connect to NASA FIRMS API - check internet connection")
        return False
    except requests.Timeout:
        log_error("❌ Connection to NASA FIRMS API timed out")
        return False
    except Exception as e:
        log_error(f"❌ Unexpected error: {e}")
        return False

def test_token_authentication(token):
    """Test token authentication with NASA API"""
    log_info("Testing NASA token authentication...")
    
    # Use a simple API endpoint that requires authentication
    test_url = "https://nrt4.modaps.eosdis.nasa.gov/api/v2/content/archives/FIRMS/"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Nokekoi-App/1.0"
    }
    
    try:
        response = requests.get(test_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            log_info("✅ NASA token authentication successful")
            return True
        elif response.status_code == 401:
            log_error("❌ NASA token authentication failed - invalid token")
            return False
        elif response.status_code == 403:
            log_error("❌ NASA token authentication failed - access forbidden")
            return False
        else:
            log_warn(f"⚠️  Unexpected response status: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        log_error(f"❌ Request failed: {e}")
        return False

def test_data_availability(token):
    """Test if current data is available"""
    log_info("Testing data availability...")
    
    # Get yesterday's date for testing
    yesterday = datetime.now() - timedelta(days=1)
    year = yesterday.year
    day_of_year = yesterday.timetuple().tm_yday
    
    file_name = f"SUOMI_VIIRS_C2_South_America_VNP14IMGTDL_NRT_{year}{day_of_year:03d}.txt"
    test_url = f"https://nrt4.modaps.eosdis.nasa.gov/api/v2/content/archives/FIRMS/suomi-npp-viirs-c2/South_America/{file_name}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Nokekoi-App/1.0"
    }
    
    try:
        # HEAD request to check if file exists without downloading
        response = requests.head(test_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            content_length = response.headers.get('Content-Length', 'Unknown')
            log_info(f"✅ Yesterday's data is available (Size: {content_length} bytes)")
            return True
        elif response.status_code == 404:
            log_warn(f"⚠️  Yesterday's data not yet available ({file_name})")
            
            # Try day before yesterday
            day_before = datetime.now() - timedelta(days=2)
            year = day_before.year
            day_of_year = day_before.timetuple().tm_yday
            
            file_name_2 = f"SUOMI_VIIRS_C2_South_America_VNP14IMGTDL_NRT_{year}{day_of_year:03d}.txt"
            test_url_2 = f"https://nrt4.modaps.eosdis.nasa.gov/api/v2/content/archives/FIRMS/suomi-npp-viirs-c2/South_America/{file_name_2}"
            
            response_2 = requests.head(test_url_2, headers=headers, timeout=15)
            if response_2.status_code == 200:
                log_info(f"✅ Data from 2 days ago is available ({file_name_2})")
                return True
            else:
                log_warn("⚠️  Recent data not available - this may be normal")
                return False
        else:
            log_error(f"❌ Unexpected response status: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        log_error(f"❌ Request failed: {e}")
        return False

def test_ssl_certificate():
    """Test SSL certificate validity"""
    log_info("Testing SSL certificate...")
    
    try:
        import ssl
        import socket
        
        hostname = "nrt4.modaps.eosdis.nasa.gov"
        context = ssl.create_default_context()
        
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                # Check if certificate is valid
                not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                if not_after > datetime.now():
                    log_info(f"✅ SSL certificate is valid until {not_after}")
                    return True
                else:
                    log_error(f"❌ SSL certificate expired on {not_after}")
                    return False
                    
    except Exception as e:
        log_error(f"❌ SSL certificate test failed: {e}")
        return False

def test_environment_setup():
    """Test environment setup for production"""
    log_info("Testing environment setup...")
    
    checks = []
    
    # Check required environment variables
    required_vars = [
        'URL_SUOMI_VIIRS_C2',
        'BASE_SUOMI_FILE_NAME',
        'SUOMI_DATA_PATH',
        'PARQUET_PATH'
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            log_info(f"✅ {var} is configured")
            checks.append(True)
        else:
            log_warn(f"⚠️  {var} is not configured (using defaults)")
            checks.append(False)
    
    # Check if data directories exist
    data_path = os.getenv('SUOMI_DATA_PATH')
    if data_path and Path(data_path).parent.exists():
        log_info("✅ Data directory structure exists")
        checks.append(True)
    elif data_path:
        log_warn(f"⚠️  Data directory does not exist: {data_path}")
        checks.append(False)
    else:
        log_warn("⚠️  Data directory structure needs to be created")
        checks.append(False)
    
    return all(checks)

def generate_report(results):
    """Generate a test report"""
    log_info("Generating test report...")
    
    report = f"""
NASA FIRMS API Test Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}

Test Results:
- API Connectivity: {'✅ PASS' if results.get('connectivity') else '❌ FAIL'}
- Token Authentication: {'✅ PASS' if results.get('authentication') else '❌ FAIL'}
- Data Availability: {'✅ PASS' if results.get('data_availability') else '⚠️  WARNING'}
- SSL Certificate: {'✅ PASS' if results.get('ssl') else '❌ FAIL'}
- Environment Setup: {'✅ PASS' if results.get('environment') else '⚠️  WARNING'}

Overall Status: {'🎉 READY FOR PRODUCTION' if all([results.get('connectivity'), results.get('authentication'), results.get('ssl')]) else '⚠️  NEEDS ATTENTION'}

Recommendations:
"""
    
    if not results.get('authentication'):
        report += "- Configure a valid NASA FIRMS token in NTR_TOKEN environment variable\n"
    
    if not results.get('data_availability'):
        report += "- Check data availability - this may be normal if recent data isn't processed yet\n"
    
    if not results.get('environment'):
        report += "- Configure optional environment variables for better control\n"
    
    if all([results.get('connectivity'), results.get('authentication'), results.get('ssl')]):
        report += "- System is ready for production use!\n"
    
    return report

def main():
    """Main test function"""
    print(f"{GREEN}🔥 Nokekoi App - NASA API Test{NC}")
    print("=" * 50)
    
    # Load environment
    load_environment()
    
    # Get token
    token = get_nasa_token()
    if not token:
        log_error("❌ Cannot proceed without NASA token")
        return 1
    
    # Run tests
    results = {}
    
    results['connectivity'] = test_api_connectivity()
    results['ssl'] = test_ssl_certificate()
    
    if results['connectivity']:
        results['authentication'] = test_token_authentication(token)
        
        if results['authentication']:
            results['data_availability'] = test_data_availability(token)
        else:
            results['data_availability'] = False
    else:
        results['authentication'] = False
        results['data_availability'] = False
    
    results['environment'] = test_environment_setup()
    
    # Generate and display report
    print("\n" + "=" * 50)
    report = generate_report(results)
    print(report)
    
    # Return appropriate exit code
    critical_tests = ['connectivity', 'authentication', 'ssl']
    if all(results.get(test, False) for test in critical_tests):
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main()) 