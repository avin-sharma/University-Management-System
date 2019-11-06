import os
from collections import defaultdict
from prettytable import PrettyTable
from typing import Set
from student import Student
from instructor import Instructor
from major import Major
from helpers import file_reading_gen

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