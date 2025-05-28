"""
유틸리티 함수들
"""
import streamlit as st
import os
import urllib.request
import urllib.parse
import re
from collections import Counter

@st.cache_resource
def ensure_font():
    """폰트 파일 확인 및 다운로드"""
    font_path = "./NanumGothic.ttf"
    
    if not os.path.exists(font_path):
        with st.spinner("한글 폰트 다운로드 중..."):
            try:
                # 나눔고딕 폰트 다운로드 (공식 GitHub 저장소)
                url = "https://github.com/naver/nanumfont/raw/master/fonts/NanumFontSetup_TTF_GOTHIC/NanumGothic.ttf"
                urllib.request.urlretrieve(url, font_path)
                st.success("✅ 한글 폰트 다운로드 완료!")
            except Exception as e:
                st.error(f"❌ 폰트 다운로드 실패: {e}")
                
                # 대체 URL 시도
                try:
                    alt_url = "https://cdn.jsdelivr.net/gh/naver/nanumfont@master/fonts/NanumFontSetup_TTF_GOTHIC/NanumGothic.ttf"
                    urllib.request.urlretrieve(alt_url, font_path)
                    st.success("✅ 한글 폰트 다운로드 완료! (대체 경로)")
                except:
                    st.warning("⚠️ 폰트 다운로드 실패. 키워드가 영문으로 표시될 수 있습니다.")
                    return None
    
    return font_path

def show_loading_animation():
    """로딩 애니메이션 표시"""
    loading_placeholder = st.empty()
    loading_placeholder.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <div class="spinner"></div>
        <p style="margin-top: 1rem; color: #667eea; font-weight: 600;">
            <i class="fas fa-brain"></i> AI가 제품 정보를 분석하고 있습니다...
        </p>
        <div class="progress-bar">
            <div class="progress-fill"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    return loading_placeholder

def extract_keywords(texts):
    """텍스트에서 핵심 키워드 추출"""
    # 확장된 불용어 정의
    stopwords = {
        # 일반 불용어
        '수', '있습니다', '있어요', '있음', '좋습니다', '좋아요', '좋음', 
        '나쁩니다', '나빠요', '나쁨', '않습니다', '않아요', '않음',
        '입니다', '이다', '되다', '하다', '있다', '없다', '같다',
        '위해', '통해', '대해', '매우', '정말', '너무', '조금',
        '그리고', '하지만', '그러나', '또한', '때문', '경우',
        '제공합니다', '제공', '합니다', '해요', '드립니다', '드려요',
        '위한', '위하여', '따라', '따른', '통한', '대한', '관한',
        '됩니다', '됨', '되어', '되었습니다', '했습니다', '하는',
        '이', '그', '저', '것', '것이', '것을', '것은', '것도',
        '더', '덜', '꽤', '약간', '살짝', '많이', '적게', '조금',
        '모든', '각', '각각', '여러', '몇', '몇몇', '전체', '일부',
        '항상', '가끔', '종종', '자주', '언제나', '절대', '전혀',
        '만', '도', '까지', '부터', '에서', '에게', '으로', '로',
        '와', '과', '하고', '이고', '이며', '거나', '든지', '라고',
        '들', '등', '등등', '따위', '및', '또는', '혹은', '즉',
        '의', '를', '을', '에', '가', '이', '은', '는', '와', '과',
        '했다', '한다', '하며', '하여', '해서', '하고', '하니', '하면',
        '그래서', '그러니', '그러므로', '따라서', '때문에', '왜냐하면',
        '비해', '보다', '처럼', '같이', '만큼', '대로', '듯이',
        '점', '면', '측면', '부분', '경우', '상황', '상태', '정도',
        '이런', '저런', '그런', '어떤', '무슨', '어느', '어떻게',
        '가능', '불가능', '필요', '불필요', '중요', '사용', '이용',
        '느낌', '기분', '마음', '생각', '의견', '감정', '인상',
        '한', '두', '세', '네', '몇', '여러', '많은', '적은',
        '첫', '둘', '셋', '넷', '첫째', '둘째', '셋째', '마지막',
        '좀', '꼭', '딱', '막', '참', '진짜', '정말로', '확실히',
        '거의', '대부분', '대체로', '보통', '일반적', '평균적',
        '특히', '특별히', '주로', '대개', '대체로', '전반적'
    }
    
    # 모든 텍스트를 결합하고 키워드 추출
    all_text = ' '.join(texts)
    
    # 한글만 추출 (영어, 숫자 제외)
    words = re.findall(r'[가-힣]+', all_text)
    
    # 필터링 조건 강화
    filtered_words = []
    for word in words:
        if (len(word) >= 2 and 
            word not in stopwords and
            not word.endswith('습니다') and
            not word.endswith('합니다') and
            not word.endswith('입니다') and
            not word.endswith('됩니다') and
            not word.startswith('있') and
            not word.startswith('없') and
            not word.startswith('하') and
            not word.startswith('되') and
            not word.startswith('않')):
            filtered_words.append(word)
    
    # 단어 빈도 계산
    word_freq = Counter(filtered_words)
    
    # 빈도수가 1인 단어는 제외
    word_freq = {word: freq for word, freq in word_freq.items() if freq > 1}
    
    return word_freq

def generate_coupang_search_link(product_name):
    """쿠팡 검색 링크 생성"""
    # 검색어 URL 인코딩
    encoded_keyword = urllib.parse.quote(product_name)
    
    # 쿠팡 검색 링크 생성
    coupang_search_link = f"https://www.coupang.com/np/search?q={encoded_keyword}"
    
    return coupang_search_link

def get_sample_coupang_product(product_name):
    """쿠팡 상품 정보 샘플 생성 (승인용)"""
    # 승인을 위한 샘플 상품 정보
    sample_product = {
        "productName": f"{product_name}",
        "productPrice": "최저가 확인",
        "productImage": "https://via.placeholder.com/200x200/ff6b35/ffffff?text=COUPANG",
        "isRocket": True,
        "productUrl": generate_coupang_search_link(product_name),
        "vendorName": "쿠팡",
        "description": f"{product_name}의 다양한 옵션을 쿠팡에서 확인해보세요!"
    }
    return sample_product
