import os

class Student:
    def __init__(self, student_id, student_name, email, semester):
        self.student_id = student_id
        self.name = student_name
        self.email = email
        self.semester = semester

class Course:
    def __init__(self, course_id, course_name):
        self.course_id = course_id
        self.course_name = course_name

class GradeSystem:
    def __init__(self, student_id, course, marks):
        self.student_id = student_id
        self.course = course
        self.marks = marks
        self.grade = self.grade_conversion_letter()     # auto conversion grade + grade point
        self.grade_point = self.grade_conversion_point(self.grade)

    def grade_conversion_letter(self):
        if self.marks >= 80:
            return "A+"
        elif self.marks >= 75:
            return "A"
        elif self.marks >= 70:
            return "B+"
        elif self.marks >= 65:
            return "B"
        elif self.marks >= 60:
            return "B-"
        elif self.marks >= 55:
            return "C+"
        elif self.marks >= 50:
            return "C"
        else:
            return "F"

    @staticmethod
    def grade_conversion_point(grade):
        points = {"A+": 4.00, "A": 3.67, "B+": 3.33, "B": 3.00,
                  "B-": 2.67, "C+": 2.33, "C": 2.00, "F": 0.00}
        return points[grade]


class GradeManager:
    def __init__(self):
        self.students = []
        self.courses = []
        self.grades = []

    def add_students(self, student_id, name, email, semester):
        student = Student(student_id, name, email, semester)
        self.students.append(student)

    def add_course(self, course_id, course_name):
        course = Course(course_id, course_name)
        self.courses.append(course)

    def add_grade(self, student_id, course_id, marks):
        grade = GradeSystem(student_id, course_id, marks)
        self.grades.append(grade)

    def read_students(self, filename ="students.txt"):  # txt format A | B | C
        try:
            with open(filename, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    parts = [p.strip() for p in line.split('|')]    # should be changed to , (delete empty spaces)

                    student_id, student_name, email, current_semester = parts[:4]   # ignore var after 3rd
                    self.add_students(student_id, student_name, email, current_semester)

            print("Loaded successfully!")

        except FileNotFoundError:
            print("File not found!")

    def read_course(self, filename ="courses.txt"):
        try:
            with open(filename, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    parts = [p.strip() for p in line.split('|')]

                    course_id, course_name = parts[:2]
                    self.add_course(course_id, course_name)

        except FileNotFoundError:
            print("File not found!")

    def read_grade(self, filename ="grades.txt"):
        try:
            with open(filename, "r") as f:
                for line in f:
                    line = line.strip()     ## remove spaces btw chars
                    if not line:            ## skip if empty line
                        continue

                    parts = [p.strip() for p in line.split('|')]

                    student_id, course_id, marks = parts[:3]
                    self.add_grade(student_id, course_id, float(marks))

            print("Loaded successfully!")

        except FileNotFoundError:
            print("File not found!")

    def update_marks(self, student_id, course_id,  new_marks):
        for grade in self.grades:
            if grade.student_id == student_id and grade.course_id == course_id: #
                grade.marks = new_marks
                grade.grade = grade.grade_conversion_letter()
                grade.grade_point = grade.grade_conversion_letter(grade.grade)

                print("Marks updated successfully!")
                return

        print("Grade record not found!")


    """def delete_mark(self, student_id, mark):
        while True:
            try:
                print("choose which mark to be updated")

            except IndexError:
                print("No mark available!")

    """


# main function for users
if __name__ == "__main__":
    gm = GradeManager()

    gm.read_students()
    gm.read_course()
    gm.read_grade()

    print("Files loaded successfully!")



## missing delete, gpa + cgpa for semesters calc, save function