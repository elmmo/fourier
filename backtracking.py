# import timeit

# code_to_test = """
from scrape import Degree, Department
from utils import parseChoose, getConstraints, createAssociation, TopologicalSort


# From the course's constraints we pull out the semesters that the course can be taken and the course's prerequisites
def getPossibleSemesters(course):
    if type(course) == list:
        i = 1
        while i < len(course):
            getPossibleSemesters(course[i])
            i += 1
    else:
        possibleSemesters[course] = []
        time = 'none'
        constraints = getConstraints(course, degree)
        time = constraints[0].lower()
        if time == 'none':
            time = 'fall and spring semesters'
        standing = constraints[2]

        for semester in schedule.keys():
            # Odd Fall
            if time.find('even') == -1 and time.find('fall') != -1 and semester[0] == '1' and int(semester[2]) % 2 != 0:
                possibleSemesters[course].append(semester)
            # Odd Jan
            if time.find('even') == -1 and time.find('jan') != -1 and semester[0] == '2' and int(semester[2]) % 2 != 0:
                possibleSemesters[course].append(semester)
            # Odd Spring
            if time.find('even') == -1 and time.find('spring') != -1 and semester[0] == '3' and int(semester[2]) % 2 != 0:
                possibleSemesters[course].append(semester)
            # Even Fall
            if time.find('odd') == -1 and time.find('fall') != -1 and semester[0] == '1' and int(semester[2]) % 2 == 0:
                possibleSemesters[course].append(semester)
            # Even Jan
            if time.find('odd') == -1 and time.find('jan') != -1 and semester[0] == '2' and int(semester[2]) % 2 == 0:
                possibleSemesters[course].append(semester)
            # Even Spring
            if time.find('odd') == -1 and time.find('spring') != -1 and semester[0] == '3' and int(semester[2]) % 2 == 0:
                possibleSemesters[course].append(semester)

            # Freshman Standing
            if standing.lower().find('freshman') != -1 and semester != '119' and semester != '220' and semester != '320' and semester in possibleSemesters[course]:
                possibleSemesters[course].remove(semester)
            # Sophomore Standing
            if standing.lower().find('sophomore') != -1 and semester != '120' and semester != '221' and semester != '321' and semester in possibleSemesters[course]:
                possibleSemesters[course].remove(semester)
            # Junior Standing
            if standing.lower().find('junior') != -1 and semester != '121' and semester != '222' and semester != '322' and semester in possibleSemesters[course]:
                possibleSemesters[course].remove(semester)
            # Senior Standing
            if standing.lower().find('senior') != -1 and semester != '122' and semester != '223' and semester != '323' and semester in possibleSemesters[course]:
                possibleSemesters[course].remove(semester) 


def hasPrereqBeenFulfilled(prereq, targetSemester):
        for previousSemester in schedule:
            if targetSemester != previousSemester and (targetSemester[1:3] > previousSemester[1:3] or (targetSemester[1:3] == previousSemester[1:3] and (targetSemester[0] == '1') or (targetSemester[0] == '3' and previousSemester[0] == '2'))):
                if prereq in schedule[previousSemester]:
                    return True
                    
            


def backtrack(courses, numToSchedule):
    i = 0
    while i < len(courses):
        # If course is a group course recurse on that list of courses passing in the number of courses in the group to schedule
        if type(courses[i]) == list:
            backtrack(courses[i][1:], parseChoose(courses[i]))
        elif numToSchedule != 0:
            scheduled = False

            # Create an entry in attempts if one doesn't exist so we can check attempts for every course
            if courses[i] not in attempts:
                attempts[courses[i]] = []

            # Get prerequisites for the course and add missed Physics 2 prerequisite
            prerequisites = getConstraints(courses[i], degree)[1]
            if courses[i] == 'PS 153' and prerequisites == []:
                prerequisites = ['PS 151']

            # Go through each possible semester for this course that hasn't been attempted
            for targetSemester in possibleSemesters[courses[i]]:
                if targetSemester not in attempts[courses[i]]:
                    canSchedule = True

                    # Check if each prerequisite has been fulfilled
                    for prereq in prerequisites:
                        if not hasPrereqBeenFulfilled(prereq, targetSemester):
                            canSchedule = False

                    # Check if the semester is full
                    if ((targetSemester[0] == '1' or targetSemester[0] == '3') and len(schedule[targetSemester]) >= 3) or (targetSemester[0] == '2' and len(schedule[targetSemester]) >= 1):
                        canSchedule = False

                    # Schedule the course
                    if canSchedule:
                        schedule[targetSemester].append(courses[i])
                        attempts[courses[i]].append(courses[i])
                        scheduled = True
                        break
            if scheduled:
                numToSchedule -= 1
                print('Scheduled ' + str(courses[i]))
            else:
                print('Unable to schedule ' + str(courses[i]))
                if numToSchedule > -1000 and numToSchedule < 0:
                    for semester in schedule:
                        if courses[i-1] in schedule[semester]:
                            schedule[semester].remove(courses[i-1])
                    i -= 2
        i += 1






