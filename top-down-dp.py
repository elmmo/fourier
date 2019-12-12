from scrape import Department

url = 'http://catalog.whitworth.edu/undergraduate/mathcomputerscience/#text'
dept = Department(url)
degree = dept.getDegree()