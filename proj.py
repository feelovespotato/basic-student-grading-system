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

    print("student deleted")

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
        parts = g.split("|")
        c_id = parts[1].strip()

        if c_id != course_id:
            new_grade_list.append(g)

    with open("grades.txt", "w") as f:
        for item in new_grade_list:
            f.write(item + "\n")

    print("course deleted")

#Main function
def main():

    #Example student data
    students = [
        "509-001-031 | Yersh Poorvasaran | 509031@student.edu.my | Semester 3",
        "509-001-032 | Marcus Chong | 509032@student.edu.my | Semester 2",
        "509-001-033 | David Lim | 509033@student.edu.my | Semester 4",
    ]

    courses = [
    "CSC101 | Programming Fundamentals",
    "CSC102 | Data Structures and Algorithms",
    "CSC103 | Database Systems",
    ]

    grades = [
    "509-001-031 | CSC101 | 88 | A | 4.0",
    "509-001-032 | CSC102 | 76 | B+ | 3.3",
    "509-001-033 | CSC103 | 67 | B | 3.0",
    ]

    write_file("students.txt", students)
    write_file("courses.txt", courses)
    write_file("grades.txt", grades)

    students_data = read_file("students.txt")
    courses_data = read_file("courses.txt")
    grades_data = read_file("grades.txt")

    print("\n--- Students ---")
    for s in students_data:
        print(s)

    print("\n--- Courses ---")
    for c in courses_data:
        print(c)

    print("\n--- Grades ---")
    for g in grades_data:
        print(g)

if __name__ == "__main__":
    main()