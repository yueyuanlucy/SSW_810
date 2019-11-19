# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 20:43:22 2019

@author: yueyu
"""
import unittest
import os
from HW11_Yuan_Yue import Major, Student, Instructor, Repository, file_reading_gen


class TestRepository(unittest.TestCase):
    
    def test_Major_Table(self):
        expected=[['SFEN' , ['SSW 540', 'SSW 555', 'SSW 810'] , ['CS 501', 'CS 546']],
                  ['CS' , ['CS 546', 'CS 570'], ['SSW 565', 'SSW 810']]]
        
        calculated=[major.pt_row() for major in Repository('C:/Users/yueyu/Desktop', False)._majors.values()]
        
        self.assertEqual(expected, calculated)

        
    def test_Student_Table(self):
        expected=[['10103', 'Jobs, S', 'SFEN',['CS 501', 'SSW 810'],{'SSW 555', 'SSW 540'},None],
                  ['10115', 'Bezos, J', 'SFEN',['SSW 810'],{'SSW 555', 'SSW 540'},{'CS 501', 'CS 546'}],
                  ['10183', 'Musk, E', 'SFEN',['SSW 555', 'SSW 810'],{'SSW 540'},{'CS 501', 'CS 546'}],
                  ['11714', 'Gates, B', 'CS',['CS 546', 'CS 570', 'SSW 810'],set(),None],
                  ['11717', 'Kernighan, B', 'CS',[],{'CS 570', 'CS 546'},{'SSW 565', 'SSW 810'}]]

        
        calculated=[student.pt_row() for student in Repository('C:/Users/yueyu/Desktop', False)._students.values()]
        
        self.assertEqual(expected, calculated)
        
    def test_Instructor_Table(self):
        expected=[['98764', 'Cohen, R', 'SFEN', 'CS 546', 1],
                  ['98763', 'Rowland, J', 'SFEN', 'SSW 810', 4],
                  ['98763', 'Rowland, J', 'SFEN', 'SSW 555', 1],
                  ['98762', 'Hawking, S', 'CS', 'CS 501', 1],
                  ['98762', 'Hawking, S', 'CS', 'CS 546', 1],
                  ['98762', 'Hawking, S', 'CS', 'CS 570', 1]]

        
        calculated=[detail for instructor in Repository('C:/Users/yueyu/Desktop', False)._instructors.values() for detail in instructor.pt_row()]
        
        self.assertEqual(expected, calculated)

    def test_Instructor_Table_From_Database(self):
        expected=[('98762', 'Hawking, S', 'CS', 'CS 501', 1),
                  ('98762', 'Hawking, S', 'CS', 'CS 546', 1),
                  ('98762', 'Hawking, S', 'CS', 'CS 570', 1),
                  ('98763', 'Rowland, J', 'SFEN', 'SSW 555', 1),
                  ('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4),                  
                  ('98764', 'Cohen, R', 'SFEN', 'CS 546', 1)]
        
        calculated=[row for row in Repository('C:/Users/yueyu/Desktop', False)._get_instructor_table_db("810_startup.db")]
        
        self.assertEqual(expected, calculated)

       
if __name__=="__main__":
    unittest.main(exit=False, verbosity=2)