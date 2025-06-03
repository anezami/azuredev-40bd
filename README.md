# Azure AI Foundry Agent Client

This project provides an interactive command-line interface for interacting with an Azure AI Foundry agent. It enables users to send prompts to an AI agent and receive responses in a conversational manner.

## Features

- Interactive chat interface with the Azure AI agent
- Support for creating new conversation threads
- Display of source citations for AI responses
- Ability to continue conversations in existing threads
- Command-line options for various configuration settings

## Prerequisites

- Python 3.6 or higher
- Azure account with access to Azure AI Foundry
- Required Python packages (see Installation)

## Installation

1. Clone this repository or download the source code.

2. Create a virtual environment:

```powershell
# On Windows with PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

Or simply run the install script:

```bash
# On macOS/Linux
./install.sh

# On Windows with Git Bash or similar
bash install.sh
```

## Usage

### Basic Usage

To run the agent with interactive prompts:

```bash
python run_agent.py
```

This will:
- Connect to the Azure AI agent
- Create a new conversation thread
- Prompt you to enter your questions or commands

### Command Line Options

The script supports several command line options:

```bash
python run_agent.py [--thread_id THREAD_ID] [--prompt PROMPT] [--debug]
```

- `--thread_id`: Use an existing thread instead of creating a new one
- `--prompt`: Specify an initial prompt (otherwise, you'll be prompted interactively)
- `--debug`: Enable debug output to see detailed message information

### Interactive Commands

While the script is running, you can use these special commands:

- `help`: Show a list of available commands
- `thread`: Display the current thread ID (useful for continuing conversations later)
- `clear`: Create a new conversation thread
- `exit` or `quit`: Exit the application

## Examples

1. Start a new conversation:

```bash
python run_agent.py
```

2. Continue an existing conversation:

```bash
python run_agent.py --thread_id thread_123456789
```

3. Send a one-time prompt:

```bash
python run_agent.py --prompt "What is the current weather in San Diego?"
```

## Troubleshooting

If you encounter authentication issues:
- Ensure you're logged into your Azure account
- Verify that you have access to the Azure AI Foundry project

If responses aren't appearing:
- Try using the `--debug` flag to see the raw message structure
- Check that the agent ID in the script is correct

## License

This project is licensed under the terms of the MIT license.

## Acknowledgments

- Azure AI Foundry team for providing the underlying API
- Azure Identity library for authentication

