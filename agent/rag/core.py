
# Data Retrieval

from pathlib import Path
from typing import List

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


load_dotenv()


# 1. Initialize Embedding Model

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


# 2. Initialize ChromaDB

BASE_DIR = Path(__file__).resolve().parent
CHROMA_PATH = BASE_DIR / "chroma_db"

vectorstore = Chroma(collection_name="credit_policy",embedding_function=embeddings,persist_directory=str(CHROMA_PATH))


# 3. Initialize Retriever

retriever = vectorstore.as_retriever(search_type="similarity",search_kwargs={"k": 4})


# 4. Retrieve Relevant Documents


def search_policy(query: str) -> List[Document]:
    """
    Retrieve relevant Credit Policy documents.

    Args:
        query: User query or credit investigation question.

    Returns:
        List of relevant Document objects.
    """

    documents = retriever.invoke(query)

    return documents


# 5. Test Retrieval

if __name__ == "__main__":

    query = "What are the eligibility requirements for a loan?"

    results = search_policy(query)

    for i, doc in enumerate(results, start=1):

        print(f"\n--- Document {i} ---")
        print("Source:", doc.metadata.get("source"))
        print("Page:", doc.metadata.get("page"))
        print("Content:", doc.page_content)