# MAIN

url = 'http://catalog.whitworth.edu/undergraduate/mathcomputerscience/#text'
dept = Department(url)
degree = dept.getDegree()
debug = False

schedule = {
    '119': [],
    '220': [],
    '320': [],
    '120': [],
    '221': [],
    '321': [],
    '121': [],
    '222': [],
    '322': [],
    '122': [],
    '223': [],
    '323': [],
}

possibleSemesters = {}
scheduledCourses = []
attempts = {}

# remove labels like 'Core Courses'
i = 0
while i < len(degree.courses):
    if type(degree.courses[i]) == str and len(degree.courses[i]) >= 12:
        del degree.courses[i]
        i -= 1
    i += 1

assoc = createAssociation(degree)
degree.courses = TopologicalSort(assoc[0])

recommended = []
i = 0
while i < len(degree.courses):
    # While topologically sorting, we renamed group courses to make them easier to work with
    # This loop restores their names
    j = 0
    while j < len(assoc[1]):
        if degree.courses[i] == j:
            degree.courses[i] = assoc[1][j]
        j += 1

    # Remove lab courses and other unwanted characters
    if type(degree.courses[i]) == list:
        continueFlag = False
        j = 0
        while j < len(degree.courses[i]):
            if degree.courses[i][j].find('L') != -1:
                del degree.courses[i]
                i -= 1
                continueFlag = True
                break
                
            if degree.courses[i][j].find('L') != -1:
                del degree.courses[i]
                i -= 1
                continueFlag = True
                break
            if degree.courses[i][j].lower().find('or') != -1:
                degree.courses[i][j] = degree.courses[i][j].replace('or', '')
                degree.courses[i][j] = degree.courses[i][j].replace('OR', '')
                degree.courses[i][j] = degree.courses[i][j].strip()
            if degree.courses[i][j].find('&') != -1:
                degree.courses[i][j] = degree.courses[i][j].replace('&', '')
                degree.courses[i][j] = degree.courses[i][j].strip()
            if degree.courses[i][j].strip() == '':
                del degree.courses[i]
                i -= 1
                continueFlag = True
                break    
            j += 1
        
        # Move recommended courses to the end so they are given lowest priority
        if degree.courses[i][0].find('Recommended') != -1:
            recommended.append(degree.courses[i])
            del degree.courses[i]
            i -= 1
            continueFlag = True

        if continueFlag:
            continue
    else:
        if degree.courses[i].find('L') != -1:
            del degree.courses[i]
            i -= 1
            continue
        if degree.courses[i].lower().find('or') != -1:
            degree.courses[i] = degree.courses[i].replace('or', '')
            degree.courses[i] = degree.courses[i].replace('OR', '')
            degree.courses[i] = degree.courses[i].strip()
        if degree.courses[i].find('&') != -1:
            degree.courses[i] = degree.courses[i].replace('&', '')
            degree.courses[i] = degree.courses[i].strip()
        if degree.courses[i].strip() == '':
            del degree.courses[i]
            i -= 1
            continue
    i += 1

# Move recommended courses to the end so they are given lowest priority
for val in recommended:
    degree.courses.append(val)



for course in degree.courses:
    getPossibleSemesters(course)


print(degree.title)
backtrack(degree.courses, -1)
print('\n')
for x in schedule:
    print(x + ' - ' + str(schedule[x]))
# """

# elapsed_time = timeit.timeit(code_to_test, number=100)/100
# print(elapsed_time)
