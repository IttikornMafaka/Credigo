
from typing import List
import asyncio
from pathlib import Path
import hashlib

from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma


load_dotenv()

# 1. Initialize Embedding Model

model = "text-embedding-3-small"

embeddings = OpenAIEmbeddings(model=model,chunk_size=50,retry_min_seconds=15)


# 2. Connect to ChromaDB

BASE_DIR = Path(__file__).resolve().parent

CHROMA_PATH = BASE_DIR / "chroma_db"

vectorstore = Chroma(collection_name="credit_policy",embedding_function=embeddings,persist_directory=str(CHROMA_PATH))

# 3. Document Ingestion

async def index_document_async(documents: List[Document],batch_size: int = 50):
    """Split, embed, and index documents into ChromaDB."""

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)

    split_docs = text_splitter.split_documents(documents)

    if not split_docs:
        raise ValueError("No text chunks were created")

    print(f"Documents loaded: {len(documents)}")
    print(f"Chunks created: {len(split_docs)}")

    # Create batches
    batches = [split_docs[i:i + batch_size]for i in range(0, len(split_docs), batch_size)]

    successful = 0
    total_vectors = 0

    for i, batch in enumerate(batches):

        try:
            # Generate stable IDs
            ids = []

            for doc in batch:

                source = str(doc.metadata.get("source", ""))
                page = int(doc.metadata.get("page", 0))

                chunk_id = hashlib.sha256(f"{source}:{page}:{doc.page_content}".encode("utf-8")).hexdigest()

                ids.append(chunk_id)

                # Add metadata
                doc.metadata["source"] = source
                doc.metadata["page"] = page
                doc.metadata["title"] = "Credit Policy"

            # Upload documents to ChromaDB
            vectorstore.add_documents(documents=batch,ids=ids)

            successful += 1
            total_vectors += len(batch)

            print(f"Batch {i + 1}/{len(batches)} indexed successfully: "f"{len(batch)} vectors")

        except Exception as e:

            print(f"\nBatch {i + 1} failed!")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {e}")

            raise

    print(f"Successful batches: {successful}/{len(batches)}")

    return total_vectors


# 4. PDF File Path

PDF_PATH = BASE_DIR / "documents" / "Credit_policy.pdf"


# 5. Load PDF Documents

def load_documents():
    """Load Credit Policy PDF."""

    if not PDF_PATH.exists():
        raise FileNotFoundError(f"PDF file not found: {PDF_PATH}")

    loader = PyPDFLoader(str(PDF_PATH))

    documents = loader.load()

    if not documents:
        raise ValueError("No documents were loaded.")

    print("PDF loaded successfully!")
    print(f"Total pages: {len(documents)}")

    return documents


# 6. Main Function

async def main():

    # Step 1: Load PDF
    documents = load_documents()

    # Step 2: Index documents into ChromaDB
    total_vectors = await index_document_async(documents)

    print("\nIngestion completed!")
    print(f"Total vectors indexed: {total_vectors}")

    print(f"ChromaDB location: {CHROMA_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
