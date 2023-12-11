class Original:
    # Representing an original item 
    def __init__(self, val, original_index, next_promoted_left, next_promoted_right):
        self.val = val
        self.original_index = original_index # this element's index in the original array
        self.next_promoted_left = next_promoted_left # pointer to the next promoted item from the left node
        self.next_promoted_right = next_promoted_right # pointer to the next promoted item from the right node

class Promoted_Left:
    # Representing an promoted item 
    def __init__(self, val, below_index, next_original, next_promoted_right):
        self.val = val
        self.below_index = below_index # a pointer down to its position in the array that it was promoted from
        self.next_original = next_original # pointer to the next original item
        self.next_promoted_right = next_promoted_right # pointer to the next promoted item from the right node

class Promoted_Right:
    # Representing an promoted item 
    def __init__(self, val, below_index, next_original, next_promoted_left):
        self.val = val
        self.below_index = below_index # a pointer down to its position in the array that it was promoted from
        self.next_original = next_original # pointer to the next original item
        self.next_promoted_left = next_promoted_left # pointer to the next promoted item from the right node   

class Node:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right
        self.search_ans = -2
    
def preorder_traversal(node):
    if node is None:
        return []
    
    # Visit the current node
    result = [node]
    
    # Recursively traverse the left and right subtrees
    result += preorder_traversal(node.left)
    result += preorder_traversal(node.right)
    
    return result

def binary_search(arr, target):
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid].val == target:
            return mid
        elif arr[mid].val < target:
            low = mid + 1
        else:
            high = mid - 1

    return low 

def print_fc_arr(node):
    ans = ""
    for i in range(len(node.val)):
        item = ""
        if isinstance(node.val[i], Original):
            item = "(Original: "+str(node.val[i].val)+", "+str(node.val[i].original_index)+", "+str(node.val[i].next_promoted_left)+", "+str(node.val[i].next_promoted_right)+"), "
        elif isinstance(node.val[i], Promoted_Left):
            item = "(Promoted Left: "+str(node.val[i].val)+", "+str(node.val[i].below_index)+", "+str(node.val[i].next_original)+", "+str(node.val[i].next_promoted_right)+"), "
        else:
            item = "(Promoted Right: "+str(node.val[i].val)+", "+str(node.val[i].below_index)+", "+str(node.val[i].next_original)+", "+str(node.val[i].next_promoted_left)+"), "
        ans += item
    return ans

def build_fractional_cascading(arrays, direction):
    fc_data = arrays

    for k in range(1, len(fc_data)): # O(k)
        prev_arr = fc_data[k - 1]
        curr_arr = fc_data[k]

        n, m = 0, 0 # O(n) is essentially O(m)
        while n < len(prev_arr) and m < len(curr_arr): # O(n)
            if prev_arr[n].val <= curr_arr[m].val:
                if n%2 != 0:
                    if direction == "left":
                        curr_arr.insert(m, Promoted_Left(prev_arr[n].val, n, -1, -1))
                    else:
                        curr_arr.insert(m, Promoted_Right(prev_arr[n].val, n, -1, -1))
                    m += 1
                n += 1
            else:
                m += 1

        while n < len(prev_arr): # O(n) to deal with the leftover
            if n%2 != 0:
                if direction == "left":
                    curr_arr.insert(m, Promoted_Left(prev_arr[n].val, n, -1, -1))
                else:
                    curr_arr.insert(m, Promoted_Right(prev_arr[n].val, n, -1, -1))
            n += 1
    return fc_data

def fixPointer(cas_key):
    # give promoted item pointer to next original item
    i = 0
    for j in range(1, len(cas_key)):
        if isinstance(cas_key[j], Original):
            while i < j:
                if not isinstance(cas_key[i], Original):
                    cas_key[i].next_original = j
                i += 1
    # give item pointer to next promoted item from left node
    i = 0
    for j in range(1, len(cas_key)):
        if isinstance(cas_key[j], Promoted_Left):
            while i < j:
                if not isinstance(cas_key[i], Promoted_Left):
                    cas_key[i].next_promoted_left = j
                i += 1
    # give item pointer to next promoted item from right node
    i = 0
    for j in range(1, len(cas_key)):
        if isinstance(cas_key[j], Promoted_Right):
            while i < j:
                if not isinstance(cas_key[i], Promoted_Right):
                    cas_key[i].next_promoted_right = j
                i += 1
    return cas_key

def build_bt_fc(node):
    cas_key = []
    if node is None:
        return None
    else:
        for i in range(len(node.val)):
            cas_key.append(Original(node.val[i], i, -1, -1))
        if node.left is None and node.right is None:
            return Node(cas_key, None, None)
        else:
            cascaded_left = build_bt_fc(node.left)
            cascaded_right = build_bt_fc(node.right)
            left_2d_arr = [cascaded_left.val, cas_key]
            cas_key = build_fractional_cascading(left_2d_arr, "left")[1]
            right_2d_arr = [cascaded_right.val, cas_key]
            cas_key = build_fractional_cascading(right_2d_arr, "right")[1]
            cas_key = fixPointer(cas_key)
            return Node(cas_key, cascaded_left, cascaded_right)
        
