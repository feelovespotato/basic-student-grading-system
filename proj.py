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
    students = read_file("students.txt")
    new_list = []

    for line in students:
        parts = line.split(",")
        if parts[0].strip() != stu_id:
            new_list.append(line)

    with open("students.txt", "w") as f:
        for item in new_list:
            f.write(item + "\n")

    # Delete from grades.txt
    grades = read_file("grades.txt")
    new_grade_list = []

    for g in grades:
        parts = g.split(",")
        if parts[0].strip() != stu_id:
            new_grade_list.append(g)

    with open("grades.txt", "w") as f:
        for item in new_grade_list:
            f.write(item + "\n")

    print("Student deleted successfully.")


# Function for delete course + its grades.
def delete_course(course_id):
    # Delete from courses.txt
    courses = read_file("courses.txt")
    new_list = []

    for line in courses:
        parts = line.split(",")
        if parts[0].strip() != course_id:
            new_list.append(line)

    with open("courses.txt", "w") as f:
        for item in new_list:
            f.write(item + "\n")

    # Remove grades for this course from grades.txt
    grades = read_file("grades.txt")
    new_grade_list = []

    for g in grades:
        parts = g.split(",")
        if len(parts) < 3:
            continue
        c_id = parts[2].strip()

        if c_id != course_id:
            new_grade_list.append(g)

    with open("grades.txt", "w") as f:
        for item in new_grade_list:
            f.write(item + "\n")

    print("Course deleted successfully.")

# Part 2 – Goyu
# Check if student ID exists in students.txt
def student_exist(stu_id):
    student = read_file("students.txt")
    for s in student:
        parts = s.split(",")
        if len(parts) > 0 and parts[0].strip() == stu_id:
            return True
    return False
#Check if semester exists
def semester_check(semester):
    students= read_file("students.txt")
    for s in students:
        parts= s.split(",")
        if len(parts) >=4 and parts[3].strip() == semester:
            return True
    return False
#Check if student ID matches semester
def student_semester(stu_id, semester):
    students = read_file("students.txt")
    for s in students:
        parts = s.split(",")
        if len(parts) >= 4 and parts[0].strip() == stu_id and parts[3].strip() == semester:
            return True
    return False


# Check if course exists.
def course_exist(course_id):
    course = read_file("courses.txt")
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
    write_file("students.txt", [newstu])
    print(f"Student added successfully to semester {selected_semester}")

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
    courses= read_file("courses.txt")
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
    with open("courses.txt", "w") as f:
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
    write_file("courses.txt", [new_course])
    print("Course added successfully.")
# Search course by id or name.
def search_course(selected_semester):
    keyw = input("Enter Course ID or Name to search: ").strip().lower()
    courses = read_file("courses.txt")
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
    students = read_file("students.txt")
    found = False
    for c in students:
        parts= c.split(",")
        if len(parts) >= 4 and parts[3].strip() == selected_semester:
            if keyw in c.lower():
                print(c)
                found = True
    if not found:
        print(f"No matching student found in semester {selected_semester}")
#check semester
def select_semester():
    while True:
        semester= input("Please Choose a semester: ")
        if not semester.isdigit():
            print("Invalid! Must be a number")
            continue
        if not semester_check(semester):
            print("Invalid! semester not found in database")
            continue
        print(f'semester {semester} selected')
        return semester
        

# Main Menu function.
def main():
    print("Welcome!")
    while True:
        print("Menu")       
        print("1. Add Student")
        print("2. Delete Student")
        print("3. Search Student")
        print("4. Login")
        print("0. Exit")
        choice = input("Choose: ")

        if choice == "1":
            sem = input("Enter current semester for new student: ")
            add_student(sem)

        elif choice == "2":
            sem = input("Enter the current semester of student to delete: ")
            delete_student_in_semester(sem)

        elif choice == "3":
            sem = input("Enter the current semester of student to search: ")
            search_student(sem)

        elif choice == "4":
            break

        elif choice == "0":
            print("Exiting program...")
            return

        else:
            print("Invalid choice.")
    #login function 
    while True:
        print("\n--- LOGIN ---")
        stu_id = input("Enter your Student ID: ").strip()
        if student_exist(stu_id):
            print(f"Login successful! Welcome, Student {stu_id}")
            break
        else:
            print("error! Student not found.")
            print("Try again.")
    selected_semester = select_semester()
    while True:
        print(f"\n--- COURSE MENU (Semester {selected_semester}) ---")
        print("1. Add Course")
        print("2. Delete Course")
        print("3. Search Course")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_course(selected_semester)

        elif choice == "2":
            delete_course_menu(selected_semester)

        elif choice == "3":
            search_course(selected_semester)

        elif choice == "0":
            print("Exiting...")
            return

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
