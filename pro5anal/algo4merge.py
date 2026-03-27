# 리스트 안에 들어있는 자료를 오름차순 정렬
# 3) 병합(merge) 정렬
# 리스트 자료를 반으로 나눔. 요소가 1개씩 남을 때 까지 반복
# 분할된 리스트를 정렬하며 하나로 합친다(정렬 상태 유지)

# 방법1 : 이해 위주
def merge_sort(a):
    n = len(a) # 리스트의 길이를 구함
    if n <= 1: # 종료 조건: 리스트의 요소가 1개 이하면 이미 정렬된 상태
        return a
    
    mid = n // 2   # 중간을 기준으로 두 그룹으로 분할
    # 함수는 독립적인 공간을 가짐. 아래의 g1, g2는 서로 간섭 안함.
    g1 = merge_sort(a[:mid])   # 왼쪽 그룹 분할 (재귀 호출)
    print('g1 : ', g1)
    g2 = merge_sort(a[mid:])   # 오른쪽 그룹 분할 (재귀 호출)
    print('g2 : ', g2)

    # 두 그룹을 병합하며 정렬
    result = []
    while g1 and g2: # 두 그룹에 모두 요소가 남아있는 동안 반복
        print(g1[0], ' ', g2[0])
        if g1[0] < g2[0]: # 더 작은 값을 결과 리스트에 추가
            result.append(g1.pop(0))
        else:
            result.append(g2.pop(0))
        print('result : ', result)

    # 한쪽 그룹이 소진된 후 남은 요소들을 결과 리스트에 추가
    while g1: # g1에 남은 요소가 있다면 추가
        result.append(g1.pop(0))
    while g2: # g2에 남은 요소가 있다면 추가
        result.append(g2.pop(0))

    return result # 병합된 리스트 반환

d = [6, 8, 3, 1, 2, 4, 7, 5]
print(merge_sort(d))

print()
# 방법2 : 일반 알고리즘
# 재귀 호출이 정렬된 리스트를 반환.
# 병합도 새 리스트를 만들어 반환.
# 원본 리스트는 그대로이고 정렬된 결과는 새 리스트에 저장.
def merge_sort2(a):
    if len(a) <= 1: # 종료 조건
        return a
    
    mid = len(a) // 2 # 중간 지점 계산
    left = merge_sort2(a[:mid]) # 왼쪽 분할
    right = merge_sort2(a[mid:]) # 오른쪽 분할

    result = [] # 병합 결과를 담을 리스트
    i = 0
    j = 0
    while i < len(left) and j < len(right): # 인덱스를 사용하여 비교 및 병합
        if left[i] < right[j]: # 왼쪽 요소가 작으면 추가
            result.append(left[i])
            i += 1
        else: # 오른쪽 요소가 작으면 추가
            result.append(right[j])
            j += 1
    
    # 슬라이싱을 이용해 남은 요소들을 한꺼번에 추가
    result += left[i:] 
    result += right[j:]
    return result

d = [6, 8, 3, 1, 2, 4, 7, 5]
sorted_d = merge_sort2(d)
print('일반 알고리즘 : ', sorted_d)