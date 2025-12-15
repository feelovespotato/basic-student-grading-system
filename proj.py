import os
import sys
import time

from grade_manager import(
    grade_conversion_letter,
    grade_conversion_point,
    calc_gpa,
    calc_cgpa,
    add_grade,
    delete_grade,
    update_grade,
    load_data,
    save_data
)

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
    except Exception as e:
        print(f"Error writing {file_name}: {e}")
        return []

# Function for reading file.
def read_file(file_name):
    try:
        with open(file_name, "r") as f:
            lines = [line.strip() for line in f.readlines()]
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
        if len(parts) >= 4 and parts[0].strip() == stu_id and int(parts[3].strip()) == semester:
            return True
    return False


# Check if course exists.
def course_exist(stu_id,course_id):
    course = read_file(file_path("courses.txt"))
    for c in course:
        parts = c.split(",")
        if len(parts) >= 4 and parts[1].strip() == course_id and parts[0].strip()== stu_id:
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
    course_id = input("Please input course ID to be deleted: ").strip().upper()
    if course_id == "QUIT" or course_id == "EXIT":
        exit_program()
    courses= read_file(file_path("courses.txt"))
    grades = read_file(file_path("grades.txt"))
    updated_courses = []
    updated_grades = []
    course_found = False
    for line in courses:
        parts = line.split(",")
        if len(parts) >= 4:
            c_id = parts[1].strip().upper()
            c_sem = int(parts[3].strip())

            # if course matches ID & semester → skip (delete)
            if c_id == course_id and c_sem == selected_semester:
                course_found = True
                continue
            updated_courses.append(line)
            #delete grades in the deleted course
    for line in grades:
        parts = line.split(",")
        if len(parts) >= 4:
            g_id = parts[2].strip().upper()
            g_sem = int(parts[1].strip())

            # if course matches ID & semester → skip (delete)
            if g_id == course_id and g_sem == selected_semester:
                continue

            updated_grades.append(line)
        

    if not course_found:
        print(f"ERROR! Course {course_id} not found in Semester {selected_semester}.")
        return
    with open(file_path("courses.txt"), "w") as f:
        for item in updated_courses:
            f.write(item + "\n")
    with open(file_path("grades.txt"), "w") as f:
        for item in updated_grades:
            f.write(item + "\n")

    print(f"Course {course_id} deleted successfully from Semester {selected_semester}")



# Function to add course
def add_course_with_grade(stu_id, selected_semester):
    course_id = input("Input new course ID: ").strip().upper()
    if course_id == "QUIT" or course_id == "EXIT":
        exit_program()
    if course_exist(stu_id,course_id):
        print("ERROR! Course already exists.")
        return
    name = input("Enter course name: ").strip().upper()
    while True:
        mark=input(f"Enter student {stu_id} mark on this course (0-100): ").strip()
        try:
            mark_value = int(mark)
            if 0 <= mark_value <= 100:
                mark= str(mark_value)
                break
            else:
                print("Invalid mark, have to be 0-100")
        except ValueError:
            print("Invalid input! must be number")

    # by andy / to calc grade letter& points
    letter_grade = grade_conversion_letter(mark_value)
    grade_point = grade_conversion_point(letter_grade)

    new_course = f"{stu_id},{course_id},{name},{selected_semester}"
    write_file(file_path("courses.txt"), [new_course])

    new_marks= f"{stu_id},{selected_semester},{course_id},{mark},{letter_grade}"
    write_file(file_path("grades.txt"), [new_marks])


    # by andy / use add_grade func to save instead of ^^

    print("Course added successfully.")
    print()

# to update students grade specific course
def update_grade_menu(stu_id, selected_semester):
    course_id = input("Input course ID: ").strip().upper()
    if course_id == "quit" or course_id == "exit":
        exit_program()

    if not(course_exist(stu_id,course_id)):
        print("ERROR! Course does not exist.")
        return

    while True:
        new_mark = input("Enter new mark: ").strip()
        try:
            new_mark = int(new_mark)
            if 0 <= new_mark <= 100:
                break
            else:
                print("Invalid mark, have to be 0-100")
        except ValueError:
            print("Invalid input! must be number")

    letter_grade = grade_conversion_letter(new_mark)
    grade_points = grade_conversion_point(letter_grade)

    records = load_data()
    bool_successs = update_grade(records, stu_id, course_id, new_mark)

    if bool_successs:
        print("Successfully updated grade.")
        print(f"New mark: {new_mark}, Grade: {letter_grade}, Points: {grade_points}")

    else:
        print("Grade not found hence not updated.")


