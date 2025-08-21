#!/usr/bin/env python3
"""
Test script to verify Phoenix OpenTelemetry integration
Run this to check if Phoenix is properly configured and accessible.
"""

import requests
import time

def test_phoenix_connection():
    """Test if Phoenix server is accessible."""
    
    print("🔍 Testing Phoenix connection...")
    
    # Test basic connectivity
    try:
        response = requests.get("http://localhost:6006", timeout=5)
        if response.status_code == 200:
            print("✅ Phoenix server is accessible")
            return True
        else:
            print(f"⚠️  Phoenix responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Phoenix at http://localhost:6006")
        print("💡 Make sure Phoenix is running:")
        print("   - beeai platform start --set phoenix.enabled=true")
        print("   - or: pip install phoenix && phoenix start")
        return False
    except requests.exceptions.Timeout:
        print("⏰ Phoenix connection timed out")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_trace_endpoint():
    """Test if the trace endpoint is accessible."""
    
    print("\n🔍 Testing trace endpoint...")
    
    try:
        response = requests.get("http://localhost:6006/v1/traces", timeout=5)
        if response.status_code in [200, 405]:  # 405 is expected for GET to trace endpoint
            print("✅ Trace endpoint is accessible")
            return True
        else:
            print(f"⚠️  Trace endpoint responded with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing trace endpoint: {e}")
        return False

def main():
    """Main test function."""
    
    print("🐝 Phoenix Integration Test")
    print("=" * 40)
    
    # Test basic connectivity
    phoenix_accessible = test_phoenix_connection()
    
    if phoenix_accessible:
        # Test trace endpoint
        trace_accessible = test_trace_endpoint()
        
        print("\n📊 Test Results:")
        print(f"  Phoenix Server: {'✅ Accessible' if phoenix_accessible else '❌ Not accessible'}")
        print(f"  Trace Endpoint: {'✅ Accessible' if trace_accessible else '❌ Not accessible'}")
        
        if phoenix_accessible and trace_accessible:
            print("\n🎉 Phoenix integration is ready!")
            print("💡 You can now run the main demo:")
            print("   python beeai_python_demo.py")
        else:
            print("\n⚠️  Some Phoenix services are not accessible")
            print("💡 Check your Phoenix configuration")
    else:
        print("\n❌ Phoenix is not accessible")
        print("💡 Please start Phoenix before running the demo")
    
    print("\n🔗 Phoenix URLs:")
    print("  Main Interface: http://localhost:6006")
    print("  Trace Endpoint: http://localhost:6006/v1/traces")

if __name__ == "__main__":
    main()
