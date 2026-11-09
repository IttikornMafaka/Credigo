from typing import TypedDict
from uuid import UUID
class InvestigationState(TypedDict,total=False) : 
    
    # 1. Customer Information
    customer_id : UUID
    customer_data : dict 
    
    # 2. Validation Result
    validation_result : dict 
    
    # 3. Machine Learning Prediction
    ml_prediction : dict 
    
    # 4. RAG Credit Policy
    retrieval : list[dict]
    
    # 5. LLM Analysis
    policy_analysis : dict 
    ai_recommend : str 
    
    # 6. Evidence หลักฐานประกอบ
    evidence :  list[dict] 
    
    #7. Report
    report_path : str 
    
    #8 Status
    status : str 
    error : str    