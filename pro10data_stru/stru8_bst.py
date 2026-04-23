# BST(Binary Search Tree, 이진 탐색 트리)
# 각 노드를 기준으로 left < root < right 규칙을 만족한다.
# 왼쪽 서브트리에는 현재 노드보다 작은 값,
# 오른쪽 서브트리에는 현재 노드보다 큰 값이 들어간다.
# 중위 순회(left -> root -> right)를 하면 값이 오름차순으로 출력된다.


# BST 노드 정의
class Node:
    def __init__(self, key):
        self.key = key  # 노드가 저장하는 값
        self.left = None  # 왼쪽 자식 노드
        self.right = None  # 오른쪽 자식 노드

# BST 삽입
def insert(root, key):
    # 현재 위치가 비어 있으면 새 노드를 만들어 연결한다.
    if root is None:
        return Node(key)

    # 더 작은 값은 왼쪽 서브트리에 재귀적으로 삽입한다.
    if key < root.key:
        root.left = insert(root.left, key)

    # 더 큰 값은 오른쪽 서브트리에 재귀적으로 삽입한다.
    elif key > root.key:
        root.right = insert(root.right, key)

    # 같은 값은 이 예제에서 중복 삽입하지 않고 그대로 둔다.
    return root

# 중위 순회: BST에서는 정렬된 결과를 확인할 때 자주 사용한다.
def in_order(root, result):
    if root is None:
        return result

    in_order(root.left, result)
    result.append(root.key)
    in_order(root.right, result)
    return result

values = [10, 5, 8, 3, 7, 2, 4, 6, 9, 1]
root = None

# 리스트의 값을 하나씩 넣으면서 BST를 만든다.
for v in values:
    root = insert(root, v)

# BST 정렬 결과
sorted_result = []
in_order(root, sorted_result)
print('중위 순회 결과(BST 정렬) : ', sorted_result)
