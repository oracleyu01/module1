"""
LangGraph 워크플로우
"""
from typing import TypedDict, Annotated, List, Union, Dict
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
import operator
import streamlit as st
import time
from supabase import create_client
from config.settings import get_api_keys
from core.crawler import ProConsLaptopCrawler

# State 정의
class SearchState(TypedDict):
    """검색 프로세스의 상태"""
    product_name: str
    search_method: str
    results: dict
    pros: List[str]
    cons: List[str]
    sources: List[dict]
    messages: Annotated[List[Union[HumanMessage, AIMessage]], operator.add]
    error: str

# 클라이언트 초기화
@st.cache_resource
def get_supabase_client():
    keys = get_api_keys()
    return create_client(keys["SUPABASE_URL"], keys["SUPABASE_KEY"]) if keys["SUPABASE_URL"] and keys["SUPABASE_KEY"] else None

@st.cache_resource
def get_crawler():
    keys = get_api_keys()
    return ProConsLaptopCrawler(keys["NAVER_CLIENT_ID"], keys["NAVER_CLIENT_SECRET"]) if keys["NAVER_CLIENT_ID"] and keys["NAVER_CLIENT_SECRET"] else None

def search_database(state: SearchState) -> SearchState:
    """데이터베이스에서 제품 검색"""
    product_name = state["product_name"]
    supabase = get_supabase_client()
    
    if not supabase:
        state["messages"].append(
            AIMessage(content="⚠️ 데이터베이스가 설정되지 않았습니다. 웹 검색으로 진행합니다.")
        )
        state["results"] = {"data": None}
        return state
    
    state["messages"].append(
        HumanMessage(content=f"📊 데이터베이스에서 '{product_name}' 검색 중...")
    )
    
    try:
        exact_match = supabase.table('laptop_pros_cons').select("*").eq('product_name', product_name).execute()
        if exact_match.data:
            state["search_method"] = "database"
            state["results"] = {"data": exact_match.data}
            state["messages"].append(
                AIMessage(content=f"✅ 데이터베이스에서 '{product_name}' 정보를 찾았습니다! ({len(exact_match.data)}개 항목)")
            )
            return state
        
        state["messages"].append(
            AIMessage(content=f"❌ 데이터베이스에서 '{product_name}'을(를) 찾을 수 없습니다. 웹에서 검색합니다...")
        )
        state["results"] = {"data": None}
        return state
        
    except Exception as e:
        state["error"] = str(e)
        state["messages"].append(
            AIMessage(content=f"⚠️ 데이터베이스 검색 오류: {str(e)}")
        )
        state["results"] = {"data": None}
        return state

