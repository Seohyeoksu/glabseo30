import os
from openai import OpenAI
import streamlit as st

os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

st.set_page_config(
    page_title="우리반 문집 첨삭지도",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="auto",
)

st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
            font-family: 'Noto Sans KR', sans-serif;
        }
        h1 {
            color: #1e3a8a;
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 2rem;
        }
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .instructions {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        .instructions h3 {
            color: #2563eb;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        .section {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        .stButton>button {
            background-color: #2563eb;
            color: white;
            font-size: 1rem;
            font-weight: 600;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #1e40af;
        }
        .stTextArea>div>div>textarea {
            border-radius: 5px;
            border: 1px solid #e5e7eb;
        }
        .stSelectbox>div>div>select {
            border-radius: 5px;
            border: 1px solid #e5e7eb;
        }
        .feedback-section {
            background-color: #f0f7ff;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            border-left: 4px solid #3b82f6;
        }
        .expand-tips {
            background-color: #fff7ed;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            border-left: 4px solid #f97316;
        }
        .writing-tip {
            background-color: #f3f4f6;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 5px;
        }
        .example-text {
            background-color: #f8fafc;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 5px;
            font-style: italic;
        }
        .original-text {
            background-color: #fff5f5;
            padding: 1.5rem;
            border-radius: 5px;
            margin-top: 1rem;
            border-left: 4px solid #f56565;
        }
        .revised-text {
            background-color: #f0fff4;
            padding: 1.5rem;
            border-radius: 5px;
            margin-top: 1rem;
            border-left: 4px solid #48bb78;
        }
        .comparison {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-top: 1rem;
        }
        .highlight {
            background-color: #fef3c7;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
        }
        .emoji-bullet {
            margin-right: 0.5rem;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown("<h1>우리반 문집 참삭지도 도우미 📝</h1>", unsafe_allow_html=True)

st.markdown("""
<div class="instructions">
    <h3>사용 설명서 ✏️</h3>
    <ul>
        <li><strong>글의 주제</strong>: 작성하고 싶은 글의 주제를 자유롭게 입력해주세요.</li>
        <li><strong>글의 유형</strong>: 어떤 종류의 글을 쓸지 선택해주세요.</li>
        <li><strong>학년 선택</strong>: 학년에 맞는 글쓰기 지도를 받을 수 있습니다.</li>
        <li><strong>글 입력</strong>: 작성한 글 전체를 입력해주세요.</li>
        <li>모든 정보를 입력한 후 <strong>'도움받기'</strong> 버튼을 클릭하면, AI 선생님이 글쓰기 도움말과 함께 수정된 글을 제시합니다.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    topic = st.text_input("글의 주제를 입력하세요", 
                         placeholder="예: 운동회에서 있었던 일, 봄나들이, 우리 가족 이야기 등")
    
    writing_types = ["시", "일기", "수필", "관찰문", "편지글", "감상문", "설명문", "기행문", "자기소개서"]
    writing_type = st.selectbox("글의 유형을 선택하세요", writing_types)
    
    if writing_type == "시":
        poetry_types = ["자유시", "산문시", "동시", "혼시", "연시"]
        poetry_style = st.selectbox("시의 형식을 선택하세요", poetry_types)
    
    grade_options = ["초등학교 3학년", "초등학교 4학년", "초등학교 5학년", "초등학교 6학년"]
    grade = st.selectbox("학년을 선택하세요", grade_options)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    if writing_type == "시":
        student_text = st.text_area(
            "작성한 시 전체를 입력해주세요", 
            height=300,
            placeholder="여기에 작성한 시를 붙여넣거나 입력해주세요."
        )
        if student_text:
            st.markdown("<div class='writing-tip'>", unsafe_allow_html=True)
            st.markdown("💡 **시 쓰기 팁**: 감각적인 표현과 비유를 활용하면 더 풍부한 시를 쓸 수 있어요!")
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        student_text = st.text_area(
            "작성한 글 전체를 입력해주세요", 
            height=300,
            placeholder="여기에 작성한 글을 붙여넣거나 입력해주세요."
        )
        if student_text:
            st.markdown("<div class='writing-tip'>", unsafe_allow_html=True)
            st.markdown("💡 **글쓰기 팁**: 구체적인 예시와 자세한 설명을 덧붙이면 더 풍부한 글이 됩니다!")
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

if st.button('도움받기', key='generate_button'):
    if not topic.strip():
        st.error("글의 주제를 입력해주세요.")
    elif not student_text.strip():
        st.error("작성한 글을 입력해주세요.")
    else:
        with st.spinner('글을 꼼꼼히 읽고 생각하는 중입니다...'):
            prompt = f"""
            주제: {topic}
            글의 유형: {writing_type}
            {'시의 형식: ' + poetry_style if writing_type == "시" else ''}
            학년: {grade}
            작성한 글: {student_text}
            """
            
            if writing_type == "시":
                system_content = """당신은 학생들의 시 쓰기를 돕는 따뜻하고 세심한 국어 선생님입니다. 
                학생이 작성한 시를 꼼꼼히 읽고 다음과 같은 방식으로 도와주세요:

                1. 전반적인 평가
                   - 시의 주제 전달력
                   - 시적 표현의 적절성
                   - 운율과 리듬감
                   - 이미지와 감각적 표현
                   
                2. 구체적인 장점 분석
                   - 인상적인 시어나 표현 직접 인용
                   - 효과적으로 사용된 비유와 상징
                   - 시의 구성과 전개 방식의 장점
                   
                3. 보완이 필요한 부분
                   - 시어 선택이나 표현의 미숙한 부분
                   - 보충하면 좋을 이미지나 감각
                   - 수정이 필요한 운율이나 리듬
                   
                4. 분량 늘리기 구체적 방법
                   - 감각적 이미지 추가 방법
                   - 구체적 정서 표현 방법
                   - 비유와 상징 확장 방법
                   - 연과 행 구성 방법
                   
                5. 시 쓰기 기술 향상을 위한 조언
                   - 학년 수준에 맞는 시어 추천
                   - 효과적인 비유 만들기
                   - 감각적 표현 방법
                   
                6. 수정 예시 제공
                   - 원문의 일부를 수정한 구체적 예시
                   - 분량을 늘린 구체적 예시
                   
                7. 다음 시를 위한 조언
                   - 소재 찾기 방법
                   - 시적 발상 방법
                   - 퇴고 방법

                응답은 다음 형식으로 구성해주세요:

                ### 전반적인 평가
                [시의 주요 특징과 전체적인 평가]

                ### 잘된 점들
                1. [구체적인 예시와 함께 설명]
                2. [구체적인 예시와 함께 설명]
                3. [구체적인 예시와 함께 설명]

                ### 보완하면 좋을 점들
                1. [구체적인 예시와 함께 설명]
                2. [구체적인 예시와 함께 설명]
                3. [구체적인 예시와 함께 설명]

                ### 분량 늘리기 방법
                1. 감각적 이미지 추가하기
                   - 구체적인 예시
                   - 적용 가능한 부분 제시
                2. 정서 표현 확장하기
                   - 구체적인 예시
                   - 적용 가능한 부분 제시
                3. 비유와 상징 더하기
                   - 구체적인 예시
                   - 적용 가능한 부분 제시

                ### 추천 시어와 표현
                [학년 수준에 맞는 시어와 표현 목록]

                ### 수정된 시
                [제안 사항을 반영한 수정본]

                ### 수정 내용 설명
                [각 수정 부분에 대한 상세한 설명]

                ### 다음 시를 위한 조언
                [구체적인 시 쓰기 전략과 방법]
                """
            else:
                system_content = """당신은 학생들의 글쓰기를 돕는 따뜻하고 세심한 국어 선생님입니다. 
                학생이 작성한 글을 꼼꼼히 읽고 다음과 같은 방식으로 도와주세요:

                1. 전반적인 평가
                   - 주제 전달력
                   - 내용의 일관성
                   - 표현의 적절성
                   - 문장의 정확성
                   
                2. 구체적인 장점 분석
                   - 인상적인 표현이나 문장 직접 인용
                   - 효과적으로 사용된 표현 기법
                   - 글의 구성상 잘된 점
                   
                3. 보완이 필요한 부분
                   - 문장 구성이나 표현의 미숙한 부분
                   - 보충하면 좋을 내용
                   - 고쳐쓰기가 필요한 부분
                   
                4. 분량 늘리기 구체적 방법
                   - 더 자세히 설명할 수 있는 부분 예시
                   - 감각적 묘사를 추가할 수 있는 부분
                   - 구체적인 사례나 경험을 덧붙일 수 있는 부분
                   - 대화나 행동 묘사를 추가할 수 있는 부분
                   
                5. 글쓰기 기술 향상을 위한 조언
                   - 학년 수준에 맞는 어휘 추천
                   - 문장 만들기 연습
                   - 효과적인 묘사 방법
                   
                6. 수정 예시 제공
                   - 원문의 일부를 수정한 구체적 예시
                   - 분량을 늘린 구체적 예시
                   
                7. 다음 글을 위한 조언
                   - 글감 선정 방법
                   - 개요 작성 방법
                   - 퇴고 방법

                응답은 다음 형식으로 구성해주세요:

                ### 전반적인 평가
                [글의 주요 특징과 전체적인 평가]

                ### 잘된 점들
                1. [구체적인 예시와 함께 설명]
                2. [구체적인 예시와 함께 설명]
                3. [구체적인 예시와 함께 설명]

                ### 보완하면 좋을 점들
                1. [구체적인 예시와 함께 설명]
                2. [구체적인 예시와 함께 설명]
                3. [구체적인 예시와 함께 설명]

                ### 분량 늘리기 방법
                1. 세부 묘사 추가하기
                   - 구체적인 예시
                   - 적용 가능한 부분 제시
                2. 경험과 사례 덧붙이기
                   - 구체적인 예시
                   - 적용 가능한 부분 제시
                3. 대화와 행동 묘사 더하기
                   - 구체적인 예시
                   - 적용 가능한 부분 제시

                ### 추천 표현과 어휘
                [학년 수준에 맞는 표현과 어휘 목록]

                ### 수정된 글
                [제안 사항을 반영한 수정본]

                ### 수정 내용 설명
                [각 수정 부분에 대한 상세한 설명]

                ### 다음 글을 위한 조언
                [구체적인 글쓰기 전략과 방법]
                """
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    },
                    {
                        "role": "system",
                        "content": system_content
                    }
                ],
                model="gpt-4",
            )
            
            result = chat_completion.choices[0].message.content
            
            st.markdown("<div class='section'>", unsafe_allow_html=True)
            
            # 전반적인 평가 표시
            st.markdown("<div class='feedback-section'>", unsafe_allow_html=True)
            st.markdown("### 📝 전반적인 평가")
            evaluation_part = result.split("### 전반적인 평가")[1].split("###")[0].strip()
            st.write(evaluation_part)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # 잘된 점들 표시
            st.markdown("<div class='feedback-section'>", unsafe_allow_html=True)
            st.markdown("### ⭐ 잘된 점들")
            good_points = result.split("### 잘된 점들")[1].split("###")[0].strip()
            st.write(good_points)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # 보완점 표시
            st.markdown("<div class='feedback-section'>", unsafe_allow_html=True)
            st.markdown("### 💡 보완하면 좋을 점들")
            improvement_points = result.split("### 보완하면 좋을 점들")[1].split("###")[0].strip()
            st.write(improvement_points)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # 분량 늘리기 방법 표시
            st.markdown("<div class='expand-tips'>", unsafe_allow_html=True)
            st.markdown("### 📚 분량 늘리기 방법")
            expansion_tips = result.split("### 분량 늘리기 방법")[1].split("###")[0].strip()
            st.write(expansion_tips)
            
            # 추가 팁 표시
            st.markdown("#### 🔍 추가 팁")
            st.markdown("""
            - 각 문장을 2-3개의 문장으로 확장해보세요
            - 오감을 활용한 묘사를 추가해보세요
            - 구체적인 예시나 경험을 덧붙여보세요
            - 인물의 감정이나 생각을 자세히 표현해보세요
            """)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # 추천 표현과 어휘 표시
            st.markdown("<div class='feedback-section'>", unsafe_allow_html=True)
            st.markdown("### ✨ 추천 표현과 어휘")
            expressions = result.split("### 추천 표현과 어휘")[1].split("###")[0].strip()
            st.write(expressions)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # 원본과 수정본 비교 표시
            st.markdown("### 📋 원본과 수정본 비교")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div class='original-text'>", unsafe_allow_html=True)
                st.markdown("#### 원본 글")
                st.write(student_text)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='revised-text'>", unsafe_allow_html=True)
                st.markdown("#### 수정된 글")
                revised_text = result.split("### 수정된 글")[1].split("###")[0].strip()
                st.write(revised_text)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # 수정 설명 표시
            st.markdown("<div class='feedback-section'>", unsafe_allow_html=True)
            st.markdown("### 📌 수정 내용 설명")
            revision_explanation = result.split("### 수정 내용 설명")[1].split("###")[0].strip()
            st.write(revision_explanation)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # 다음 글을 위한 조언 표시
            st.markdown("<div class='feedback-section'>", unsafe_allow_html=True)
            st.markdown("### 🎯 다음 글을 위한 조언")
            next_writing_tips = result.split("### 다음 글을 위한 조언")[1].strip()
            st.write(next_writing_tips)
            st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    st.sidebar.markdown("""
    ### 도움말
    1. 글의 주제를 자유롭게 입력해주세요
    2. 글의 유형을 선택해주세요
    3. 학년을 선택해주세요
    4. 작성한 글을 입력해주세요
    5. '도움받기' 버튼을 클릭하세요
    
    ### 글쓰기 팁
    - 구체적인 경험과 감정을 표현해보세요
    - 비유와 상징을 활용해보세요
    - 오감을 활용한 묘사를 시도해보세요
    - 대화를 활용하면 글이 더 생생해져요
    """)
