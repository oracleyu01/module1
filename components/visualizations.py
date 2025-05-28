"""
시각화 컴포넌트
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from collections import Counter
import re
import io
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from utils.helpers import extract_keywords, generate_coupang_search_link, get_sample_coupang_product

def create_pros_cons_chart(pros_count, cons_count):
    """장단점 차트 생성"""
    fig = go.Figure(data=[
        go.Bar(
            name='장점',
            x=['분석 결과'],
            y=[pros_count],
            marker_color='#28a745',
            text=f'{pros_count}개',
            textposition='auto',
            hovertemplate='장점: %{y}개<extra></extra>'
        ),
        go.Bar(
            name='단점',
            x=['분석 결과'],
            y=[cons_count],
            marker_color='#dc3545',
            text=f'{cons_count}개',
            textposition='auto',
            hovertemplate='단점: %{y}개<extra></extra>'
        )
    ])
    
    fig.update_layout(
        barmode='group',
        height=300,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14),
        showlegend=True,
        legend=dict(x=0.3, y=1.1, orientation='h'),
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
        bargap=0.3
    )
    
    return fig

def create_wordcloud(texts, title, color_scheme):
    """워드클라우드 생성"""
    if not texts:
        return None
    
    # 키워드 추출
    word_freq = extract_keywords(texts)
    
    if not word_freq:
        return None
    
    # 빈도수 기준으로 상위 키워드만 선택 (최대 40개)
    top_keywords = dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:40])
    
    # 프로젝트 루트의 폰트 파일 우선 사용
    font_path = "./NanumGothic.ttf"
    
    # 폰트 파일이 없는 경우 다른 경로 시도
    if not os.path.exists(font_path):
        font_paths = [
            "NanumGothic.ttf",
            "./fonts/NanumGothic.ttf",
            "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
            "C:/Windows/Fonts/malgun.ttf",
            "/System/Library/Fonts/AppleSDGothicNeo.ttc"
        ]
        
        for path in font_paths:
            if os.path.exists(path):
                font_path = path
                break
    
    # 워드클라우드 생성
    plt.figure(figsize=(10, 6), facecolor='white')
    
    if font_path and os.path.exists(font_path) and top_keywords:
        try:
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color='white',
                colormap=color_scheme,
                font_path=font_path,
                relative_scaling=0.7,
                min_font_size=14,
                max_words=30,
                prefer_horizontal=0.8,
                margin=15,
                collocations=False
            ).generate_from_frequencies(top_keywords)
            
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.tight_layout(pad=0)
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
            buf.seek(0)
            plt.close()
            
            return buf
            
        except Exception as e:
            plt.close()
            st.error(f"워드클라우드 생성 오류: {str(e)}")
            return None
    else:
        st.warning(f"한글 폰트를 찾을 수 없습니다. NanumGothic.ttf 파일을 프로젝트 루트에 추가해주세요.")
        return None

def create_text_cloud(texts, title, color):
    """워드클라우드 대신 텍스트 기반 시각화"""
    if not texts:
        return
    
    # 키워드 추출
    word_freq = extract_keywords(texts)
    
    if not word_freq:
        return
    
    # 상위 20개 키워드
    top_words = word_freq.most_common(20)
    
    # 최대 빈도수
    max_freq = top_words[0][1] if top_words else 1
    
    # HTML로 워드클라우드 스타일 표현
    html_words = []
    for word, freq in top_words:
        size = 1 + (freq / max_freq) * 2
        opacity = 0.5 + (freq / max_freq) * 0.5
        
        html_words.append(
            f'<span style="font-size: {size}rem; color: {color}; opacity: {opacity}; '
            f'margin: 0.3rem; display: inline-block; font-weight: bold;">{word}</span>'
        )
    
    import random
    random.shuffle(html_words)
    
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem; background: white; 
                border-radius: 15px; border: 2px solid {color}20;">
        <h4 style="color: {color}; margin-bottom: 1rem;">{title}</h4>
        <div style="line-height: 2.5;">
            {''.join(html_words)}
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_wordclouds(pros, cons):
    """장단점 워드클라우드 표시"""
    col1, col2 = st.columns(2)
    
    with col1:
        if pros:
            st.markdown("""
            <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #d4f1d4 0%, #b8e6b8 100%); border-radius: 15px;">
                <h3 style="color: #28a745; margin: 0;">
                    <i class="fas fa-check-circle"></i> 장점 키워드
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            pros_wordcloud = create_wordcloud(pros, "", "Greens")
            if pros_wordcloud:
                st.image(pros_wordcloud, use_container_width=True)
            else:
                create_text_cloud(pros, "장점 키워드 분석", "#28a745")
            
            keywords = extract_keywords(pros)
            if keywords and isinstance(keywords, dict):
                sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:5]
                if sorted_keywords:
                    st.markdown("**🔑 주요 키워드:**")
                    keyword_html = " ".join([f'<span style="background: #d4f1d4; padding: 0.2rem 0.5rem; border-radius: 15px; margin: 0.2rem; display: inline-block;">{word} ({count})</span>' 
                                            for word, count in sorted_keywords])
                    st.markdown(keyword_html, unsafe_allow_html=True)
    
    with col2:
        if cons:
            st.markdown("""
            <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #ffd6d6 0%, #ffb8b8 100%); border-radius: 15px;">
                <h3 style="color: #dc3545; margin: 0;">
                    <i class="fas fa-times-circle"></i> 단점 키워드
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            cons_wordcloud = create_wordcloud(cons, "", "Reds")
            if cons_wordcloud:
                st.image(cons_wordcloud, use_container_width=True)
            else:
                create_text_cloud(cons, "단점 키워드 분석", "#dc3545")
            
            keywords = extract_keywords(cons)
            if keywords and isinstance(keywords, dict):
                sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:5]
                if sorted_keywords:
                    st.markdown("**🔑 주요 키워드:**")
                    keyword_html = " ".join([f'<span style="background: #ffd6d6; padding: 0.2rem 0.5rem; border-radius: 15px; margin: 0.2rem; display: inline-block;">{word} ({count})</span>' 
                                            for word, count in sorted_keywords])
                    st.markdown(keyword_html, unsafe_allow_html=True)

def create_comparison_chart(pros, cons):
    """장단점 비교 시각화 (레이더 차트)"""
    # 카테고리별 분류
    categories = {
        '성능': ['성능', '속도', '빠르', '느리', '렉', '버벅', '프로세서', 'CPU', 'GPU', '메모리'],
        '디자인': ['디자인', '외관', '예쁘', '이쁘', '못생', '색상', '모양', '두께', '얇'],
        '가격': ['가격', '비싸', '저렴', '가성비', '비용', '돈', '할인', '세일'],
        '품질': ['품질', '마감', '재질', '튼튼', '약하', '고장', '내구성', '견고'],
        '기능': ['기능', '편의', '편리', '불편', '사용', '조작', '인터페이스'],
        '배터리': ['배터리', '충전', '전원', '지속', '방전'],
        '화면': ['화면', '디스플레이', '선명', '밝기', '해상도'],
        '기타': []
    }
    
    # 각 카테고리별 장단점 수 계산
    category_pros = {cat: 0 for cat in categories}
    category_cons = {cat: 0 for cat in categories}
    
    # 장점 분류
    for pro in pros:
        categorized = False
        for cat, keywords in categories.items():
            if cat != '기타' and any(keyword in pro for keyword in keywords):
                category_pros[cat] += 1
                categorized = True
                break
        if not categorized:
            category_pros['기타'] += 1
    
    # 단점 분류
    for con in cons:
        categorized = False
        for cat, keywords in categories.items():
            if cat != '기타' and any(keyword in con for keyword in keywords):
                category_cons[cat] += 1
                categorized = True
                break
        if not categorized:
            category_cons['기타'] += 1
    
    # 데이터가 있는 카테고리만 필터링
    active_categories = [cat for cat in categories if category_pros[cat] > 0 or category_cons[cat] > 0]
    
    if not active_categories:
        return None
    
    # 레이더 차트 생성
    fig = go.Figure()
    
    # 장점 데이터
    fig.add_trace(go.Scatterpolar(
        r=[category_pros[cat] for cat in active_categories],
        theta=active_categories,
        fill='toself',
        fillcolor='rgba(40, 167, 69, 0.3)',
        line=dict(color='#28a745', width=2),
        name='장점',
        hovertemplate='%{theta}<br>장점: %{r}개<extra></extra>'
    ))
    
    # 단점 데이터
    fig.add_trace(go.Scatterpolar(
        r=[category_cons[cat] for cat in active_categories],
        theta=active_categories,
        fill='toself',
        fillcolor='rgba(220, 53, 69, 0.3)',
        line=dict(color='#dc3545', width=2),
        name='단점',
        hovertemplate='%{theta}<br>단점: %{r}개<extra></extra>'
    ))
    
    # 최대값 계산
    max_value = max(
        max(category_pros.values()) if category_pros else 1,
        max(category_cons.values()) if category_cons else 1
    )
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max_value + 1]
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=True,
        title={
            'text': '🎯 카테고리별 장단점 분포',
            'font': {'size': 24, 'color': '#333333'},
            'x': 0.5,
            'xanchor': 'center'
        },
        height=600,
        width=600,
        margin=dict(l=50, r=50, t=120, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(x=0.82, y=0.98, font=dict(size=16))
    )
    
    return fig, category_pros, category_cons, categories

def display_results(final_state, show_process):
    """검색 결과 표시"""
    from components.ui import get_theme_colors
    colors = get_theme_colors()
    
    # 프로세스 로그 표시
    if show_process and final_state["messages"]:
        with st.expander("🔧 검색 프로세스", expanded=False):
            for msg in final_state["messages"]:
                if hasattr(msg, 'content'):
                    if isinstance(msg, type(final_state["messages"][0])):  # HumanMessage
                        st.write(f"👤 {msg.content}")
                    else:  # AIMessage
                        st.write(f"🤖 {msg.content}")
    
    # 결과 표시
    if final_state["pros"] or final_state["cons"]:
        # 검색 정보
        st.markdown(f"""
        <div class="process-info fade-in">
            <strong><i class="fas fa-info-circle"></i> 검색 방법:</strong> {
                '데이터베이스' if final_state["search_method"] == "database" else '웹 크롤링'
            } | 
            <strong><i class="fas fa-thumbs-up"></i> 장점:</strong> {len(final_state["pros"])}개 | 
            <strong><i class="fas fa-thumbs-down"></i> 단점:</strong> {len(final_state["cons"])}개
        </div>
        """, unsafe_allow_html=True)
        
        # 장단점 상세 표시
        st.markdown("---")
        st.markdown("### 📋 상세 분석 결과")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="pros-section fade-in">
                <h3 style="color: #28a745; margin-bottom: 1.5rem;">
                    <i class="fas fa-check-circle"></i> 장점
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            if final_state["pros"]:
                for idx, pro in enumerate(final_state["pros"], 1):
                    st.markdown(f"""
                    <div class="pros-item">
                        <span style="color: #28a745; font-weight: bold;">
                            <i class="fas fa-check"></i> {idx}.
                        </span> {pro}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("장점 정보가 없습니다.")
        
        with col2:
            st.markdown("""
            <div class="cons-section fade-in">
                <h3 style="color: #dc3545; margin-bottom: 1.5rem;">
                    <i class="fas fa-times-circle"></i> 단점
                </h3>
            </div>
