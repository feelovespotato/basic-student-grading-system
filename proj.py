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
# Check if student exists.
def student_exist(stu_id):
    student = read_file("students.txt")
    for s in student:
        parts = s.split(",")
        if len(parts) > 0 and parts[0].strip() == stu_id:
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


# Function to add student.
def add_student():
    stu_id = input("Input student ID to add: ").strip()
    if student_exist(stu_id):
        print("ERROR! Student already exists.")
        return

    name = input("Enter student name: ").strip()
    email = input("Enter student email: ").strip()
    semester = input("Enter the semester of student (number only): ").strip()

    newstu = f"{stu_id},{name},{email},{semester}"
    write_file("students.txt", [newstu])
    print("Student added successfully.")


# Function to delete student.
def delete_student_menu():
    stu_id = input("Please input student ID to be deleted: ").strip()
    if not student_exist(stu_id):
        print("ERROR! Student doesn't exist.")
        return
    delete_student(stu_id)


# Function to delete course.
def delete_course_menu():
    course_id = input("Please input course ID to be deleted: ").strip()
    if not course_exist(course_id):
        print("ERROR! Course doesn't exist.")
        return
    delete_course(course_id)


# Function to add course.
def add_course():
    course_id = input("Input new course ID: ").strip()
    if course_exist(course_id):
        print("ERROR! Course already exists.")
        return

    coursename = input("Enter course name: ").strip()
    semester = input("Enter semester for this course (number only): ").strip()

    new_course = f"{course_id},{coursename},{semester}"
    write_file("courses.txt", [new_course])
    print("Course added successfully.")
# Search course by id or name.
def search_course():
    keyw = input("Enter Course ID or Name to search: ").strip().lower()
    courses = read_file("courses.txt")
    found = False
    for x in courses:
        if keyw in x.lower():
            print(x)
            found = True
    if not found:
        print("No matching course found in database.")


# Search student by id or name.
def search_student():
    keyw = input("Enter Student ID or Name to search: ").strip().lower()
    students = read_file("students.txt")
    found = False
    for c in students:
        if keyw in c.lower():
            print(c)
            found = True
    if not found:
        print("No matching student found in database.")


# Main Menu function.
def main():
    print("Choose an option")
    print("1. Add Student")
    print("2. Delete Student")
    print("3. Add Course")
    print("4. Delete Course")
    print("5. Search Student")
    print("6. Search Course")

    choice_str = input("Choose 1-6: ").strip()
    if not choice_str.isdigit():
        print("Invalid input. Please enter a number between 1 and 6.")
        return

    choice = int(choice_str)

    if choice == 1:
        add_student()
    elif choice == 2:
        delete_student_menu()
    elif choice == 3:
        add_course()
    elif choice == 4:
        delete_course_menu()
    elif choice == 5:
        search_student()
    elif choice == 6:
        search_course()
    else:
        print("Invalid input. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()