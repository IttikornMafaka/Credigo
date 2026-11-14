
import json

from dotenv import load_dotenv
from openai import OpenAI

from backend.prompts.credit_risk_prompt import CREDIT_RISK_SYSTEM_PROMPT
from backend.services.report_validator import validate_recommendation , validate_evidence_references , validate_risk_severity , validate_overall_risk_level , validate_credit_risk_report
from backend.schemas.credit_risk_report import CreditRiskReport


load_dotenv()

MODEL_NAME = "gpt-4.1-mini"


def generate_credit_risk_report(evidence_context: dict) -> CreditRiskReport:

    # 1. Prepare Evidence Context
    evidence_json = json.dumps(evidence_context,ensure_ascii=False,indent=2)

    # 2. Create OpenAI Client
    client = OpenAI(timeout=30.0,max_retries=2)

    # 3. Send request to OpenAI
    completion = client.chat.completions.parse(
        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": CREDIT_RISK_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": (
                    "Investigate this credit application "
                    "using the following evidence:\n\n"
                    f"{evidence_json}"
                )
            }
        ],

        response_format=CreditRiskReport,

        temperature=0.2
    )

    # 4. Extract response
    message = completion.choices[0].message

    if message.refusal:
        raise RuntimeError(
            f"LLM refused the request: {message.refusal}"
        )

    report = message.parsed

    if report is None:
        raise RuntimeError(
            "LLM did not return a valid CreditRiskReport."
        )

     # 5. Validate Evidence References
    report = validate_evidence_references(report=report,evidence_context=evidence_context)
    report = validate_recommendation(report=report,evidence_context=evidence_context)
    report = validate_risk_severity(report)
    report = validate_overall_risk_level(report=report,evidence_context=evidence_context)
    report = validate_credit_risk_report(report=report,evidence_context=evidence_context)


    # 7. Return validated report
    return report