def update_values(dict_A_b, dict_A, constant):
    for key, value_b in dict_A_b.items():
        # 이전 상태의 밸류 리스트와 현재 상태의 밸류 리스트
        value = dict_A[key]
        
        # 이전 상태의 평균값 계산
        average_b = (value_b[1] + value_b[3]) / 2
        # 현재 상태의 평균값 계산
        average = (value[1] + value[3]) / 2
        
        # 이전 상태의 평균값이 20을 넘지 않다가 현재 상태에서 넘게 되면
        if average_b < 20 and average > 20:
            # 밸류 리스트에 1을 추가
            value.append(1)
            # 상수에 1을 더함
            constant += 1
            print(f"평균값이 20을 넘는 키 {key} 발견! 상수 {constant}에 1을 더하고 리스트에 1을 추가합니다.")

    return constant

# 예시 딕셔너리 A의 이전 상태
A_b = {1: [10, 15, 17, 18], 2: [20, 15, 23, 22], 3: [25, 30, 30, 30]}
# 예시 딕셔너리 A의 현재 상태
A = {1: [10, 15, 25, 18], 2: [20, 25, 23, 22], 3: [25, 30, 30, 30]}
# 예시 상수 초기값
my_constant = 0

# 함수 호출하여 평균값이 20을 넘는 경우 상수 업데이트 및 리스트에 1 추가
my_constant = update_values(A_b, A, my_constant)
print("업데이트된 상수:", my_constant)
print("업데이트된 딕셔너리 A:", A)
