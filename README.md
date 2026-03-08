# LLM Project with Anthropic Claude

This project uses LangChain with Anthropic's Claude API and environment variable management.

## Project Structure

```
.
├── .env                    # Your environment variables (DO NOT COMMIT)
├── .env.example           # Template for environment variables (safe to commit)
├── .gitignore            # Git ignore file
├── config.py             # Configuration loader
├── Fundamentals.py       # Main agent implementation
├── example_usage.py      # Example usage script
├── requirements.txt      # Python dependencies
└── venv/                # Virtual environment
```

## Setup Instructions

### 1. Activate Virtual Environment

```bash
source venv/bin/activate
```

### 2. Install Dependencies (if not already installed)

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

**Option A: Copy from template**
```bash
cp .env.example .env
```

**Option B: Edit the existing .env file**
```bash
# Edit .env and add your API key
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

Get your API key from: https://console.anthropic.com/settings/keys

### 4. Run the Example

```bash
python example_usage.py
```

## Using the Configuration

### Import from config.py

```python
from config import ANTHROPIC_API_KEY, DEFAULT_MODEL, DEFAULT_TEMPERATURE

# Use in your code
print(f"Using model: {DEFAULT_MODEL}")
```

### Available Configuration Variables

From `config.py`:
- `ANTHROPIC_API_KEY` - Your Anthropic API key (required)
- `DEFAULT_MODEL` - Claude model to use (default: claude-3-5-sonnet-20241022)
- `DEFAULT_TEMPERATURE` - Temperature setting (default: 0.7)
- `DEBUG` - Debug mode flag (default: False)
- `ENVIRONMENT` - Environment name (default: development)

## Security Notes

⚠️ **Important:**
- Never commit your `.env` file to version control
- The `.env` file is already in `.gitignore`
- Share `.env.example` instead, which contains no secrets
- Keep your API keys secure and never share them publicly

## Environment Variables

Edit `.env` to customize:

```bash
# Required
ANTHROPIC_API_KEY=your_api_key_here

# Optional (with defaults)
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
TEMPERATURE=0.7
ENVIRONMENT=development
DEBUG=False
```

## Usage Examples

### Basic Usage

```python
from Fundamentals import agent
from langchain_core.messages import HumanMessage

result = agent.invoke({
    "user_message": HumanMessage(content="Hello!")
})
```

### Using Config Directly

```python
from config import ANTHROPIC_API_KEY, DEFAULT_MODEL
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model=DEFAULT_MODEL,
    api_key=ANTHROPIC_API_KEY
)

response = llm.invoke("Tell me a joke")
print(response.content)
```

## Troubleshooting

### "ANTHROPIC_API_KEY not found" Error

1. Make sure `.env` file exists in the project root
2. Verify the API key is set correctly in `.env`
3. Check that you're running Python from the project directory

### Import Errors

Make sure the virtual environment is activated:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Available Models

- `claude-3-5-sonnet-20241022` (default, most capable)
- `claude-3-5-haiku-20241022` (fast, cost-effective)
- `claude-3-opus-20240229` (most powerful)

Change the model in `.env`:
```bash
ANTHROPIC_MODEL=claude-3-5-haiku-20241022
```
