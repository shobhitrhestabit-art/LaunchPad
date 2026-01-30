import streamlit as st
import requests



API_URL = "http://127.0.0.1:8000/generate"

st.set_page_config(
    page_title="Local GGUF LLM",
    layout="centered"
)



st.title("Local GGUF LLM")
st.caption("Minimal interface for local llama.cpp inference")



prompt = st.text_area(
    "Prompt",
    placeholder="Enter your prompt here...",
    height=140
)

temperature = st.slider(
    "Temperature",
    min_value=0.1,
    max_value=2.0,
    value=0.6,
    step=0.1
)

top_p = st.slider(
    "Top-p (Nucleus Sampling)",
    min_value=0.0,
    max_value=1.0,
    value=0.85,
    step=0.05
)


if st.button("Generate"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        payload = {
            "prompt": prompt,
            "temperature": temperature,
            "top_p": top_p
        }

        with st.spinner("Generating response..."):
            try:
                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=120
                )

                if response.status_code == 200:
                    data = response.json()

                    st.subheader("Response")
                    st.write(data["text"])

                    with st.expander("Generation Details"):
                        st.json({
                            "tokens_used": data.get("tokens_used"),
                            "model_info": data.get("model_info")
                        })

                else:
                    st.error(f"API Error ({response.status_code})")
                    st.text(response.text)

            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to backend: {e}")
