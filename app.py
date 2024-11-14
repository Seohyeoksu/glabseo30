import streamlit as st
from openai import OpenAI
import os

# OpenAI API 설정
os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 페이지 설정
st.set_page_config(page_title="글쓰기기 첨삭지도", page_icon="📝", layout="wide")

# CSS 스타일
st.markdown("""
    <style>
        .main { background-color: #f0f2f6; font-family: 'Noto Sans KR', sans-serif; }
        h1 { color: #1e3a8a; text-align: center; font-size: 2.5rem; font-weight: 700; margin-bottom: 2rem; }
        .section { background-color: #ffffff; padding: 1.5rem; border-radius: 10px; 
                  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 2rem; }
        .feedback-section { background-color: #f0f7ff; padding: 1.5rem; border-radius: 10px;
                          margin-bottom: 1rem; border-left: 4px solid #3b82f6; }
        .original-text { background-color: #fff5f5; padding: 1.5rem; border-radius: 5px;
                       margin-top: 1rem; border-left: 4px solid #f56565; }
        .revised-text { background-color: #f0fff4; padding: 1.5rem; border-radius: 5px;
                      margin-top: 1rem; border-left: 4px solid #48bb78; }
        .writing-tip { background-color: #f3f4f6; padding: 1rem; margin: 0.5rem 0; border-radius: 5px; }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

def get_poetry_prompt(text, topic, poetry_type, grade):
    return f"""주제: {topic}
시의 유형: {poetry_type}
학년: {grade}
작성한 시: {text}

아래 항목을 상세히 분석해주세요:

#전반적_평가#
- 시적 주제 전달력
- 운율과 리듬감
- 시어 선택의 적절성
- 이미지와 감각적 표현
- 시의 구조
- 정서 전달
- 창의성과 독창성

#잘된_점#
- 효과적인 시어와 표현
- 운율과 리듬
- 이미지 표현
- 감정 전달력
- 비유와 상징
- 독창적 발상
- 형식의 활용

#개선점#
- 시어 선택 (대안 제시)
- 운율과 리듬 보완
- 이미지 강화
- 감정 표현 심화
- 형식 다듬기
- 주제 발전
- 시적 긴장감

#표현_향상#
- 감각적 이미지 활용법
- 참신한 비유 방법
- 운율 활용 방법
- 시어 선택 기준
- 연 구성 방법
- 수사법 활용
- 여백의 미 살리기
- 시적 상상력 키우기

#수정본#
반드시 아래 기준으로 시를 개선하여 작성해주세요:
- 원문의 정서와 의미 유지
- 이미지와 감각적 표현 강화
- 운율과 리듬감 보강
- 시어 선택 개선
- 형식 다듬기
[개선된 시를 여기 작성]

#창작_조언#
1. 시적 발상법
2. 소재 선정
3. 운율 살리기
4. 이미지 표현법
5. 감정 표현법
6. 시어 선택법
7. 퇴고 방법
8. 형식 활용법"""

def get_regular_prompt(text, topic, writing_type, grade):
    return f"""주제: {topic}
글의 유형: {writing_type}
학년: {grade}
작성한 글: {text}

#전반적_평가#
- 주제 전달력
- 내용의 일관성
- 구성의 체계성
- 표현의 적절성
- 문장의 정확성
- 단락 구성
- 글의 완성도
- 독자의 흥미

#잘된_점#
- 효과적인 표현과 문장
- 적절한 어휘 사용
- 문단 구성
- 감정/생각 표현
- 묘사와 설명
- 창의적 아이디어
- 독자와의 소통
- 주제 전달력

#개선점#
- 어휘와 표현 (대안 제시)
- 문장 구조 개선
- 내용 보충
- 구성 보완
- 묘사 강화
- 독자 고려
- 주제 심화
- 문체 개선

#표현_향상#
- 감각적 묘사 방법
- 비유와 상징 활용
- 감정 표현 방법
- 대화문 활용법
- 장면 묘사 기법
- 인물 묘사 방법
- 배경 묘사 기법
- 분위기 조성법

#수정본#
반드시 아래 기준으로 글을 개선하여 작성해주세요:
- 원문의 핵심 내용 유지
- 문장 구조 개선
- 어휘 수준 향상
- 구체적 묘사 추가
- 문단 구성 보완
[개선된 글을 여기 작성]

#세부_조언#
1. 글감 선정법
2. 개요 작성법
3. 퇴고 방법
4. 문장 다듬기
5. 어휘 선택
6. 구성 방법
7. 독자 고려하기
8. 일관성 유지하기"""

def get_feedback(text, topic, writing_type, grade, poetry_type=None):
    prompt = get_poetry_prompt(text, topic, poetry_type, grade) if writing_type == "시" else \
             get_regular_prompt(text, topic, writing_type, grade)
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

def display_feedback(feedback, writing_type):
    sections = {
        "전반적_평가": "📝 전반적인 평가",
        "잘된_점": "⭐ 잘된 점",
        "개선점": "💡 개선이 필요한 점",
        "표현_향상": "✨ 표현 향상 방법",
        "수정본": "📋 수정된 글",
        "세부_조언" if writing_type != "시" else "창작_조언": "🎯 조언"
    }
    
    for section_id, title in sections.items():
        try:
            content = feedback.split(f"#{section_id}#")[1].split("#")[0].strip()
            st.markdown(f"<div class='feedback-section'>", unsafe_allow_html=True)
            st.markdown(f"### {title}")
            st.write(content)
            st.markdown("</div>", unsafe_allow_html=True)
        except IndexError:
            st.error(f"{title} 생성 중 오류가 발생했습니다.")

def main():
    st.markdown("<h1>글쓰기 첨삭지도 도우미 📝</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        topic = st.text_input("글의 주제를 입력하세요", 
                            placeholder="예: 봄날, 우리 가족, 운동회 등")
        writing_type = st.selectbox("글의 유형을 선택하세요", 
                                  ["시", "일기", "수필", "관찰문", "편지글", "감상문", "설명문", "기행문"])
        
        if writing_type == "시":
            poetry_type = st.selectbox("시의 유형을 선택하세요", 
                                     ["자유시", "동시", "산문시"])
        
        grade = st.selectbox("학년을 선택하세요", 
                           ["초등학교 3학년", "초등학교 4학년", "초등학교 5학년", "초등학교 6학년"])
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        placeholder = "여기에 시를 입력해주세요." if writing_type == "시" else "여기에 글을 입력해주세요."
        student_text = st.text_area("작성한 글을 입력하세요", height=300, placeholder=placeholder)
        
        if writing_type == "시" and student_text:
            st.markdown("<div class='writing-tip'>💡 **시 쓰기 팁**: 감각적 표현과 비유를 활용하면 더 풍부한 시가 됩니다!</div>", 
                       unsafe_allow_html=True)
        elif student_text:
            st.markdown("<div class='writing-tip'>💡 **글쓰기 팁**: 구체적인 예시와 자세한 설명을 덧붙이면 더 풍부한 글이 됩니다!</div>", 
                       unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button('분석하기'):
        if not topic or not student_text:
            st.error("주제와 글을 모두 입력해주세요.")
            return
        
        with st.spinner('분석 중...'):
            poetry_type = poetry_type if writing_type == "시" else None
            feedback = get_feedback(student_text, topic, writing_type, grade, poetry_type)
            
            # 원본과 수정본 비교
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<div class='original-text'>", unsafe_allow_html=True)
                st.markdown(f"#### 원본 {'시' if writing_type == '시' else '글'}")
                st.write(student_text)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='revised-text'>", unsafe_allow_html=True)
                st.markdown(f"#### 수정된 {'시' if writing_type == '시' else '글'}")
                try:
                    revised = feedback.split("#수정본#")[1].split("#")[0].strip()
                    st.write(revised)
                except IndexError:
                    st.error("수정본이 생성되지 않았습니다. 다시 시도해주세요.")
                st.markdown("</div>", unsafe_allow_html=True)
            
            display_feedback(feedback, writing_type)

if __name__ == "__main__":
    main()
