import os
import sys
import time

def clear_terminal():
    os.system('cls' #clear terminal
              if os.name == "nt" #check the operating system (nt=windows)
              else "clear")
#exit program feature
def exit_program():
    while True:
        print(" do you want to continue student grading system? type (Yes/No)")
        exit_program_or_not= str(input("enter: ").strip().lower())
        if str(exit_program_or_not.lower()) == "yes":
            main()
        elif str(exit_program_or_not.lower())== "no":
            clear_terminal()
            message ="Thank you for using student grading system \n BYE BYE"
            for i in message:
                print(i,end="",flush=True) #effect , flush to ignore buffering
                time.sleep(0.05)
            sys.exit(0)
            break
        else: 
            print(" please answer yes/no only")
            time.sleep(1)
            clear_terminal()

def loaddstudent_file():
    users = {}
    with open(file_path("students.txt"),"r") as file :
        data = file.readlines()
    
    for i in data:
        i=i.strip()
        if not i:  # skip empty lines
            continue
        spliting = i.split(',')

        studentid_infile = spliting[0]
        name= spliting[1]
        email = spliting[2]
        semester = int(spliting[3])
        
        users[studentid_infile ] = {
            "name": name,
            "email": email,
            "semester": semester,
            "courses": [], # empty list for courses
            "grades": []   # empty list for grades
        }
    return users

def loadcourse_file(semester):
    courses = [] # make it as a list bc one student has many subject (can store many dictionary)

    with open(file_path("courses.txt"),"r") as file:
        data= file.readlines()
    
    for i in data:
        i=i.strip()
        if not i:
            continue  # skip empty lines
        spliting = i.split(',')

        course_num= spliting[0]
        course_name = spliting[1]
        sem = int(spliting[2])

        if sem == semester : # filterrrr
            courses.append({ 
                "course_code": course_num,
                "course_name": course_name})
    return courses


def loadgrade_file(stu_id):
    grades= []

    with open(file_path("grades.txt"),"r") as file :
        data = file.readlines()
    
    for i in data:
        i=i.strip()
        if not i:
            continue  # skip empty lines
        spliting = i.split(',')
        studentid_infile = spliting[0]
        grade_sem = int(spliting[1])
        course_num= spliting[2]
        marks = spliting[3]
        #grade = spliting[4]
        #gpa = spliting [5]

        #get student id from part 2 
        if studentid_infile == stu_id: 
            grades.append({
                    "semester": grade_sem,
                    "course_code": course_num,
                    "marks": marks,
                    #"grade": grade,#"gpa": gpa,
                    })
    return grades
    
def file_path(*path_parts):
    folder_basepath = os.path.dirname(__file__)
    return os.path.join(folder_basepath,*path_parts)

def export_performance_report(stu_id,semester,users):
    student= users[stu_id]
    current_semester = student['semester']
    courses = loadcourse_file(current_semester)
    grades = loadgrade_file(stu_id)
    #loop through every single grade for that particular sem
    semester_grades = [
        g for g in grades 
        if g["semester"] == current_semester]

    for c in courses:
    # find matching grade record for this course
        grade_record = next(
        (g for g in semester_grades if g["course_code"] == c["course_code"]),
        None
        )
        marks_str = grade_record["marks"] if grade_record else "N/A"

    while True:
        export_or_not = input("do you want to export you performance summary file? (please answer yes or no): ").strip()
        if str(export_or_not.lower()) == "yes":
            info_forexport(stu_id,users)
            #for different name file 1,2,3,4...
            i=0
            while True: #for checking the num of file exist
                performance_summarytxt= f"student performance summary({i}).txt"
                fullpathtxt = file_path(performance_summarytxt)
                if not os.path.exists(fullpathtxt):
                    break
                i=i+1

            #create file in the specific path
            with open(fullpathtxt, "w") as file:
                file.write(f"ID: {stu_id}\n")
                file.write(f"Name: {student['name']}\n")
                file.write(f"Email: {student['email']}\n")
                file.write(f"Current Semester: {student['semester']}\n\n")

                for c in courses:
                    grade_record = next(
                    (g for g in grades if g["course_code"] == c["course_code"] and g["semester"] == current_semester),
                    None
                    )
                    grade_str = grade_record["marks"] if grade_record else "N/A"
                    file.write(f"{c['course_code']} - {c['course_name']} | Grade: {grade_str}\n")
                
            print("exported file, you can check your file in ")
            print(fullpathtxt)
            exit_program()
            break

        elif str(export_or_not.lower()) == "no":
            print("returning to main page...")
            time.sleep(1)
            clear_terminal()
            #main()
            break

        else: 
            print("please answer yes or no only")
            time.sleep(1)
            clear_terminal()
    
def info_forexport(stu_id,users):
    student = users[stu_id]
    courses = loadcourse_file(student['semester'])
    grades = loadgrade_file(stu_id)

    print("exporting information below:")
    print(f"ID: {stu_id}")
    print(f"Name: {student['name']}")
    print(f"Email: {student['email']}")
    print(f"Current semester: {student['semester']}")

    for c in courses:
        grade_record = next(
            (g for g in grades if g["course_code"] == c["course_code"] and g["semester"] == student['semester']),
            None
        )
        grade_str = grade_record["marks"] if grade_record else "N/A"
        print(f"{c['course_code']} - {c['course_name']} | Grade: {grade_str}")

students_data = "students.txt"
courses_data = "courses.txt"
grades_data = "grades.txt"


