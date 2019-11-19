# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 10:07:29 2019

@author: yueyu
"""

import os
from collections import defaultdict
from prettytable import PrettyTable
from HW08_Yuan_YueT import file_reading_gen

class Student:
    '''CWID, Name, Department, courses/grades'''
    
    PT_FIELDS = ['CWID', 'Name', 'Courses']  # Global
    
    def __init__(self, cwid, name, major):
        self._cwid = cwid
        self._name = name        
        self._major = major
        self._courses = dict()  # _course[course]=grade
     
    def add_course(self, course, grade):
        '''store the grade associated with a course for this student'''
        self._courses[course] = grade
        
    def pt_row(self): #######
        '''return a list of values to populate the prettytable'''
        return [self._cwid, self._name, sorted(self._courses.keys())] #####give you want, not more, protect


class Instructor:
    '''CWID, Name, Deparment, courses/#students'''
    
    PT_FIELDS=['CWID', 'Name', 'Dept', 'Course', '# of students']
    
    
    def __init__(self, cwid, name, dept):
        self._cwid = cwid
        self._name = name        
        self._dept = dept
        self._courses = defaultdict(int)   # track _courses[course]=# of students

    def add_student(self, course):
        '''Note that the instructor taught another course to the student'''
        self._courses[course] +=1 ### 
        
    def pt_row(self):
        '''A generator returning rows to be added to the Instructor prettytable
           The prettytable includes only those instructors who have taught at least one course'''
        
        for course, students in self._courses.items():
            yield [self._cwid, self._name, self._dept, course, students] #give you want, not more, protect
        
        
class Repository:
    '''store information about students, instructors '''
    def __init__(self, path, ptable=True): #######
        self._path = path
        self._students = dict() #students[cwid]=Student()
        self._instructors = dict() #instructor[cwid]=Instructor()  value is class Instructor
        
        try:
            self._get_students(os.path.join(path, "students.txt"))
            self._get_instructors(os.path.join(path, "instructors.txt"))
            self._get_grades(os.path.join(path, "grades.txt"))
        
        except ValueError as ve:
            print(ve)
        except FileNotFoundError as fnfe:
            print(fnfe)
        
        
        if ptable:
            print("Student Summary")
            self.student_prettytable()  
            
            print("\nInstructor Summary")
            self.instructor_prettytable()
              
        
    def _get_students(self, path):
        '''read the students and populate _get_students'''
        try:
            for cwid, name, major in file_reading_gen(path, 3, sep='\t', header=False):
                self._students[cwid] = Student(cwid, name, major) #####
        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)
            
    def _get_instructors(self, path):
        '''similar to get students, read the studnets and populate _get_students'''
        try:
            for cwid, name, dept in file_reading_gen(path, 3, sep='\t', header=False):
                self._instructors[cwid] = Instructor(cwid, name, dept) #####
        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)
            
            
    def _get_grades(self, path):
        '''read grade files, assign grade to student and instructor'''
        try:
            for student_cwid, course, grade, instructor_cwid in file_reading_gen(path, 4, sep='\t', header=False):               

                if student_cwid in self._students:
                    self._students[student_cwid].add_course(course, grade) # tell student about you took a course with this grade
                else:
                    print(f"Found grade for unknown student {student_cwid}")
                    
                if instructor_cwid in self._instructors:
                    self._instructors[instructor_cwid].add_student(course) # # tell instructor about a course/student, you took a course with this grade
                else:
                    print(f"Found grade for unknown instructor {instructor_cwid}")    
                
        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)


    def student_prettytable(self):
        '''print the student pretty table'''
        pt = PrettyTable(field_names=Student.PT_FIELDS)  ###shouldn't have []
        
        for student in self._students.values():
            pt.add_row(student.pt_row())
            
        print(pt)  ####
           

    def instructor_prettytable(self):
        '''print the instructor pretty table'''
        pt = PrettyTable(field_names=Instructor.PT_FIELDS) ###shouldn't have []
        
        for instructor in self._instructors.values():
            # each instructor may teach many classes
            for row in instructor.pt_row():                
                pt.add_row(row)
            
        print(pt)   ####


def main():
    Stevens=Repository('C:/Users/yueyu/Desktop', ptable=True)


if __name__=='__main__':
    main()








        





