# Graph : Node(vertex)와 Edge의 집합으로 이루어진 자료구조

# Tree : 계층구조, Root 있음, 사이클(순환) 없음, 항상 연결
# Graph : 일반 네트워크 구조, Root 없음, 사이클(순환) 있음, 연결/비연결 모두 가능

graph = {
    'A':('B','C'),
    'B':('D','E'),
    'C':('F'),
    'D':(),
    'E':(),
    'F':(),
}

# DFS - 깊이 우선 탐색 방식 - 재귀함수 또는 스텍으로 구현
def dfsFunc(graph, start, visited):
    visited.append(start)
    for next_node in graph[start]:
        if next_node not in visited:
            dfsFunc(graph, next_node, visited)

visited_dfs = []
dfsFunc(graph, 'A', visited_dfs)
print('DFS 방문 순서 : ', visited_dfs)
# A -> B -> D -> (끝) -> E -> (끝) -> C -> F  : 방문 즉시 아래로 내려감. 재귀(call stack)

# BFS - 너비 우선 탐색 방식 - 큐로 구현
from collections import deque

def bfsFunc(graph, start):
    visited = []
    visited.append(start)
    queue = deque([start])  # 큐 사용(FIFO)
    while queue:
        node = queue.popleft()
        for next_node in graph[node]:
            if next_node not in visited:
                visited.append(next_node)
                queue.append(next_node)
    return visited


visited_bfs = bfsFunc(graph, 'A')
print('BFS 방문 순서 : ', visited_bfs)
# A -> B, C -> D, E ,F 방문 즉시 큐에 쌓고 먼저 들어온 것부터 처리(거리 <레벨> 개념이 생김)