def bt_fc_search(node, max_len, target, pass_index):
    if node is not None:
        if pass_index == -2:
            curr_index = binary_search(node.val, target) # O(log n) but only once
        else:
            curr_index = pass_index
        if curr_index == 0:
            node.search_ans = 0
            if node.left is not None:
                bt_fc_search(node.left, max_len, target, 0)
            elif node.right is not None:
                bt_fc_search(node.right, max_len, target, 0)
        elif curr_index >= len(node.val): # if the item is bigger than the largest item in the list
            node.search_ans = max_len
            if node.left is not None:
                pass_index_left = len(node.left.val)-1
                bt_fc_search(node.left, max_len, target, pass_index_left)
            elif node.right is not None:
                pass_index_right = len(node.right.val)-1
                bt_fc_search(node.right, max_len, target, pass_index_right)
        else:
            if pass_index != -2 and node.val[curr_index-1].val >= target:
                curr_index -= 1
            curr_element = node.val[curr_index]
            if isinstance(curr_element, Original):
                node.search_ans = curr_element.original_index
                if node.left is not None:
                    if curr_element.next_promoted_left == -1:
                        pass_index_left = len(node.left.val)-1
                    else:
                        pass_index_left = node.val[curr_element.next_promoted_left].below_index
                    bt_fc_search(node.left, max_len, target, pass_index_left)
                if node.right is not None:
                    if curr_element.next_promoted_right == -1:
                        pass_index_right = len(node.right.val)-1
                    else:
                        pass_index_right = node.val[curr_element.next_promoted_right].below_index
                    bt_fc_search(node.right, max_len, target, pass_index_right)
            elif isinstance(curr_element, Promoted_Left):
                if curr_element.next_original == -1:
                    node.search_ans = max_len
                    pass_index_left = len(node.left.val)-1
                    bt_fc_search(node.left, max_len, target, pass_index_left)
                    if node.right is not None:
                        pass_index_right = len(node.right.val)-1
                        bt_fc_search(node.right, max_len, target, pass_index_right)
                else:
                    node.search_ans = node.val[curr_element.next_original].original_index
                    bt_fc_search(node.left, max_len, target, curr_element.below_index)
                    if node.right is not None:
                        if curr_element.next_promoted_right == -1:
                            bt_fc_search(node.right, max_len, target, len(node.right.val)-1)
                        else:
                            pass_index_right = node.val[curr_element.next_promoted_right].below_index
                            bt_fc_search(node.right, max_len, target, pass_index_right)
            else:
                if curr_element.next_original == -1:
                    node.search_ans = max_len
                    pass_index_right = len(node.right.val)-1
                    bt_fc_search(node.right, max_len, target, pass_index_right)
                    if node.left is not None:
                        pass_index_left = len(node.left.val)-1
                        bt_fc_search(node.left, max_len, target, pass_index_left)
                else:
                    node.search_ans = node.val[curr_element.next_original].original_index
                    bt_fc_search(node.right, max_len, target, curr_element.below_index)
                    if node.left is not None:
                        if curr_element.next_promoted_left == -1:
                            bt_fc_search(node.left, max_len, target, len(node.left.val)-1)
                        else:
                            pass_index_left = node.val[curr_element.next_promoted_left].below_index
                            bt_fc_search(node.left, max_len, target, pass_index_left)


leaf_left_left = Node([15, 38, 41, 67], None, None)
leaf_left_right = Node([3, 10, 29, 57], None, None)
leaf_right_left = Node([7, 12, 42, 70], None, None)
leaf_right_right = Node([6, 15, 41, 42], None, None)
branch_left = Node([5, 22, 30, 48], leaf_left_left, leaf_left_right)
branch_right = Node([11, 21, 45, 60], leaf_right_left, leaf_right_right)
root = Node([6, 34, 39, 70], branch_left, branch_right)

leaf_left2 = Node([2,3,10], None, None)
leaf_right2 = Node([0,5,6], None, None)
root2 = Node([1,5,7], leaf_left2, leaf_right2)

print("Following nodes follow preorder traversal ")
fc_node = build_bt_fc(root)
arr_of_nodes = preorder_traversal(fc_node)
target = 24
print(f"The target integer is {target}")
bt_fc_search(fc_node, 4, target, -2)

for i in range(len(arr_of_nodes)):
    print(f"Node {i}: {print_fc_arr(arr_of_nodes[i])} -> target should be inserted at {arr_of_nodes[i].search_ans}")