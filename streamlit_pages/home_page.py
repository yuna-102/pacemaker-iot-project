import streamlit as st

from utils.streamlit_display_functions import display_new_line


# 메인화면 페이지
def home_page() -> None:
    banner_col1, banner_col2 = st.columns([2, 3])
    # 메인화면 상단 배너
    with banner_col1:
        display_new_line(3)

        st.subheader("Get Pace Get Healthy!")
        st.markdown(
            '<p style="font-family:Courier; color:black; font-size: 15px;">Kickstart Your Health <br> With Pacemaker <br> Pace Your Workouts!</p>',
            unsafe_allow_html=True,
        )

    with banner_col2:
        st.image("images/home_banner.png")

    display_new_line(3)

    st.markdown(
        "<h3 style='color: #4487DC;'>what is Pacemaker?</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<SPAN style='color: #4487DC; text-decoration:overline; '>ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ</SPAN>",
        unsafe_allow_html=True,
    )

    display_new_line(1)

    # 페이스메이커 소개
    icon_col1, _, icon_col2, _, icon_col3 = st.columns(5)
    with icon_col1:
        st.image("images/home_running_icon.png")
        st.markdown(
            "<p style='text-align: center; color: black;'>러닝 보조</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align: center; color: black;font-size: 10px;'>페이스 메이커 로봇을 따라 <br> 트랙을 달려보세요.</p>",
            unsafe_allow_html=True,
        )

    with icon_col2:
        st.image("images/home_sound_icon.png")
        st.markdown(
            "<p style='text-align: center; color: black;'>음성 코치</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align: center; color: black;font-size: 10px;'>음성 서비스를 통해 <br> 동기부여를 얻으세요.</p>",
            unsafe_allow_html=True,
        )

    with icon_col3:
        st.image("images/home_report_icon.png")
        st.markdown(
            "<p style='text-align: center; color: black;'>개인 기록 관리</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align: center; color: black;font-size: 10px;'> 페이스 메이커와 함께한 운동 <br> 기록을 관리하세요.</p>",
            unsafe_allow_html=True,
        )

    display_new_line(6)

    # 데모 비디오
    st.markdown("<h3 style='color: #4487DC;'>Demo Video</h3>", unsafe_allow_html=True)
    st.markdown(
        "<SPAN style='color: #4487DC; text-decoration:overline; '>ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ</SPAN>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p style="font-family:"Gill sans"; color:black; font-size: 15px;"> 😃 Demo Video will be uploaded soon! </p>',
        unsafe_allow_html=True,
    )

    st.image("images/home_video_player_image.png")
