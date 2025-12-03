import os
import sys
import time

def file_path(*path_parts):
    folder_basepath = os.path.dirname(__file__)
    return os.path.join(folder_basepath,*path_parts)

# Part 1 – File handling
# Function for writing to file.
def write_file(file_name, data_list):
    try:
        with open(file_name, "a") as x:
            for line in data_list:
                x.write("\n" + line if x.tell() else line + "\n")
        print(f"Data written to {file_name}")
    except Exception as e:
        print(f"Error writing {file_name}: {e}")
        return []

# Function for reading file.
def read_file(file_name):
    try:
        with open(file_name, "r") as f:
            lines = [line.strip() for line in f.readlines()]
        print(f"Data read from {file_name}")
        return lines
    except FileNotFoundError:
        print(f"Warning: {file_name} not found! Returning empty list.")
        return []
    except Exception as e:
        print(f"Error reading {file_name}: {e}")
        return []


# Function for delete student data + grades.
def delete_student(stu_id):
    # Delete from students.txt
    students = read_file(file_path("students.txt"))
    new_list = []

    for line in students:
        parts = line.split(",")
        if parts[0].strip() != stu_id:
            new_list.append(line)

    with open(file_path("students.txt"), "w") as f:
        for item in new_list:
            f.write(item + "\n")

    # Delete from grades.txt
    grades = read_file(file_path("grades.txt"))
    new_grade_list = []

    for g in grades:
        parts = g.split(",")
        if parts[0].strip() != stu_id:
            new_grade_list.append(g)

    with open(file_path("grades.txt"), "w") as f:
        for item in new_grade_list:
            f.write(item + "\n")

    print("Student deleted successfully.")


# Function for delete course + its grades.
def delete_course(course_id):
    # Delete from courses.txt
    courses = read_file(file_path("courses.txt"))
    new_list = []

    for line in courses:
        parts = line.split(",")
        if parts[0].strip() != course_id:
            new_list.append(line)

    with open(file_path("courses.txt"), "w") as f:
        for item in new_list:
            f.write(item + "\n")

    # Remove grades for this course from grades.txt
    grades = read_file(file_path("grades.txt"))
    new_grade_list = []

    for g in grades:
        parts = g.split(",")
        if len(parts) < 3:
            continue
        c_id = parts[2].strip()

        if c_id != course_id:
            new_grade_list.append(g)

    with open(file_path("grades.txt"), "w") as f:
        for item in new_grade_list:
            f.write(item + "\n")

    print("Course deleted successfully.")

# Part 2 – Goyu
# Check if student ID exists in students.txt
def student_exist(stu_id):
    student = read_file(file_path("students.txt"))
    for s in student:
        parts = s.split(",")
        if len(parts) > 0 and parts[0].strip() == stu_id:
            return True
    return False
#Check if student ID matches semester
def student_semester(stu_id, semester):
    students = read_file(file_path("students.txt"))
    for s in students:
        parts = s.split(",")
        if len(parts) >= 4 and parts[0].strip() == stu_id and parts[3].strip() == semester:
            return True
    return False


# Check if course exists.
def course_exist(course_id):
    course = read_file(file_path("courses.txt"))
    for c in course:
        parts = c.split(",")
        if len(parts) > 0 and parts[0].strip() == course_id:
            return True
    return False


# Function to add student in semester.
def add_student(selected_semester):
    stu_id = input("Input student ID to add: ").strip()
    if student_exist(stu_id):
        print("ERROR! Student already exists.")
        return

    name = input("Enter student name: ").strip()
    email = input("Enter student email: ").strip()

    newstu = f"{stu_id},{name},{email},{selected_semester}"
    write_file(file_path("students.txt"), [newstu])
    clear_terminal()
    print(f"Student added successfully to semester {selected_semester}")
    print("Please login with your student ID")

#delete student from selected semester
def delete_student_in_semester(selected_semester):
    stu_id = input("Enter Student ID to delete: ").strip()
    if not student_semester(stu_id, selected_semester):
        print(f"Student not found in Semester {selected_semester}")
        return
    delete_student(stu_id)

# Function to delete course.
def delete_course_menu(selected_semester):
    course_id = input("Please input course ID to be deleted: ").strip()
    courses= read_file(file_path("courses.txt"))
    updated_courses = []
    course_found = False
    for x in courses:
        parts = x.split(",")
        if len(parts) >= 3:
            c_id = parts[0].strip()
            c_sem = parts[2].strip()

            # if course matches ID & semester → skip (delete)
            if c_id == course_id and c_sem == selected_semester:
                course_found = True
                continue

        updated_courses.append(x)

    if not course_found:
        print(f"ERROR! Course {course_id} not found in Semester {selected_semester}.")
        return
    with open(file_path("courses.txt"), "w") as f:
        for item in updated_courses:
            f.write(item + "\n")

    print(f"Course {course_id} deleted successfully from Semester {selected_semester}")



# Function to add course
def add_course(selected_semester):
    course_id = input("Input new course ID: ").strip()
    if course_exist(course_id):
        print("ERROR! Course already exists.")
        return
    name = input("Enter course name: ").strip()
    new_course = f"{course_id},{name},{selected_semester}"
    write_file(file_path("courses.txt"), [new_course])
    print("Course added successfully.")
# Search course by id or name.
def search_course(selected_semester):
    keyw = input("Enter Course ID or Name to search: ").strip().lower()
    courses = read_file(file_path("courses.txt"))
    found = False
    for x in courses:
        parts= x.split(",")
        if len(parts) >= 3 and parts[2].strip() == selected_semester:
            if keyw in x.lower():
                print(x)
                found = True
    if not found:
        print(f"No matching course found in semester {selected_semester}")


