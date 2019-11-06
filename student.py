class Student:
    """
    Holds all the information of a student.

    Args:
        cwid (str): CWID of the student.
        name (str): Name of the student.
        major (str): Major of the student.

    Attributes:
        cwid (str): CWID of the student.
        name (str): Name of the student.
        major (str): Major of the student.
        courses_completed (set): Courses completed by the student.
        grades (dict): (Course Code -> Grade) Grades of all the completed courses.
    """
    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.courses_completed = set()
        self.grades = {}                # key:CourseID -> val:Grades
    
    def __str__(self):
        return "CWID: {}, Name: {}, Major: {}, Courses Completed: {}, Grades: {}".format(self.cwid, self.name, self.major, self.courses_completed, self.grades)