#Task_4
input = open("input4.txt")
output = open("output4.txt","w")

NM_line_lst = input.readline().strip().split(" ")
N = int(NM_line_lst[0])
M = int(NM_line_lst[1])

tasks_lst = []
for i in range(N):
  line = input.readline().strip().split(" ")
  u = int(line[0])
  v = int(line[1])
  tasks_lst.append((u,v))

temp_lst = []
for i in range(M):
  temp_lst.append([(0,0)])

for i in range(N):
  for j in range(N):
    if tasks_lst[i][1] == tasks_lst[j][1]:
      if tasks_lst[i][0] < tasks_lst[j][0]:
        tasks_lst[i],tasks_lst[j] = tasks_lst[j],tasks_lst[i]

    elif tasks_lst[i][1] < tasks_lst[j][1]:
      tasks_lst[i],tasks_lst[j] = tasks_lst[j],tasks_lst[i]

comp_tasks_lst = []
for t in tasks_lst:
  for p in temp_lst:
    if p == [(0,0)] or p[-1][-1] <= t[0]:
      p.append(t)
      comp_tasks_lst.append(t)

      for i in range(len(temp_lst)):
        for j in range(i + 1, len(temp_lst)):
          if temp_lst[i][-1][-1] < temp_lst[j][-1][-1]:
            temp_lst[i], temp_lst[j] = temp_lst[j], temp_lst[i]
      break

max_activity = len(comp_tasks_lst)
output.write(f'{max_activity}')
output.close()