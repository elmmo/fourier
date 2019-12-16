from bs4 import BeautifulSoup
import requests
import re 
from utils import Term, formatData, Alternation, Term

def printDegreeKey(): 
    print("Degree Plan Key")
    print("index | Degree Option")
    print("------|----------------------------------------")
    print("  0   | Mathematics - General Major, B.A.")
    print("  1   | Mathematics - Education Major, B.A.")
    print("  2   | Mathematics Major, B.S.")
    print("  3   | Mathematical Economics Major, B.A.")
    print("  4   | Computer Science Core Courses")
    print("  5   | International Project Management Option")
    print("  6   | Business Option")
    print("  7   | Network Systems Option")
    print("  8   | Computer Science Major, B.S.")
    print("  9   | Bioinformatics Major, B.S.")
    print("  10  | Human-Computer Interaction Major, B.A.")
    print("  11  | Mathematics Minor")
    print("  12  | Computer Science Minor")
    print("  13  | Information Technology Minor")
    
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
    def getDegree(self, degIndex = -1): 
        printDegreeKey(); 
        if degIndex == -1:
            choice = input("Which degree would you like to create a list of requirements for? ")
            choice = int(choice.strip())
        else: 
            choice = degIndex
        degree = self.majorsClasses[choice] # Change the index here to change the degree plan according to the key above
        courses = []
        coursesByName = {}
        self.__parseCourseRequirements(degree, courses, coursesByName)
        self.__addFootnotes(courses)
        title = self.__getTitle(degree)
        constraints = self.__getConstraints()
        print(courses)
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
            title = "{} {}".format(titleParts[0], titleParts[1])
            descr = rows[1].get_text()
            # search for prerequisites and corequisites 
            prereqs = re.search(r'Prerequisite:(\s[\w,]*)*', descr)
            parsedPrereqs = []
            if (prereqs != None):
                # put prereq marker at the front to signify constraint type
                parsedPrereqs.append("Prerequisite")
                # find all classes that are prereqs 
                parsedPrereqs.append(re.findall(r'([A-Z]{1,4}\s\w{1,4})', prereqs.group(0))) 
            # search for spring / fall / jan timing 
            timesOffered = re.findall(r'jan|spring|fall', descr.lower())
            if timesOffered != []: 
                formatData(timesOffered, Term, "Time", parsedPrereqs)
            # search for even / odd year timing 
            timesOffered = re.findall(r'even|odd', descr.lower())
            if timesOffered != []: 
                formatData(timesOffered, Alternation, "Alternation", parsedPrereqs)
            if parsedPrereqs != []: 
                constraints.update( { title : parsedPrereqs })
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
        # group requirements like "two of the following courses" into arrays of the form:
        # ['two of the following courses', 'MA 317', 'MA 357', 'MA 410', 'MA 430W', 'MA 430', 'MA 440']
        # So it is easier to access which classes are under which requirements
        i = 0
        while i < len(courses):
            courseNote = courses[i] if (type(courses[i]) == str) else courses[i][0]
            if courseNote.find("of the following") != -1:
                j = i + 1
                while j < len(courses):
                    # set to ignore labs 
                    if len(courses[j]) > 12:
                        break
                    else:
                        if type(courses[i]) == type([]):
                            courses[i].append(courses[j])
                        else:
                            courses[i] = [courses[i], courses[j]]
                    j += 1
                k = 0
                while k < len(courses[i])-1:
                    del courses[i+1]
                    k += 1

            i += 1
        return courses, coursesByName
