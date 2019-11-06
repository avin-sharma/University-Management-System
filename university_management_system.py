import os
from collections import defaultdict
from prettytable import PrettyTable

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

class University:
    """
    Contains all the students and instructors of a University.

    Args:
        university_files_path: Path of the folder where all 
            the three files of a university exists.
    
    Attributes:
        path (str): path of the folder containing relevant files.
        students (dict): (CWID -> Student) that contains all the
            Students of the university mapped to their CWID.
        instructors (dict): (CWID -> Instructors) that contains all the
            Instructors of the university mapped to their CWID.
    """
    def __init__(self, university_files_path):
        self.path = university_files_path
        self.students = {}                  # CWID -> Student
        self.instructors = {}               # CWID -> Instructor
        self.get_students()
        self.get_instructors()
        self.update_course_info()

    def get_students(self):
        """Reads student details from a file and saves them."""
        students_file = os.path.join(self.path, "students.txt")
        for student in file_reading_gen(students_file, 3, '\t'):
            # CWID | Name | Major
            cwid = student[0]
            name = student[1]
            major = student[2]
            self.students[cwid] = Student(cwid, name, major)

    def get_instructors(self):
        """
        Reads student details from a file and saves them.
        """
        instructor_file = os.path.join(self.path, "instructors.txt")
        for instructor in file_reading_gen(instructor_file, 3, '\t'):
            # CWID | Name | Dept
            cwid = instructor[0]
            name = instructor[1]
            dept = instructor[2]
            self.instructors[cwid] = Instructor(cwid, name, dept)
    
    def __str__(self):
        student_table = PrettyTable()
        student_table.field_names = ['CWID', 'Name', 'Completed Courses']
        for key in self.students:
            student = self.students[key]
            student_table.add_row([student.cwid, student.name, sorted(list(student.courses_completed))])
        
        instructor_table = PrettyTable()
        instructor_table.field_names = ['CWID', 'Name', 'Deptartment', 'Course', 'Students']
        for key in self.instructors:
            instructor = self.instructors[key]
            for course in instructor.courses_taught:
                instructor_table.add_row([instructor.cwid, instructor.name, instructor.department, course, instructor.student_count[course]])
        
        return student_table.get_string() + '\n' + instructor_table.get_string()

    def update_course_info(self):
        """
        Updates courses completed and grades of students and 
        updates courses taught and number of students taught.
        """
        grades_file = os.path.join(self.path, "grades.txt")
        try:
            for info in file_reading_gen(grades_file, 4, '\t'):
                # StudentID | Course | Grade | InstructorID
                student_id = info[0]
                course_code = info[1]
                grade = info[2]
                instructor_id = info[3]

                if student_id not in self.students:
                    raise KeyError("Student with student id {} does not exists in students.txt".format(student_id))
                if instructor_id not in self.instructors:
                    raise KeyError("Instructor with instructor id {} does not exists in instructors.txt".format(instructor_id))

                student = self.students[student_id]
                instructor = self.instructors[instructor_id]

                student.courses_completed.add(course_code)
                student.grades[course_code] = grade

                instructor.courses_taught.add(course_code)
                instructor.student_count[course_code] += 1
        except ValueError:
            raise ValueError("Invalid data in grades.txt")
        


def file_reading_gen(path, fields, sep=',', header=False):
    """ Yield fileds from a file seperated by the provided seperator"""
    
    with open(path) as f:
        if header:
            data = f.readline()
            data = data.split(sep)
            if len(data) != fields:
                raise ValueError("Expected {} fields, but got {} in the header".format(fields, len(data)))
        offset = 1
        if header:
            offset = 2
        for i, line in enumerate(f, offset):
            if line[-1] == '\n':
                line = line[:-1]
            data = line.split(sep)
            if len(data) != fields:
                raise ValueError("Expected {} fields, but got {} at line {}".format(fields, len(data), i))

            yield tuple(data)

if __name__ == "__main__":
    stevens = University(os.path.dirname(os.path.abspath(__file__)))
    print(stevens)