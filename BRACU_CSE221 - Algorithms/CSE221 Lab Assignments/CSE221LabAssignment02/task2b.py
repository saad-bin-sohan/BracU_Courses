#Task_2b
input = open("/content/input2b.txt")
output = open("/content/output2b.txt", "w")

num_of_elem_arr1 = int(input.readline())
line1 = input.readline().strip().split(" ")
arr1 = [0] * len(line1)
for i in range(len(line1)):
  arr1[i] = int(line1[i])

num_of_elem_arr2 = int(input.readline())
line2 = input.readline().strip().split(" ")
arr2 = [0] * len(line2)
for i in range(len(line2)):
  arr2[i] = int(line2[i])

def merge_sorted_arrays(arr1, arr2):
    len_arr1 = len(arr1)
    len_arr2 = len(arr2)
    pointer1 = 0
    pointer2 = 0
    merged_arr = []

    while pointer1 < len_arr1 and pointer2 < len_arr2:
        if arr1[pointer1] <= arr2[pointer2]:
            merged_arr.append(arr1[pointer1])
            pointer1 += 1
        else:
            merged_arr.append(arr2[pointer2])
            pointer2 += 1

    while pointer1 < len_arr1:
        merged_arr.append(arr1[pointer1])
        pointer1 += 1

    while pointer2 < len_arr2:
        merged_arr.append(arr2[pointer2])
        pointer2 += 1

    return merged_arr

merged_arr = merge_sorted_arrays(arr1, arr2)

for num in merged_arr:
    output.write(f'{num} ')

output.close()

# The time complexity of this code is O(n),
# where n is the total number of elements in both arr.
# The code iterates over the two arr simultaneously using two pointers,
# comparing the elements and merging them into a single sorted list. Since each element is visited only once,
# the time complexity is linear with respect to the total number of elements, resulting in O(n) complexity.