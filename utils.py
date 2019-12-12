import re

def parseChoose(course):
    if type(course) == type(""):
        return 1
    numOfCourses = 0
    if course[0].lower().find("one") != -1:
        numOfCourses = 1
    elif course[0].lower().find("two") != -1:
        numOfCourses = 2
    elif course[0].lower().find("three") != -1:
        numOfCourses = 3
    elif course[0].lower().find("four") != -1:
        numOfCourses = 4
    elif course[0].lower().find("five") != -1:
        numOfCourses = 5
    elif course[0].lower().find("six") != -1:
        numOfCourses = 6
    return numOfCourses

# This function parses the constraints for a course and splits them into time constraints and prerequisites
def getConstraints(course, degree):
    time = "none"
    prerequisites = []
    standing = "none"
    if course in degree.constraints:
        for rule in degree.constraints[course]:
            if rule.lower().find("semester") != -1 or rule.lower().find("term") != -1:
                time = rule
            elif rule.find("Prerequisite") != -1:
                i = 0
                while i < len(rule.split()):
                    # Regex looks for three numbers in a row and makes sure the whole string doesn't contain a "+"
                    # This handles the cases where an optional prerequisite is having a high enough SAT score
                    # While also making sure to grab all course numbers
                    # (?!.*\+)^ my look like an expletive, but it checks to see if anywhere in the string there is a "+"
                    # [0-9][0-9][0-9] looks for 3 digits in sequence
                    if re.search("(?!.*\+)^[0-9][0-9][0-9]", rule.split()[i]):
                        prerequisites.append(rule.split()[i-1] + " " + rule.split()[i])
                    i += 1
            elif rule.lower().find("standing") != -1:
                for word in rule.lower().split():
                    if word == "freshman" or word == "sophomore" or word == "junior" or word == "senior":
                        standing = word
        i = 0
        while i < len(prerequisites):
            prerequisites[i] = prerequisites[i].replace(",", "")
            if prerequisites[i] not in degree.coursesByName or prerequisites[i].find("L") != -1:
                del prerequisites[i]
                i -= 1
            i += 1
    return time, prerequisites, standing


def createAssociation(degree):
    association = {}
    i = 1
    for course in degree.courses:
        if type(course) == type(""):
            association[course] = getConstraints(course, degree)[1]
        else:
            association[i] = []
            for option in course:
                for prereq in getConstraints(option, degree)[1]:
                    association[i].append(prereq)
            association[i] = list(set(association[i]))
            i += 1
    for node in association:
        i = 1
        for course in degree.courses:
            if type(course) == type([]):
                for option in course:
                    if option in association[node]:
                        association[node].remove(option)
                        association[node].append(i)
                i += 1
        association[node] = list(set(association[node]))
    for node in association:
        for edge in association[node]:
            if edge == node:
                association[node].remove(edge)
    return association    

# This is a depth first search that orders on popped as opposed to on visited
def TopologicalSort(association):
    popped = []
    stack = []
    for node in association:
        for edge in association[node]:
            if edge not in popped:
                TopologicalSort(association)
        popped.append(node)
    popped.reverse()
    return popped
