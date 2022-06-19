import asyncio
from typing import Type

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

from database import UserDB
from pacemaker import PaceMakerCar
from utils.streamlit_display_functions import display_new_line


def login_page(user_db: Type[UserDB]):
    """
    stremalit sidebar에서 메뉴에서 "Login" 버튼을 클릭할 시 나타나는 페이지

    - Login 체크박스 누를 시
        - 로그인 정보가 올바른 경우: 페이스메이커 작동, 내 기록보기, 내 정보 변경 기능 활성화
        - 로그인 정보가 올바르지 않은 경우: 로그인 실패 알림 메시지 표시
    - Login 체크박스 누르지 않은 경우
        - 로그인 시도 알림 메시지 표시

    Args:
        user_db (UserDB): 유저 데이터 베이스

    """

    # 유저 네임과 비밀번호를 로그인 정보로 받음
    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password", type="password")

    # 로그인 체크박스를 누를 시에 해당 로그인 정보로 로그인 시도
    if st.sidebar.checkbox("Login"):

        # usertable 또는 recordtable이 없는 경우 테이블 생성
        user_db.create_usertable()
        user_db.create_recordtable()

        # 받은 로그인 정보를 바탕으로 usertable에서 유저 정보를 찾음
        hashed_password = user_db.make_hashes(password)
        login_user_data = user_db.login_user(
            username, user_db.check_hashes(password, hashed_password)
        )

        # 로그인 정보가 존재하여 유저 계정이 있는 것이 확인될 경우 3가지 task를 할 수 있는 페이지로 이동
        if login_user_data:
            (
                user_id,
                user_name,
                password,
                user_height,
                user_weight,
            ) = login_user_data[0]

            # Pacemaker, My Record, Setting 중에 메뉴 선택
            task = option_menu(
                None,
                ["Pacemaker", "My Record", "Setting"],
                icons=["robot", "clipboard-data", "gear"],
                menu_icon="cast",
                default_index=0,
                orientation="horizontal",
                styles={"nav-link-selected": {"background-color": "#FA5991"}},
            )

            # Pacemaker 선택 시
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

                # 페이스메이커 기본 속도 설정
                if "default_speed" not in st.session_state:
                    st.session_state.default_speed = None
                st.text("1️⃣ 기본 속도를 입력해주세요")
                st.session_state.default_speed = st.slider("", 0, 100, 60)

                display_new_line(1)

                # 페이스메이커 모드 설정
                st.text("2️⃣ 모드를 선택해주세요")
                selected_mode = st.selectbox("", ("쉬운 모드", "보통 모드", "힘든 모드"), index=1)

                display_new_line(1)

                # streamlit 세션이 재구동되어도 유지되어야 하는 변수 초기화
                if "bundle" not in st.session_state:
                    st.session_state.bundle = None
                if "pacemaker" not in st.session_state:
                    st.session_state.pacemaker = None
                if "processor" not in st.session_state:
                    st.session_state.processor = None
                if "model" not in st.session_state:
                    st.session_state.model = None
                if "mb_melgan" not in st.session_state:
                    st.session_state.mb_melgan = None

                # 기본 속도 및 모드 설정 저장 및 페이스메이커 연결
                _, load_col, _ = st.columns(3)
                if load_col.button("💾 설정 저장 및 연결하기"):
                    with st.spinner("페이스메이커에 연결하는 중입니다."):
                        loop = asyncio.new_event_loop()
                        st.session_state.bundle = loop.run_until_complete(
                            PaceMakerCar.load_modi()
                        )
                    if st.session_state.bundle:
                        st.success("페이스메이커에 성공적으로 연결되었습니다.")
                    else:
                        st.error("페이스메이커 연결이 실패했습니다.")
                        st.warning("연결을 해제하고 재연결 후 다시 시도해보세요.")

                # 연결 성공 시 페이스메이커 동작 시작 또는 끄기 버튼 활성화
                if st.session_state.bundle:
                    st.session_state.pacemaker = PaceMakerCar(
                        user_id,
                        st.session_state.default_speed,
                        st.session_state.bundle,
                    )
                    st.info("시작을 누르면 페이스메이커를 작동합니다.")
                    _, start_col, _, _, _, end_col, _ = st.columns(7)
                    if start_col.button("📲 시작"):
                        st.session_state.pacemaker.run()
                    if end_col.button("📴 끄기"):
                        with st.spinner("페이스메이커를 끄는 중입니다."):
                            st.session_state.pacemaker.stop()
                        st.session_state.bundle = None
                        st.success("페이스메이커가 종료되었습니다.")
                        user_db.add_user_record(st.session_state.pacemaker.user_data)

            # 유저 기록
            elif task == "My Record":
                st.info("다음 분석 정보는 데모용 데이터입니다.")
                display_new_line(1)

                user_record = pd.DataFrame(
                    user_db.get_user_record(user_id),
                    columns=["id", "date", "consumed_calories", "running_distance"],
                )
                user_record = pd.read_csv(
                    "../demo_data/user_record.csv",
                    usecols=["id", "date", "consumed_calories", "running_distance"],
                    index_col=0,
                )

                user_record = user_record.rename(columns={"date": "index"}).set_index(
                    "index"
                )
                weight_col, running_distance_col, achievement_col = st.columns(3)
                weight_col.metric("🧑 Weight", "70 Kg", "-4Kg")
                running_distance_col.metric("🏃‍♀️ Running Distance ", "3 Km", "-1Km")
                achievement_col.metric("🏆 Achievement Rate", "86%", "4%")

                display_new_line(3)

                st.line_chart(user_record[["consumed_calories", "running_distance"]])

            # 유저 정보 변경
            elif task == "Setting":
                # 유저 데이터에서 기존 정보를 불러오고, 해당 정보를 보여주는 칸에 수정 후 저장 시 정보 변경 가능, 이름은 변경 불가능.
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

        # 로그인 정보가 존재하지 않아 유저 계정이 있는 것이 확인되지 않을 경우
        else:
            st.error("잘못된 아이디/비밀번호 입니다.")
            st.warning("아직 계정이 없으면 SignUp 메뉴에서 새로운 계정을 만드세요.")

    # 로그인 체크박스를 누르지 않은 경우
    else:
        st.warning("왼쪽 사이드바에서 로그인해주세요")
