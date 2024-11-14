import streamlit as st
from openai import OpenAI
import os

# OpenAI API 설정
os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 페이지 설정
st.set_page_config(page_title="글쓰기 첨삭지도", page_icon="📝", layout="wide")

# CSS 스타일
st.markdown("""
    <style>
        .main { background-color: #f0f2f6; font-family: 'Noto Sans KR', sans-serif; }
        h1 { color: #1e3a8a; text-align: center; font-size: 2.5rem; font-weight: 700; margin-bottom: 2rem; }
        .section { background-color: #ffffff; padding: 1.5rem; border-radius: 10px; 
   기 첨삭지도 도우미 📝</h1>", unsafe_allow_html=True)
    
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
