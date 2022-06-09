import asyncio
import tempfile
from typing import Type

import numpy as np
import pandas as pd
import soundfile as sf
import streamlit as st
from streamlit_option_menu import option_menu

from pacemaker import PaceMakerCar
from user_database import UserDB
from voice_synthesis import load_voice_model, text_to_speech


def display_new_line(num_line: int) -> None:
    for i in range(num_line):
        st.text(" ")


def home_page() -> None:
    banner_col1, banner_col2 = st.columns([2, 3])
    with banner_col1:
        st.markdown("<u style='color: #FA5991; '>ㅤㅤㅤㅤㅤㅤㅤㅤㅤ</u>", unsafe_allow_html=True)
        st.subheader("Get Pace Get Healty")
        st.markdown(
            '<p style="font-family:Courier; color:black; font-size: 15px;">Kickstart Your Health <br> with Pacemaker <br> that Can Pace Your Workouts</p>',
            unsafe_allow_html=True,
        )

    with banner_col2:
        st.image("images/home_banner.jpg")

    display_new_line(3)
    # st.markdown("<hr style='height:1px; width:50%; border-width:0; color:#FA5991; background-color:#FA5991'>", unsafe_allow_html=True)

    st.markdown(
        "<h3 style='color: #FA5991;'>what is Pacemaker?</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<SPAN style='color: #FA5991; text-decoration:overline; '>ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ</SPAN>",
        unsafe_allow_html=True,
    )

    display_new_line(1)

    icon_col1, _, icon_col2, _, icon_col3 = st.columns(5)
    with icon_col1:
        st.image("images/running_icon.png")
        st.markdown(
            "<p style='text-align: center; color: black;'>Some title</p>",
            unsafe_allow_html=True,
        )
    with icon_col2:
        st.image("images/report_icon.png")
        st.markdown(
            "<p style='text-align: center; color: black;'>Some title</p>",
            unsafe_allow_html=True,
        )
    with icon_col3:
        st.image("images/people_icon.png")
        st.markdown(
            "<p style='text-align: center; color: black;'>Some title</p>",
            unsafe_allow_html=True,
        )

    display_new_line(6)

    st.markdown("<h3 style='color: #FA5991;'>Demo Video</h3>", unsafe_allow_html=True)
    st.markdown(
        "<SPAN style='color: #FA5991; text-decoration:overline; '>ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ</SPAN>",
        unsafe_allow_html=True,
    )
    st.video("https://www.youtube.com/watch?v=TeGyIz971ao")


