# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 14:27:32 2019
HW08_Yuan_Yue
@author: yueyu
"""

# Part 2
    
def file_reading_gen(path, fields, sep=',', header=False):
    '''Write a generator function to read field-separated text files and 
    yield a tuple with all of the values from a single line in the file'''
    try: 
        fp = open(path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: Can't open {path}")
    else:        
        with fp:          
            #lines=fp.readlines() no need to write this 
            for i, line in enumerate(fp):
                newline=line.strip("\n").split(sep)   #rstrip
                
                if len(newline)!=fields:
                    raise ValueError(f"ValueError: {path} has {len(newline)} fields on line {i+1} but expected {fields}")
               
                elif header==False:
                    yield tuple(newline)
                else:
                    if i==0:
                        continue
                    else:
                        yield tuple(newline)
                        
                #elif header==True and i==0:                   
                #   continue
                #else:                    
                #   yield tuple(newline)
             
#for cwid, name, major in file_reading_gen("student_majors_header.txt", 3, sep='|', header=True):  
    #print(f"cwid: {cwid} name: {name} major: {major}") 
   
