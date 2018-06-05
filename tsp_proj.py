import sys
import math
import time


class Vertex:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y



class Graph:
    def __init__(self):
        # list of cities
        self.vertices = []
        # 2D matrix of distances between city pairs
        self.distances = []
        self.cityCount = 0


    # creates a new vertex and adds it to the graph's vertices list
    def add_vertex(self, id, x, y):
        self.vertices.append(Vertex(id, x, y))
        self.cityCount = self.cityCount + 1


    # calculates the distance between cities to nearest int
    def calculate_edge(self, vertex1, vertex2):
        x_dist = vertex1.x - vertex2.x
        y_dist = vertex1.y - vertex2.y
        dist = math.sqrt((x_dist**2)+(y_dist**2))
        return round(dist)


    # initialize 2D matrix to store values
    def build_dist_matrix(self):
        self.distances = [[0 for x in range(self.cityCount)] for y in range(self.cityCount)]

        for i in range(self.cityCount):
            for j in range(self.cityCount):
                if i != j and self.distances[i][j] == 0:
                    self.distances[i][j] = self.calculate_edge(self.vertices[i], self.vertices[j])
                    self.distances[j][i] = self.distances[i][j]
                #print(self.distances[i][j])


    def check_distance(self, vertex1, vertex2):
        city_dist = self.distances[vertex1.id][vertex2.id]
        return city_dist



def nearestNeighborTSP(cities, start_city):
    start = cities.vertices[start_city]
    currentCity = start
    path = [currentCity.id]
    solution = 0

    unvisited = set(city.id for city in cities.vertices[:])
    unvisited.remove(start_city)

    # ** I didn't see a way to remove objects from
    # a set based on the object's attribute, so I changed it to
    # be a set of just the city IDs. There might be a better way
    while unvisited:
        edgeLength = float('inf')
        # determine shortest edge on current vertex
        for cityID in unvisited:
            if cities.check_distance(currentCity, cities.vertices[cityID]) < edgeLength:
                edgeLength = cities.check_distance(currentCity, cities.vertices[cityID])
                nextCityID = cityID

        path.append(nextCityID)
        solution = solution + cities.check_distance(currentCity, cities.vertices[nextCityID])

        unvisited.remove(nextCityID)
        currentCity = cities.vertices[nextCityID]

    solution = solution + cities.check_distance(currentCity, start)
    return solution, path



start = time.time()


# input file is last in command line args
filename = sys.argv[-1]
file_in = open(filename, 'r')

# output is same filename but with .tour filetype
file_out = open(filename + '.tour', 'w')

cities = Graph()

# add cities to graph as vertices
for line in file_in:
    cityLine = line.strip()
    arr = list(map(int, cityLine.split()))
    cities.add_vertex(arr[0], arr[1], arr[2])


# calculate the distances and run algorithm once
cities.build_dist_matrix()
#solution, final_path = nearestNeighborTSP(cities, 0)


# run repetitive nearest neighbor with variable number of  startpoints
solution = float('inf')
if cities.cityCount > 5000:
    startpoints = 5
elif cities.cityCount > 2000:
    startpoints = 11
elif cities.cityCount > 1000:
    startpoints = 35
elif cities.cityCount > 500:
    startpoints = 100
else:
    startpoints = cities.cityCount

for x in range(startpoints):
    distance, path = nearestNeighborTSP(cities, x)
    if(distance < solution):
        solution = distance
        final_path = path


# test distance calculator
#print(cities.calculate_edge(cities.vertices[5], cities.vertices[1]))

# test distance retrieval
#print(cities.check_distance(cities.vertices[1], cities.vertices[2]))


# output first line is total distance, then city IDs
file_out.write(str(solution) + '\n')
for city in final_path:
    file_out.write(str(city) + '\n')
    print(city)

file_in.close()
file_out.close()

finish = time.time()
elapsed = (finish - start) * 1000

print("path length is ", solution)
print("time taken was ", elapsed, " ms")

