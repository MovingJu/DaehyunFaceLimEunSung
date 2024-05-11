def replace_values(dict_A, list_B, error=3):
    # A에 있는 키들의 집합
    keys_A = set(dict_A.keys())
    
    # A에 없는 키를 위한 새로운 키 값
    new_key = max(keys_A) + 1 if keys_A else 1
    
    # B의 원소를 하나씩 검사
    for value_B in list_B:
        # B의 원소와 A의 각 값 비교
        for key, value_A in dict_A.items():
            for i in range(len(value_A)):
                if abs(value_A[i] - value_B[i]) > error:
                    break
            else:  # 오차 범위 내에 있으면 해당 값을 대체하고 종료
                dict_A[key] = value_B
                break
        else:  # 오차 범위 내에 없는 경우 새로운 키와 함께 추가
            dict_A[new_key] = value_B
            new_key += 1

# 예시 딕셔너리와 리스트
A = {}
B = [[2, 3, 4, 5], [6, 7, 8, 9], [13, 14, 15, 16], [17,18,19,20]]

# 함수 호출하여 딕셔너리의 값을 리스트로 대체 및 추가
replace_values(A, B)

print("변경된 딕셔너리 A:", A)
