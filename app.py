import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


import streamlit as st
from supadata import Supadata
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.chat_message_histories import ChatMessageHistory
from main import get_chain 
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title='Chat With YouTube Video',
    page_icon='🤖'
)
st.title("YouTube Chat ▶️")
st.caption('Chat with your favorite youtube videos')

#Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.history = ChatMessageHistory()
    st.session_state.chain = None


url = st.text_input('Enter video url')

if url and st.button("Load Video"):
    try:
        with st.spinner("⏳ Loading transcript & building vector store..."):
            api_key = os.getenv("SUPADATA_API_KEY") or st.secrets.get("SUPADATA_API_KEY", None)
            supadata_client = Supadata(api_key=api_key)
            transcript = supadata_client.transcript(url=url, text=True)
            transcript_text = transcript.content
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_text(transcript_text)
            st.session_state.chain = get_chain(chunks)
            st.session_state.video_url = url

            st.session_state.messages = []
            st.session_state.history = ChatMessageHistory()
        st.success("✅ Video loaded! Start asking questions.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        
if "video_url" in st.session_state:
    st.video(st.session_state.video_url)

for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.write(msg['content'])

if query := st.chat_input("Ask a question about the video"):
    if not st.session_state.chain:
        st.warning("⚠️ Please load a video first!")
    else:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.write(query)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chain.invoke({
                    "question": query,
                    "chat_history": st.session_state.history.messages
                })
                st.write(response)
        st.session_state.history.add_user_message(query)
        st.session_state.history.add_ai_message(response)
        st.session_state.messages.append({"role": "assistant", "content": response})