import re
import random
from scrape import Degree, Department
from utils import parseChoose


# This function parses the constraints for a course and splits them into time constraints and prerequisites
def getConstraints(course):
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
            if prerequisites[i] not in degree.coursesByName or prerequisites[i].find("L") != -1:
                del prerequisites[i]
                i -= 1
            i += 1
    return time, prerequisites, standing

# This function looks at the constraints for each course and tries to fit it in the schedule
def planIndividualCourse(course):
    if course.find("L") != -1:
        return False
    if course.lower().find("or") != -1:
        course = course.replace("or", "")
        course = course.replace("OR", "")
        course = course.strip()
    if course.find("&") != -1:
        course = course.replace("&", "")
        course = course.strip()
    if course.strip() == "":
        return False
    
    
    # From the course's constraints we pull out the semesters that the course can be taken and the course's prerequisites
    time = "none"
    prerequisites = []
    constraints = getConstraints(course)
    time = constraints[0].lower()
    if time == "none":
        time = "fall and spring semesters"
    prerequisites = constraints[1]
    standing = constraints[2]
    scheduled = False

    flags = {
        "119": False,
        "220": False,
        "320": False,
        "120": False,
        "221": False,
        "321": False,
        "121": False,
        "222": False,
        "322": False,
        "122": False,
        "223": False,
        "323": False,
    }

    # For each semester we look at if the course can be taken that semester based on time constraints
    # As well as if the course's prerequisites have already been taken
    # If both of these requirements are met, the class is scheduled for this semester
    if course not in scheduledCourses:
        if len(schedule["119"]) < 3 and (standing == "freshman" or standing == "none"):
            if time.find("fall") != -1 and time.find("even") == -1:
                eligible = len(prerequisites) == 0
                flags["119"] = True
                if eligible:
                    schedule["119"].append(course)
                    scheduledCourses.append(course)
                    scheduled = True
        if len(schedule["220"]) < 1 and scheduled == False and (standing == "freshman" or standing == "none"):
            if time.find("jan") != -1 and time.find("odd") == -1:
                eligible = True
                flags["220"] = True
                for prereq in prerequisites:
                    if prereq not in schedule["119"]:
                        eligible = False
                        break
                if eligible:
                    schedule["220"].append(course)
                    scheduledCourses.append(course)
                    scheduled = True
        if len(schedule["320"]) < 3 and scheduled == False and (standing == "freshman" or standing == "none"):
            if time.find("spring") != -1 and time.find("odd") == -1:
                eligible = True
                flags["320"] = True
                for prereq in prerequisites:
                    if prereq not in schedule["119"] and prereq not in schedule["220"]:
                        eligible = False
                        break
                if eligible:
                    schedule["320"].append(course)
                    scheduledCourses.append(course)
                    scheduled = True
        if len(schedule["120"]) < 3 and scheduled == False and (standing == "sophomore" or standing == "none"):
            if time.find("fall") != -1 and time.find("odd") == -1:
                eligible = True
                flags["120"] = True
                for prereq in prerequisites:
                    if prereq not in schedule["119"] and prereq not in schedule["220"] and prereq not in schedule["320"]:
                        eligible = False
                        break
                if eligible:
                    schedule["120"].append(course)
                    scheduledCourses.append(course)
                    scheduled = True
        if len(schedule["221"]) < 1 and scheduled == False and (standing == "sophomore" or standing == "none"):
            if time.find("jan") != -1 and time.find("even") == -1:
                eligible = True
                flags["221"] = True
                for prereq in prerequisites:
                    if prereq not in schedule["119"] and prereq not in schedule["220"] and prereq not in schedule["320"] and prereq not in schedule["120"]:
                        eligible = False
                        break
                if eligible:
                    schedule["221"].append(course)
                    scheduledCourses.append(course)
                    scheduled = True
        if len(schedule["321"]) < 3 and scheduled == False and (standing == "sophomore" or standing == "none"):
            if time.find("spring") != -1 and time.find("even") == -1:
                eligible = True
                flags["321"] = True
                for prereq in prerequisites:
                    if prereq not in schedule["119"] and prereq not in schedule["220"] and prereq not in schedule["320"] and prereq not in schedule["120"] and prereq not in schedule["221"]:
                        eligible = False
                        break
                if eligible:
                    schedule["321"].append(course)
                    scheduledCourses.append(course)
                    scheduled = True
        if len(schedule["121"]) < 3 and scheduled == False and (standing == "junior" or standing == "none"):
            if time.find("fall") != -1 and time.find("even") == -1:
                eligible = True
                flags["121"] = True
                for prereq in prerequisites:
                    if prereq not in schedule["119"] and prereq not in schedule["220"] and prereq not in schedule["320"] and prereq not in schedule["120"] and prereq not in schedule["221"] and prereq not in schedule["321"]:
                        eligible = False
                        break
                if eligible:
                    schedule["121"].append(course)
                    scheduledCourses.append(course)
                    scheduled = True
        if len(schedule["222"]) < 1 and scheduled == False and (standing == "junior" or standing == "none"):
            if time.find("jan") != -1 and time.find("odd") == -1:
                eligible = True
                flags["222"] = True
                for prereq in prerequisites:
                    if prereq not in schedule["119"] and prereq not in schedule["220"] and prereq not in schedule["320"] and prereq not in schedule["120"] and prereq not in schedule["221"] and prereq not in schedule["321"] and prereq not in schedule["121"]:
                        eligible = False
                        break
                if eligible:
                    schedule["222"].append(course)
                    scheduledCourses.append(course)
                    scheduled = True
        if len(schedule["322"]) < 3 and scheduled == False and (standing == "junior" or standing == "none"):
            if time.find("spring") != -1 and time.find("odd") == -1:
                eligible = True
                flags["322"] = True
                for prereq in prerequisites:
                    if prereq not in schedule["119"] and prereq not in schedule["220"] and prereq not in schedule["320"] and prereq not in schedule["120"] and prereq not in schedule["221"] and prereq not in schedule["321"] and prereq not in schedule["121"] and prereq not in schedule["222"]:
                        eligible = False
                        break
                if eligible:
                    schedule["322"].append(course)
                    scheduledCourses.append(course)
                    scheduled = True
        if len(schedule["122"]) < 3 and scheduled == False and (standing == "senior" or standing == "none"):
            if time.find("fall") != -1 and time.find("odd") == -1:
                eligible = True
                flags["122"] = True
                for prereq in prerequisites:
                    if prereq not in schedule["119"] and prereq not in schedule["220"] and prereq not in schedule["320"] and prereq not in schedule["120"] and prereq not in schedule["221"] and prereq not in schedule["321"] and prereq not in schedule["121"] and prereq not in schedule["222"] and prereq not in schedule["322"]:
                        eligible = False
                        break
                if eligible:
                    schedule["122"].append(course)
                    scheduledCourses.append(course)
                    scheduled = True
        if len(schedule["223"]) < 1 and scheduled == False and (standing == "senior" or standing == "none"):
            if time.find("jan") != -1 and time.find("odd") == -1:
                eligible = True
                flags["223"] = True
                for prereq in prerequisites:
                    if prereq not in schedule["119"] and prereq not in schedule["220"] and prereq not in schedule["320"] and prereq not in schedule["120"] and prereq not in schedule["221"] and prereq not in schedule["321"] and prereq not in schedule["121"] and prereq not in schedule["222"] and prereq not in schedule["322"] and prereq not in schedule["122"]:
                        eligible = False
                        break
                if eligible:
                    schedule["223"].append(course)
                    scheduledCourses.append(course)
                    scheduled = True
        if len(schedule["323"]) < 3 and scheduled == False and (standing == "senior" or standing == "none"):
            if time.find("spring") != -1 and time.find("odd") == -1:
                eligible = True
                flags["323"] = True
                for prereq in prerequisites:
                    if prereq not in schedule["119"] and prereq not in schedule["220"] and prereq not in schedule["320"] and prereq not in schedule["120"] and prereq not in schedule["221"] and prereq not in schedule["321"] and prereq not in schedule["121"] and prereq not in schedule["222"] and prereq not in schedule["322"] and prereq not in schedule["122"] and prereq not in schedule["223"]:
                        eligible = False
                        break
                if eligible:
                    schedule["323"].append(course)
                    scheduledCourses.append(course)
                    scheduled = True

    if not scheduled:
        if debug:
            print("\nUnable to schedule " + course)
        if debug:
            if (course in scheduledCourses):
                print("Previously scheduled")
            else:
                print(prerequisites)
                print(time)
                print(flags)
        return False
    if debug:
        print("\nScheduled " + course)
    return True
    
