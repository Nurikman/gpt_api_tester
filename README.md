# OpenAI API Tester

A simple Streamlit application for testing OpenAI API calls with different models and parameters.

## Features

- 🔐 Secure API key input (password-masked)
- 🤖 Multiple OpenAI model selection (GPT-4o, GPT-4, GPT-3.5 Turbo, etc.)
- ⚙️ Adjustable parameters (temperature, max tokens, top_p)
- 📊 Token usage tracking
- 🔍 Full JSON response viewer
- 🎨 Clean, user-friendly interface

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd gpt_api_tester
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the displayed local URL (usually `http://localhost:8501`)

3. In the sidebar:
   - Enter your OpenAI API key
   - Select the model you want to use
   - Adjust parameters if needed

4. Enter your prompt in the input area and click "Send Request"

## Requirements

- Python 3.7+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Supported Models

**Flagship Models:**
- **GPT-4o** - OpenAI's most advanced multimodal model (text, image, audio)
- **GPT-4o Mini** - Fast, cost-effective version with strong performance
- **GPT-4 Turbo** - High-performance text model with 128k context window
- **GPT-4** - Original GPT-4 with excellent reasoning capabilities

**Efficient Models:**
- **GPT-3.5 Turbo** - Balanced performance for everyday tasks

**Reasoning Models:**
- **O1 Preview** - Advanced reasoning for complex problems
- **O1 Mini** - Compact reasoning model for STEM tasks

## Security Note

Your API key is only used for the current session and is not stored anywhere. The input field is password-masked for security.

## License

MIT License