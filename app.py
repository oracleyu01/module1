"""
스마트한 쇼핑 앱 - LangGraph 버전
"""
import streamlit as st
from config.settings import configure_page, initialize_session_state
from components.ui import render_header, render_sidebar, render_search_section
from components.visualizations import display_results
from core.workflow import create_search_workflow
from utils.helpers import ensure_font

# 페이지 설정
configure_page()

# 폰트 확인
ensure_font()

# 세션 상태 초기화
initialize_session_state()

# CSS 적용
from components.ui import apply_custom_css
apply_custom_css()

# 사이드바
render_sidebar()

# 헤더
render_header()

# 검색 섹션
search_term, search_button, show_process = render_search_section()

# 검색 실행
if search_button and search_term:
    from utils.helpers import show_loading_animation
    
    loading_placeholder = show_loading_animation()
    
    # LangGraph 워크플로우 실행
    search_app = create_search_workflow()
    initial_state = {
        "product_name": search_term,
        "search_method": "",
        "results": {},
        "pros": [],
        "cons": [],
        "sources": [],
        "messages": [],
        "error": ""
    }
    
    final_state = search_app.invoke(initial_state)
    loading_placeholder.empty()
    
    # 결과 표시
    display_results(final_state, show_process)

# 하단 정보
from components.ui import render_footer
render_footer()
