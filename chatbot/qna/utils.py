from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
import logging

logger = logging.getLogger("qna")


def load_qa_model(text):
    # Split the text into smaller chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_text(text)
    logger.info(f"#qna#utils#load_qa_model# texts: {texts}")

    # Create embeddings for the text chunks
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts, embeddings)
    logger.info(f"#qna#utils#load_qa_model# vectorstore: {vectorstore}")

    # Load the QA chain
    qa_chain = load_qa_chain(OpenAI())
    logger.info(f"#qna#utils#load_qa_model# qa_chain: {qa_chain}")

    return vectorstore, qa_chain


def answer_question(question, text):
    vectorstore, qa_chain = load_qa_model(text)
    logger.info(f"#qna#utils#answer_question# vectorstore: {vectorstore}, qa_chain:{qa_chain}")

    # Get relevant text chunks
    docs = vectorstore.similarity_search(question, k=3)
    logger.info(f"#qna#utils#answer_question# docs: {docs}")

    # Use the QA chain to answer the question
    answer = qa_chain.run(input_documents=docs, question=question)
    logger.info(f"#qna#utils#answer_question# answer:{answer}")

    return answer
