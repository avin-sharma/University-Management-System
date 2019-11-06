import os
from collections import defaultdict
from prettytable import PrettyTable
from typing import Set

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

class Major:
    """
    Contains required courses and electives of a major.

    Attributes:
        required_courses (set): A set of all the required courses for this major
        elective_courses (set): A set of all the electives offered
    """
    def __init__(self):
        self.required_courses = set()
        self.elective_courses = set()
    
    def add(self, flag, course):
        """
        Adds a new course to required/elective courses according to the flag passed.

        Args:
            flag (str): 'R' or 'E' for required course or elective course respectively.
            course (str): Name of the course to be added to the Major's course list.
        """
        if flag == 'R':
            self.required_courses.add(course)
        else:
            self.elective_courses.add(course)
    
    def get_remaining_required_courses(self, student: Student) -> Set[str]:
        """
        Finds remaining required courses for a student.

        Args:
            student (Student): Student whose remaining courses we are trying to find.
        
        Return:
            Set of remaining required courses.
        """
        return self.required_courses - student.courses_completed
    
    def get_remaining_elective_courses(self, student: Student) -> Set[str]:
        """
        Finds remaining elective courses for a student.

        Args:
            student (Student): Student whose remaining courses we are trying to find.
        
        Return:
            Set of all electives if none of the electives are completed otherwise empty set is returned.
        """
        return self.elective_courses if self.elective_courses.isdisjoint(student.courses_completed) else set()



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
        self.majors = defaultdict(Major)    # Major(str) -> Major(class)
        self.get_students()
        self.get_instructors()
        self.update_course_info()
        self.get_majors()
    
    def get_majors(self):
        """ Reads a majors details from a file and adds courses to them. """
        majors_file = os.path.join(self.path, "majors.txt")
        try:
            for major in file_reading_gen(majors_file, 3, '\t', True):
                # Major | Flag | Course
                name = major[0]
                flag = major[1]
                course = major[2]

                self.majors[name].add(flag, course)

        except ValueError:
            raise ValueError("Invalid data in majors.txt")

    def get_students(self):
        """Reads student details from a file and saves them."""
        students_file = os.path.join(self.path, "students.txt")
        try:
            for student in file_reading_gen(students_file, 3, ';', True):
                # CWID | Name | Major
                cwid = student[0]
                name = student[1]
                major = student[2]
                self.students[cwid] = Student(cwid, name, major)
        except ValueError:
            raise ValueError("Invalid data in students.txt")
        

    def get_instructors(self):
        """
        Reads student details from a file and saves them.
        """
        instructor_file = os.path.join(self.path, "instructors.txt")
        try:
            for instructor in file_reading_gen(instructor_file, 3, '|'):
                # CWID | Name | Dept
                cwid = instructor[0]
                name = instructor[1]
                dept = instructor[2]
                self.instructors[cwid] = Instructor(cwid, name, dept)
        except ValueError:
            raise ValueError("Invalid data in instructors.txt")
    
    def __str__(self):
        student_table = PrettyTable()
        student_table.field_names = ['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives']

        for key in self.students:
            student = self.students[key]
            cwid = student.cwid
            name = student.name
            major = student.major
            if major not in self.majors:
                raise ValueError('{} is not a valid major. Please fix the student record of student with ID: {} or add the major to majors.txt'.format(major, cwid))
            
            courses_completed = sorted(list(student.courses_completed))

            required = sorted(self.majors[major].get_remaining_required_courses(student))
            if len(required) == 0:
                required = None

            electives = sorted(self.majors[major].get_remaining_elective_courses(student))
            if len(electives) == 0:
                electives = None
            student_table.add_row([cwid, name, major, courses_completed, required, electives])
        
        instructor_table = PrettyTable()
        instructor_table.field_names = ['CWID', 'Name', 'Deptartment', 'Course', 'Students']
        for key in self.instructors:
            instructor = self.instructors[key]
            for course in instructor.courses_taught:
                instructor_table.add_row([instructor.cwid, instructor.name, instructor.department, course, instructor.student_count[course]])
        
        majors_table = PrettyTable()
        majors_table.field_names = ['Dept', 'Required', 'Electives']
        for major in self.majors:
            required = sorted(self.majors[major].required_courses)
            electives = sorted(self.majors[major].elective_courses)
            majors_table.add_row([major, required, electives])

        return 'Student Summary\n' + student_table.get_string() + '\n\nInstructor Summary\n' + instructor_table.get_string() + '\n\nMajors Summary\n' + majors_table.get_string()

    def update_course_info(self):
        """
        Updates courses completed and grades of students and 
        updates courses taught and number of students taught.
        """
        grades_file = os.path.join(self.path, "grades.txt")
        try:
            for info in file_reading_gen(grades_file, 4, '|', True):
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
        


def file_reading_gen(path: str, fields: int, sep: str = ',', header: bool =False):
    """ 
    Reads fields from a file seperated by the provided seperator.

    Args:
        path (str): path of the file we want to read.
        fields (int): Number of fields expected in the file we are reading.
        sep (str): Separator that separates the fields from one another.
        header (bool): Signifies if there is a header in the file being passed to read.
    
    Yields:
        Tuple of data after separation.
    
    Raises:
        ValueError: When we encounter a different number of fields than expected.
    """
    
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