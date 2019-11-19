# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 10:07:29 2019

@author: yueyu
"""

import os
from collections import defaultdict
from prettytable import PrettyTable
from HW08_Yuan_YueT import file_reading_gen
import sqlite3

class Major:
    '''Track required courses and electives for each major'''
    PT_FIELDS = ['Major', 'Required Courses', 'Electives']
    passing_grades = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}
    
    def __init__(self, dept):
        self._dept = dept
        self._required = set()
        self._elective = set()
        
    def add_course(self, course, type):
        '''add a new course to the major where type is either 'R' or 'E'''
        if type == 'R':
            self._required.add(course)
        elif type == 'E':
            self._elective.add(course)
        else:
            raise ValueError(f"Expected 'R' or 'E' but found '{type}'")
    
    def remaining(self, completed):
        '''Calculate the remaining required and elective courses'''
        passed = {course for course, grade in completed.items() if grade in Major.passing_grades}
        rem_required = self._required - passed
        
        if self._elective.intersection(passed):
            rem_elective = None
        else:
            rem_elective = self._elective
        
        return self._dept, passed, rem_required, rem_elective
    
    def pt_row(self):
        '''Return a list of values to include in Major prettytable'''
        return [self._dept, sorted(self._required), sorted(self._elective)]

class Student:
    '''CWID, Name, Department, courses/grades'''
    
    PT_FIELDS = ['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Elective']  # Global
    
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
        major, passed, rem_required, rem_elective = self._major.remaining(self._courses) ####
        return [self._cwid, self._name, major, sorted(passed), rem_required, rem_elective] #####give you want, not more, protect


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
        self._majors = dict()#
        self._instructors = dict() #instructor[cwid]=Instructor()  value is class Instructor
        
        try:
            self._get_majors(os.path.join(path, "majors.txt"))#
            self._get_students(os.path.join(path, "students.txt"))
            self._get_instructors(os.path.join(path, "instructors.txt"))
            self._get_grades(os.path.join(path, "grades.txt"))
        
        except ValueError as ve:
            print(ve)
        except FileNotFoundError as fnfe:
            print(fnfe)
            
        if ptable:
            print("Majors Summary")#
            self.major_prettytable()#
            
            print("\nStudent Summary")
            self.student_prettytable()  
            
            print("\nInstructor Summary")
            self.instructor_prettytable()
            
            print("\nInstructor Summary From Database")###############################################################
            self.instructor_table_db(os.path.join(path, "810_startup.db")) ###########################################           
            
            
    def _get_majors(self, path):
        '''read major files and assign course to the majors''' 
        try:
            for major, flag, course in file_reading_gen(path, 3, sep='\t', header=True):
                if major not in self._majors:
                    self._majors[major] = Major(major)
                    
                self._majors[major].add_course(course, flag)
                
        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)        
            
        
    def _get_students(self, path):
        '''read the students and populate _get_students'''
        try:
            for cwid, name, major in file_reading_gen(path, 3, sep='\t', header=True):
                if major not in self._majors:
                    print(f"Student {cwid} {name} has unknown major {major}")
                else:
                    self._students[cwid] = Student(cwid, name, self._majors[major]) #####
        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)
            
    def _get_instructors(self, path): 
        '''similar to get students, read the studnets and populate _get_students'''
        try:
            for cwid, name, dept in file_reading_gen(path, 3, sep='\t', header=True):
                self._instructors[cwid] = Instructor(cwid, name, dept) #####
        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)
            
            
    def _get_grades(self, path):
        '''read grade files, assign grade to student and instructor'''
        try:
            for student_cwid, course, grade, instructor_cwid in file_reading_gen(path, 4, sep='\t', header=True):               

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

    def _get_instructor_table_db(self, dbname): ###############################################################
        "get connected with the database and execute the query"
        
        #DB_file="D:\sqlite\810_startup.db"
        try:
            db=sqlite3.connect(dbname)
        except sqlite3.OperationalError:
            print(f"Error: Unable to connect to database at {dbname}")
        else:
            query="select i.CWID, i.Name, i.Dept, g.Course, count(g.StudentCWID)\
                    from instructors i join grades g\
                    on i.CWID=g.InstructorCWID\
                    group by i.CWID, i.Name, i.Dept, g.Course"

        for row in db.execute(query):
            yield row


    def major_prettytable(self):
        '''print the major pretty table'''
        pt = PrettyTable(field_names=Major.PT_FIELDS)  ###shouldn't have []
        
        for dept in self._majors.values():
            pt.add_row(dept.pt_row())
            
        print(pt)  ####


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

    def instructor_table_db(self, dbname): ###############################################################
        '''print the instructor pretty table'''
        pt = PrettyTable(field_names=Instructor.PT_FIELDS)
        for row in self._get_instructor_table_db(dbname):
            pt.add_row(row)
            
        print(pt)


def main():
    Stevens=Repository('C:/Users/yueyu/Desktop', ptable=True)


if __name__=='__main__':
    main()








        





