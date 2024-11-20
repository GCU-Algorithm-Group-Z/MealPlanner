from data import food_korean, food_Japanese, food_Chinese, food_etc
import random

# 사용자 정보 입력 함수
def get_user_info():
    while True:
        try:
            age = int(input("나이를 입력하세요 (1~99): "))
            print(f"입력된 나이: {age}")  # 디버깅용 메시지
            if not (1 <= age <= 99):
                print("나이가 범위를 벗어났습니다. 재측정 후 다시 입력해주세요.")
                continue
            
            weight = float(input("몸무게를 입력하세요 (10~200 kg): "))
            print(f"입력된 몸무게: {weight}")  # 디버깅용 메시지
            if not (10 <= weight <= 200):
                print("몸무게가 범위를 벗어났습니다. 재측정 후 다시 입력해주세요.")
                continue

            height = float(input("키를 입력하세요 (cm): "))
            print(f"입력된 키: {height}")  # 디버깅용 메시지
            gender = input("성별을 입력하세요 (남/여): ")
            print(f"입력된 성별: {gender}")  # 디버깅용 메시지
            if gender not in ["남", "여"]:
                print("성별은 '남' 또는 '여'로만 입력해주세요.")
                continue

            return age, weight, height, gender
        except ValueError:
            print("유효한 숫자를 입력해주세요.")

# BMR 계산 함수
def calculate_bmr(age, weight, height, gender):
    if gender == "남":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender == "여":
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr

# 칼로리 목표 설정 함수
def set_calorie_goal(bmr):
    while(1):
        goal = input("목표를 입력하세요 (다이어트/벌크업): ")
        if goal == "다이어트":
            return int(max(1200, bmr - 200))  # 다이어트 목표는 최소 1200 이상 유지하고, 정수로 변환
        elif goal == "벌크업":
            return int(min(3000, bmr + 200))  # 최대 3000 이하 유지하고, 정수로 변환
        else:
            print("유효한 목표를 입력해주세요.")
            continue

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
            selected_items.append((name,restaurant))
            j -= cal  # 남은 칼로리 줄이기

    if dp[n][calories] == 0: # 조건을 만족하는 음식이 없으면 
        lowest_cal_item = find_min_cal_item(items_list) #카테고리 중 가장 칼로리가 낮은 음식 리턴
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

# 실행 함수 예시
def main():

    while (1):
        age, weight, height, gender = get_user_info()
        bmr = int(round(calculate_bmr(age, weight, height, gender),0))
        if bmr > 3000:
            print("BMR이 상한값을 초과했습니다. 정보를 다시 입력해주세요.")
            continue
        else:
            break

    print(f"사용자 정보: 나이={age}, 몸무게={weight}, 키={height}, 성별={gender}, BMR={bmr}")

    calorie_goal = set_calorie_goal(bmr)
    print(f"사용자의 하루 목표 칼로리: {calorie_goal} kcal")

    #아침, 점심, 저녁 시간대와 각 시간대별 칼로리 (비율=2:3:3)
    time = ['아침', '점심', '저녁'] 
    time_kcal = [(calorie_goal * 2 ) // 8, (calorie_goal * 3 ) // 8, (calorie_goal * 3 ) // 8]

    #최대 단백질 섭취량과 그에 따른 메뉴 계산
    print("-----------------")
    for i in range(3):
        print(f"{time[i]} 식사: {time_kcal[i]}칼로리")
        #음식 카테고리 랜덤 선택
        food_category, food_items = select_food_category()
        print(f"선택된 음식 카테고리: {food_category}")
        max_protein , food_list= max_protein_intake(time_kcal[i], food_items)
        #출력
        print(f"최대 단백질 섭취량: {max_protein}g")
        print(f"선택된 음식 메뉴: {food_list}")
        print("-----------------")

#실행
main()