"""
Module: supplies

An application to solve the Disaster Planning problem.

"""
from sys import argv, exit
import re

class InvalidFileFormatError(Exception):
    pass

def parse_network_data(filename: str) -> tuple[dict[str, set[str]], dict[str, tuple[int,int]]]:
    """
    Reads city connection data <filename>, returning a dictionary that
    associates each city with the set of cities that are directly connected to
    it.

    DO NOT MODIFY THIS FUNCTION IN ANY WAY!!!!!

    Parameters:
        filename (str): Name of the file containing city connections.

    Returns:
        (tuple[dict[str, set[str]], dict[str, tuple[int,int]]]): Two dictionaries:
            (1) The cities and the set of cities they are directly connected
            (2) The "logical" location of these cities.
    """
    network = {}
    location = {}

    with open(filename, 'r') as f:
        for line in f:
            clean_line = line.strip()

            # skip over comment lines (start with a '#') and blank lines
            if len(clean_line) == 0 or clean_line[0] == '#':
                continue

            # use a regular expression to parse this line, pulling out the
            # city as well as comma separated list of neighbors.
            match = re.fullmatch("(?P<city>[\w\-\. ]+)\s+\((?P<x>\d+),\s*(?P<y>\d+)\):(\s+(?P<neighbors>[\w\-\. ]+(,\s+[\w\-\. ]+)*))?", clean_line)
            if not match:
                raise InvalidFileFormatError(f"Invalid line: {clean_line}")

            #print("Match:", clean_line)
            city = match.group('city')
            x_loc = int(match.group('x'))
            y_loc = int(match.group('y'))
            location[city] = (x_loc, y_loc)

            neighbors = match.group('neighbors')
            if neighbors is None:
                continue

            listed_neighbors = {n.strip() for n in neighbors.split(',')}

            # add a link from this city to all the listed neighbors
            network[city] = network.get(city, set()) | listed_neighbors

            # add a link back from each listed neighbor to this city
            for n in listed_neighbors:
                n_neighbors = network.get(n, set())
                n_neighbors.add(city)
                network[n] = n_neighbors


    return network, location


def can_be_disaster_ready(road_network: dict[str, set[str]], num_cities: int, supply_locations: set[str]) -> bool:
    """
    This function will determine if a region can be disaster ready by stockpiling supplies in most num_cities locations.
    
    Preconditions:
        num_cities must be a non-negative value

    Parameters:
        road_network(dict[str, set[str]]): A dictionary storing the keys which are city names and the values that are the sets of adjacent cities.
        num_cities(int): The maximum number of cities allowed to stockpile supplies
        supply_locations(set[str]): A set that will be populated with supply located only if the region is disaster ready
    
    Returns:
        bool: True if the region can be disaster ready,
              False otherise.
    """
    assert num_cities>=0, "The number of supply cities cannot be negative"
    #asserts the pre condition of the function

    #finds uncovered cities
    covered = {city for city in supply_locations}
    for city in supply_locations: 
        for nearby in road_network[city]:
            if nearby not in covered:
                covered.add(nearby)
    uncovered=[city for city in road_network if city not in covered]  #list of cities not covered by supplies
    
    if len(uncovered)==0:
        return True #returns true because there are no more cities needed to be covered
    
    if len(supply_locations)>=num_cities: 
        return False #This loop checks if we can cover all cities with the remaining supply locations
    
    next_city=uncovered[0]
    options=[next_city] 
    #starts adding supplies to the uncovered citys, beginning with the current city itself
   
    for next in road_network[next_city]:
        if next not in options:
            options.append(next) #adds next city into a list of possible supply cities
    for city in options:
        supply_locations.add(city) #adds city to supply list
        if can_be_disaster_ready(road_network, num_cities, supply_locations): #uses recursion to find possible solution
            return True
        supply_locations.remove(city) #backtracks if it doesn't work
    return False #No solution found



if __name__ == "__main__":
    
    if len(argv) != 3:
        print("Error: wrong number of command line parameters")
        exit(1)

    n, _ = parse_network_data(argv[1])
    max_num_cities = int(argv[2])

    supply_cities: set[str] = set()

    ok = can_be_disaster_ready(n, max_num_cities, supply_cities)
    if ok:
        print("Supply Locations:", supply_cities)
        assert len(supply_cities) <= max_num_cities, f"Problem constraint has been voilated: too many cities ({len(supply_cities)}) selected!"
    else:
        print("No solution possible!")
