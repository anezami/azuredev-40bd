from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import argparse
import sys
import time
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def print_help():
    """Print help information about available commands"""
    print("\nAvailable commands:")
    print("  help       - Show this help message")
    print("  exit       - Exit the application")
    print("  thread     - Show current thread ID")
    print("  clear      - Create a new thread")
    print("  <any text> - Send as a prompt to the agent")
    print()

def main():
    parser = argparse.ArgumentParser(description='Interact with an AI agent.')
    parser.add_argument('--thread_id', help='Optional existing thread ID to use. If not provided, a new thread will be created.')
    parser.add_argument('--prompt', help='Prompt to send to the agent. If not provided, you will be prompted interactively.')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()

    debug = args.debug

    # Get connection string and agent ID from environment variables
    ai_conn_str = os.getenv('AI_PROJECT_CONNECTION_STRING')
    agent_id = os.getenv('AZURE_EXISTING_AGENT_ID')

    # Initialize the project client
    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str=ai_conn_str)

    # Get the agent
    agent = project_client.agents.get_agent(agent_id)
    print(f"Connected to agent: {agent.name if hasattr(agent, 'name') else agent.id}\n")

    # Get or create a thread
    thread = None
    if args.thread_id:
        try:
            thread = project_client.agents.get_thread(args.thread_id)
            print(f"Using existing thread: {thread.id}")
        except Exception as e:
            print(f"Error accessing thread {args.thread_id}: {e}")
            print("Creating a new thread instead.")
            thread = project_client.agents.create_thread()
            print(f"Created new thread: {thread.id}")
    else:
        thread = project_client.agents.create_thread()
        print(f"Created new thread: {thread.id}")

    print("Type 'help' for available commands.")
    
    # Get the user prompt
    user_prompt = args.prompt
    if not user_prompt:
        user_prompt = input("\nEnter your prompt: ")
    
    while user_prompt.lower() not in ('exit', 'quit'):
        # Handle special commands
        if user_prompt.lower() == 'help':
            print_help()
        elif user_prompt.lower() == 'thread':
            print(f"\nCurrent thread ID: {thread.id}")
        elif user_prompt.lower() == 'clear':
            thread = project_client.agents.create_thread()
            print(f"\nCreated new thread: {thread.id}")
        else:
            # Process regular prompt
            print("\n----- Sending your prompt to the agent -----")
            
            # Create a user message in the thread
            message = project_client.agents.create_message(
                thread_id=thread.id,
                role="user",
                content=user_prompt
            )
            
            # Create and process a run
            print("Processing your request...")
            run = project_client.agents.create_and_process_run(
                thread_id=thread.id,
                agent_id=agent.id)
            
            # Get all messages
            messages = project_client.agents.list_messages(thread_id=thread.id)
            
            # Display the agent's response
            print("\n----- Agent Response -----")
            
            # Debug: Print message structure
            if debug and len(messages.text_messages) > 0:
                print("First message structure:")
                print(json.dumps(messages.text_messages[0].as_dict(), indent=2))
            
            # Based on the debug output, we can see messages are in reverse chronological order
            # The first message should be the latest response from the agent
            if messages.text_messages and len(messages.text_messages) >= 1:
                # Get the first message which should be the agent's response
                response = messages.text_messages[0].as_dict()
                
                # Extract and print the text value
                if 'text' in response and 'value' in response['text']:
                    print(response['text']['value'])
                    
                    # Print source citations if any
                    if 'annotations' in response['text']:
                        for annotation in response['text']['annotations']:
                            if annotation.get('type') == 'url_citation' and 'url_citation' in annotation:
                                url_info = annotation['url_citation']
                                print(f"\nSource: {url_info.get('title', 'Unknown')}")
                                print(f"URL: {url_info.get('url', 'No URL')}")
                else:
                    print("Response received but no text content was found.")
            else:
                print("No response received from the agent.")
            
            print("--------------------------")
        
        # Get the next prompt
        user_prompt = input("\nEnter your prompt: ")
    
    print("\nExiting. Thank you for using the Azure AI agent!")

if __name__ == "__main__":
    main()