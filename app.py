import streamlit as st
import openai
from openai import OpenAI
import json

# Set page config
st.set_page_config(
    page_title="OpenAI API Tester",
    page_icon="🤖",
    layout="wide"
)

# Title and description
st.title("🤖 OpenAI API Tester")
st.markdown("Test OpenAI API calls with different models and prompts")

# Sidebar for API configuration
st.sidebar.header("API Configuration")

# API Key input
api_key = st.sidebar.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="sk-..."
)

# Model selection with descriptions
model_info = {
    "gpt-4o": {
        "name": "GPT-4o",
        "description": "GPT-4o (“o” for “omni”) is our versatile, high-intelligence flagship model. It accepts both text and image inputs, and produces text outputs (including Structured Outputs). It is the best model for most tasks, and is our most capable model outside of our o-series models."
    },
    "o4-mini": {
        "name": "o4-mini", 
        "description": "o4-mini is our latest small o-series model. It's optimized for fast, effective reasoning with exceptionally efficient performance in coding and visual tasks."
    },
    "gpt-4.1": {
        "name": "GPT-4.1",
        "description": "GPT-4.1 is our flagship model for complex tasks. It is well suited for problem solving across domains."
    },
    "o3": {
        "name": "o3",
        "description": "o3 is a well-rounded and powerful model across domains. It sets a new standard for math, science, coding, and visual reasoning tasks. It also excels at technical writing and instruction-following. Use it to think through multi-step problems that involve analysis across text, code, and images."
    }
}

model_options = list(model_info.keys())

selected_model = st.sidebar.selectbox(
    "Select Model",
    model_options,
    index=0
)

# Display model description
if selected_model in model_info:
    st.sidebar.markdown("### Model Info")
    st.sidebar.markdown(f"**{model_info[selected_model]['name']}**")
    st.sidebar.markdown(model_info[selected_model]['description'])

# Advanced parameters
st.sidebar.subheader("Parameters")

# Check if selected model is o-series
is_o_series_model = selected_model.startswith(('o3', 'o4-mini', 'o1'))

if is_o_series_model:
    st.sidebar.warning("⚠️ O-series models only support default temperature (1.0) and top_p (1.0). These sliders will be ignored.")

temperature = st.sidebar.slider("Temperature", 0.0, 2.0, 0.7, 0.1, disabled=is_o_series_model)

# Temperature guide
st.sidebar.markdown("""
**💡 Temperature Quick Guide:**
- **0.0-0.3**: Focused, consistent, factual
- **0.4-0.7**: Balanced creativity vs accuracy
- **0.8-1.2**: Creative, varied responses
- **1.3-2.0**: Very creative, unpredictable

*Lower = More predictable, Higher = More creative*
""")

max_tokens = st.sidebar.number_input("Max Tokens", 1, 100000, 10000)

# Max tokens guide
st.sidebar.markdown("""
**💡 Max Tokens Quick Guide:**
- **Short answers**: 50-300 tokens
- **Explanations**: 300-800 tokens  
- **Long content**: 1000-3000 tokens
- **Code/Essays**: 1500-4000 tokens

*~75 words = 100 tokens*
""")

top_p = st.sidebar.slider("Top P", 0.0, 1.0, 1.0, 0.1, disabled=is_o_series_model)

# Top P guide
st.sidebar.markdown("""
**💡 Top P Quick Guide:**
- **1.0**: Maximum diversity (all words)
- **0.8-0.9**: Creative writing, brainstorming
- **0.5-0.7**: Balanced conversations
- **0.1-0.4**: Focused, technical answers

*Lower = More focused responses*
""")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Input")
    
    # Prompt input
    prompt = st.text_area(
        "Enter your prompt:",
        height=300,
        placeholder="Type your message here..."
    )
    
    # Submit button
    submit_button = st.button("Send Request", type="primary")

with col2:
    st.header("Response")
    
    # Response area
    if submit_button:
        if not api_key:
            st.error("Please enter your OpenAI API key in the sidebar.")
        elif not prompt:
            st.error("Please enter a prompt.")
        else:
            try:
                # Initialize OpenAI client
                client = OpenAI(api_key=api_key)
                
                # Show loading spinner
                with st.spinner("Generating response..."):
                    # Prepare API call parameters
                    api_params = {
                        "model": selected_model,
                        "messages": [{"role": "user", "content": prompt}]
                    }
                    
                    # Check if this is an o-series model (has parameter restrictions)
                    is_o_series = selected_model.startswith(('o3', 'o4-mini', 'o1'))
                    
                    if is_o_series:
                        # O-series models: limited parameters
                        api_params["max_completion_tokens"] = max_tokens
                        # Note: o-series models only support temperature=1.0 and top_p=1.0
                    else:
                        # Standard models: full parameter support
                        api_params["temperature"] = temperature
                        api_params["top_p"] = top_p
                        api_params["max_tokens"] = max_tokens
                    
                    # Make API call
                    response = client.chat.completions.create(**api_params)
                
                # Display response
                st.subheader("AI Response:")
                st.write(response.choices[0].message.content)
                
                # Show usage info
                st.subheader("Usage Information:")
                usage = response.usage
                col_prompt, col_completion, col_total = st.columns(3)
                
                with col_prompt:
                    st.metric("Prompt Tokens", usage.prompt_tokens)
                with col_completion:
                    st.metric("Completion Tokens", usage.completion_tokens)
                with col_total:
                    st.metric("Total Tokens", usage.total_tokens)
                
                # Show full response (expandable)
                with st.expander("View Full Response JSON"):
                    st.json(response.model_dump())
                    
            except openai.AuthenticationError:
                st.error("Invalid API key. Please check your OpenAI API key.")
            except openai.RateLimitError:
                st.error("Rate limit exceeded. Please try again later.")
            except openai.APIError as e:
                st.error(f"OpenAI API error: {str(e)}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Instructions
st.markdown("---")
st.markdown("""
### How to use:
1. **Enter your OpenAI API key** in the sidebar (find yours at [platform.openai.com](https://platform.openai.com/api-keys))
2. **Select the model** that best fits your use case (see descriptions in sidebar)
3. **Adjust parameters** if needed:
   - **Temperature**: Higher = more creative, Lower = more focused
   - **Max Tokens**: Maximum length of response
   - **Top P**: Controls response diversity
4. **Enter your prompt** in the input area
5. **Click "Send Request"** to get the AI response

### Model Recommendations:

**🌟 For Advanced Tasks:**
- **GPT-4o**: Versatile flagship model with text & image capabilities, best for most tasks
- **GPT-4.1**: Complex problem-solving across multiple domains

**⚡ For Speed & Efficiency:**
- **o4-mini**: Fast reasoning with efficient performance in coding and visual tasks

**🧠 For Advanced Reasoning & Analysis:**
- **o3**: Powerful across all domains - excels at math, science, coding, and visual reasoning

### Notes:
- Your API key is not stored and is only used for the current session
- Different models have different costs - check [OpenAI pricing](https://openai.com/pricing) for details
- **O-series models (o3, o4-mini)** have special characteristics:
  - Take longer to respond as they "think" through problems
  - Only support default temperature (1.0) and top_p (1.0) values
  - Use `max_completion_tokens` instead of `max_tokens`
- Some models may not be available based on your OpenAI plan
""") 