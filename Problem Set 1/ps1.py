###########################
# 6.00.2x Problem Set 1: Space Cows 

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================


def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    

    order = []
    cow_copy = cows.copy()
    cow_sort = sorted(cow_copy.items(), key=lambda x: x[1], reverse = True)
    
    
    while len(cow_copy) > 0:
        trip = []
        trip_limit = limit
        for cow, weight in cow_sort:
            if cow in cow_copy and weight <= trip_limit:
                trip.append(cow)
                trip_limit = trip_limit - weight
                del cow_copy[cow]
        order.append(trip)
    
    return order
                



# Problem 2
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    
    order = []
    
    # Use helper function to get all possible partitions of cows
    collections = sorted(get_partitions(cows), key = len)
    
    # The number of possible partitions 
    clen = len(collections)
    
    # Create a dictionary that holds the indices of the partitions as keys 
    # and their weight validity as values
    possible_dict = {}
    for i in range(clen):
        possible_dict[i] = True # Default is True
        for trip in collections[i]: # Each list inside the partition is a trip
            total = 0
            for cow in trip:
                total += cows[cow]
                if total > limit:
                    possible_dict[i] = False # Change the value to False if the total weight on board exceeds the limit
        
    # Create a dictionary with partitions whose trips are all valid            
    valid_dict = {}
    for valid_trip in possible_dict: # iterating over index numbers (integers)
        if possible_dict[valid_trip] == 1:
            length = len(collections[valid_trip])
            valid_dict[valid_trip] = length
    
    # Set the variable "minimum" to be the minimum number of trips found among all valid collections
    minimum = min(valid_dict.values())
    
    # Find a collection with the minimum number of trips
    for v_trip in valid_dict: # iterating over index numbers (integers)
        if valid_dict[v_trip] == minimum:
            order = collections[v_trip]
            break
    
    return order
                    
        
        
# Problem 3
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cows = load_cows("ps1_cow_data.txt")
    limit = 10
    
    greedy_start = time.time()
    greedy = greedy_cow_transport(cows, limit)
    greedy_end = time.time()
    print("The number of trips returned by the greedy algorithm is", len(greedy))
    print('The time that the greedy algorithm takes to run is', greedy_end - greedy_start)
    
    
    brute_start = time.time()
    brute = brute_force_cow_transport(cows, limit)
    brute_end = time.time()
    print("The number of trips returned by the brute force algorithm is", len(brute))
    print('The time that the brute force algorithm takes to run is', brute_end - brute_start)
    


"""
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

# cows = load_cows("ps1_cow_data.txt")
# limit=100
# print(cows)

# print(greedy_cow_transport(cows, limit))
# print(brute_force_cow_transport(cows, limit))


