from scrape import Department
from utils import parseChoose

url = 'http://catalog.whitworth.edu/undergraduate/mathcomputerscience/#text'
dept = Department(url)
degree = dept.getDegree()

def createCourseList(reqs, originalArr, chooseInt = -1): 
    chosen = 0
    for x in range(len(reqs)):
        if type(reqs[x]) == str and reqs[x] in degree.coursesByName: 
            if chooseInt == -1: 
                originalArr.append(reqs[x])
            # if iterating through a sub-list, will take the first x courses, bounded by chooseInt
            elif chosen < chooseInt: 
                originalArr.append(reqs[x])
                chosen += 1
        elif type(reqs[x]) == list: 
            choose = parseChoose(reqs[x][0])
            createCourseList(reqs[x],originalArr,choose)

def topDownDP(): 
    courseList = [] 
    createCourseList(degree.courses, courseList)
    print(courseList)

print("PROGRAM RUNNING")
topDownDP()