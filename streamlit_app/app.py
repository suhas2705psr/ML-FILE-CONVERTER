import streamlit as st
import requests
import pandas as pd
from pathlib import Path

API = "http://127.0.0.1:8000/api"

st.set_page_config(
    page_title="ML File Converter",
    page_icon="🔄",
    layout="wide"
)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.title("🔄 ML File Converter")
st.sidebar.markdown("**P. Sri Ranga Suhas**")
st.sidebar.markdown("github.com/suhas2705psr")
st.sidebar.divider()
page = st.sidebar.radio("Navigate", ["🔄 Convert", "🧠 Classify", "📊 History & Stats"])

# ─── Page 1: Convert ──────────────────────────────────────────────────────────
if page == "🔄 Convert":
    st.title("🔄 File Converter")
    st.markdown("Upload any file and convert it to your desired format.")

    col1, col2 = st.columns(2)

    with col1:
        uploaded = st.file_uploader(
            "Upload your file",
            type=["pdf","docx","xlsx","csv","json","xml","html","pptx","txt","png","jpg","jpeg"]
        )

    with col2:
        format_options = {
            "PDF":   "pdf",
            "DOCX":  "docx",
            "Excel": "xlsx",
            "CSV":   "csv",
            "JSON":  "json",
            "HTML":  "html",
            "TXT":   "txt",
        }
        out_label = st.selectbox("Convert to", list(format_options.keys()))
        output_format = format_options[out_label]

    if uploaded and st.button("🚀 Convert Now", type="primary"):
        with st.spinner("Converting..."):
            try:
                response = requests.post(
                    f"{API}/convert",
                    files={"file": (uploaded.name, uploaded.getvalue(), uploaded.type)},
                    data={"output_format": output_format},
                )
                if response.status_code == 200 and "error" not in response.headers.get("content-type",""):
                    st.success("✅ Conversion successful!")
                    st.download_button(
                        label="📥 Download Converted File",
                        data=response.content,
                        file_name=f"converted.{output_format}",
                        mime="application/octet-stream",
                    )
                else:
                    st.error(f"Conversion failed: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")

# ─── Page 2: Classify ─────────────────────────────────────────────────────────
elif page == "🧠 Classify":
    st.title("🧠 Document Classifier")
    st.markdown("Upload a file and the ML model will detect what type of document it is.")

    uploaded = st.file_uploader(
        "Upload your file",
        type=["pdf","docx","xlsx","csv","json","xml","html","pptx","txt","png","jpg","jpeg"]
    )

    if uploaded and st.button("🔍 Classify Document", type="primary"):
        with st.spinner("Classifying..."):
            try:
                response = requests.post(
                    f"{API}/classify",
                    files={"file": (uploaded.name, uploaded.getvalue(), uploaded.type)},
                )
                result = response.json()

                col1, col2, col3 = st.columns(3)
                col1.metric("Document Type", result["document_type"].upper())
                col2.metric("Confidence", f"{result['confidence']:.1%}")
                col3.metric("File", uploaded.name)

                st.divider()
                st.subheader("📊 Top 3 Predictions")
                for item in result.get("top3", []):
                    st.progress(
                        item["confidence"],
                        text=f"{item['type'].capitalize()} — {item['confidence']:.1%}"
                    )

                st.divider()
                st.subheader("💡 Recommended Output Formats")
                cols = st.columns(len(result.get("recommendations", [])))
                for i, fmt in enumerate(result.get("recommendations", [])):
                    cols[i].success(f"**{fmt.upper()}**")

            except Exception as e:
                st.error(f"Error: {e}")

# ─── Page 3: History & Stats ──────────────────────────────────────────────────
elif page == "📊 History & Stats":
    st.title("📊 Conversion History & Stats")

    # Stats
    try:
        stats = requests.get(f"{API}/stats").json()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Conversions", stats["total_conversions"])
        col2.metric("Successful",        stats["successful"])
        col3.metric("Success Rate",      f"{stats['success_rate']}%")
        col4.metric("Avg Duration",      f"{stats['avg_duration_ms']}ms")
    except:
        st.warning("Could not load stats.")

    st.divider()

    # History table
    st.subheader("Recent Conversions")
    try:
        limit = st.slider("Show last N conversions", 5, 100, 20)
        data = requests.get(f"{API}/history?limit={limit}").json()
        if data["logs"]:
            df = pd.DataFrame(data["logs"])
            st.dataframe(df, use_container_width=True)

            # Chart
            st.subheader("📈 Conversions by Format")
            format_counts = df["input_format"].value_counts()
            st.bar_chart(format_counts)
        else:
            st.info("No conversions yet — upload a file to get started!")
    except Exception as e:
        st.error(f"Could not load history: {e}")