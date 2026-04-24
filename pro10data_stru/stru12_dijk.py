# pdf 내용 코드로 구현
import heapq
INF = int(1e9)

# 그래프 (인접 리스트 방식) - (노드번호, 비용) 형태로
graph = [
    [(1,2),(2,5),(3,1)],  # 1번 노드 (2번, 2), (3번, 5)
    [(0,2),(2,3),(3,2)],  # 2번 노드
    [(0,5),(1,3),(3,3),(4,1),(5,5)],
    [(0,1),(1,2),(2,3),(4,1)],
    [(2,1),(3,1),(5,2)],
    [(2,5),(4,2)],
]

n = 6  # 노드 갯수
distance = [INF] * n  # 최단 거리 배열 초기화

def dijkstraFunc(start):
    pq = []
    heapq.heappush(pq,(0,start))
    distance[start] = 0
    while pq:
        dist, now = heapq.heappop(pq)

        if distance[now] < dist:
            continue

        for next_node, cost in graph[now]:
            new_cost = dist + cost

            if new_cost < distance[next_node]:
                distance[next_node] = new_cost
                heapq.heappush(pq, (new_cost, next_node))




dijkstraFunc(0)

# 각 노드까지의 최단 거리
for i in range(n):
    print(f"{i}번 노드까지의 최단 거리 : {distance[i]}")
