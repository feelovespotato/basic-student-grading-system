import os
import sys
import time

def login_system():
    print("ha")

def add_newstudent():
    print("add code here") 

def add_newcourse():
    print("file linkage to new student and add delete")

def student_mark():
    print("save data here")

def display_performance_summary():
    print("student > course > sem > all subject and grades")

def clear_terminal():
    os.system('cls' #clear terminal
              if os.name == "nt" #check the operating system (nt=windows)
              else "clear") #all the rest is mac/linux

def file_path(*path_parts):
    folder_basepath = os.path.dirname(__file__)
    return os.path.join(folder_basepath,*path_parts)

def export_performance_report():
    while True:
        export_or_not = input("do you want to export you performance summary file? (please answer yes or no): ").strip()
        if str(export_or_not.lower()) == "yes":
            #checking the file if its existed for THAT number file
            i=0
            while True:
                performance_summarytxt= f"student performance summary({i}).txt"
                fullpathtxt = file_path(performance_summarytxt)
                if not os.path.exists(fullpathtxt):
                    break
                i=i+1

            #create file in the specific path
            with open(fullpathtxt, "w") as file:
                file.write("write something")
                
                print("exported file, you can check your file in ")
                print(fullpathtxt)
            #main_page()
            break

        elif str(export_or_not.lower()) == "no":
            print("returning to main page...")
            time.sleep(1)
            clear_terminal()
            #main_page()
            break

        else: 
            print("please answer yes or no only")
            time.sleep(1)
            clear_terminal()
    
def exit_program():
    while True:
        print(" do you want to continue? type (Yes/No)")
        exit_program_or_not= str(input("enter: ").strip())
        if str(exit_program_or_not.lower()) == "yes":
            print("continue")
        elif str(exit_program_or_not.lower())== "no":
            clear_terminal()
            message ="Thank you for using student grading system \n BYE BYE"
            for i in message:
                print(i,end="",flush=True) #effect , flush to ignore buffering
                time.sleep(0.05)
            break
        else: 
            print(" please answer yes/no ")
            time.sleep(1)
            clear_terminal()
export_performance_report()
exit_program()


students_data = "students.txt"
courses_data = "courses.txt"
grades_data = "grades.txt"


