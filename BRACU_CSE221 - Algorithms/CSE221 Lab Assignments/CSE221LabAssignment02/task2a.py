#Task_2a
input = open("/content/input2a.txt")
output = open("/content/output2a.txt", "w")

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

total_arr = arr1 + arr2
total_len = len(total_arr)

def merge_sort(arr, start, total_len):
    if start >= total_len:
        return arr
    else:
        mid = start + (total_len - start) // 2
        merge_sort(arr, start, mid)
        merge_sort(arr, mid + 1, total_len)
        merge(arr, start, mid, total_len)
        return arr

def merge(array, start, mid, total_len):
    len_new_arr1 = mid - start + 1
    len_new_arr2 = total_len - mid
    
    new_arr1 = [0] * len_new_arr1
    new_arr2 = [0] * len_new_arr2

    for i in range(len_new_arr1):
        new_arr1[i] = array[start + i]

    for j in range(len_new_arr2):
        new_arr2[j] = array[mid + j + 1]

    i, j, k = 0, 0, start

    while i < len_new_arr1 and j < len_new_arr2:
        if new_arr1[i] <= new_arr2[j]:
            array[k] = new_arr1[i]
            i += 1
        else:
            array[k] = new_arr2[j]
            j += 1
        k += 1

    while i < len_new_arr1:
        array[k] = new_arr1[i]
        i += 1
        k += 1

    while j < len_new_arr2:
        array[k] = new_arr2[j]
        j += 1
        k += 1

    return array

sorted_array = merge_sort(total_arr, 0, len(total_arr)-1)

for num in sorted_array:
    output.write(f'{num} ')

output.close()