from scrape import Department
from utils import parseChoose, Term
from math import floor

url = 'http://catalog.whitworth.edu/undergraduate/mathcomputerscience/#text'
dept = Department(url)
degree = dept.getDegree()

fullyPlanned = set()
baseYear = 19

def createCoursePlan(reqs, originalArr, chooseInt = -1): 
    chosen = 0
    for x in range(len(reqs)):
        if type(reqs[x]) == str and reqs[x] in degree.coursesByName: 
            # if adding in courses that are always required 
            if chooseInt == -1: 
                originalArr[reqs[x]] = 0
            # if iterating through a sub-list, will take the first x courses, bounded by chooseInt
            elif chosen < chooseInt: 
                originalArr[reqs[x]] = 0 
                chosen += 1
        elif type(reqs[x]) == list: 
            choose = parseChoose(reqs[x][0])
            createCoursePlan(reqs[x],originalArr,choose)

def topDownDP(): 
    # generate list of courses an user must take 
    courseList = {}
    createCoursePlan(degree.courses, courseList)
    print(courseList)
    # recursively add classes 
    planClass('CS171', courseList)


# def planClasses()
#     if courseList[0] in degree.constraints: 
#         classConstraints = degree.constraints[courseList[0]]
#         preReqStart = 1
#         if "Prerequisite" in classConstraints: 
#             preReqStart = classConstraints.index("Prerequisite")
#             planClasses(classConstraints[preReqStart+1:])
#         if planClass(courseList[0], classConstraints, classConstraints[preReqStart+1:]) == 1: 
#             planClasses(courseList[1:])
#             print(plan)
#         else: 
#             print("Error (:)")
#     elif courseList[0] == "Time" or courseList[0] == "Standing" or courseList[0] == "Alternation":
#         return 1

def planClass(name, plan): 
    # if already planned, return term 
    if name in fullyPlanned: 
        return plan[name]
    # set operating defaults to build off of 
    term = 1
    year = baseYear 
    # handle prerequisites 
    if name in degree.constraints: 
        classConstraints = degree.constraints[name]
        if "Prerequisite" in classConstraints: 
            prereqs = classConstraints[classConstraints.index("Prerequisite")+1]
            
    

    



# def planClass(name, constraints, prereqs = []):
#     possible = [119,220,320,120,221,321,121,222,322,123,223]
#     if name in fullyPlanned: 
#         return 1
#     alternation, time = [],[]
#     alternationStart = constraints.index("Alternation") if "Alternation" in constraints else len(constraints)
#     if alternationStart != len(constraints):
#         alternation = constraints[alternationStart+1]
#     if ("Time" in constraints):
#         timeStart = constraints.index("Time")
#         time = constraints[timeStart+1:alternationStart]
#     for term in possible:
#         if (time != []):
#             # disqualified if term doesn't fit constraint 
#             sem = floor(term/100)
#             if sem not in time:
#                 print("Removed {} because {} isn't a valid scheduling term".format(term,sem))
#                 possible.remove(term)
#                 break 
#             # disqualified if sem already fully planned 
#             maxload = 3 if sem == 1 or sem == 3 else 2
#             if len(plan[str(term)]) == maxload: 
#                 print("Removed {} because term was at max fullness {}.".format(term,maxload))
#                 possible.remove(term)
#                 break 
#         if (alternation != []):
#             # disqualified if course only available even years and it's an odd year 
#             year = term % 100
#             if year % 2 == 0 and 2 not in alternation: 
#                 print("Removed {} because needed an odd year and year was even.".format(term))
#                 possible.remove(term)
#                 break 
#             # disqualified if course only available odd years and it's an even year 
#             elif year % 2 != 0 and 1 not in alternation: 
#                 print("Removed {} because needed an even year and year was odd.".format(term))
#                 possible.remove(term)
#                 break 
#         if (prereqs != []):
#             for p in prereqs:
#                 if p in plan[str(term)]: 
#                     print("Removed {} because prereq {} was in same term.".format(term,p))
#                     possible.remove(term)
#                     break 
#     plan[str(possible[0])].append(name)
#     fullyPlanned.append(name)
#     return 1 

print("\nPROGRAM RUNNING")
topDownDP()