def login_page(user_db: Type[UserDB]):
    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.checkbox("Login"):

        user_db.create_usertable()
        user_db.create_recordtable()
        hashed_password = user_db.make_hashes(password)

        login_user_data = user_db.login_user(
            username, user_db.check_hashes(password, hashed_password)
        )

        if login_user_data:
            (
                user_id,
                user_name,
                password,
                user_height,
                user_weight,
            ) = login_user_data[0]

            task = option_menu(
                None,
                ["Pacemaker", "My Record", "Setting"],
                icons=["robot", "clipboard-data", "gear"],
                menu_icon="cast",
                default_index=0,
                orientation="horizontal",
                styles={"nav-link-selected": {"background-color": "#FA5991"}},
            )

            if task == "Pacemaker":
                if not (user_height and user_weight):
                    st.warning("현재 입력된 키와 몸무게 정보가 없습니다.")
                    st.info("Setting에서 키와 몸무게를 입력해주십시오.")
                else:
                    st.info(
                        "🧑 {}님의 현재 키는 {}, 몸무게는 {} 입니다.".format(
                            username, user_height, user_weight
                        )
                    )

                if "default_speed" not in st.session_state:
                    st.session_state.default_speed = None
                st.text("1️⃣ 기본 속도를 입력해주세요")
                st.session_state.default_speed = st.slider("", 0, 130, 25)

                display_new_line(1)

                st.text("2️⃣ 모드를 선택해주세요")
                selected_mode = st.selectbox("", ("쉬운 모드", "보통 모드", "힘든 모드"), index=1)

                display_new_line(1)

                if "bundle" not in st.session_state:
                    st.session_state.bundle = None
                if "pacemaker" not in st.session_state:
                    st.session_state.pacemaker = None

                _, load_col, _ = st.columns(3)
                if load_col.button("💾 설정 저장 및 연결하기"):
                    with st.spinner("페이스메이커에 연결하는 중입니다."):
                        loop = asyncio.new_event_loop()
                        st.session_state.bundle = loop.run_until_complete(
                            PaceMakerCar.load_modi()
                        )

                    if st.session_state.bundle:
                        st.success("페이스메이커에 성공적으로 연결되었습니다.")
                        st.info("페이스메이커를 작동합니다.")
                    else:
                        st.error("페이스메이커 연결이 실패했습니다.")
                        st.warning("블루투스를 껐다가 다시 시도해보세요.")

                if st.session_state.bundle:
                    st.session_state.pacemaker = PaceMakerCar(
                        st.session_state.default_speed, st.session_state.bundle
                    )
                    _, start_col, _, _, _, end_col, _ = st.columns(7)
                    if start_col.button("📲 시작"):
                        st.session_state.pacemaker.run()
                    if end_col.button("📴 끄기"):
                        with st.spinner("페이스메이커를 끄는 중입니다."):
                            st.session_state.pacemaker.stop()
                        st.session_state.bundle = None
                        st.success("페이스메이커가 종료되었습니다.")
                        user_db.add_user_record(st.session_state.pacemaker.user_data)

            elif task == "My Record":
                display_new_line(1)

                user_record = pd.DataFrame(
                    user_db.get_user_record(user_id),
                    columns=["id", "date", "consumed_calories", "running_distance"],
                )
                #  user_record['date'] = pd.to_datetime(user_record['date'], format='%Y-%m-%d %H:%M:%S.%f')
                #  user_record['date'] = user_record['date'].values.astype('int64')
                #  st.dataframe(user_record)
                user_record = user_record.rename(columns={"date": "index"}).set_index(
                    "index"
                )
                weight_col, running_distance_col, achievement_col = st.columns(3)
                weight_col.metric("🧑 Weight", "70 Kg", "-4Kg")
                running_distance_col.metric("🏃‍♀️ Running Distance ", "3 Km", "-1Km")
                achievement_col.metric("🏆 Achievement Rate", "86%", "4%")

                display_new_line(3)

                st.line_chart(user_record[["consumed_calories", "running_distance"]])

            elif task == "Setting":
                st.text_input("이름", user_name, disabled=True)
                new_password = st.text_input("비밀번호", type="password")
                new_height = st.text_input(
                    "키", 0 if user_height is None else user_height
                )
                new_weight = st.text_input(
                    "몸무게", 0 if user_weight is None else user_weight
                )
                if st.button("변경사항 저장하기"):
                    try:
                        if new_password:
                            user_db.modify_userdata(
                                int(new_height),
                                int(new_weight),
                                user_db.make_hashes(new_password),
                                user_id,
                            )
                        else:
                            user_db.modify_userdata(
                                int(new_height), int(new_weight), password, user_id
                            )
                        st.success("성공적으로 변경되었습니다.")
                    except:
                        st.error("잘못된 값을 넣으셨습니다. 다시 시도해주십시오.")

        else:
            st.error("잘못된 아이디/비밀번호 입니다.")
            st.warning("아직 계정이 없으면 SignUp 메뉴에서 새로운 계정을 만드세요.")

    else:
        st.warning("왼쪽 사이드바에서 로그인해주세요")


def signup_page(user_db: Type[UserDB]) -> None:
    st.subheader("새 계정 만들기")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type="password")

    if st.button("Signup"):
        user_db.create_usertable()
        user_db.add_userdata(new_user, user_db.make_hashes(new_password), None, None)
        st.success("성공적으로 계정을 생성하였습니다.")
        st.info("Login 메뉴에서 로그인하세요.")


def lab_page() -> None:
    st.subheader("​👀​🔎 Welcome to Voice Synthesis Laboratory 📢")

    display_new_line(2)

    if "processor" not in st.session_state:
        st.session_state.processor = None
    if "model" not in st.session_state:
        st.session_state.model = None
    if "mb_melgan" not in st.session_state:
        st.session_state.mb_melgan = None

    selected_langauge = st.selectbox("언어를 설정해주세요", ("ko", "en", "ch"))
    if st.button("설정"):
        with st.spinner("음성 모델을 불러오는 중입니다."):
            loop = asyncio.new_event_loop()
            (
                st.session_state.processor,
                st.session_state.model,
                st.session_state.mb_melgan,
            ) = loop.run_until_complete(load_voice_model(selected_langauge))

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
            if audio is not None:
                with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
                    sf.write(tmp.name, audio, 22050, "PCM_16", format="wav")
                    st.audio(tmp.name, format="audio/wav")


def main() -> None:
    user_db = UserDB()
    st.image("images/main_logo.png", width=300)

    with st.sidebar:
        st.image("images/sidebar_logo.png")
        sidebar_choice = option_menu(
            "",
            ["Home", "Login", "SignUp", "Lab"],
            icons=["house", "box-arrow-in-right", "plus-square", "lightbulb"],
            menu_icon="cast",
            default_index=0,
            styles={"nav-link-selected": {"background-color": "#FA5991"}},
        )

    if sidebar_choice == "Home":
        home_page()

    elif sidebar_choice == "Login":
        login_page(user_db)

    elif sidebar_choice == "SignUp":
        signup_page(user_db)

    elif sidebar_choice == "Lab":
        lab_page()


if __name__ == "__main__":
    main()
