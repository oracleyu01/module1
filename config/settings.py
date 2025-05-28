"""
설정 및 환경변수 관리
"""
import os
import streamlit as st
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# API 키 설정
def get_api_keys():
    return {
        "SUPABASE_URL": os.getenv("SUPABASE_URL") or st.secrets.get("SUPABASE_URL", ""),
        "SUPABASE_KEY": os.getenv("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY", ""),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", ""),
        "NAVER_CLIENT_ID": os.getenv("NAVER_CLIENT_ID") or st.secrets.get("NAVER_CLIENT_ID", ""),
        "NAVER_CLIENT_SECRET": os.getenv("NAVER_CLIENT_SECRET") or st.secrets.get("NAVER_CLIENT_SECRET", ""),
        "COUPANG_PARTNER_ID": os.getenv("COUPANG_PARTNER_ID") or st.secrets.get("COUPANG_PARTNER_ID", ""),
        "COUPANG_ACCESS_KEY": os.getenv("COUPANG_ACCESS_KEY") or st.secrets.get("COUPANG_ACCESS_KEY", ""),
        "LANGSMITH_API_KEY": os.getenv("LANGSMITH_API_KEY") or st.secrets.get("LANGSMITH_API_KEY", "")
    }

def configure_page():
    """Streamlit 페이지 설정"""
    st.set_page_config(
        page_title="스마트한 쇼핑 (LangGraph)",
        page_icon="🛒",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def initialize_session_state():
    """세션 상태 초기화"""
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    if 'bookmarks' not in st.session_state:
        st.session_state.bookmarks = []
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
    if 'total_searches' not in st.session_state:
        st.session_state.total_searches = 0
    if 'saved_products' not in st.session_state:
        st.session_state.saved_products = 0

def setup_langsmith():
    """LangSmith 설정"""
    keys = get_api_keys()
    if keys["LANGSMITH_API_KEY"]:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_PROJECT"] = "smart-shopping-app"
        os.environ["LANGCHAIN_API_KEY"] = keys["LANGSMITH_API_KEY"]
    else:
        os.environ["LANGCHAIN_TRACING_V2"] = "false"
