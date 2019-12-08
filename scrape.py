from bs4 import BeautifulSoup
import requests

# Degree Plan Key
# index | Degree Option
# ------|----------------------------------------
#   0   | Mathematics - General Major, B.A.
#   1   | Mathematics - Education Major, B.A.
#   2   | Mathematics Major, B.S.
#   3   | Mathematical Economics Major, B.A.
#   4   | Computer Science Core Courses
#   5   | International Project Management Option
#   6   | Business Option
#   7   | Network Systems Option
#   8   | Computer Science Major, B.S.
#   9   | Bioinformatics Major, B.S.
#  10   | Human-Computer Interaction Major, B.A.
#  11   | Mathematics Minor
#  12   | Mathematics Minor
#  13   | Computer Science Minor
#  14   | Information Technology Minor

class Degree: 
    def __init__(self, title, courses, coursesByName, constraints): 
        self.title = title
        self.courses = courses
        self.coursesByName = coursesByName
        self.constraints = constraints

class Department: 
    def __init__(self, link):
        self.link = link 
        self.page = requests.get(link)
        if (self.page.status_code != 200): 
            raise ValueError("Invalid page response. Could not connect.")
        self.soup = BeautifulSoup(self.page.text, 'html.parser')
        self.optionsByTitle = self.soup.find_all('h3')
        self.majorsClasses = self.soup.find_all(class_='sc_courselist')

    # will ask for user input that will search for and specify the correct degree plan 
    def getDegree(self): 
        print("Implement later: ask for degree name and look up degree by name")
        # for i in range(len(self.optionsByTitle)):
        #     print(self.optionsByTitle[i].get_text())
        degree = self.majorsClasses[8] # Change the index here to change the degree plan according to the key above
        courses = []
        coursesByName = {}
        self.__parseCourseRequirements(degree, courses, coursesByName)
        self.__addFootnotes(courses)
        title = self.__getTitle(degree)
        constraints = self.__getConstraints()
        return Degree(title, courses, coursesByName, constraints)
    
    # checks for any extra degree notes 
    def __addFootnotes(self, courses):
        footnotes = self.soup.find_all(class_='sc_footnotes')
        for i in range(len(footnotes)):
            courses.append(footnotes[i].find('p').get_text())
        
    # gets the title of the degree 
    def __getTitle(self, degree):
        return degree.find_all('h3')[0].get_text()

    # gets all the constraints (prereqs, time availability) associated with all the classes in the department 
    # returns a dictionary. Key: class name, value: constraints 
    def __getConstraints(self):
        courses = self.soup.find_all(class_="courseblock")
        constraints = {}
        for i in range(len(courses)):
            rows = courses[i].find_all('tr')
            titleParts = rows[0].get_text().split(" ")
            descr = rows[1].get_text()
            constraintIndex = descr.find('Prerequisite')
            if (constraintIndex != -1):
                title = "{} {}".format(titleParts[0], titleParts[1]) 
                constraints.update({ title : descr[constraintIndex:] })
        # split constraints values by "." separating them into prerequisites and semesters offered
        for course in constraints:
            constraints[course] = constraints[course].split(".")
            for i in range(len(constraints[course])):
                constraints[course][i] = constraints[course][i].strip()
                if constraints[course][i] == "":
                    del constraints[course][i]
        return constraints

    # gets the table corresponding to the core courses
    def __getCoreCoursesTitle(self):
        for i in range(len(self.majorsClasses)):
            title = self.__getTitle(self.majorsClasses[i])
            if (title.find("Core Courses") != -1):
                return self.majorsClasses[i]

    # strips the input of trailing and leading whitespace as well as bad characters 
    def __stripInvalidChars(self, input): 
        if (input.find("\xa0") != -1):
            input = input.replace("\xa0", " ") 
        return input.strip()
        
    # returns a degree object 
    def __parseCourseRequirements(self, degree, courses, coursesByName):
        rows = degree.find_all('tr')
        for i in range(len(rows)):
            courseInfo = rows[i].find_all('td')
            if (len(courseInfo) > 0):
                # collect data 
                cInfo = courseInfo[0].get_text()
                cName = courseInfo[1].get_text()
                # in the case that core classes are a part of the degree but not all listed under it 
                if (cInfo.lower().find('core classes') != -1 and len(cName) > 0):
                    self.__parseCourseRequirements(self.__getCoreCoursesTitle(), courses, coursesByName)
                # special "&" case
                if (cInfo.find("&") != -1):
                    cInfo = cInfo.split("\xa0")
                    cName = cName.split("and")
                    while (len(cInfo) > 0):
                        # special case add to local storage 
                        courses.append(cInfo[0])
                        cInfo[0] = cInfo[0].replace("&", "")
                        coursesByName.update({ cInfo[0].strip() : cName[0].strip() })
                        del cInfo[0]
                        del cName[0]
                else:
                    # input validation in the case that there's an or option 
                    self.__stripInvalidChars(cInfo)
                    # add to local storage 
                    courses.append(cInfo) 
                    if (len(cInfo) < 8 and len(cName) > 1): # for coursesByName, ignore all comments 
                        coursesByName.update({ cInfo : cName })
        return courses, coursesByName

url = 'http://catalog.whitworth.edu/undergraduate/mathcomputerscience/#text'
dept = Department(url)
degree = dept.getDegree()

print(degree.title)
print("\nCourses By Name:")
print(degree.coursesByName)
print("\nCourses:")
print(degree.courses)
