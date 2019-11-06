from collections import defaultdict

class Instructor:
    """
    Holds all the information of an instructor.

    Args:
        cwid (str): CWID of the instructor.
        name (str): Name of the instructor.
        department (str): Department instructor works in.

    Attributes:
        cwid (str): CWID of the instructor.
        name (str): Name of the instructor.
        department (str): Department instructor works in.
        courses_taught (set): The courses taught by the professor
        student_count (dict): (Course Code -> Count) Number of students
            that enrolled in the course
    """
    def __init__(self, cwid, name, department):
        self.name = name
        self.cwid = cwid
        self.department = department
        # Can students repeate a course? If so list might be a better choice
        self.courses_taught = set()
        self.student_count = defaultdict(int)     # key:CourseID -> val:StudentCount
    
    def __str__(self):
        return "CWID: {}, Name: {}, Department: {}, Courses Taught: {}, Student_Count: {}".format(self.cwid, self.name, self.department, self.courses_taught, self.student_count)
