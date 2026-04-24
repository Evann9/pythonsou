# Heap : 모든 Node가 특정한 순서를 유지하며 구성된 완전 이진트리 형태의 자료 구조
# 내부 구현 없이 Heap 개념 이해

import heapq  # 기본이 Min Heap

# Min Heap
heap = []
heapq.heappush(heap, 30)
heapq.heappush(heap, 10)
heapq.heappush(heap, 20)
print('현재 힙 상태 : ', heap)  # 내부적으로 힙 구조가 유지

# 최소값 꺼내기
print('가장 작은 값 : ', heapq.heappop(heap))
print('가장 작은 값 : ', heapq.heappop(heap))
print('현재 힙 상태 : ', heap)

# Max heap
heap = []
heapq.heappush(heap, -30)
heapq.heappush(heap, -10)
heapq.heappush(heap, -20)
print('현재 힙 상태 : ', heap)  # 내부적으로 힙 구조가 유지

# 최대값 꺼내기
print('가장 큰 값 : ', -heapq.heappop(heap))
print('가장 큰 값 : ', -heapq.heappop(heap))
print('현재 힙 상태 : ', heap)