# delete grade
def delete_grade_specific_student(stu_id, selected_semester):
    course_id = input("Input course ID to delete grade: ").strip().upper()

    if not (course_exist(stu_id, course_id)):
        print("ERROR! Course does not exist.")
        return

    while True:
        confirm = input(f"Are you sure you want to delete grade for {course_id}? (yes/no): ").strip().upper()

        if confirm == "YES":
            break

        if confirm == "NO":
            print("Grade deletion cancelled.")
            return

        else:
            print("please answer yes or no only")
            time.sleep(1)
            clear_terminal()

    records = load_data()
    success = delete_grade(records, stu_id, course_id, selected_semester)

    if success:
        print("Successfully deleted grade.")

        # remove the student from the specific course in course.txt
        courses = read_file(file_path("courses.txt"))
        updated_courses = []

        for line in courses:
            parts = line.split(",")
            # check if all the id match, then skip that line to append
            if len(parts) >= 4:
                if (parts[0].strip() == stu_id and
                        parts[1].strip() == course_id and
                        int(parts[3].strip()) == selected_semester):
                    continue
                else:
                    updated_courses.append(line)
            else:
                updated_courses.append(line)

        with open (file_path("courses.txt"), "w") as f:
            for item in updated_courses:
                f.write(item + "\n")

    else:
        print("Grade not found hence not deleted.")



# Search course by id or name.
def search_course(selected_semester):
    keyw = input("Enter Course ID or Name to search: ").strip().lower()
    if keyw == "quit" or keyw == "exit":
        exit_program()
    courses = read_file(file_path("courses.txt"))
    found = False
    for x in courses:
        parts= x.split(",")
        if len(parts) >= 4 and int(parts[3]) == selected_semester:
            if keyw in x.lower():
                print("course info as below: ")
                print(f"Student ID: {parts[0]}")
                print(f"Course ID: {parts[1]}")
                print(f"Course Name: {parts[2]}")
                print(f"Semester: {parts[3]}")
                found = True
    if not found:
        print(f"No matching course found in semester {selected_semester}")


# Search student by id or name.
def search_student(selected_semester):
    keyw = input("Enter Student ID or Name to search: ").strip().lower()
    students = read_file(file_path("students.txt"))
    
    for c in students:
        parts = [p.strip() for p in c.split(",")]
        if len(parts) < 4:
            continue

        stu_id = parts[0]
        name = parts[1]
        email = parts[2]
        sem = int(parts[3])

        # Check semester matches
        if sem != selected_semester:
            continue

        # Check if input matches ID exactly or name (substring, case-insensitive)
        if keyw == stu_id.lower() or keyw in name.lower():
            print(
                f"\nStudent found."
                f"\nID: {stu_id}"
                f"\nName: {name}"
                f"\nEmail: {email}"
                f"\nSemester: {sem}"
            )
            return stu_id 
            
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
def display_individual_performance(selected_semester,stu_id):
    if stu_id is None:
        print("No info to display. Student not found.")
        return
    # read grades.txt using Andy's one consistent
    lines = load_data()

    if selected_semester != 1:
        print("\n--- Past Academic Performance (Sem 1 to Sem", selected_semester, ") ---")
    else:
        print(("\n--- Past Academic Performance (Sem 1) ---"))

    found = False
    # Collect all grade lines for this student
    for line in lines:
        if line["student_id"] == stu_id and line["semester"] <= selected_semester:
            found = True
            sem = int(line["semester"]) 
            course= line["course_id"]
            score = line["marks"]
            letter_grade=grade_conversion_letter(score)
            print(f"Semester {sem} | Course: {course} | Score: {score} | Grade: {letter_grade}")

    if not found:
        print("No grades found for this student.")
        return
    
    #calculate GPA 
    semester_gpas = calc_gpa(lines, stu_id, selected_semester)

    if selected_semester in semester_gpas:
        print(f"GPA for semester {selected_semester}: {semester_gpas[selected_semester]}")

    else:
        print(f"No grade gpa found for sem {selected_semester}")

    #calculate cgpa
    cgpa = calc_cgpa(lines, stu_id)
    print(f"CGPA (All semesters): {cgpa:.2f}") #keep 2 decimal place

    past_gpas = {sem: gpa for sem, gpa in semester_gpas.items() if sem < selected_semester}
    if past_gpas: # show gpas history (past sem)
        print(f"Past semester GPA history")
        for sem, gpa in sorted(semester_gpas.items()):
            print(f"Semester {sem} | GPA: {gpa:2f}")
            time.sleep(2)


