import streamlit as st
from playsound import playsound
from streamlit_option_menu import option_menu

from database import UserDB
from streamlit_pages import home_page, lab_page, login_page, signup_page
from utils.streamlit_display_functions import display_new_line


def main() -> None:
    """
    stremalit sidebar에서 메뉴 설정 시 해당 메뉴에 해당하는 페이지 화면으로 전환

        - Home: 메인 화면
        - Login: 로그인창이 사이드바에 나타나며 로그인 성공 시 개인 유저 페이지로 이동
        - SignUp: 계정 생성 화면
        - Lab: 음성 합성을 체험해볼 수 있는 화면

    """
    # 데이터 베이스 불러오기
    user_db = UserDB()
    st.image("images/main_logo.png", width=300)

    # 사이드바 옵션 메뉴
    with st.sidebar:
        st.image("images/sidebar_logo.png")
        sidebar_choice = option_menu(
            "",
            ["Home", "Login", "SignUp", "Lab"],
            icons=["house", "box-arrow-in-right", "plus-square", "lightbulb"],
            menu_icon="cast",
            default_index=0,
            styles={"nav-link-selected": {"background-color": "#4487DC"}},
        )

    if sidebar_choice == "Home":
        home_page.home_page()

    elif sidebar_choice == "Login":
        login_page.login_page(user_db)

    elif sidebar_choice == "SignUp":
        signup_page.signup_page(user_db)

    elif sidebar_choice == "Lab":
        lab_page.lab_page()


if __name__ == "__main__":
    main()
