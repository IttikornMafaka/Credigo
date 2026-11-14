from __future__ import annotations
import requests
import streamlit as st
from config import API_BASE_URL, REQUEST_TIMEOUT


class ApiError(Exception):
    def __init__(self, msg: str, status: int | None = None):
        super().__init__(msg)
        self.status = status


@st.cache_resource
def _session() -> requests.Session:
    s = requests.Session()
    s.trust_env = False
    s.headers.update({"Accept": "application/json"})
    return s


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
            f"HTTP {r.status_code} | URL: {url} | Response: {r.text[:500]}",
            r.status_code
        )

    return r.json()


def get(path, params=None):  return _request("GET", path, params=params)

def post(path, json):        return _request("POST", path, json=json)

    
def check_health():
    return get("/health")


def search_customer(national_id: str):
    return get(
        "/api/customers/search",
        params={"national_id": national_id}
    )


def get_customer(customer_id: str):
    return get(f"/api/customers/{customer_id}")


def run_investigation(customer_id: str, application_id: str):
    return post(
        "/api/investigations/run",
        json={
            "customer_id": customer_id,
            "application_id": application_id
        }
    )