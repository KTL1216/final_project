def binary_search(arr, target):
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid][0] == target:
            return mid
        elif arr[mid][0] < target:
            low = mid + 1
        else:
            high = mid - 1

    return low 

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

def contextualize(fc_data, ans, target):
    print("Target value:", target)
    for k, indices in enumerate(ans):
        if len(fc_data[k]) > indices and fc_data[k][indices][0] == target:
            print(f"For array {k}: target with value {target} is found at index {indices}")
        else:
            print(f"For array {k}: target with value {target} should be inserted at index {indices}")


def fc_search(fc_data, target):
    ans = []
    prev_index = -1
    for k in range(len(fc_data)-1, -1, -1):
        if prev_index == -1: # O(log n) but only once
            curr_index = binary_search(fc_data[k], target)
            ans.append(curr_index)
        else: # O(1)
            curr_index = prev_index
            ans.append(curr_index)
        if prev_index > 0 and prev_index < len(fc_data[k]):
            prev_index = fc_data[k][curr_index][1]
    contextualize(fc_data, ans, target)
    return ans

arrays = [
    [11, 32, 42, 46],
    [13, 20, 39, 92],
    [18, 29, 43, 74]
]

fc_data = build_fractional_cascading(arrays)


for i, arr in enumerate(fc_data):
    print(f"Array {i}: {arr}")
target = int(input("Enter the target value: "))
res = fc_search(fc_data, target)