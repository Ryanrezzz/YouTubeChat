import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
load_dotenv()

#Vector Store

def get_vector_store(chunks):
    embedding = GoogleGenerativeAIEmbeddings(model='gemini-embedding-2-preview')
    vector_store = FAISS.from_texts(chunks,embedding)
    return vector_store


# Retriever

def get_retriever(vector_store):
    retriever = vector_store.as_retriever(
        search_kwargs={'k':5}
    )
    return retriever

#Prompt
def get_prompt():
    prompts = ChatPromptTemplate([
        ('system','You are a helpful assistant that answers questions based on YouTube video transcripts. Use the provided context to answer. If the answer is truly not in the context, say so.'),
        ('placeholder','{chat_history}'),
        ('human','''Context from transcript:
{context}

Question: {question}''')
    ])
    return prompts

#LLM 
def get_llm():
    model = ChatGroq(
        model='llama-3.3-70b-versatile',
        temperature=0.7,
        max_tokens=600
    )
    return model

def format_docs(retrieved_docs):
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
    return context_text

#chain



def get_chain(chunks):
    chain = RunnableParallel(
        {
            'context': RunnableLambda(lambda x: x["question"]) | get_retriever(get_vector_store(chunks)) | RunnableLambda(format_docs),
            'question': RunnableLambda(lambda x: x["question"]),
            'chat_history': RunnableLambda(lambda x: x["chat_history"])
        }
    )
    main_chain = chain | get_prompt() | get_llm() | StrOutputParser()
    return main_chain


if __name__ == "__main__":
    Url = input("Enter video link: ")
    video_id = Url.split("v=")[1].split("&")[0]

    try:
        transcript = YouTubeTranscriptApi().fetch(video_id)
        transcript_text = " ".join(snippet.text for snippet in transcript)
    except TranscriptsDisabled:
        print("Transcripts are disabled for this video")
        exit()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    history = ChatMessageHistory()
    chunks = splitter.split_text(transcript_text)

    chain = get_chain(chunks)
    while True:
        query = input("Ask a question: ")
        if query.lower() == "exit":
            break
        response = chain.invoke({
            'question':query,
            'chat_history':history.messages
        })
        print(response)
        history.add_user_message(query)
        history.add_ai_message(response)
