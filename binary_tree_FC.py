def build_fractional_cascading(arrays):
    fc_data = []

    for k, arr in enumerate(arrays):
        fc_data.append([(value, k) for value in arr])

    for k in range(1, len(fc_data)): # O(k)
        prev_arr = fc_data[k - 1]
        curr_arr = fc_data[k]

        n, m = 0, 0 # O(n) is essentially O(m)
        while n < len(prev_arr) and m < len(curr_arr): # O(n)
            if prev_arr[n][0] <= curr_arr[m][0]:
                n += 1
            else:
                curr_arr[m] = (curr_arr[m][0], n)
                m += 1

        while m < len(curr_arr): # O(n)
            curr_arr[m] = (curr_arr[m][0], n)
            m += 1

    return fc_data # pre processing takes O(k*n)

class Node:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right
    
def preorder_traversal(node):
    if node is None:
        return []
    
    # Visit the current node
    result = [node.val]
    
    # Recursively traverse the left and right subtrees
    result += preorder_traversal(node.left)
    result += preorder_traversal(node.right)
    
    return result

def build_bt_fc(node):
    if node is None:
        return None
    elif node.left is None and node.right is None:
        cas_key = []
        cas_key.append([[num, 0, 0] for num in node.val])
        return Node(cas_key, None, None)
    else:
        cascaded_left = build_bt_fc(node.left)
        cascaded_right = build_bt_fc(node.right)
        left_2d_arr = [node.left.val, node.val]
        right_2d_arr = [node.right.val, node.val]
        first_pointer_arr = build_fractional_cascading(left_2d_arr)
        second_pointer_arr = build_fractional_cascading(right_2d_arr)
        cas_key = []
        for i in range(len(first_pointer_arr[1])):
            cas_key.append([first_pointer_arr[1][i][0], first_pointer_arr[1][i][1], second_pointer_arr[1][i][1]])
        return Node(cas_key, cascaded_left, cascaded_right)

leaf_left_left = Node([15, 38, 41, 67], None, None)
leaf_left_right = Node([3, 10, 29, 57], None, None)
leaf_right_left = Node([7, 12, 42, 70], None, None)
leaf_right_right = Node([6, 15, 41, 42], None, None)

branch_left = Node([5, 22, 30, 48], leaf_left_left, leaf_left_right)
branch_right = Node([11, 21, 45, 60], leaf_right_left, leaf_right_right)

root = Node([6, 34, 39, 70], branch_left, branch_right)

print("Following nodes follow preorder traversal ")
for i, arr in enumerate(preorder_traversal(build_bt_fc(root))):
    print(f"Node {i}: {arr}")