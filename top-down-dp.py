from scrape import Department
from utils import parseChoose, Term
from math import floor
import random

url = 'http://catalog.whitworth.edu/undergraduate/mathcomputerscience/#text'
dept = Department(url)
degree = dept.getDegree()

plot = []
costs = {}
            
# creates an adjacency matrix based off of the 
def createMatrix(constraints, verbose):
    # create matrix of zeros, according to the number of classes there are to be plot 
    matrix = [[0 for col in range(len(constraints))] for row in range(len(constraints))]
    if verbose: 
        print("Creating adjacency matrix...")
    for course in constraints:
        if "Prerequisite" in constraints[course]:
            prereqStart = constraints[course].index("Prerequisite")
            prereqs = constraints[course][prereqStart+1]
            for i in range(len(prereqs)):
                row = plot.index(prereqs[i])
                matrix[row][len(plot)] = 1
                if verbose: 
                    print("Plotting: Course {} with the prereq {}".format(course, prereqs[i]))
        plot.append(course)
    if verbose: 
        print("Returning adjacency matrix.")
    return matrix

# takes in a matrix and performs transitive closure on it using Warshall's Algorithm
def transitiveClosure(mtx, verbose): 
    if verbose: 
        print("Performing transitive closure...")
    # works assuming that the size of the matrix is n x n
    for k in range(len(mtx[0])):
        for i in range(len(mtx[0])):
            for j in range(len(mtx[0])):
                if matrix[i][k] and matrix[k][j]:
                    if verbose: 
                        print("Found: {} is a prereq for {}".format(plot[i], plot[j]))
                    matrix[i][j] = 1
    if verbose: 
        print("Transitive closure complete.\n")


# chooses the classes that will be put in the fourier plan 
def createCoursePlan(courses, constraints, mtx, verbose):
    plan = []
    for course in courses: 
        if type(course) == list: 
            plan.extend(getShortestPathOptions(course, mtx, verbose))
        # set to ignore lab classes 
        elif course in degree.coursesByName and 'L' not in course: 
            if verbose:
                print("Adding {} to course plan".format(course))
            plan.append(course)
    return plan

# when there's a choose option, will randomly select a course to plan based on the options with the shortest paths 
def getShortestPathOptions(options, mtx, verbose):
    prereqCosts = []
    chosen = []
    # if all options are labs, choice is void 
    for i in range(1, len(options)):
        if 'L' in options[i]:
            return chosen 
    # set to ignore lab options 
    if parseChoose(options) > 0: 
        chooseInt = parseChoose(options)
        for option in options: 
            # verify option is a course
            if option in degree.coursesByName: 
                prereqCosts.append(getPathLength(option, mtx, verbose))
        for i in range(chooseInt): 
            if verbose: 
                print("Choosing {} option(s)...".format(chooseInt))
            minReq = min(prereqCosts)
            minOptions = []
            for j in range(len(prereqCosts)):
                if prereqCosts[j] == minReq: 
                    minOptions.append(j)
            index = random.randint(0, len(minOptions)-1)
            chosen.append(options[minOptions[index]])
            if verbose: 
                print("Chosen: {}, with a cost of {}".format(chosen[i], minReq))
        if verbose: 
            print("Finished choosing options.")
    if verbose: 
        print("Course plan fully generated.")
    return chosen


# calculates the overall cost to get to any one class using dynamic programming 
def getPathLength(course, mtx, verbose):
    if verbose: 
        print("Calculating cost to get to {}...".format(course))
    classCol = plot.index(course)

    # base case
    latestClass = 0
    # works assuming that the matrix is n x n
    for row in range(len(mtx[0])):
        if mtx[row][classCol]: 
            # if the class has a prereq, take note of the prereq closest to it  
            latestClass = row
    if latestClass == 0: 
        return 0

    # check if prereq value is stored 
    prereq = plot[latestClass]
    # if prereq cost is stored, return it; else, recursively track cost and return it 
    costs[course] = costs[prereq] + 1 if prereq in costs else getPathLength(prereq, mtx, verbose) + 1
    if verbose: 
        print("The cost to get to {} is {}".format(course, costs[course]))
    return costs[course]

print("\nPROGRAM RUNNING")
matrix = createMatrix(degree.constraints, False)
transitiveClosure(matrix, False)
coursePlan = createCoursePlan(degree.courses, degree.constraints, matrix, True)
print(coursePlan)


