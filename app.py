import streamlit as st

# 페이지 설정
st.set_page_config(page_title="Google 검색 및 제품 카탈로그", page_icon="🔍", layout="centered")

# 상단 이미지 (Google 로고)
st.image("https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png", width=300)

# 검색 입력창
query = st.text_input("Google 검색 또는 URL 입력", "")

# 검색 버튼
if st.button("Google 검색"):
    st.write(f"'{query}'에 대한 검색을 시도 중입니다...")

# 제품 카테고리 탭 설정
categories = ['세라제류', '세정제류', '살균제류, 세정제류']
tab1, tab2, tab3 = st.tabs(categories)

with tab1:
    # st.header("세라제류")
    sub_categories = ['자동차용', '가정용']
    sub_tab1, sub_tab2 = st.tabs(sub_categories)

    with sub_tab1:
        # st.subheader("자동차용 세라제류")
        auto_products = ['세라믹 코트', '글라스 코팅', '바닥 왁스', '자동차 코팅제', '보호 필름']
        for product in auto_products:
            st.write(f"- {product}")

    with sub_tab2:
        # st.subheader("가정용 세라제류")
        home_products = ['방수 스프레이', '가구 왁스', '바닥 광택제', '욕실용 코팅제', '키친 탑 코팅']
        for product in home_products:
            st.write(f"- {product}")

with tab2:
    # st.header("세정제류")
    sub_categories = ['자동차용', '가정용']
    sub_tab1, sub_tab2 = st.tabs(sub_categories)

    with sub_tab1:
        # st.subheader("자동차용 세라제류")
        auto_products = ['세라믹 코트', '글라스 코팅', '바닥 왁스', '자동차 코팅제', '보호 필름']
        for product in auto_products:
            st.write(f"- {product}")

    with sub_tab2:
        # st.subheader("가정용 세라제류")
        home_products = ['방수 스프레이', '가구 왁스', '바닥 광택제', '욕실용 코팅제', '키친 탑 코팅']
        for product in home_products:
            st.write(f"- {product}")

with tab3:
    # st.header("살균제류, 세정제류")
    sub_categories = ['자동차용', '가정용']
    sub_tab1, sub_tab2 = st.tabs(sub_categories)

    with sub_tab1:
        # st.subheader("자동차용 세라제류")
        auto_products = ['세라믹 코트', '글라스 코팅', '바닥 왁스', '자동차 코팅제', '보호 필름']
        for product in auto_products:
            st.write(f"- {product}")

    with sub_tab2:
        # st.subheader("가정용 세라제류")
        home_products = ['방수 스프레이', '가구 왁스', '바닥 광택제', '욕실용 코팅제', '키친 탑 코팅']
        for product in home_products:
            st.write(f"- {product}")
# 실행 방법 안내
st.info("터미널에서 'streamlit run app.py' 명령어로 실행하세요.")
