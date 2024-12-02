import streamlit as st
import random
from data import food_korean, food_Japanese, food_Chinese, food_etc


# 사용자 정보 입력 함수 / streamlit(st.)를 이용한 UI구현
def get_user_info():
    age = st.number_input("나이를 입력하세요 (1~99):", min_value=1, max_value=99)
    weight = st.number_input(
        "몸무게를 입력하세요 (kg) (10~200 kg):",
        min_value=10.0,
        max_value=200.0,
        step=0.1,
    )
    height = st.number_input(
        "키를 입력하세요 (cm):", min_value=50.0, max_value=250.0, step=0.1
    )
    gender = st.selectbox("성별을 선택하세요:", options=["남", "여"])
    return age, weight, height, gender


# BMR 계산 함수
def calculate_bmr(age, weight, height, gender):
    if gender == "남":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender == "여":
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr


# 칼로리가 최소인 음식 검색 함수
def find_min_cal_item(items_list):
    lowest_cal_item = items_list[0]

    for item in items_list:
        if item[2] < lowest_cal_item[2]:
            lowest_cal_item = item

    return lowest_cal_item


# 0-1 Knapsack 문제를 이용한 최대 단백질 섭취 계산
def max_protein_intake(calories, items):
    items_list = [
        (name, details["protein"], details["calories"], details["restaurant"])
        for name, details in items.items()
    ]

    n = len(items_list)
    dp = [[0] * (calories + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        name, protein, cal, restaurant = items_list[i - 1]
        for j in range(calories + 1):
            if cal <= j:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - cal] + protein)
            else:
                dp[i][j] = dp[i - 1][j]

    # 선택한 음식 추적
    selected_items = []
    j = calories
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i - 1][j]:  # i번째 아이템이 선택되었으면
            name, protein, cal, restaurant = items_list[i - 1]
            selected_items.append((name, restaurant))
            j -= cal  # 남은 칼로리 줄이기

    if dp[n][calories] == 0:  # 조건을 만족하는 음식이 없으면
        lowest_cal_item = find_min_cal_item(
            items_list
        )  # 카테고리 중 가장 칼로리가 낮은 음식 리턴
        return lowest_cal_item[1], [(lowest_cal_item[0], lowest_cal_item[3])]

    else:
        return dp[n][calories], selected_items


# 음식 카테고리 랜덤 선택 함수
def select_food_category():
    food_types = ["한식", "일식", "중식", "기타"]
    selected_category = random.choice(food_types)
    if selected_category == "한식":
        return selected_category, food_korean
    elif selected_category == "일식":
        return selected_category, food_Japanese
    elif selected_category == "중식":
        return selected_category, food_Chinese
    else:
        return selected_category, food_etc


# 실행 함수
def main():
    st.title("하루 식단 추천 앱")

    # form 생성
    with st.form(key="user_info_form"):
        st.header("사용자 정보 입력")
        age, weight, height, gender = get_user_info()

        st.header("목표 설정")
        goal = st.selectbox("목표를 선택하세요:", options=["다이어트", "벌크업"])

        submit_button = st.form_submit_button(label="계산하기")

    if submit_button:
        # BMR 계산
        bmr = int(round(calculate_bmr(age, weight, height, gender), 0))

        if bmr > 3000:
            st.error("BMR이 상한값을 초과했습니다. 정보를 다시 입력해주세요.")
            return

        # 칼로리 목표 설정
        if goal == "다이어트":
            calorie_goal = int(max(1200, bmr - 200))
        elif goal == "벌크업":
            calorie_goal = int(min(3000, bmr + 200))

        st.info(f"사용자의 하루 목표 칼로리: {calorie_goal} kcal")

        # 아침, 점심, 저녁 시간대와 각 시간대별 칼로리 (비율=2:3:3)
        time_slots = ["아침", "점심", "저녁"]
        time_kcal = [
            (calorie_goal * 2) // 8,
            (calorie_goal * 3) // 8,
            (calorie_goal * 3) // 8,
        ]

        st.header("식사별 추천 메뉴")
        for i in range(3):
            with st.expander(f"{time_slots[i]} 식사: {time_kcal[i]} kcal"):
                st.write(f"**{time_slots[i]} 식사: {time_kcal[i]} kcal**")

                # 음식 카테고리 랜덤 선택
                food_category, food_items = select_food_category()
                st.write(f"선택된 음식 카테고리: **{food_category}**")

                # 최대 단백질 섭취량과 그에 따른 메뉴 계산
                max_protein, food_list = max_protein_intake(time_kcal[i], food_items)

                # 출력
                st.write(f"**최대 단백질 섭취량:** {max_protein}g")
                st.write("**선택된 음식 메뉴:**")
                for item in food_list:
                    st.write(f"- {item[0]} ({item[1]})")
                st.write("---")


if __name__ == "__main__":
    main()
