import streamlit as st
import os
import openai

openai_api_key = os.getenv("OPENAI_API_KEY")
messages = []
if 'code_executed' not in st.session_state:
    # Initialize the OpenAI client and create a thread
    api_config = st.secrets["api"]
    openai_api_key = api_config["openai_api_key"]
    st.session_state.messages = []
    st.session_state.client = openai.OpenAI(api_key=openai_api_key)
    st.session_state.thread = st.session_state.client.beta.threads.create()
    st.session_state.code_executed = True

# Streamlit app
def main():
    import re
    global messages
    thread = st.session_state.thread
    from dotenv import load_dotenv
    load_dotenv()

    # Create a layout with two columns
    left_column, right_column = st.columns([1, 3])

    # Add an image to the left column
    left_column.image("rubo-bot.png", use_column_width=True)

    # Input field for the question
    with right_column:
        st.title(f"CPEB 2024 - Posez-nous vos questions...")
        question = st.text_input("Entrez votre question:")
        if st.button("Obtenir la réponse"):
            # Check if a question is provided
            if not question:
                st.warning("Please enter a question.")
            else:
                # Generate and display the answer
                messages = question_answer(question)
                question = ''
                for msg in reversed(messages):
                 role = msg.role
                 content = msg.content[0].text.value
                 if role.lower() == "user":
                     background_color = "lightblue"
                 elif role.lower() == "assistant":
                     background_color = "lightgrey"
                 else:
                     background_color = "white"
                 pattern = re.compile(r'&#8203;``【oaicite:3】``&#8203;')    
                 styled_content = f"<div style='background-color:{background_color}; padding:10px;'>{re.sub(pattern, '', content)}</div>"
                 st.markdown(styled_content, unsafe_allow_html=True)


def question_answer(question):
 global counter
 client = st.session_state.client
 thread = st.session_state.thread
 messages = []
 import time

 message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role = "user",
    content = question
)
 run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id = 'asst_ClB4u6msV6MOYyH57halU5cU',
)
 time.sleep(40)

 run_status = client.beta.threads.runs.retrieve(
  thread_id = thread.id,
  run_id = run.id
 )

 if run_status.status == 'completed':
  messages = client.beta.threads.messages.list(
  thread_id = thread.id
  st.session_state.messages = messages
  )
 else:
  messages = st.session_state.messages

 return(messages.data)

if __name__ == "__main__":

    main()