def course_performance_summary(course_id, selected_semester):
    course_id = course_id.upper().strip()
    print(f"\n---COURSE PERFORMANCE FOR {course_id}---")

    # read the file
    with open(file_path("grades.txt"), "r") as f:
        lines = f.readlines()     

    #gather marks
    marks = []
    course_found = False

    for line in lines:
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 4:
            continue
  

        sem = int(parts[1])
        course = parts[2].strip().upper()
        try:
            score = float(parts[3])
        except ValueError:
            continue
    
        if course == course_id and sem == selected_semester:
            course_found = True
            marks.append(score)

    if not course_found:
        print("Course not found in your semester.")
        return
    if not marks:
        print("No grades found for this course.")
        return
    
    # Calculate stats
    avg_mark = sum(marks) / len(marks)
    highest = max(marks)
    lowest = min(marks)

    # use imported convert func
    avg_letter = grade_conversion_letter(avg_mark)
    avg_points = grade_conversion_point(avg_letter)
    
    print(f"Students Enrolled: {len(marks)}")
    print(f"Average Mark: {avg_mark:.2f}")
    print(f"Highest Mark: {highest}")
    print(f"Lowest Mark: {lowest}")
    print(f"Average Letter Grade: {avg_letter}")
    print(f"Average Points: {avg_points}")

    from grade_calc import GradeSystem
    grade_obj = GradeSystem(None, None,  avg_mark)
    print(f"Overall letter grade: {grade_obj.grade}")  
    time.sleep(2)                                                                               
    
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
            clear_terminal()
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

def loadcourse_file(stu_id,current_semester):
    courses = [] # make it as a list bc one student has many subject (can store many dictionary)

    with open(file_path("courses.txt"),"r") as file:
        data= file.readlines()
    
    for i in data:
        i=i.strip()
        if not i:
            continue  # skip empty lines
        spliting = i.split(',')

        student_infile = spliting[0]
        course_num= spliting[1]
        course_name = spliting[2]
        sem = int(spliting[3])

        if student_infile == stu_id and sem == current_semester : # filterrrr
            courses.append({ 
                "course_code": course_num,
                "course_name": course_name})
    return courses

    
def file_path(*path_parts):
    folder_basepath = os.path.dirname(__file__)
    return os.path.join(folder_basepath,*path_parts)

def export_performance_report(stu_id,semester,users):
    student= users[stu_id]
    current_semester = semester #pass selexted semester into variable
    courses = loadcourse_file(stu_id,current_semester)
    
    all_records = load_data()
    #filter this student grade 
    student_grades = []
    for g in all_records:
        if g["student_id"] == stu_id:
            student_grades.append(g)
    semester_gpas = calc_gpa(all_records, stu_id, current_semester)
    cgpa = calc_cgpa(all_records, stu_id)

    while True:
        export_or_not = input("do you want to export current semester performance summary file? (please answer yes or no): ").strip()
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

                #loop through the dictionary list and check each course code and semester
                for c in courses:  #course file dictionary loop 
                    grade_record = None
                    for g in student_grades:
                        if g["course_id"] == c["course_code"] and g["semester"] == current_semester: # if course and grade match
                            grade_record = g  
                            break
                    if grade_record: #write in txt file
                        marks= grade_record["marks"]
                        letter = grade_conversion_letter(marks) 
                        file.write(f"{c['course_code']} - {c['course_name']} | Grade: {marks} | Grade: {letter}\n")
                    else:
                        file.write(f"{c['course_code']} - {c['course_name']} | Marks: N/A | Grade: N/A\n")

                #gpa and cgpa 
                gpa_str = f"{semester_gpas.get(current_semester, 0):.2f}"
                file.write(f"\nGPA for semester {current_semester}: {gpa_str}\n")
                file.write(f"CGPA (All semesters): {cgpa:.2f}\n")
                
            print("exported file, you can check your file in ")
            print(fullpathtxt)
            time.sleep(1)
            exit_program()
            break

        elif str(export_or_not.lower()) == "no":
            print("returning to main page...")
            time.sleep(1)
            clear_terminal()
            return

        elif str(export_or_not.lower()) == "exit" or str(export_or_not.lower())== "quit":
            exit_program()
            break

        else: 
            print("please answer yes or no only")
            time.sleep(1)
            clear_terminal()
    