# When we get a "choose n courses" type, this function takes each course option and calls the planIndividualCourse function on it
# If a group of courses is recommended, we try to schedule all of them
def planGroupCourse(course):
    numOfCourses = parseChoose(course)
    shouldPlan = True
    i = 1
    count = 0
    if course[0].lower().find("recommend") == -1:
        while i < len(course):
            if course[i] in scheduledCourses:
                count += 1
            if count >= numOfCourses:
                shouldPlan = False
                return True
            i += 1
    else:
        numOfCourses = len(course)-1
    if shouldPlan:
        index = 1
        count = 0
        while count < numOfCourses and index < len(course):
            if planIndividualCourse(course[index]):
                count += 1
            index += 1
        return count < numOfCourses

# Duplicate all courses except recommended courses and move recommended courses to the end
# Because of the defined order of the courses some classes weren't getting scheduled because their prerequisites were being scheduled after them
# Now each course except recommended courses will try to be scheduled twice
def duplicate(courses):
    recommended = []
    temp = []
    i = 0
    while i < len(courses):
        if type(courses[i]) == type([]) and courses[i][0].find("Recommended") != -1:
            recommended.append(courses[i])
            del courses[i]
        if i < len(courses):
            temp.append(courses[i])
        i += 1
    for val in temp:
        courses.append(val)
    for val in recommended:
        courses.append(val)
    return courses

# Directs each course to the method it should use for planning itself
def plan(course):
    # If it is a single course, send it to the function for planning individual courses
    if type(course) == type(""):
        if not planIndividualCourse(course):
            return False
    # If it is a "choose n courses" type, send it to the function for planning group courses
    elif type(course) == type([]):
        planGroupCourse(course)
    return True

# Recursive brute force function
def bruteForce(courses):
    for course in courses:
        plan(course)



# MAIN

url = 'http://catalog.whitworth.edu/undergraduate/mathcomputerscience/#text'
dept = Department(url)
degree = dept.getDegree()
debug = True

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

scheduledCourses = []

# remove labels like "Core Courses"
i = 0
while i < len(degree.courses):
    if type(degree.courses[i]) == type("") and len(degree.courses[i]) >= 12:
        del degree.courses[i]
        i -= 1
    i += 1

degree.courses = duplicate(degree.courses)
bruteForce(degree.courses)
print("\n")
for x in schedule:
    print(x + " - " + str(schedule[x]))
