import os 
from dotenv import load_dotenv 
from langchain_openai import ChatOpenAI
from agent.schemas import CreditAnalysisResult

load_dotenv()

model = "gpt-4.1-mini"

def get_llm() -> ChatOpenAI : 
    """
    Initialize and return OpenAI Chat Model  
    """
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key : 
        raise ValueError("OPENAI_API_KEY IS MISSING ")
    
    llm = ChatOpenAI(model=model,temperature=0,api_key=api_key)
    return llm 
