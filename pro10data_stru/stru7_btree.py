# Binary Tree (이진 트리) = 자식이 둘 이하(차수가 2이하)인 노드로 구성된 트리
# 노드 방문 방법 3가지 : pre-order(전위) - in_order(중위) - post-order (후뤼)

tree = {
    'A':['B','C'],
    'B':['D','E'],
    'C':[None, None],
    'D':[None, None],
    'E':[None, None],    
}

# 전위순회
def preOrder(node):
    if node is None:
        return 
    print(node, end=' ')
    left, right = tree[node]
    preOrder(left)  # 재귀
    preOrder(right)

print('전위 순회 결과 : ', end='')
preOrder('A')
print()

# 중위순회
def inOrder(node):
    if node is None:
        return 
    left, right = tree[node]
    inOrder(left)  # 재귀
    print(node, end=' ')
    inOrder(right)

print('중위 순회 결과 : ', end='')  # BST(Binary Search Tree) 정렬
inOrder('A')
print()

# 후위순회
def postOrder(node):
    if node is None:
        return 
    left, right = tree[node]
    postOrder(left)  # 재귀
    postOrder(right)
    print(node, end=' ')

print('후위 순회 결과 : ', end='')
postOrder('A')
print()