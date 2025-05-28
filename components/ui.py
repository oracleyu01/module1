"""
UI 컴포넌트
"""
import streamlit as st
from datetime import datetime

def get_theme_colors():
    """테마 색상 가져오기"""
    if st.session_state.dark_mode:
        return {
            'bg_gradient': "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)",
            'card_bg': "#0f3460",
            'text_color': "#ffffff",
            'secondary_text': "#e94560",
            'header_gradient': "linear-gradient(135deg, #e94560 0%, #0f3460 100%)"
        }
    else:
        return {
            'bg_gradient': "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
            'card_bg': "white",
            'text_color': "#333333",
            'secondary_text': "#667eea",
            'header_gradient': "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        }

def apply_custom_css():
    """커스텀 CSS 적용"""
    colors = get_theme_colors()
    
    st.markdown(f"""
    <style>
        /* 전체 배경 및 기본 스타일 */
        .stApp {{
            background: {colors['bg_gradient']};
        }}
        
        /* 메인 헤더 개선 */
        .main-header {{
            text-align: center;
            padding: 3rem 0;
            background: {colors['header_gradient']};
            color: white;
            border-radius: 20px;
            margin-bottom: 3rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            position: relative;
            overflow: hidden;
        }}
        
        .main-header h1 {{
            text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3), 
                         0 0 20px rgba(255, 255, 255, 0.2);
        }}
        
        .main-header p {{
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }}
        
        .main-header::before {{
            content: "";
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: shimmer 3s infinite;
        }}
        
        @keyframes shimmer {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        /* 카드 스타일 */
        .search-card {{
            background: {colors['card_bg']};
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
            margin-bottom: 2rem;
            color: {colors['text_color']};
        }}
        
        /* 장점 섹션 개선 */
        .pros-section {{
            background: linear-gradient(135deg, #d4f1d4 0%, #b8e6b8 100%);
            padding: 2rem;
            border-radius: 15px;
            margin: 1rem 0;
            border: none;
            box-shadow: 0 5px 15px rgba(40, 167, 69, 0.1);
            transition: transform 0.3s ease;
        }}
        
        .pros-section:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(40, 167, 69, 0.15);
        }}
        
        /* 단점 섹션 개선 */
        .cons-section {{
            background: linear-gradient(135deg, #ffd6d6 0%, #ffb8b8 100%);
            padding: 2rem;
            border-radius: 15px;
            margin: 1rem 0;
            border: none;
            box-shadow: 0 5px 15px rgba(220, 53, 69, 0.1);
            transition: transform 0.3s ease;
        }}
        
        .cons-section:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(220, 53, 69, 0.15);
        }}
        
        /* 프로세스 정보 개선 */
        .process-info {{
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1.5rem 0;
            border: none;
            box-shadow: 0 3px 10px rgba(33, 150, 243, 0.1);
        }}
        
        /* 버튼 스타일 개선 */
        .stButton > button {{
            background: {colors['header_gradient']};
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            border-radius: 30px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }}
        
        /* 입력 필드 스타일 */
        .stTextInput > div > div > input {{
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            padding: 0.75rem 1rem;
            transition: all 0.3s ease;
            background: {colors['card_bg']};
            color: {colors['text_color']};
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: {colors['secondary_text']};
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}
        
        /* 메트릭 카드 */
        .metric-card {{
            background: {colors['card_bg']};
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
            text-align: center;
            transition: all 0.3s ease;
            color: {colors['text_color']};
        }}
        
        .metric-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.12);
        }}
        
        /* 애니메이션 효과 */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .fade-in {{
            animation: fadeIn 0.6s ease-out;
        }}
        
        /* 로딩 스피너 */
        .spinner {{
            width: 50px;
            height: 50px;
            margin: 0 auto;
            border: 5px solid #f3f3f3;
            border-top: 5px solid {colors['secondary_text']};
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        /* 프로스/콘스 아이템 */
        .pros-item, .cons-item {{
            background: white;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 8px;
            transition: all 0.3s ease;
            animation: fadeIn 0.5s ease-out;
        }}
        
        .pros-item {{
            border-left: 4px solid #28a745;
        }}
        
        .cons-item {{
            border-left: 4px solid #dc3545;
        }}
        
        .pros-item:hover, .cons-item:hover {{
            transform: translateX(5px);
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
        }}
        
        /* 검색 섹션 스타일 */
        .search-section {{
            margin-top: -3rem;
            padding: 1rem 0 2rem 0;
        }}
        
        .search-title {{
            text-align: center;
            color: #333;
            margin-bottom: 1.5rem;
            margin-top: -1rem;
            font-size: 2.5rem;
            font-weight: 700;
            letter-spacing: -0.5px;
        }}
        
        .big-search .stTextInput > div > div > input {{
            height: 100px !important;
            font-size: 2.2rem !important;
            font-weight: 700 !important;
            padding: 2rem 3.5rem !important;
            border-radius: 50px !important;
            border: 4px solid #e0e0e0 !important;
            transition: all 0.3s ease !important;
            text-align: center !important;
            letter-spacing: 1px !important;
            line-height: 1.2 !important;
        }}
        
        .big-search .stTextInput > div > div > input:focus {{
            border-color: {colors['secondary_text']} !important;
            box-shadow: 0 0 0 8px rgba(102, 126, 234, 0.15) !important;
            transform: translateY(-2px) !important;
            border-width: 4px !important;
        }}
        
        /* 플레이스홀더 스타일 */
        .big-search .stTextInput > div > div > input::placeholder {{
            color: #aaa !important;
            font-size: 1.5rem !important;
            text-align: center !important;
            font-weight: 400 !important;
            opacity: 0.7 !important;
        }}
        
        /* 버튼 크기 조정 */
        .search-buttons .stButton > button {{
            height: 60px !important;
            font-size: 1.4rem !important;
            padding: 0 3.5rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.5px !important;
        }}
        
        /* 인기 검색어 버튼 스타일 */
        .popular-search-buttons .stButton > button {{
            height: 45px !important;
            font-size: 1.1rem !important;
            font-weight: 500 !important;
        }}
        
        /* 모바일 반응형 */
        @media (max-width: 768px) {{
            .main-header {{
                padding: 2rem 1rem;
                font-size: 0.9rem;
            }}
            .main-header h1 {{
                font-size: 1.8rem;
            }}
            .search-card {{
                padding: 1.5rem 1rem;
            }}
            .pros-section, .cons-section {{
                padding: 1.5rem 1rem;
            }}
        }}
        
        /* 프로그레스 바 */
        .progress-bar {{
            width: 100%;
            height: 8px;
            background-color: #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
            margin: 1rem 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: {colors['header_gradient']};
            animation: progress 2s ease-out;
        }}
        
        @keyframes progress {{
            from {{ width: 0%; }}
            to {{ width: 100%; }}
        }}
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """사이드바 렌더링"""
    with st.sidebar:
        st.markdown("### ⚙️ 설정")
        dark_mode = st.checkbox("🌙 다크모드", value=st.session_state.dark_mode)
        st.session_state.dark_mode = dark_mode
        
        st.markdown("### 📌 북마크")
        if st.session_state.bookmarks:
            for bookmark in st.session_state.bookmarks:
                if st.button(f"🔖 {bookmark}", key=f"bookmark_{bookmark}"):
                    st.session_state.selected_bookmark = bookmark
        else:
            st.info("북마크가 없습니다")
        
        st.markdown("### 📊 사용 통계")
        st.metric("총 검색 수", f"{st.session_state.total_searches}회")
        st.metric("저장된 제품", f"{st.session_state.saved_products}개")

def render_header():
    """헤더 렌더링"""
    st.markdown("""
    <div class="main-header">
        <h1 style="margin-bottom: 0.5rem;">🛒 스마트한 쇼핑 (LangGraph Edition)</h1>
        <p style="font-size: 1.2rem; margin-top: 0.5rem;">
            LangGraph로 구현한 지능형 제품 리뷰 분석 시스템
        </p>
        <p style="font-size: 0.9rem; margin-top: 0.3rem; opacity: 0.8;">
            <i class="fas fa-robot"></i> AI가 수천 개의 리뷰를 분석하여 핵심 장단점을 요약해드립니다
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_search_section():
    """검색 섹션 렌더링"""
    col1, col2, col3 = st.columns([1, 5, 1])
    
    with col2:
        st.markdown('<div class="search-section">', unsafe_allow_html=True)
        
        st.markdown("""
        <h2 class="search-title">
            어떤 제품을 찾고 계신가요?
        </h2>
        """, unsafe_allow_html=True)
        
        # 북마크에서 선택된 항목이 있으면 자동 입력
        default_value = ""
        if 'selected_bookmark' in st.session_state:
            default_value = st.session_state.selected_bookmark
            del st.session_state.selected_bookmark
        elif 'search_query' in st.session_state:
            default_value = st.session_state.search_query
        
        # 검색창
        st.markdown('<div class="big-search">', unsafe_allow_html=True)
        product_name = st.text_input(
            "제품명 입력",
            placeholder="예: 맥북 프로 M3, LG 그램 2024, 갤럭시북4 프로",
            value=default_value,
            label_visibility="collapsed",
            key="product_search_input"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 버튼들
        st.markdown('<div class="search-buttons" style="margin-top: 1.8rem;">', unsafe_allow_html=True)
        col_btn1, col_btn2, col_btn3 = st.columns([3, 2.5, 0.5])
        with col_btn1:
            search_button = st.button("🔍 검색하기", use_container_width=True, type="primary")
        with col_btn2:
            show_process = st.checkbox("🔧 프로세스 보기", value=True)
        with col_btn3:
            if product_name and st.button("📌", help="북마크에 추가", key="bookmark_btn"):
                if product_name not in st.session_state.bookmarks:
                    st.session_state.bookmarks.append(product_name)
                    st.success("북마크에 추가되었습니다!")
                    st.session_state.total_searches += 1
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 인기 검색어
        st.markdown("""
        <div class="popular-search-buttons" style="text-align: center; margin-top: 2rem;">
            <p style="opacity: 0.7; font-size: 1.2rem; margin-bottom: 1rem; color: #666; font-weight: 500;">인기 검색어</p>
        """, unsafe_allow_html=True)
        
        popular_searches = ["맥북 프로 M3", "LG 그램 2024", "갤럭시북4 프로", "델 XPS 15"]
        cols = st.columns(len(popular_searches))
        for idx, (col, search) in enumerate(zip(cols, popular_searches)):
            with col:
                if st.button(
                    search, 
                    key=f"popular_{idx}", 
                    use_container_width=True,
                    help=f"{search} 검색하기"
                ):
                    st.session_state.search_query = search
                    st.rerun()
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    # 검색어 결정
    if 'search_query' in st.session_state and st.session_state.search_query:
        search_term = st.session_state.search_query
        st.session_state.search_query = ""
    else:
        search_term = product_name
    
    return search_term, search_button, show_process

def render_footer():
    """하단 정보 렌더링"""
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <i class="fas fa-brain" style="color: #667eea;"></i>
            <p>LangGraph로 구현된<br>체계적인 검색 프로세스</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <i class="fas fa-sync-alt" style="color: #28a745;"></i>
            <p>DB 우선 검색<br>→ 없으면 웹 크롤링</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <i class="fas fa-save" style="color: #dc3545;"></i>
            <p>검색 결과<br>자동 저장</p>
        </div>
        """, unsafe_allow_html=True)
    
    current_date = datetime.now().strftime('%Y년 %m월 %d일')
    st.markdown(f"""
    <div style="text-align: center; color: #666; padding: 2rem; margin-top: 2rem;">
        <p style="margin-bottom: 0.5rem;">
            <i class="fas fa-clock"></i> 마지막 업데이트: {current_date}
        </p>
        <p style="font-size: 0.9rem; opacity: 0.8;">
            Powered by LangGraph & OpenAI | Made with <i class="fas fa-heart" style="color: #e74c3c;"></i> by Smart Shopping Team
        </p>
    </div>
    """, unsafe_allow_html=True)
