# bubble sort : 이웃한 요소와 비교
# [2 4 5 1 3]
# [2 4 5 1 3]
# [2 4 1 5 3] # 자리 바꿈
# [2 4 1 3 5] # 자리 바꿈
# ...
def bubble_sort(a):
    n = len(a)
    while True:
        changed = False  # 자료를 앞뒤 변경 여부
        
        for i in range(0, n-1):
            if a[i] > a[i+1]:   # 앞이 뒤보다 크면
                a[i], a[i+1] = a[i+1], a[i]  # 자리 바꿈
                changed = True

        if changed == False:
            return
    
d = [2, 4, 5, 1, 3]
bubble_sort(d)
print(d)