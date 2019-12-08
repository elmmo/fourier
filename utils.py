def parseChoose(course):
    if type(course) == type(""):
        return 1
    numOfCourses = 0
    if course[0].lower().find("two") != -1:
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