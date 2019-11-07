import os
import unittest
from student import Student
from instructor import Instructor
from university import University

class TestUniversity(unittest.TestCase):
    """Test Student, Instructor and University classes"""
    
    def testStudent(self):
        """Test if the student class can be created successfully."""
        student = Student('1', 'A', 'CS')
        self.assertEqual(student.cwid, '1')
        self.assertEqual(student.name, 'A')
        self.assertEqual(student.major, 'CS')
    
    def testInstructor(self):
        """Test if the Instructor class can be created successfully."""
        instructor = Instructor('100', 'Prof', 'CS')
        self.assertEqual(instructor.cwid, '100')
        self.assertEqual(instructor.name, 'Prof')
        self.assertEqual(instructor.department, 'CS')

    def testUniversity(self):
        """ 
        Test if the University class contains correct students and instructors
        and modifies them correctly after parsing grades.txt.
        """
        nyu = University(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_files'), ('\t', False), ('\t', False), ('\t', False), (',', False))
        self.assertEqual(len(nyu.students), 2)
        self.assertEqual(len(nyu.instructors), 2)
        self.assertEqual(nyu.students['1'].grades['CS555'], 'A')
        self.assertEqual(nyu.students['1'].grades['CS111'], 'C')
        self.assertEqual(nyu.students['2'].grades['CS555'], 'B')
        self.assertEqual(nyu.students['2'].grades['CS666'], 'A-')
        self.assertEqual(len(nyu.instructors['100'].courses_taught), 2)
        self.assertEqual(len(nyu.instructors['200'].courses_taught), 1)
        self.assertEqual(nyu.instructors['100'].student_count['CS555'], 2)
        self.assertEqual(nyu.instructors['200'].student_count['CS666'], 1)
        self.assertEqual(len(nyu.majors['CS'].required_courses) , 2)
        self.assertEqual(len(nyu.majors['FE'].required_courses) , 1)
        self.assertEqual(len(nyu.majors['CS'].elective_courses) , 1)
        self.assertEqual(len(nyu.majors['FE'].elective_courses) , 1)
        
        self.assertEqual(nyu.instructor_table._rows, [['100', 'Prof1', 'CS', 'CS555', 2], ['100', 'Prof1', 'CS', 'CS111', 1], ['200', 'Prof2', 'FE', 'CS666', 1]])
        self.assertEqual(nyu.student_table._rows, [['1', 'Avin Sharma', 'CS', ['CS111', 'CS555'], ['CS570'], ['CS546']], ['2', 'Someone Random', 'FE', ['CS555', 'CS666'], ['FE800'], ['CS546']]])
        self.assertEqual(nyu.majors_table._rows, [['CS', ['CS555', 'CS570'], ['CS546']], ['FE', ['FE800'], ['CS546']]])

        print(nyu)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)