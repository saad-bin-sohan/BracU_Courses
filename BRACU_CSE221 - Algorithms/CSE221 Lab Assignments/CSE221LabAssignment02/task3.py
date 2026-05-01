#Task_3
input = open("input3.txt")
output = open("output3.txt","w")
tasks = int(input.readline().strip())
tasks_lst = []
comp_tasks_lst = []

for i in range(tasks):
  u_v_lst = input.readline().strip().split(" ")
  u = int(u_v_lst[0])
  v = int(u_v_lst[1])
  tasks_lst.append((u,v))

for i in range(tasks):
  for j in range(tasks):
    if tasks_lst[i][1] == tasks_lst[j][1]:
      if tasks_lst[i][0] < tasks_lst[j][0]:
        tasks_lst[i],tasks_lst[j] = tasks_lst[j],tasks_lst[i]

    elif tasks_lst[i][1] < tasks_lst[j][1]:
      tasks_lst[i],tasks_lst[j] = tasks_lst[j],tasks_lst[i]

comp_tasks_lst.append(tasks_lst[0])
i = 1
while i < tasks:
  if tasks_lst[i][0] >= comp_tasks_lst[-1][1]:
    comp_tasks_lst.append(tasks_lst[i])
    i += 1
  else:
    i += 1

comp_tasks = len(comp_tasks_lst)
output.write(f"{comp_tasks}\n")
for tup in comp_tasks_lst:
  output.write(f"{tup[0]} {tup[1]}\n")

output.close()