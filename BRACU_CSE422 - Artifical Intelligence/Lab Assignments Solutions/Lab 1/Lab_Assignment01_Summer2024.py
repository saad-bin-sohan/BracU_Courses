import heapq

inp_txt_file = open("/Users/sohan/Downloads/Education/BRACU Summer 2024/CSE422/422 labs/Lab 1/Assignment 1 (A*)/22101704_Sk Md Saad Bin Sohan_CSE422_06_Lab_Assignment01_InputFile_Summer2024.txt", 'r')
temp_list = inp_txt_file.readlines( )
inp_lines = [ ]

for line in temp_list:
    inp_lines.append( line.strip( ) )

entire_country_map = { }

for each_line in inp_lines:
    parts_of_the_line = each_line.split(' ')
    city = parts_of_the_line[0]
    heuristic = int(parts_of_the_line[1])
    neighbors = [ ]
    for i in range(2, len(parts_of_the_line), 2):
        neighbor_city = parts_of_the_line[i]
        neighbor_distance = parts_of_the_line[i + 1]
        neighbors.append(tuple((neighbor_city, neighbor_distance)))

    entire_country_map[city] = [heuristic] + neighbors

def h_finder(node):

    for key, values in entire_country_map.items():
        if key == node:
            return values[0]

def a_star_algo(graph, start_node, destination_to_reach_goal):
    
    g_start = 0
    
    to_be_visited_list = [ ]

    first_heuristic_value = h_finder(start_node)
    first_f_value = g_start + first_heuristic_value

    start_node_mini_list = (first_f_value, start_node)

    to_be_visited_list.append(start_node_mini_list)

    alr_visited_nodes = [ ]
    g_n = {start_node: 0}
    parent_mapping = {start_node: None}

    while len(to_be_visited_list) != 0:
        f_n, present_visiting = heapq.heappop(to_be_visited_list)

        if present_visiting == destination_to_reach_goal:
            path_to_cross = [ ]
            while present_visiting:
                path_to_cross.append(present_visiting)
                present_visiting = parent_mapping[present_visiting]
            reversed_path_to_cross = path_to_cross[ : : -1 ]
            total_distance = g_n[destination_to_reach_goal]
            return reversed_path_to_cross, total_distance

        alr_visited_nodes.append(present_visiting)

        each_neighbour = graph[present_visiting][1:]
        for neighbor, distance in each_neighbour:
            neighbor = neighbor.strip()
            distance = int(distance)
            if neighbor in alr_visited_nodes:
                continue

            probable_g_n = g_n[present_visiting] + distance

            if neighbor not in g_n or probable_g_n < g_n[neighbor]:
                g_n[neighbor] = probable_g_n
                f_n = probable_g_n + h_finder(neighbor)
                heapq.heappush(to_be_visited_list, (f_n, neighbor))
                parent_mapping[neighbor] = present_visiting

    return 'No Path Found', 0

huristic_mini_lists = [ ]

graph = entire_country_map

start_of_your_journey = input('what is your start city name: ')
end_of_your_journey = input('what is your destination city name: ')

path_of_your_journey, total_journey_distance = a_star_algo(entire_country_map, start_of_your_journey, end_of_your_journey)

opt_file_path = "/Users/sohan/Downloads/Education/BRACU Summer 2024/CSE422/422 labs/Lab 1/Assignment 1 (A*)/output file.txt"

with open(opt_file_path, 'w') as output_file:
    if path_of_your_journey != 'No Path Found':
        output_file.write(' -> '.join(path_of_your_journey) + f"\nTotal distance: {total_journey_distance} km")
    else:
        output_file.write(path_of_your_journey)