import random

def routine_creator(nmbr_courses, slot_cnt):
    possible_rtn = []
    for nmbr_for_itr in range(slot_cnt):
        time_sch = [0] * nmbr_courses
        idx = random.randint(0, nmbr_courses-1)
        position = 1
        time_sch[idx] = position
        possible_rtn.extend(time_sch)
    return possible_rtn

def evalt_quality(possibly_rtn, toral_crs, num_slots):
    overlap_clash_existing = 0
    consistency_existing = 0

    for nmbr1_for_itr in range(num_slots):
        strt_idx = nmbr1_for_itr * toral_crs
        end_index = (nmbr1_for_itr + 1) * toral_crs
        slot = possibly_rtn[strt_idx:end_index]
        overlap_clash_existing += max(0, sum(slot) - 1)

    for nmbr2_for_itr in range(toral_crs):
        course_sum = 0
        for nmbr1_for_itr in range(num_slots):
            idx = nmbr2_for_itr + nmbr1_for_itr * toral_crs
            course_sum += possibly_rtn[idx]
        consistency_existing += abs(course_sum - 1)

    return -(overlap_clash_existing + consistency_existing)

def pickup_parents(pop, fits):
    minim_fit = min(fits)
    normalized_of_the_fits = []
    for f in fits:
        normalized_fitness = f - minim_fit + 1
        normalized_of_the_fits.append(normalized_fitness)
        
    the_parents_chosen = random.choices(pop, weights = normalized_of_the_fits, k=2)
    return the_parents_chosen


def recombine(anc1, anc2):
    cut_place = random.randint(1, len(anc1) - 1)
    offspr_1 = anc1[:cut_place] + anc2[cut_place:]
    off_Spr2 = anc2[:cut_place] + anc1[cut_place:]
    return offspr_1, off_Spr2

def chrm_variat_generate(chromo, rate=0.01):
    for idx in range(len(chromo)):
        if random.random() < rate:
            chromo[idx] = 1 - chromo[idx]

def get_the_best_chromosome(popult_list, eval_func, nmbr_courses, num_slots):
    opt_routine_found = None
    highest_fitness = float('-inf')
    for chromo in popult_list:
        current_fitness = eval_func(chromo, nmbr_courses, num_slots)
        if current_fitness > highest_fitness:
            highest_fitness = current_fitness
            opt_routine_found = chromo
    return opt_routine_found

def two_p_crossingover(parent1, parent2):
    pnt1 = random.randint(1, len(parent1) - 2)
    pnt2 = random.randint(pnt1 + 1, len(parent1) - 1)
    chld1 = parent1[:pnt1] + parent2[pnt1:pnt2] + parent1[pnt2:]
    chld2 = parent2[:pnt1] + parent1[pnt1:pnt2] + parent2[pnt2:]
    return chld1, chld2

inp_file_pt = "Sohan_CSE422_Lab_Assignment02_InputFile_Summer2024.txt"
with open(inp_file_pt, 'r') as ipt_file:
    first_line = ipt_file.readline().strip().split()
    N = int(first_line[0])
    T = int(first_line[1])
    course_list = [ipt_file.readline().strip() for jt in range(N)]

popult_size = 10
popult = [routine_creator(N, T) for jk in range(popult_size)]

max_genarates = 50000
for gen in range(max_genarates):
    fits = [evalt_quality(chromo, N, T) for chromo in popult]
    if max(fits) == 0:
        break
    new_popult = [ ]
    for nmbr_for_itr in range(popult_size // 2):
        anc1, anc2 = pickup_parents(popult, fits)
        offspr_1, off_sp2 = recombine(anc1, anc2)
        chrm_variat_generate(offspr_1)
        chrm_variat_generate(off_sp2)
        new_popult.extend([offspr_1, off_sp2])
    popult = new_popult

best_chrom = get_the_best_chromosome(popult, evalt_quality, N, T)
best_fit = evalt_quality(best_chrom, N, T)
output_text = ''.join(map(str, best_chrom))
opt_file_finder = "output.txt"

parent1 = random.choice(popult)
parent2 = random.choice(popult)
child1, child2 = two_p_crossingover(parent1, parent2)

with open(opt_file_finder, 'w') as outpt_file:
    outpt_file.write(output_text + "\n")
    outpt_file.write(str(best_fit) + "\n")
    outpt_file.write(f"Result for part 2\nParent 1: {''.join(map(str, parent1))}\nParent 2: {''.join(map(str, parent2))}\nSo the two resultant offsprings are, {''.join(map(str, child1))} & {''.join(map(str, child2))}")