# Search student by id or name.
def search_student(selected_semester):
    keyw = input("Enter Student ID or Name to search: ").strip().lower()
    students = read_file(file_path("students.txt"))
    
    for c in students:
        parts= c.split(",")
        if len(parts) >= 4 and parts[3].strip() == selected_semester:
            if keyw in c.lower():
                print(
                    f"\nStudent found."
                    f"\nID: {parts[0]}"
                    f"\nName: {parts[1]}"
                    f"\nEmail: {parts[2]}"
                    f"\nSemester: {parts[3]}"
                )
                return parts[0] 
    print(f"No matching student found in semester {selected_semester}")
    return None
#get current semester
def get_current_sem(stu_id):
    students=read_file(file_path("students.txt"))
    for s in students:
        parts=s.split(",")
        if parts[0].strip()== stu_id:
            return int(parts[3])
    return 1
#check semester
def select_semester(current_semester):
    while True:      
        semester= input(f"Please choose a semester (1 to {current_semester}): ")
        if not semester.isdigit():
            print("Invalid! Must be a number")
            continue
        semester= int(semester)
        if semester < 1 or semester > current_semester:
            print(f"Invalid, must be between 1 and {current_semester}.")
            continue
        print(f"Semester {semester} selected")
        return semester
    
#part 4 - darvesh
def display_individual_performance(selected_semester):
    id_stu = search_student(selected_semester)
    
    if id_stu is None:
        print("Cannot display performance. Student not found.")
        return
    
    # read the file
    with open(file_path("grades.txt"), "r") as f:
        lines = f.readlines()
    
    #find student in grades.txt
    from grade_calc import GradeSystem
    
    for line in lines:
        parts = [p.strip() for p in line.split(",")]
        if parts[0] == id_stu: # match student id
            marks = float(parts[3])   
            grade_obj = GradeSystem(parts[0], parts[2], marks)
            print(
                f"\n\nStudent Data:"
                f"\nID: {parts[0]}"
                f"\nSem: {parts[1]}"
                f"\nCourse: {parts[2]}"
                f"\nMark: {parts[3]}"
                f"\nGrade: {grade_obj.grade}"
                f"\nGrade Point: {grade_obj.grade_point}"
                f"\nCGPA: "
                
               


            )
            return

    
    print("Student ID not found in file.")

def course_performance_summary(course_id):
    print(f"\nCOURSE PERFORMANCE FOR {course_id}")

    # read the file
    with open(file_path("grades.txt"), "r") as f:
        lines = f.readlines()     

    marks = []
    for line in lines:
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 4:
            continue

        if parts[2]  == course_id:
            mark = float(parts[3])  
            marks.append(mark)  
    if not marks:
        print("No grades found for this course.")
        return
    
    from grade_calc import GradeSystem


    # Calculate stats
    avg_mark = sum(marks) / len(marks)
    highest = max(marks)
    lowest = min(marks)
    
    print(f"Students Enrolled: {len(marks)}")
    print(f"Average Mark: {avg_mark:.2f}")
    print(f"Highest Mark: {highest}")
    print(f"Lowest Mark: {lowest}")

    grade_obj = GradeSystem(None, None,  avg_mark)
    print(f"Overall letter grade: {grade_obj.grade}")                                                                                 
    
#for cleaning terminal
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
    semester_grades = [g for g in grades if g["semester"] == current_semester]

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
            main()
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

# Main Menu function.
def main():
    print("Welcome to student grading system!")
    while True:
        print("Menu")       
        print("1. Add Student")
        print("2. Delete Student")
        print("3. Search Student")
        print("4. Anaylize Course")
        print("5. Login")
        print("0. Exit (you can exit program anytime)")
        choice = str(input("Choose: ")).strip().lower()

        if choice == "1" or choice=="add student":
            sem = input("Enter current semester for new student: ")
            add_student(sem)

        elif choice == "2"or choice=="delete student":
            sem = input("Enter the current semester of student to delete: ")
            delete_student_in_semester(sem)

        elif choice == "3"or choice=="search student":
            sem = input("Enter the current semester of student to search: ")
            display_individual_performance(sem)
        
        elif choice == "4"or choice=="anaylize course":
            cou = input("Enter the course you want to analise: ").upper()
            course_performance_summary(cou)
        
        elif choice == "5"or choice=="login":
            break

        elif choice == "0"or choice=="exit":
            clear_terminal()
            print("Exiting program...")
            exit_program()

        else:
            print("Invalid choice.")
    #login function 
    while True:
        print("\n--- LOGIN ---")
        stu_id = str(input("Enter your Student ID: ")).strip()
        if student_exist(stu_id):
            print(f"Login successful! Welcome, Student {stu_id}")
            break
        if stu_id.lower().strip() == "quit" or stu_id.lower().strip() == "exit":
            clear_terminal
            exit_program()
            
        else:
            print("error! Student not found.")
            print("Try again.")
            time.sleep(1)
            clear_terminal()
    current_sem= get_current_sem(stu_id)
    selected_semester = select_semester(current_sem)
    while True:
        print(f"\n--- COURSE MENU (Semester {selected_semester}) ---")
        print("1. Add Course")
        print("2. Delete Course")
        print("3. Search Course")
        print(f"4. export  semester report from Semester 1 to {current_sem}")
        print("0. Exit")

        choice = input("Choose: ").strip().lower()

        if choice == "1" or choice == "add course":
            add_course(selected_semester)

        elif choice == "2" or choice == "delete course":
            delete_course_menu(selected_semester)

        elif choice == "3" or choice == "search course":
            search_course(selected_semester)

        elif choice == "4" or choice == "export current semester report":
            users = loaddstudent_file()
            export_performance_report(stu_id,selected_semester,users)
            break

        elif choice == "0" or choice == "exit":
            print("Exiting...")
            exit_program()
            return

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
