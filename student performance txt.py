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
    
student_list = []
def loaddstudent_file():
    with open("student.txt","r") as file :
        data = file.readlines()
        users = {}
    for i in data[1:]:
        i.strip()
        spliting = i.split(',')
        id = spliting[0]
        name= spliting[1]
        email = spliting[2]
        semester = spliting[3]
        users[id] = {
            "name": name,
            "email": email,
            "semester": semester,
            "courses": [], # empty list for courses
            "grades": []   # empty list for grades
        }
    return users

def loadcourse_file():
    with open("course.txt","r") as file:
        data= file.readlines()
    
    for i in data[1:]:
        i.strip()
        spliting = i.split(',')
        id = spliting[0]
        semester = spliting[1]
        course_num= spliting[2]
        course_name = spliting[3]


def loadgrade_file(users):
    with open("grade.txt","r") as file :
        data = file.readlines()
    
    for i in data[1:]:
        i.strip()
        spliting = i.split(',')
        id = spliting[0]
        course_num= spliting[1]
        marks = spliting[2]
        grade = spliting[3]
        gpa = spliting [4]
            #get student id from part 2 
        if id in users:
            users[id]["grades"].append({
            "course_num": course_num,
            "marks": marks,
            "grade": grade,
            "gpa": gpa
            })
        return users
    

            
                

def file_path(*path_parts):
    folder_basepath = os.path.dirname(__file__)
    return os.path.join(folder_basepath,*path_parts)

def export_performance_report():
    while True:
        export_or_not = input("do you want to export you performance summary file? (please answer yes or no): ").strip()
        if str(export_or_not.lower()) == "yes":
            question_forexport()
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
    
def question_forexport(users):
    id = input("please enter your id (example: 12114545): ").strip()
    
    if id in users:
        print("Please check information below:")
        print(f"id: {id}")
        print(f"name: {users[id]['name']}")
        print(f"email: {users[id]['email']}")
        print(f"semester: {users[id]['semester']}")

        semester = input("please enter semester that you want to export (example: 1, 2, 3): ")
        if semester <= users[id]["semester"]:
            print(f"semester {semester}")
            loadcourse_file()

    elif id == "quit":
        exit_program()
    else:
        print("ID not found.")
    


def exit_program():
    while True:
        print(" do you want to continue? type (Yes/No)")
        exit_program_or_not= str(input("enter: ").strip())
        if str(exit_program_or_not.lower()) == "yes":
            print("go to main page")
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


