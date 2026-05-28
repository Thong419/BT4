from __future__ import annotations

import os

import requests
import streamlit as st


def get_api_base_url() -> str:
    return os.getenv("API_BASE_URL", "http://localhost:8000")


def call_agent(message: str) -> dict[str, object]:
    response = requests.post(f"{get_api_base_url()}/run-agent", json={"message": message}, timeout=180)
    response.raise_for_status()
    return response.json()


st.set_page_config(page_title="Banking AI Agent", page_icon="🏦", layout="wide")

st.title("Banking AI Agent")
st.caption("Submit a customer message and inspect the structured workflow result.")

with st.sidebar:
    st.subheader("Connection")
    st.write(f"API base URL: {get_api_base_url()}")
    st.write("The frontend talks only to the FastAPI backend.")

message = st.text_area(
    "Customer message",
    value="I lost my credit card and need to block it immediately",
    height=160,
    placeholder="Enter the banking message here...",
)

col1, col2 = st.columns([1, 3])
with col1:
    submitted = st.button("Run agent", type="primary")

if submitted:
    if not message.strip():
        st.error("Please enter a customer message.")
    else:
        try:
            result = call_agent(message.strip())
            left, right = st.columns(2)

            with left:
                st.subheader("Summary")
                st.write(f"**Predicted intent:** {result.get('predicted_intent')}")
                st.write(f"**Confidence:** {result.get('confidence')}")
                st.write(f"**Risk level:** {result.get('risk_level')}")
                st.write(f"**Routing decision:** {result.get('routing_decision')}")
                st.write(f"**Next action:** {result.get('next_recommended_action')}")

            with right:
                st.subheader("Draft reply")
                st.write(result.get("draft_reply"))

            st.subheader("Structured workflow result")
            st.json(result)
        except requests.RequestException as exc:
            st.error(f"Backend request failed: {exc}")

st.divider()
st.subheader("Example")
st.code('{"message": "I lost my credit card and need to block it immediately"}', language="json")
