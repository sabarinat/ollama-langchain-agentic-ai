#!/usr/bin/env python3
"""
Test script for Simple LangChain + Ollama Agent with API Tool
Run with: source venv/bin/activate && python simple_agent_test.py
"""

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents import create_agent
import requests


@tool
def call_api(countries: list, tags: str, env: str, service: str) -> str:
    """
       Deploy services to Jenkins for specific countries and environments.
       
       Available options:
       - countries: Only ["AUS", "ZAF", "GBR"] (Australia, South Africa, UK)
       - tags: Any version string (e.g., "v1.2.9", "v2.0.0")
       - env: Only ["s1", "d1", "p1"] (s1=staging, d1=development, p1=production)
       - service: Only ["mobile-backend", "catalog", "sso"]
       
       Args:
           countries: List of country codes (e.g., ["AUS", "GBR"])
           tags: Version tag (e.g., "v1.2.9")
           env: Environment (s1, d1, or p1)
           service: Service name (mobile-backend, catalog, or sso)
       
       Returns:
           Jenkins deployment response as JSON string
       """
    try:
        payload = {
            "countries": countries,
            "tags": tags,
            "env": env,
            "service": service
        }
        
        print(f"\n[TOOL] Calling API with: {payload}")
        
        response = requests.post(
            "http://localhost:3000/api/deploy",
            json=payload,
            timeout=30
        )
        
        print(f"[TOOL] API Response: {response.text}")
        return response.text
        
    except requests.exceptions.ConnectionError:
        error_msg = "Error: Could not connect to API at localhost:3000. Make sure the server is running."
        print(f"[TOOL] {error_msg}")
        return error_msg
    except requests.exceptions.Timeout:
        error_msg = "Error: API request timed out."
        print(f"[TOOL] {error_msg}")
        return error_msg
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"[TOOL] {error_msg}")
        return error_msg


def main():
    """Main function"""
    print("=" * 60)
    print("Simple LangChain + Ollama Agent with API Tool - TEST")
    print("=" * 60)
    print()
    
    # Initialize the LLM
    print("Initializing Ollama with llama3.2...")
    llm = ChatOllama(
        model="llama3.2",
        temperature=0.7,
    )
    
    # Create the agent with the API tool
    print("Creating agent with API tool...")
    agent = create_agent(
        model=llm,
        tools=[call_api],
        system_prompt="""You are an assistant that can call an API at localhost:3000.

Use the call_api tool when the user wants to:
- Execute API commands
- Run operations in different environments (production, staging, development)
- Filter by countries, tags, or services

The API requires:
- countries: List of country codes (e.g., ["US", "UK", "IN"])
- tags: Comma-separated tags (e.g., "production,critical")
- env: Environment name (production, staging, or development)
- service: Service name (e.g., "payment", "auth", "api")

Always confirm the parameters with the user before calling the API if they're not clear.
For other questions not related to API calls, respond naturally without using the tool."""
    )
    
    print("✓ Agent ready!")
    print()
    
    # Test queries
    test_queries = [
        "Call API for US in production for payment service",
        "Execute API for UK and US with critical tags in staging environment",
        "What is your name?",  # Should not use tool
    ]


    while(True):
        query = input('enter questions')
        if(query != 'exit'):
          response = agent.invoke({"messages": [{"role": "user", "content": query}]})
        else:
            break;

    # for i, query in enumerate(test_queries, 1):
        # print("=" * 60)
        # print(f"Test {i}: {query}")
        # print("=" * 60)
        
        # try:
        #     input()
        #     response = agent.invoke({"messages": [{"role": "user", "content": query}]})
            
        #     # Extract and print response
        #     if isinstance(response, dict) and "messages" in response:
        #         messages = response["messages"]
        #         if messages:
        #             last_message = messages[-1]
        #             if hasattr(last_message, 'content'):
        #                 print(f"Response: {last_message.content}")
        #             else:
        #                 print(f"Response: {last_message}")
        #     else:
        #         print(f"Response: {response}")
                
        # except Exception as e:
        #     print(f"Error: {e}")
        
        # print()
    
    print("=" * 60)
    print("✅ Test completed!")
    print("=" * 60)
    print()
    print("To run interactively:")
    print("  python simple_agent.py")
    print()


if __name__ == "__main__":
    main()
