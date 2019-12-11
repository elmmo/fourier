import re
from scrape import Degree, Department
from utils import parseChoose

url = 'http://catalog.whitworth.edu/undergraduate/mathcomputerscience/#text'
dept = Department(url)
degree = dept.getDegree()

schedule = {
    "119": [],
    "220": [],
    "320": [],
    "120": [],
    "221": [],
    "321": [],
    "121": [],
    "222": [],
    "322": [],
    "122": [],
    "223": [],
    "323": [],
}

plannedCourses = []

def getConstraints(course):
    time = "none"
    prerequisites = []
    if course in degree.constraints:
        for rule in degree.constraints[course]:
            if rule.find("semester") != -1:
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
        i = 0
        while i < len(prerequisites):
            if prerequisites[i] not in degree.coursesByName:
                del prerequisites[i]
                i -= 1
            i += 1
    return time, prerequisites

def planIndividualCourse(course):
    time = "none"
    prerequisites = []
    constraints = getConstraints(course)
    time = constraints[0].lower()
    if time == "none":
        time = "fall and spring semesters"
    prerequisites = constraints[1]
    scheduled = False


    if len(schedule["119"]) < 3:
        if time.find("fall") != -1 and time.find("even") == -1:
            eligible = len(prerequisites) == 0
            if eligible:
                schedule["119"].append(course)
                scheduled = True
    if len(schedule["220"]) < 1 and scheduled == False:
        if time.find("jan") != -1 and time.find("odd") == -1:
            eligible = True
            for prereq in prerequisites:
                if prereq not in schedule["119"]:
                    eligible = False
                    break
            if eligible:
                schedule["220"].append(course)
                scheduled = True
    if len(schedule["320"]) < 3 and scheduled == False:
        if time.find("spring") != -1 and time.find("odd") == -1:
            eligible = True
            for prereq in prerequisites:
                if prereq not in schedule["119"] and prereq not in schedule["220"]:
                    eligible = False
                    break
            if eligible:
                schedule["320"].append(course)
                scheduled = True

    if len(schedule["120"]) < 3 and scheduled == False:
        if time.find("fall") != -1 and time.find("odd") == -1:
            eligible = True
            for prereq in prerequisites:
                if prereq not in schedule["119"] and prereq not in schedule["220"] and prereq not in schedule["320"]:
                    eligible = False
                    break
            if eligible:
                schedule["120"].append(course)
                scheduled = True
    if len(schedule["221"]) < 1 and scheduled == False:
        if time.find("jan") != -1 and time.find("even") == -1:
            eligible = True
            for prereq in prerequisites:
                if prereq not in schedule["119"] and prereq not in schedule["220"] and prereq not in schedule["320"] and prereq not in schedule["120"]:
                    eligible = False
                    break
            if eligible:
                schedule["221"].append(course)
                scheduled = True
    if len(schedule["321"]) < 1 and scheduled == False:
        if time.find("spring") != -1 and time.find("even") == -1:
            eligible = True
            for prereq in prerequisites:
                if prereq not in schedule["119"] and prereq not in schedule["220"] and prereq not in schedule["320"] and prereq not in schedule["120"] and prereq not in schedule["221"]:
                    eligible = False
                    break
            if eligible:
                schedule["321"].append(course)
                scheduled = True
    if len(schedule["121"]) < 1 and scheduled == False:
        if time.find("fall") != -1 and time.find("even") == -1:
            eligible = True
            for prereq in prerequisites:
                if prereq not in schedule["119"] and prereq not in schedule["220"] and prereq not in schedule["320"] and prereq not in schedule["120"] and prereq not in schedule["221"] and prereq not in schedule["321"]:
                    eligible = False
                    break
            if eligible:
                schedule["121"].append(course)
                scheduled = True
    if len(schedule["222"]) < 1 and scheduled == False:
        if time.find("jan") != -1 and time.find("odd") == -1:
            eligible = True
            for prereq in prerequisites:
                if prereq not in schedule["119"] and prereq not in schedule["220"] and prereq not in schedule["320"] and prereq not in schedule["120"] and prereq not in schedule["221"] and prereq not in schedule["321"] and prereq not in schedule["121"]:
                    eligible = False
                    break
            if eligible:
                schedule["222"].append(course)
                scheduled = True
    if len(schedule["322"]) < 1 and scheduled == False:
        if time.find("fall") != -1 and time.find("odd") == -1:
            eligible = True
            for prereq in prerequisites:
                if prereq not in schedule["119"] and prereq not in schedule["220"] and prereq not in schedule["320"] and prereq not in schedule["120"] and prereq not in schedule["221"] and prereq not in schedule["321"] and prereq not in schedule["121"] and prereq not in schedule["222"]:
                    eligible = False
                    break
            if eligible:
                schedule["322"].append(course)
                scheduled = True
    if len(schedule["122"]) < 1 and scheduled == False:
        if time.find("fall") != -1 and time.find("odd") == -1:
            eligible = True
            for prereq in prerequisites:
                if prereq not in schedule["119"] and prereq not in schedule["220"] and prereq not in schedule["320"] and prereq not in schedule["120"] and prereq not in schedule["221"] and prereq not in schedule["321"] and prereq not in schedule["121"] and prereq not in schedule["222"] and prereq not in schedule["322"]:
                    eligible = False
                    break
            if eligible:
                schedule["122"].append(course)
                scheduled = True
    if len(schedule["223"]) < 1 and scheduled == False:
        if time.find("fall") != -1 and time.find("odd") == -1:
            eligible = True
            for prereq in prerequisites:
                if prereq not in schedule["119"] and prereq not in schedule["220"] and prereq not in schedule["320"] and prereq not in schedule["120"] and prereq not in schedule["221"] and prereq not in schedule["321"] and prereq not in schedule["121"] and prereq not in schedule["222"] and prereq not in schedule["322"] and prereq not in schedule["122"]:
                    eligible = False
                    break
            if eligible:
                schedule["223"].append(course)
                scheduled = True
    if len(schedule["323"]) < 1 and scheduled == False:
        if time.find("fall") != -1 and time.find("odd") == -1:
            eligible = True
            for prereq in prerequisites:
                if prereq not in schedule["119"] and prereq not in schedule["220"] and prereq not in schedule["320"] and prereq not in schedule["120"] and prereq not in schedule["221"] and prereq not in schedule["321"] and prereq not in schedule["121"] and prereq not in schedule["222"] and prereq not in schedule["322"] and prereq not in schedule["122"] and prereq not in schedule["223"]:
                    eligible = False
                    break
            if eligible:
                schedule["323"].append(course)
                scheduled = True

    if not scheduled:
        print("Unable to schedule " + course)
        return False
    return True
    
def planGroupCourse(course):
    numOfCourses = parseChoose(course)
    shouldPlan = True
    i = 1
    count = 0
    while i < len(course):
        if course[i] in plannedCourses:
            count += 1
        if count >= numOfCourses:
            shouldPlan = False
            return True
        i += 1
    if shouldPlan:
        index = 1
        count = 0
        while count < numOfCourses and index < len(course):
            if planIndividualCourse(course[index]):
                count += 1
            index += 1
        return count < numOfCourses

def plan(course):
    if type(course) == type(""):
        if not planIndividualCourse(course):
            return False
    elif type(course) == type([]):
        planGroupCourse(course)
    return True

def bruteForce(courses):
    plan(courses[0])
    if len(courses) == 1:
        return 0
    return bruteForce(courses[1:])

# remove labels like "Core Courses"
i = 0
while i < len(degree.courses):
    if type(degree.courses[i]) == type("") and len(degree.courses[i]) >= 12:
        del degree.courses[i]
        i -= 1
    i += 1
bruteForce(degree.courses)
print(schedule)