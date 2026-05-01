#Task_1b
input = open("/content/input1b.txt")
output = open("/content/output1b.txt", "w")

len_and_sum_lst = input.readline().strip().split(" ")
length = int(len_and_sum_lst[0])
sum = int(len_and_sum_lst[1])

line = input.readline().strip().split(" ")
index1, index2 = 0, 0

start = 0

while start < length-1:
  if int(line[start]) + int(line[length-1]) < sum:
    start += 1
  elif int(line[start]) + int(line[length-1]) > sum:
    length -= 1
  elif int(line[start]) + int(line[length-1]) == sum:
    index1, index2 = start+1, length-1+1
    break

if index1 != 0 and index2 != 0:
  output.write(f"{index1} {index2}")
else:
  output.write("IMPOSSIBLE")

output.close()