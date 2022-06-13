import asyncio
import tempfile

import soundfile as sf
import streamlit as st

from utils.streamlit_display_functions import display_new_line
from voice_synthesis import async_load_voice_model, text_to_speech


# 음성 합성을 체험해볼 수 있는 페이지
def lab_page() -> None:
    st.subheader("​👀​🔎 Welcome to Voice Synthesis Laboratory 📢")

    display_new_line(2)

    # streamlit 세션이 재구동되어도 유지되어야 하는 변수 초기화
    if "processor" not in st.session_state:
        st.session_state.processor = None
    if "model" not in st.session_state:
        st.session_state.model = None
    if "mb_melgan" not in st.session_state:
        st.session_state.mb_melgan = None

    # 사용할 언어 선택
    selected_langauge = st.selectbox("언어를 설정해주세요", ("ko", "en", "ch"))

    # 언어 설정 버튼 클릭 시 모델 불러오기
    if st.button("설정"):
        with st.spinner("음성 모델을 불러오는 중입니다."):
            loop = asyncio.new_event_loop()
            (
                st.session_state.processor,
                st.session_state.model,
                st.session_state.mb_melgan,
            ) = loop.run_until_complete(async_load_voice_model(selected_langauge))

    # 모델이 성공적으로 불러와졌을 경우 입력된 텍스트로 음성 합성
    if (
        st.session_state.processor
        and st.session_state.model
        and st.session_state.mb_melgan
    ):
        sample_text = st.text_input("문장을 넣어주세요")
        if st.button("음성 생성하기"):
            audio = None
            try:
                audio = text_to_speech(
                    sample_text,
                    st.session_state.processor,
                    st.session_state.model,
                    st.session_state.mb_melgan,
                    language=selected_langauge,
                )

            except:
                st.error("음성을 생성할 수 없어요!")
                st.warning("언어 설정을 올바르게 했는지 다시 한 번 확인하고 모델을 불러와주세요.")

            # 생성 된 음성을 temporaryfile로 만들고 이를 streamlit audio 재생
            if audio is not None:
                with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
                    sf.write(tmp.name, audio, 22050, "PCM_16", format="wav")
                    st.audio(tmp.name, format="audio/wav")
