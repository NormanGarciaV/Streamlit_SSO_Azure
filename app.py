# app.py
import ssl
import streamlit as st
import os
import httpx

# DEV ONLY: skip TLS verification when explicitly enabled
# The secret in the .toml file is the value (not the ID)
# Create the ENV Var DEV_INSECURE_SSL = "1" before running the app.
if os.getenv("DEV_INSECURE_SSL") == "1":
    _client_init = httpx.Client.__init__
    _async_init = httpx.AsyncClient.__init__

    def _client_noverify(self, *args, **kwargs):
        kwargs["verify"] = False
        _client_init(self, *args, **kwargs)

    def _async_noverify(self, *args, **kwargs):
        kwargs["verify"] = False
        _async_init(self, *args, **kwargs)

    httpx.Client.__init__ = _client_noverify
    httpx.AsyncClient.__init__ = _async_noverify


st.set_page_config(page_title="My Secure App")

col1 = st.columns(1)[0]
with col1:
    st.header("RecOps Requisition Extractor", text_alignment="center")
    with st.container(border=True, horizontal=True):

        if not st.user.is_logged_in:
            st.subheader("Please sign in")
            if st.button("Sign in with Microsoft", icon="", type="primary"):
                st.login()
            st.stop()  # nothing below runs for anonymous users

# --- Everything below is only visible to authenticated users ---
with st.sidebar:
    st.write(f"Signed in as **{st.user.name}**")
    st.button("Sign out", on_click=st.logout)

st.title("Welcome!")
st.write(f"{st.user.name}")
st.write("Email:", st.user.get("email")) #or st.user.get("preferred_username"))

# Inspect all claims Entra returned (handy while developing)
with st.expander("Token claims"):
    st.json(st.user.to_dict())