def crawl_web(state: SearchState) -> SearchState:
    """웹에서 제품 정보 크롤링"""
    if state["results"].get("data"):
        return state
    
    product_name = state["product_name"]
    state["search_method"] = "web_crawling"
    crawler = get_crawler()
    
    if not crawler:
        state["messages"].append(
            AIMessage(content="⚠️ 웹 크롤링이 설정되지 않았습니다.")
        )
        return state
    
    state["messages"].append(
        HumanMessage(content=f"🌐 웹에서 '{product_name}' 리뷰 수집 시작...")
    )
    
    # API 키가 없을 때 샘플 데이터
    keys = get_api_keys()
    if not keys["OPENAI_API_KEY"]:
        state["pros"] = [
            "가볍고 휴대성이 좋습니다",
            "배터리 지속 시간이 깁니다",
            "디스플레이가 선명합니다",
            "성능이 우수합니다",
            "디자인이 세련되었습니다"
        ]
        state["cons"] = [
            "가격이 비쌉니다",
            "포트가 부족합니다",
            "키보드 키감이 아쉽습니다"
        ]
        state["messages"].append(
            AIMessage(content="📌 샘플 데이터를 표시합니다 (API 키 설정 필요)")
        )
        return state
    
    all_pros = []
    all_cons = []
    sources = []
    
    search_queries = [
        f"{product_name} 장단점 실사용",
        f"{product_name} 단점 후기",
        f"{product_name} 장점 리뷰"
    ]
    
    for query in search_queries:
        state["messages"].append(
            AIMessage(content=f"🔍 검색어: '{query}'")
        )
        
        result = crawler.search_blog(query, display=10)
        if not result or 'items' not in result:
            continue
        
        posts = result['items']
        state["messages"].append(
            AIMessage(content=f"→ {len(posts)}개 포스트 발견")
        )
        
        for idx, post in enumerate(posts[:5]):
            state["messages"].append(
                AIMessage(content=f"📖 분석 중: {post['title'][:40]}...")
            )
            
            content = crawler.crawl_content(post['link'])
            if not content:
                continue
            
            crawler.stats['total_crawled'] += 1
            
            pros_cons = crawler.extract_pros_cons_with_gpt(product_name, content)
            
            if pros_cons:
                all_pros.extend(pros_cons['pros'])
                all_cons.extend(pros_cons['cons'])
                sources.append({
                    'title': post['title'],
                    'link': post['link'],
                    'date': post.get('postdate', '')
                })
                
                state["messages"].append(
                    AIMessage(content=f"✓ 장점 {len(pros_cons['pros'])}개, 단점 {len(pros_cons['cons'])}개 추출")
                )
            
            time.sleep(1)
        
        time.sleep(2)
    
    unique_pros = crawler.deduplicate_points(all_pros)
    unique_cons = crawler.deduplicate_points(all_cons)
    
    state["pros"] = unique_pros
    state["cons"] = unique_cons
    state["sources"] = sources[:10]
    
    if state["pros"] or state["cons"]:
        state["messages"].append(
            AIMessage(content=f"🎉 웹 크롤링 완료! 총 장점 {len(state['pros'])}개, 단점 {len(state['cons'])}개 수집")
        )
        
        # DB에 저장
        try:
            supabase = get_supabase_client()
            if supabase:
                data = []
                
                for pro in state["pros"]:
                    data.append({
                        'product_name': product_name,
                        'type': 'pro',
                        'content': pro
                    })
                
                for con in state["cons"]:
                    data.append({
                        'product_name': product_name,
                        'type': 'con',
                        'content': con
                    })
                
                if data:
                    supabase.table('laptop_pros_cons').insert(data).execute()
                    state["messages"].append(
                        AIMessage(content="💾 데이터베이스에 저장 완료!")
                    )
                    st.session_state.saved_products += 1
        except Exception as e:
            state["messages"].append(
                AIMessage(content=f"⚠️ DB 저장 실패: {str(e)}")
            )
    else:
        state["messages"].append(
            AIMessage(content=f"😢 '{product_name}'에 대한 정보를 찾을 수 없습니다.")
        )
    
    state["messages"].append(
        AIMessage(content=f"📊 크롤링 통계: 총 {crawler.stats['total_crawled']}개 페이지, 유효 추출 {crawler.stats['valid_pros_cons']}개")
    )
    
    return state

def process_results(state: SearchState) -> SearchState:
    """결과 처리 및 정리"""
    if state["search_method"] == "database" and state["results"].get("data"):
        data = state["results"]["data"]
        state["pros"] = [item['content'] for item in data if item['type'] == 'pro']
        state["cons"] = [item['content'] for item in data if item['type'] == 'con']
        state["sources"] = []
        
        state["messages"].append(
            AIMessage(content=f"📋 결과 정리 완료: 장점 {len(state['pros'])}개, 단점 {len(state['cons'])}개")
        )
    
    return state

def should_search_web(state: SearchState) -> str:
    """웹 검색이 필요한지 판단"""
    if state["results"].get("data"):
        return "process"
    else:
        return "crawl"

@st.cache_resource
def create_search_workflow():
    """LangGraph 워크플로우 생성"""
    workflow = StateGraph(SearchState)
    
    # 노드 추가
    workflow.add_node("search_db", search_database)
    workflow.add_node("crawl_web", crawl_web)
    workflow.add_node("process", process_results)
    
    # 엣지 설정
    workflow.set_entry_point("search_db")
    workflow.add_conditional_edges(
        "search_db",
        should_search_web,
        {
            "crawl": "crawl_web",
            "process": "process"
        }
    )
    workflow.add_edge("crawl_web", "process")
    workflow.add_edge("process", END)
    
    return workflow.compile()
