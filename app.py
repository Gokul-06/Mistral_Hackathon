# Import necessary libraries
import streamlit as st
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# Set your API key and model
api_key = "jYwogAlMG9v99x82NjQPLMg50co5Zazh"
model = "mistral-large-latest"

# Initialize MistralClient
client = MistralClient(api_key=api_key)

# Create a text input field
user_query = st.text_input("Enter your search query")

# If the user enters a query, use Mistral AI to get a response
if user_query:
    chat_response = client.chat(
        model=model,
        messages=[ChatMessage(role="user", content=user_query)]
    )

    # Display the response
    st.write(chat_response.choices[0].message.content)
