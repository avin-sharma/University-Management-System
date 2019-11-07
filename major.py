from student import Student
from typing import Set
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
