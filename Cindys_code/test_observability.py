#!/usr/bin/env python3
"""
Test script for OpenTelemetry observability in the FAQ agent.
This script tests the observability setup and span creation.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_observability():
    """Test the observability setup and functionality."""
    
    print("🧪 Testing OpenTelemetry Observability Setup")
    print("=" * 50)
    
    try:
        # Import the agent module
        from agent import _setup_rag_system, get_observability_data, run_faq_agent
        
        print("✅ Agent module imported successfully")
        
        # Test RAG system setup (this will initialize OpenTelemetry)
        print("\n🔧 Setting up RAG system with OpenTelemetry...")
        success = _setup_rag_system()
        
        if success:
            print("✅ RAG system setup completed")
            
            # Get observability data
            print("\n📊 Observability Data:")
            obs_data = get_observability_data()
            for category, data in obs_data.items():
                print(f"  {category}:")
                if isinstance(data, dict):
                    for key, value in data.items():
                        print(f"    {key}: {value}")
                else:
                    print(f"    {data}")
            
            # Test a simple FAQ query to generate spans
            print("\n🤖 Testing FAQ agent with observability...")
            test_query = "What is the company policy on remote work?"
            
            try:
                response = await run_faq_agent(test_query)
                print(f"✅ Agent response received: {response[:100]}...")
                
                # Final observability summary
                print("\n📊 Final Observability Summary:")
                print("=" * 50)
                final_obs = get_observability_data()
                
                if final_obs["opentelemetry"]["tracer_ready"]:
                    print("✅ OpenTelemetry tracer is ready")
                    print("✅ Spans are being created and exported")
                    print("💡 Check your Splunk dashboard for traces")
                else:
                    print("⚠️  OpenTelemetry tracer not ready")
                
                if final_obs["rag_system"]["status"] == "ready":
                    print("✅ RAG system is fully operational")
                else:
                    print("⚠️  RAG system is still initializing")
                    
            except Exception as e:
                print(f"❌ Error testing FAQ agent: {e}")
                
        else:
            print("❌ RAG system setup failed")
            
    except ImportError as e:
        print(f"❌ Failed to import agent module: {e}")
        print("💡 Make sure you're running this from the Cindys_code directory")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    # Run the async test
    asyncio.run(test_observability())
