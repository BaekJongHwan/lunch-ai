import streamlit as st
import json
import os

# 페이지 기본 설정
st.set_page_config(page_title="역삼 정반식당 오늘의 메뉴", page_icon="🍱", layout="centered")

# 디자인 개선을 위한 CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stAlert { padding: 10px; border-radius: 10px; }
    .plus-box { background-color: #fff9db; padding: 10px; border-left: 5px solid #fab005; border-radius: 5px; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍱 역삼 정반식당 주간 식단표")
st.caption("Gemini 2.5 Flash AI가 분석한 최신 정보입니다.")
st.markdown("---")

# JSON 데이터 로드
if os.path.exists("weekly_menu.json"):
    with open("weekly_menu.json", "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            menu_list = data.get("주간_식단표") or data.get("주간식단표") or data
            
            if isinstance(menu_list, list):
                # 요일 선택 셀렉트박스
                day_names = [day.get("요일") for day in menu_list]
                selected_day_name = st.selectbox("📅 확인할 요일을 선택하세요", day_names)
                
                # 선택된 요일 데이터 매칭
                day_content = next(item for item in menu_list if item["요일"] == selected_day_name)
                menu = day_content.get("식단", {})

                # 1. 메인 점심 섹션
                st.info(f"### 🏠 {selected_day_name} 추천 점심")
                
                main_lunch = menu.get("마음까지_든_한_점심") or menu.get("마음까지_든_한점심") or []
                for dish in main_lunch:
                    st.write(f"👉 **{dish}**")
                
                # [개선] 플러스 메뉴를 메인 메뉴 바로 아래에 배치
                plus_menu = menu.get("PLUS", [])
                if plus_menu:
                    st.markdown(f"""
                        <div class="plus-box">
                            <strong>➕ 오늘의 플러스 반찬:</strong> {', '.join(plus_menu)}
                        </div>
                    """, unsafe_allow_html=True)
                
                st.divider()

                # 2. 서브 메뉴 섹션 (2열 배치)
                col1, col2 = st.columns(2)
                
                with col1:
                    st.success("🥗 프레쉬 박스")
                    fresh_box = menu.get("프레쉬_박스") or []
                    if fresh_box and fresh_box[0] != "미운영":
                        for item in fresh_box:
                            st.write(f"- {item}")
                    else:
                        st.write("오늘은 운영하지 않습니다.")
                        
                with col2:
                    st.error("💪 헬시맘 박스")
                    healthy_box = menu.get("헬시맘_박스") or []
                    if healthy_box and healthy_box[0] != "미운영":
                        for item in healthy_box:
                            st.write(f"- {item}")
                    else:
                        st.write("오늘은 운영하지 않습니다.")

            else:
                st.error("❌ 데이터 구조를 확인해주세요.")

        except Exception as e:
            st.error(f"❌ 화면 표시 중 오류 발생: {e}")
else:
    st.error("📁 weekly_menu.json 파일이 없습니다.")