#File handling
#Function for writing to file.
def write_file(file_name, data_list):
    try:
        with open(file_name, "a") as x:
            for line in data_list:
                x.write(line + "\n")
        print(f"Data written to {file_name}")
    except Exception as e:
        print(f"Error writing {file_name}: {e}")
        return []

#Function for reading file
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
    
#Function for delete student
def delete_student(stu_id):
    #Reading all student lines.
    students = read_file("students.txt")
    new_list = []

    for line in students:
        if not line.startswith(stu_id):
            new_list.append(line)

    with open("students.txt", "w") as f:
        for item in new_list:
            f.write(item + "\n")

    #Reading all grades lines
    grades = read_file("grades.txt")
    new_grade_list = []

    for g in grades:
        if not g.startswith(stu_id):
            new_grade_list.append(g)

    with open("grades.txt", "w") as f:
        for item in new_grade_list:
            f.write(item + "\n")

    print("Student deleted succesfully")

#Function for delete courses
def delete_course(course_id): 

    #Reading all courses lines.
    courses = read_file("courses.txt")
    new_list = []

    for line in courses:
        if not line.startswith(course_id):
            new_list.append(line)

    with open("courses.txt", "w") as f:
        for item in new_list:
            f.write(item + "\n")

    #Remove grades for course
    grades = read_file("grades.txt")
    new_grade_list = []

    for g in grades:
        parts = g.split(",")
        c_id = parts[1].strip()

        if c_id != course_id:
            new_grade_list.append(g)

    with open("grades.txt", "w") as f:
        for item in new_grade_list:
            f.write(item + "\n")

    print("Course deleted sucessfully")


# =================================================================================
#Part 2 Goyu
#check if student exist or no, if exist already, become true
def student_exist(stu_id):
    student=read_file('students.txt')
    for s in student:
       parts=s.split(',')
       if parts[0].strip()== stu_id:
           return True
    return False
#check if course exist or no, if exist, then become true
def course_exist(course_id):
    course= read_file('courses.txt')
    for c in course:
        parts= c.split(',')
        if parts[0].strip() == course_id:
            return True
    return False

#Function to add student
def add_student():
    stu_id=input('Input student ID to add: ').strip()
    if student_exist(stu_id):
        print('ERROR! Student already exist')
        return
    name=input('Enter student name: ').strip()
    email=input('Enter student email: ').strip()
    semester=input('Enter the semester of student: ').strip()
    newstu= f"{stu_id},{name},{email},{semester}"
    write_file('students.txt',[newstu])
    print('Student added succesfully')
#Function to delete student 
def delete_student_menu():
    stu_id=input('Please input student ID to be deleted: ').strip()
    if not student_exist(stu_id):
        print("ERROR! Student doesn't exist")
        return
    delete_student(stu_id)
#function to delete course
def delete_course_menu():
    course_id=input('Please input course ID to be deleted: ').strip()
    if not course_exist(course_id):
        print("ERROR! Course doesn't exist")
        return
    delete_course(course_id)

#function to add course
def add_course():
    course_id=input('Input new course ID: ').strip()
    if course_exist(course_id):
        print('ERROR! Course already exist')
        return
    coursename=input('Enter course name: ').strip()
    new_course=f"{course_id},{coursename}"
    write_file("courses.txt", [new_course])
    print('Course added successfully')
#search course
def search_course():
    keyw= input('Enter Course ID or Name to Search: ').strip().lower()
    courses= read_file('courses.txt')
    found= False
    for x in courses:
        if keyw in x.lower():
            print(x)
            found= True
    if not found:
        print('No matching course found in database')
#search_student
def search_student():
    keyw = input("Enter Student ID or Name to search: ").strip().lower()
    students=read_file('students.txt')
    found= False
    for c in students:
        if keyw in c.lower():
            print(c)
            found = True

        if not found:
           print('No matching student found in database')


#Main Menu function
def main():
    print('Choose an option ')
    print('1. Add Student')
    print('2. Delete Student')
    print('3. Add Course')
    print('4. Delete Course')
    print('5. Search Student')
    print('6. Search Course')
    choice= int(input('Choose 1-4: '))
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
        print('Invalid Input')

if __name__ == "__main__":
    main()