def info_forexport(stu_id,users): #for import purpose
    student = users[stu_id]

    clear_terminal()
    print("exporting information below:")
    print(f"ID: {stu_id}")
    print(f"Name: {student['name']}")
    print(f"Email: {student['email']}")
    print(f"Current semester: {student['semester']}")


# Main Menu function.
def main():
    print("Welcome to student grading system!")
    while True:
        print("\nMenu")
        print("1. Add Student")
        print("2. Delete Student")
        print("3. Login")
        print("0. Exit (you can exit program anytime)")
        choice = str(input("Choose: ")).strip().lower()

        if choice == "1" or choice=="add student":
            while True:
                sem = input("Enter current semester for new student: ")
                if sem.lower() == "quit" or sem.lower() == "exit":
                    exit_program()
                try: 
                    sem=int(sem)
                    break
                except ValueError:
                    print("Value have to be Number")
            add_student(sem)

        elif choice == "2"or choice=="delete student":
            while True:
                print("for verification")
                sem = input("Enter the current semester of student to delete: ")
                if sem.lower() == "quit" or sem.lower() == "exit":
                    exit_program()
                if len(sem) != 1:
                    print("Input has to be a single digit")
                    continue
                try: 
                    sem= int(sem)
                    break
                except ValueError:
                    print("Value have to be Number")
            delete_student_in_semester(sem)
        
        elif choice == "3"or choice=="login":
            break

        elif choice == "0"or choice=="exit" or choice == "quit":
            clear_terminal()
            print("Exiting program...")
            exit_program()

        else:
            print("Invalid choice.")
    #login function 
    while True:
        print("\n--- LOGIN ---")
        stu_id = str(input("Enter your Student ID: ")).strip()
        if stu_id.lower() == "quit" or stu_id.lower() == "exit":
            exit_program()
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
        print("3. Update Grade") # NEW
        print("4. Delete Grade for Specific Course") # NEW
        print("5. Analyze individual Course")
        print("6. Search Course")
        print("7. Search View Past Performance Report")
        print(f"8. export semester report for {selected_semester}")
        print("0. Exit")

        choice = input("Choose: ").strip().lower()

        if choice == "1" or choice == "add course":
            add_course_with_grade(stu_id, selected_semester)

        elif choice == "2" or choice == "delete course":
            delete_course_menu(selected_semester)

        elif choice == "3" or choice == "update grade":
            update_grade_menu(stu_id, selected_semester)

        elif choice == "4" or choice == "delete grade":
            delete_grade_specific_student(stu_id, selected_semester)

        elif choice == "5" or choice == "analyze":
            cou = input("Enter the course ID you want to analyze: ").upper().strip()
            course_performance_summary(cou, selected_semester)

        elif choice == "6" or choice == "search course":
            search_course(selected_semester)
            

        elif choice == "7" or choice == "Search Student & View Performance Report" or choice == "search student" or choice == " view performance report":
            display_individual_performance(selected_semester,stu_id)

        elif choice == "8" or choice == "export current semester report":
            users = loaddstudent_file()
            export_performance_report(stu_id,selected_semester,users)
            break

        elif choice == "0" or choice == "exit" or choice == "quit":
            print("Exiting...")
            exit_program()
            return

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()