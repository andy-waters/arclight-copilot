import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


import streamlit as st

from dotenv import load_dotenv
load_dotenv()

from arclight.config import SETTINGS
from arclight.models.llm import azure_llm
from arclight.agents.planner import draft_plan
from arclight.agents.researcher import execute_step
from arclight.agents.reviewer import review_and_finalize
from arclight.chains.rag_chain import retrieve_docs
from arclight.tools.py_sandbox import run_snippet
from arclight.memory.conversation_store import append_trace, export_trace



st.set_page_config(page_title="ArcLight Copilot", page_icon="💡", layout="wide")

st.title("💡 ArcLight Copilot")
st.caption("Illuminating research with agentic AI — LangChain + Azure OpenAI")

with st.sidebar:
    st.subheader("Settings")
    st.write("**Mode**: " + ("🔦 Demo Mode (no keys detected)" if SETTINGS.demo_mode else "⚡ Live AOAI"))
    st.write("**Azure OpenAI**: " + ("not configured" if SETTINGS.demo_mode else "configured"))
    rag_on = bool(SETTINGS.search_endpoint and SETTINGS.search_key and SETTINGS.search_index)
    st.write("**Azure AI Search (RAG)**: " + ("configured" if rag_on else "not configured"))
    st.divider()
    if st.button("Export Trace JSON"):
        trace = export_trace()
        st.download_button("Download trace.json", data=trace, file_name="arclight_trace.json")

prompt = st.text_area("What do you want to research or accomplish?", placeholder="e.g., Compare LangChain vs Semantic Kernel for agent workflows, with citations.", height=120)
run = st.button("Run ArcLight")

col1, col2 = st.columns([2, 1])

if run and prompt.strip():
    llm = azure_llm()
    st.session_state["log"] = []
    plan = draft_plan(llm, prompt)
    with col1:
        st.subheader("Agent Log")
        st.write("**Plan**")
        st.json(plan)
        for step in plan:
            execute_step(llm, step, prompt, st.session_state["log"])
        st.write("**Steps Executed**")
        st.json(st.session_state["log"])
        review = review_and_finalize(llm, prompt, st.session_state["log"])
        st.write("**Final Answer**")
        st.markdown(review["final"])

        append_trace({
            "prompt": prompt,
            "plan": plan,
            "log": st.session_state["log"],
            "final": review["final"]
        })

    with col2:
        st.subheader("RAG (Sample Docs)")
        docs = retrieve_docs(prompt)
        for d in docs:
            with st.container(border=True):
                st.caption(d.source)
                st.write(d.content)

        st.subheader("Python Sandbox")
        code = st.text_area("Optional: run a quick calculation (restricted env)", value="x = sum(range(10))")
        if st.button("Run Code"):
            out = run_snippet(code)
            st.json(out)

else:
    with col1:
        st.info("Enter a goal or question, then click **Run ArcLight**.")
    with col2:
        st.subheader("Status")
        st.write("- LangChain orchestrates the agent flow.")
        st.write("- Azure OpenAI powers the LLM (when configured).")
        st.write("- Azure AI Search enables RAG (optional).")

st.divider()
st.markdown("**Tip:** ArcLight runs in Demo Mode without keys. Configure `.env` to enable live LLM + RAG.")
