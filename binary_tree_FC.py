class Node:
    def __init__(self, key, left, right):
        self.val = key
        self.left = left
        self.right = right

    def build_bst_fc(self):
        if self.left == None and self.right == None:
            tempKey = []
            for num in self.key:
                tempKey.append((num, 0, 0))
            return Node(tempKey, None, None)
        


def printPreorder(node):
    if node is not None:
        print(node.val)
        printPreorder(node.left)
        printPreorder(node.right)

leaf_left_left = Node([15, 38, 41, 67, 94], None, None)
leaf_left_right = Node([3, 10, 29, 57, 94], None, None)
leaf_right_left = Node([7, 12, 42, 70, 79], None, None)
leaf_right_right = Node([6, 15, 41, 42, 65], None, None)

branch_left = Node([5, 22, 30, 48, 81], leaf_left_left, leaf_left_right)
branch_right = Node([11, 21, 45, 60, 68], leaf_right_left, leaf_right_right)

root = Node([6, 34, 39, 70, 72], branch_left, branch_right)

print("The nodes below follows preorder traversal of the binary tree")
print(printPreorder(root))