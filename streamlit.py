import streamlit as st
import requests
import json
from streamlit_lottie import st_lottie

# Function to load Lottie file
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load the brain animation
lottie_brain = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_SkhtL8.json")

# Function to call the API
def call_api(query):
    # Updated API URL
    api_url = "https://mqcb46nbcg.execute-api.eu-west-2.amazonaws.com/dev/chat"

    try:
        response = requests.post(api_url, json={"user_query": query})
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()  # This should now work correctly
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while calling the API: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON response: {str(e)}")
        return None

# Streamlit app
def main():
    st.set_page_config(page_title="IBT Learning AI Assistant", page_icon="🧠", layout="wide")
    st.title("🤖 IBT Learning Tech Connect AI Assistant")

    # Initialize session state for conversation history and input field
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    if "user_question" not in st.session_state:
        st.session_state.user_question = ""

    # User input
    user_question = st.text_input("Ask your question:", value=st.session_state.user_question)

    if st.button("Get Answer"):
        if user_question:
            # Display spinning brain while processing
            with st.spinner("Thinking..."):
                brain_placeholder = st.empty()
                with brain_placeholder:
                    st_lottie(lottie_brain, height=200, key="brain")

                # Call API
                result = call_api(user_question)

                # Remove spinning brain
                brain_placeholder.empty()

            if result:
                # Append the new question and response to conversation history
                st.session_state.conversation.append({
                    "question": user_question,
                    "answer": result.get('generated_response', 'No response body available')
                })
                # Clear the input field after response
                st.session_state.user_question = ""
            else:
                st.error("Failed to get a valid response from the API.")
        else:
            st.warning("Please enter a question.")

    # Display the conversation history
    st.subheader("Conversation History:")
    for entry in st.session_state.conversation:
        st.write("**You:**")
        st.markdown(f"> {entry['question']}")  # Display question with quote format for distinction
        st.write("**Assistant:**")
        st.markdown(f"> {entry['answer']}")
        st.write("---")  # Add a horizontal divider for separation

if __name__ == "__main__":
    main()
