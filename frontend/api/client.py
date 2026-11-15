from __future__ import annotations

import requests
import streamlit as st

from config import API_BASE_URL, REQUEST_TIMEOUT


# ==========================================
# 1. API ERROR
# ==========================================

class ApiError(Exception):

    def __init__(self, msg: str, status: int | None = None):
        super().__init__(msg)
        self.status = status


# ==========================================
# 2. REQUEST SESSION
# ==========================================

@st.cache_resource
def _session() -> requests.Session:

    s = requests.Session()
    s.trust_env = False
    s.headers.update({
        "Accept": "application/json"
    })

    return s


# ==========================================
# 3. BASE REQUEST
# ==========================================

def _request(method: str, path: str, **kw) -> dict | list:

    url = f"{API_BASE_URL.rstrip('/')}{path}"

    try:
        r = _session().request(
            method,
            url,
            timeout=REQUEST_TIMEOUT,
            **kw
        )

    except requests.Timeout:
        raise ApiError(f"Request timed out: {path}")

    except requests.ConnectionError as exc:
        raise ApiError(f"Cannot reach backend: {exc}")

    if not r.ok:
        raise ApiError(
            f"HTTP {r.status_code} | "
            f"URL: {url} | "
            f"Response: {r.text[:500]}",
            r.status_code
        )

    try:
        return r.json()

    except requests.exceptions.JSONDecodeError:
        raise ApiError(
            f"Invalid JSON response from backend: {path}",
            r.status_code
        )


# ==========================================
# 4. HTTP METHODS
# ==========================================

def get(path: str, params=None):
    return _request(
        "GET",
        path,
        params=params
    )


def post(path: str, json: dict):
    return _request(
        "POST",
        path,
        json=json
    )


# ==========================================
# 5. HEALTH CHECK
# ==========================================

def check_health():
    return get("/health")


# ==========================================
# 6. CUSTOMER APIs
# ==========================================

# Search customer using National ID
def search_customer(national_id: str):

    return get(
        "/api/customers/search",
        params={
            "national_id": national_id
        }
    )


# Get customer using Customer UUID
def get_customer(customer_id: str):

    return get(
        f"/api/customers/{customer_id}"
    )


# Get complete customer profile
def get_customer_profile(customer_id: str):

    return get(
        f"/api/customers/{customer_id}/profile"
    )


# Register new customer
def register_customer(customer_data: dict):

    return post(
        "/api/customers/",
        json=customer_data
    )


# ==========================================
# 7. INVESTIGATION APIs
# ==========================================

def run_investigation(
    customer_id: str,
    application_id: str
):

    return post(
        "/api/investigations/run",
        json={
            "customer_id": customer_id,
            "application_id": application_id
        }
    )
    

# Register new customer
def register_customer(customer_data: dict):

    return post("/api/customers/",json=customer_data)


# EMPLOYMENT APIs

def create_employment(customer_id: str,employment_data: dict):

    return post(f"/api/employment/{customer_id}",json=employment_data)

def create_account(customer_id: str, account_data: dict):
    return post(f"/api/account/{customer_id}", json=account_data)


def create_credit_history(customer_id: str, credit_data: dict):
    return post(f"/api/credit-history/{customer_id}", json=credit_data)


def create_loan(customer_id: str, loan_data: dict):
    return post(f"/api/loan/{customer_id}", json=loan_data)


def create_repayment(customer_id: str, repayment_data: dict):
    return post(f"/api/repayment/{customer_id}", json=repayment_data)


def create_loan_application(customer_id: str, application_data: dict):
    return post(f"/api/loan-application/{customer_id}", json=application_data)