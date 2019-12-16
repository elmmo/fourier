import timeit

def test(): 
    SETUP_CODE = '''
from scrape import Department
from utils import parseChoose, Term
from math import floor
import random

url = 'http://catalog.whitworth.edu/undergraduate/mathcomputerscience/#text'
dept = Department(url)
degree = dept.getDegree()

plot = []

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

# chooses the classes that will be put in the fourier plan 
def createCoursePlan(courses, constraints, mtx, verbose):
    plan = []
    for course in courses: 
        if type(course) == list: 
            plan.extend(getShortestPathOptions(course, mtx, plan, verbose))
        # set to ignore lab classes 
        elif course in degree.coursesByName and 'L' not in course: 
            if verbose:
                print("Adding {} to course plan".format(course))
            plan.append(course)
    if verbose: 
        print("Course plan fully generated.")
    return plan

# when there's a choose option, will randomly select a course to plan based on the options with the shortest paths 
def getShortestPathOptions(options, mtx, plan, verbose):
    prereqCosts = []
    chosen = []
    # if all options are labs, choice is void 
    for i in range(1, len(options)):
        if 'L' in options[i]:
            return chosen 
    if parseChoose(options) > 0: 
        chooseInt = parseChoose(options)
        for option in options: 
            # ignore recommended courses 
            if option == 'Recommended:':
                break
            # verify option is a course 
            if option in degree.coursesByName: 
                prereqCosts.append(getPathLength(option, mtx, verbose))
        while chooseInt > 0: 
            if verbose: 
                print("Choosing {} option(s)...".format(chooseInt))
            # find the minimum number of prerequisites 
            minReq = min(prereqCosts)
            minOptions = []
            for j in range(len(prereqCosts)):
                if prereqCosts[j] == minReq: 
                    # 1 needs to be added to account for the choose options text 
                    minOptions.append(j+1)
            # continue to choose random options until the options are exhausted or the correct number has been chosen 
            while len(minOptions) > 0 and chooseInt > 0: 
                index = random.randint(0, len(minOptions)-1)
                potentialClass = options[minOptions[index]]
                if potentialClass not in plan:  # verify the course isn't already in the plan 
                    chosen.append(potentialClass)
                    # reduce choose and delete the chosen class from the list of options
                    chooseInt -= 1
                    del minOptions[index]
                    if verbose:
                        print("Chosen: {}, with a cost of {}".format(potentialClass, minReq))
        if verbose: 
            print("Finished choosing options.")
    return chosen


# calculates the overall cost to get to any one class using dynamic programming 
def getPathLength(course, mtx, verbose):
    if verbose: 
        print("Calculating cost to get to {}...".format(course))
    if course in plot:
        classCol = plot.index(course)

        # base case 
        latestClass = 0
        # works assuming the matrix is n x n 
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
    else: 
        # base case - class with no constraints 
        costs[course] = 0
    return costs[course]

matrix = createMatrix(degree.constraints, False)
'''

    TEST_CODE = ''' 
costs = {}
transitiveClosure(matrix, False)
coursePlan = createCoursePlan(degree.courses, degree.constraints, matrix, False)
'''

    print(timeit.timeit(setup = SETUP_CODE, stmt = TEST_CODE, number = 100))

test()