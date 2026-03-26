# 리스트 안에 들어있는 자료를 오름차순 정렬 
# 2) 삽입(insertion) 정렬  -  앞에서 부터 하나씩 꺼내서, 자기자리 찾아 끼워넣는 정렬
# 방법1 : 이해 위주
def find_ins_idx(r, v):
    # 이미 정렬된 리스트 r에서 v가 들어갈 적절한 위치 인덱스를 찾는 함수
    for i in range(0, len(r)):
        # v 값이 i번 위치 값보다 작으면
        if v < r[i]:
            return i
    # 적정한 삽입 위치를 못 찾은 경우 맨 뒤에 삽입
    return len(r)

def ins_sort(a):
    # 리스트 a의 요소를 하나씩 꺼내어 새로운 리스트 result의 적절한 위치에 삽입하는 정렬
    result = []
    while a:
        value = a.pop(0)
        ins_idx = find_ins_idx(result, value) 
        result.insert(ins_idx, value)

    return result

d = [2,4,5,1,3]
print('연습용 : ',ins_sort(d))

print()
# 방법2 : 일반 알고리즘
def ins_sort2(a):
    # 별도의 리스트 생성 없이 원본 리스트 내에서 요소를 뒤로 밀어내며 자리를 찾아가는 방식
    n = len(a)
    # 두번째 값(인덱스 1)부터 마지막까지 차례대로 '삽입할 대상'을 선택
    for i in range(1, n):
        key = a[i]
        j = i - 1
        # key보다 큰 데이터를 오른쪽으로 한 칸씩 밀어냄
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]  # 삽입할 공간이 생기도록 값을 우측으로 밀기
            j -= 1   # 그 다음 왼쪽으로 이동하면서 다시 비교
        a[j + 1] = key # 찾은 삽입 위치에 key를 저장
    return a

d = [2, 4, 5, 1, 3]
print('일반 알고리즘 : ', ins_sort2(d))
