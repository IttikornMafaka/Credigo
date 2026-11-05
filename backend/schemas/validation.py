from pydantic import BaseModel
from uuid import UUID
from typing import Literal

class ValidationIssues(BaseModel) : 
    rule_id : str
    table : str 
    field : str 
    severity : Literal["ERROR","WARNING"]
    message : str 
    
class ValidationReport(BaseModel):
    customer_id: UUID
    total_checks: int
    passed: int
    failed: int
    overall_status: Literal["PASS", "NEEDS_REVIEW"]
    issues: list[ValidationIssues]