import itertools
import time
import random

"""
A heuristic method to find a solution to the knapsack problem using a "Most Expensive First" greedy approach
@author         Luke Nickholds
@dateCreated    10/8/2017
@dateModified   12/8/2017
@param          in_weights - [float]    - An array containing the weight of each option in order
@param          in_values  - [float]    - An array containing the value of each option in order
@param          constraint - float      - The maximum weight
@return         [total_weight, total_value, chosen_items] - returns the best combination found
@complexity     O(n^2) where n is the amount of options
"""
def expensive_first(in_weights, in_values, constraint):
    my_weights = in_weights[:]
    my_values = in_values[:]

    chosen_items = []

    total_weight = 0
    total_value = 0

    i = 0
    while i <= len(my_weights):
        index = find_max(my_values)
        if (my_weights[index] + total_weight < constraint and my_weights[index] > 0):
            total_weight += my_weights[index]
            total_value += my_values[index]
            chosen_items.append(index)
        my_weights[index] = 0
        my_values[index] = 0
        i += 1
    return [total_weight, total_value, chosen_items]

def test_expensive_first():
    weights1 = [  20,   4,   7,   7,   2,   7,  11,  18,  15,   5]
    values1  = [1125,  75, 300, 400,  10, 325, 350, 925, 425, 200]
    expected = [29, 1535, [0, 3, 4]]
    actual = expensive_first(weights1, values1, 30)
    assert(expected==actual)
    print("test_expensive_first(): All tests passed.")

"""
A heuristic method to find a solution to the knapsack problem using a "Bang for Buck" greedy approach.
The value/weight ratio of each option is considered, and the best ratios are taken first
@author         Luke Nickholds
@dateCreated    10/8/2017
@dateModified   12/8/2017
@param          in_weights - [float]    - An array containing the weight of each option in order
@param          in_values  - [float]    - An array containing the value of each option in order
@param          constraint - float      - The maximum weight
@return         [total_weight, total_value, chosen_items] - returns the best combination found
@complexity     O(n^2) where n is the amount of options
"""
def bang_for_buck(in_weights, in_values, constraint):
    my_weights = in_weights[:]
    my_values = in_values[:]
    bang_for_buck = []
    chosen_items = []

    for i in range(len(my_weights)):
        bang_for_buck.append(my_values[i] / my_weights[i])
    total_weight = 0
    total_value = 0

    i = 0
    while i <= len(my_weights):
        index = find_max(bang_for_buck)
        if (my_weights[index] + total_weight < constraint and my_weights[index] > 0):
            total_weight += my_weights[index]
            total_value += my_values[index]
            chosen_items.append(index)
        my_weights[index] = 0
        my_values[index] = 0
        bang_for_buck[index] = 0
        i += 1
    return [total_weight, total_value, chosen_items]

"""
A Brute Force approach to finding a solution to the knapsack problem
@author         Luke Nickholds
@dateCreated    10/8/2017
@dateModified   12/8/2017
@param          in_weights - [float]    - An array containing the weight of each option in order
@param          in_values  - [float]    - An array containing the value of each option in order
@param          constraint - float      - The maximum weight
@return         [best_weight, best_value, best_combo] - returns the best combination found
@complexity     O(2^n) where n is the amount of options
"""
def brute_force(in_weights, in_values, constraint):
    best_combo = []
    best_value = 0
    best_weight = 0
    combinations = generate_combinations(len(in_weights))
    for combo in combinations:
        weight = 0
        value = 0
        for item in combo:
            weight += in_weights[item]
            value += in_values[item]
        if weight < constraint and value > best_value:
            best_value = value
            best_weight = weight
            best_combo = combo
    return [best_weight, best_value, best_combo]

"""
Generates all combinations of the numbers between 1 and n (where n is the parameter passed)
@author         Luke Nickholds
@dateCreated    12/8/2017
@dateModified   12/8/2017
@param          the_length - float      - The desired max of combos
@return         combinations - a list of lists, where each inner list is a combination
@complexity     O(2^n) where n is the value of the_length
"""
def generate_combinations(the_length):
    combinations = []
    for r in range(the_length):
        combinations += itertools.combinations(range(the_length), r)
    return combinations

"""
Finds the index of the maximum item on a list
@author         Luke Nickholds
@dateCreated    10/8/2017
@dateModified   12/8/2017
@param          the_list [float]  - A list of numbers
@return         best_i - the index of the maximum item
@complexity     O(n) where n is the length of the list
"""
def find_max(the_list):
    i = 0
    best = the_list[i]
    best_i = 0
    while i < len(the_list):
        if (the_list[i] > best):
            best = the_list[i]
            best_i = i
        i += 1
    return best_i

def generate_knapsack_instance(items, min_weight, max_weight, min_bfb, max_bfb):
    weights = []
    values = []
    for _ in range(items):
        this_weight = random.randint(min_weight, max_weight)
        weights.append(this_weight)
        this_value = ((int) (this_weight * random.randrange(min_bfb, max_bfb)))
        this_value = (int) (this_value / 25) * 25 # Round to nearest 25
        values.append(this_value) 
    return [weights, values]

if __name__ == "__main__":
    weights= [ 10,   5,   7,  12,  14,   6,   9,  11,  13]
    values = [500, 450, 400, 600, 700, 300, 500, 350, 800]

    new_instance = generate_knapsack_instance(10, 2, 20, 10, 60)
    print(new_instance)

    weights = new_instance[0]
    values = new_instance[1]

    print("Expensive First")
    t1 = time.time()
    print(expensive_first(weights, values, 30))
    t2 = time.time()
    print(t2 - t1)

    test_expensive_first()

    # print("Bang for Buck")
    # t1 = time.time()
    # print(bang_for_buck(weights, values, 30))
    # t2 = time.time()
    # print(t2 - t1)
    #
    # print("Brute Force")
    # t1 = time.time()
    # print(brute_force(weights, values, 30))
    # t2 = time.time()
    # print(t2 - t1)
