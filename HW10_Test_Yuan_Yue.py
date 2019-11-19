# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 20:43:22 2019

@author: yueyu
"""
import unittest
import os
from HW10_Yuan_Yue import Major, Student, Instructor, Repository, file_reading_gen


class TestRepository(unittest.TestCase):
    #def setup(self):
        #self.test_path = 'C:/Users/yueyu/Desktop'
        #self.repo = Repository(self.test_path, False)  False!!!!
    
    def test_Major_Table(self):
        expected=[['SFEN' , ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'] , ['CS 501', 'CS 513', 'CS 545']],
                  ['SYEN' , ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810']]]
        
        calculated=[major.pt_row() for major in Repository('C:/Users/yueyu/Desktop', False)._majors.values()]
        
        self.assertEqual(expected, calculated)

        
    def test_Student_Table(self):
        expected=[['10103', 'Baldwin, C', 'SFEN',['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'],{'SSW 555', 'SSW 540'},None],
                  ['10115', 'Wyatt, X', 'SFEN', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], {'SSW 555', 'SSW 540'}, None],
                  ['10172', 'Forbes, I', 'SFEN',['SSW 555', 'SSW 567'], {'SSW 564', 'SSW 540'},{'CS 513', 'CS 501', 'CS 545'}],
                  ['10175', 'Erickson, D', 'SFEN',['SSW 564', 'SSW 567', 'SSW 687'], {'SSW 555', 'SSW 540'},{'CS 513', 'CS 501', 'CS 545'}],
                  ['10183', 'Chapman, O', 'SFEN', ['SSW 689'], {'SSW 567', 'SSW 564', 'SSW 555', 'SSW 540'},{'CS 513', 'CS 501', 'CS 545'}],
                  ['11399', 'Cordova, I', 'SYEN', ['SSW 540'], {'SYS 612', 'SYS 800', 'SYS 671'}, None],
                  ['11461', 'Wright, U', 'SYEN', ['SYS 611', 'SYS 750', 'SYS 800'], {'SYS 612', 'SYS 671'},{'SSW 565', 'SSW 810', 'SSW 540'}],
                  ['11658', 'Kelly, P', 'SYEN', [], {'SYS 612', 'SYS 800', 'SYS 671'},{'SSW 565', 'SSW 810', 'SSW 540'}],
                  ['11714', 'Morton, A', 'SYEN', ['SYS 611', 'SYS 645'], {'SYS 612', 'SYS 800', 'SYS 671'},{'SSW 565', 'SSW 810', 'SSW 540'}],
                  ['11788', 'Fuller, E', 'SYEN', ['SSW 540'], {'SYS 612', 'SYS 800', 'SYS 671'},None]]

        
        calculated=[student.pt_row() for student in Repository('C:/Users/yueyu/Desktop', False)._students.values()]
        
        self.assertEqual(expected, calculated)
        
    def test_Instructor_Table(self):
        expected=[['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4],
                  ['98765', 'Einstein, A', 'SFEN', 'SSW 540', 3],
                  ['98764', 'Feynman, R', 'SFEN', 'SSW 564', 3],
                  ['98764', 'Feynman, R', 'SFEN', 'SSW 687', 3],
                  ['98764', 'Feynman, R', 'SFEN', 'CS 501', 1],
                  ['98764', 'Feynman, R', 'SFEN', 'CS 545', 1],
                  ['98763', 'Newton, I', 'SFEN', 'SSW 555', 1],
                  ['98763', 'Newton, I', 'SFEN', 'SSW 689', 1],
                  ['98760', 'Darwin, C', 'SYEN', 'SYS 800', 1],
                  ['98760', 'Darwin, C', 'SYEN', 'SYS 750', 1],
                  ['98760', 'Darwin, C', 'SYEN', 'SYS 611', 2],
                  ['98760', 'Darwin, C', 'SYEN', 'SYS 645', 1]]

        
        calculated=[detail for instructor in Repository('C:/Users/yueyu/Desktop', False)._instructors.values() for detail in instructor.pt_row()]
        
        self.assertEqual(expected, calculated)
        
if __name__=="__main__":
    unittest.main(exit=False, verbosity=2)