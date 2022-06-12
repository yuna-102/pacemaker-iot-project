from typing import Type

import streamlit as st

from database import UserDB


# 새로운 계정 생성 페이지
def signup_page(user_db: Type[UserDB]) -> None:
    st.subheader("새 계정 만들기")

    # 새로운 계정 생성을 위한 유저 이름 및 비밀번호 입력
    new_username = st.text_input("이름")
    new_password = st.text_input("비밀번호", type="password")

    # Signup 버튼 클릭 시 계정 생성
    if st.button("Signup"):
        # usertable이 존재하지 않을 시 생성
        user_db.create_usertable()

        # 유저이름이 이미 존재하지 않는 경우에 계정 생성
        if not user_db.check_if_username_exits(new_username):
            # usertable에 새로운 계정의 데이터 추가
            user_db.add_userdata(
                new_username, user_db.make_hashes(new_password), None, None
            )
            st.success("성공적으로 계정을 생성하였습니다.")
            st.info("Login 메뉴에서 로그인하세요.")
        else:
            st.error("이미 존재하는 계정입니다.")
            st.info("다른 아이디로 가입하세요.")
