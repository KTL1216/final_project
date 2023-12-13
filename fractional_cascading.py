class Original:
    # Representing an original item 
    def __init__(self, val, original_index, next_promoted):
        self.val = val
        self.original_index = original_index # this element's index in the original array
        self.next_promoted = next_promoted # pointer to the next promoted item

class Promoted:
    # Representing an promoted item 
    def __init__(self, val, below_index, next_original):
        self.val = val
        self.below_index = below_index # a pointer down to its position in the array that it was promoted from
        self.next_original = next_original # pointer to the next original item

def build_fractional_cascading(arrays):
    fc_data = []

    for arr in arrays:
        curr_arr = []
        for n in range(len(arr)): # O(k) * O(n)
            curr_arr.append(Original(arr[n], n, -1))
        fc_data.append(curr_arr)

    for k in range(1, len(fc_data)): # O(k)
        prev_arr = fc_data[k - 1]
        curr_arr = fc_data[k]

        n, m = 0, 0 # O(n) is essentially O(m)
        while n < len(prev_arr) and m < len(curr_arr): # O(n)
            if prev_arr[n].val <= curr_arr[m].val:
                if n%2 != 0:
                    curr_arr.insert(m, Promoted(prev_arr[n].val, n, -1))
                    m += 1
                n += 1
            else:
                m += 1

        while n < len(prev_arr): # O(n) to deal with the leftover
            if n%2 != 0:
                curr_arr.append(Promoted(prev_arr[n].val, n, -1))
            n += 1

        # adjust the pointer to point to the next different type
        i = 0
        prev_type = type(fc_data[k][i])

        for j in range(1, len(fc_data[k])):
            if not isinstance(fc_data[k][j], prev_type):
                while i < j:
                    if isinstance(fc_data[k][j], Original):
                        fc_data[k][i].next_original = j
                    else:
                        fc_data[k][i].next_promoted = j
                    i += 1
            prev_type = type(fc_data[k][i])
    return fc_data

def print_fc_arr(arr_num, arr):
    ans = "Array "+str(arr_num)+": "
    for i in range(len(arr)):
        item = ""
        if isinstance(arr[i], Original):
            item = "(Original item: "+str(arr[i].val)+", "+str(arr[i].original_index)+", "+str(arr[i].next_promoted)+"), "
        elif isinstance(arr[i], Promoted):
            item = "(Promoted item: "+str(arr[i].val)+", "+str(arr[i].below_index)+", "+str(arr[i].next_original)+"), "
        ans += item
    print(ans)

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

def contextualize(fc_data, ans, target):
    print("Target value:", target)
    print(f"Answer array format: {ans}")
    for k in range(len(ans)-1, -1, -1):
        if ans[k][0]:
            print(f"For array {k}: target with value {target} is found at index {ans[k][1]}")
        else:
            print(f"For array {k}: target with value {target} should be inserted at index {ans[k][1]}")


def fc_search(fc_data, target):
    if fc_data is None:
        return None
    if len(fc_data) == 1:
        return [binary_search(fc_data[0], target)]
    max_len = len(fc_data[0])
    ans = []
    pass_index = -2
    for k in range(len(fc_data)-1, 0, -1):
        if k == len(fc_data) - 1: # O(log n) but only once
            curr_index = binary_search(fc_data[k], target) # O(log n) but only once
            if curr_index >= len(fc_data[k]): # if the item is bigger than the largest item in the list
                ans.append((False, max_len))
                pass_index = len(fc_data[k-1])-1
            else:
                curr_element = fc_data[k][curr_index]
                if isinstance(curr_element, Original):
                    ans.append((curr_element.val==target, curr_element.original_index))
                    if curr_element.next_promoted == -1:
                        pass_index = len(fc_data[k-1])-1
                    else:
                        pass_index = (fc_data[k][curr_element.next_promoted].below_index)
                else:
                    if curr_element.next_original == -1:
                        ans.append((False, max_len))
                    else:
                        ans.append((fc_data[k][curr_element.next_original].val==target, fc_data[k][curr_element.next_original].original_index))
                    pass_index = curr_element.below_index
        else:
            curr_index = pass_index
            curr_element = fc_data[k][curr_index]
            if target > curr_element.val: # if the item is bigger than the largest item in the list
                ans.append(max_len)
                pass_index = len(fc_data[k-1])-1
            else:
                if curr_index == 0: # if the item is the first thing in the list
                    ans.append((False, 0))
                else:
                    if fc_data[k][curr_index-1].val >= target:
                        curr_index -= 1
                        curr_element = fc_data[k][curr_index]
                    if isinstance(curr_element, Original):
                        ans.append((curr_element.val == target, curr_element.original_index))
                    else:
                        if curr_element.next_original == -1:
                            ans.append((False, max_len))
                        else:
                            ans.append((fc_data[k][curr_element.next_original].val==target, fc_data[k][curr_element.next_original].original_index))
                if isinstance(curr_element, Original):
                    if curr_element.next_promoted == -1:
                        pass_index = len(fc_data[k-1])-1
                    else:
                        pass_index = (fc_data[k][curr_element.next_promoted].below_index)
                else:
                    pass_index = curr_element.below_index
    curr_index = pass_index
    curr_element = fc_data[0][curr_index]
    if target > curr_element.val:
        ans.append((False, max_len))
    else:
        if curr_index == 0:
            ans.append((fc_data[0][0].val==target, 0))
        else:
            if fc_data[0][curr_index-1].val >= target:
                ans.append((fc_data[0][curr_index-1].val==target, curr_index-1))
            else:
                ans.append((fc_data[0][curr_index].val==target, curr_index))
    ans = ans[::-1]
    contextualize(fc_data, ans, target)
    return ans

arrays = [
    [11, 32, 42, 46],
    [13, 20, 39, 92],
    [18, 29, 43, 74],
    [12, 43, 50, 56]
]

arrays2 = [
    [1, 5, 8],
    [2, 7, 9],
    [3, 4, 6]
]

print("Original 2d arrays:")
for k in range(len(arrays)-1, -1, -1):
    print(f"Array {k}: {arrays[k]}")

print("FC arrays:")
fc_data = build_fractional_cascading(arrays)
for k in range(len(fc_data)-1, -1, -1):
    print_fc_arr(k, fc_data[k])

target = int(input("Enter the target value: "))
res = fc_search(fc_data, target)