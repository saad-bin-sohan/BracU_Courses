#Task_1a
input = open("/content/input1a.txt")
output = open("/content/output1a.txt", "w")

len_and_sum_lst = input.readline().strip().split(" ")
length = int(len_and_sum_lst[0])
sum = int(len_and_sum_lst[1])

line = input.readline().strip().split(" ")
index1, index2 = 0, 0

for i in range(length):
  for j in range(i+1, length):
    if int(line[i]) + int(line[j]) == sum:
      index1 = i+1
      index2 = j+1
      break

if index1 != 0 and index2 != 0:
  output.write(f"{index1} {index2}")
else:
  output.write("IMPOSSIBLE")

output.close()