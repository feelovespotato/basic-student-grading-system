import os
import sys

def file_path(*path_parts):
    folder_basepath = os.path.dirname(__file__)
    return os.path.join(folder_basepath,*path_parts)

def load_data():
    grade_record = []

    try:
        with open(file_path("grades.txt"), "r") as file:
            for line in file:
                if not line.strip():
                    continue

                parts = [p.strip() for p in line.split(',')]
                student_id, semester, course_id, marks = parts[:4]

                student_id = student_id
                semester = int(semester)
                course_id = str(course_id)
                marks = float(marks)

                grade_record.append({"student_id": student_id, "semester": semester, "course_id": course_id, "marks": marks})

        print("Loaded successfully!")
        return grade_record

    except FileNotFoundError:
        print("File not found!")
        return []

def grade_conversion_letter(marks):
    if marks >= 80:
        return "A+"
    elif marks >= 75:
        return "A"
    elif marks >= 70:
        return "B+"
    elif marks >= 65:
        return "B"
    elif marks >= 60:
        return "B-"
    elif marks >= 55:
        return "C+"
    elif marks >= 50:
        return "C"
    else:
        return "F"

def grade_conversion_point(letter):
    points = {"A+": 4.00, "A": 3.67, "B+": 3.33, "B": 3.00,
              "B-": 2.67, "C+": 2.33, "C": 2.00, "F": 0.00}
    return points[letter]

def add_grade(records, student_id, semester, course_id, marks):
    records.append({"student_id": student_id, "semester": semester, "course_id": course_id, "marks": marks})
    save_data(records)

def update_grade(records, student_id, course_id, marks):
    for r in records:
        if r["student_id"] == student_id and r["course_id"] == course_id:
            r["marks"] = marks
            save_data(records)
            return True

    return False

def delete_grade(records, student_id, course_id, semester):
    for r in records:
        if r["student_id"] == student_id and r["course_id"] == course_id and r["semester"] == semester:
            records.remove(r)
            save_data(records)
            return True

    return False
#---------------------------------------------------------------------------------------------------------------- FOR COSHIN

def calc_gpa(records, student_id, semester):
    semester_gpa = {}

    # find every sem (current + past) for each student
    student_semesters = []
    for r in records:
        if r["student_id"] == student_id:
            if r["semester"] not in student_semesters:    # prevent duplicate, add when not in list
                student_semesters.append(r["semester"])
    
    student_semesters.sort()

    for s in student_semesters:
        courses_in_sem = [] # for every courses this student have in this sem
        for r in records:
            if r["student_id"] == student_id and r["semester"] == s:
                courses_in_sem.append(r)

        total_points = 0
        for course in courses_in_sem:
            marks = course["marks"]
            letter_grade = grade_conversion_letter(marks)
            points_grade = grade_conversion_point(letter_grade)
            total_points += points_grade

        number_of_courses = len(courses_in_sem)
        if number_of_courses > 0:
            gpa = total_points / number_of_courses
        else:
            gpa = 0

        semester_gpa[s] = round(gpa, 2)
    return semester_gpa
#---------------------------------------------------------------------------------------------------------------- FOR COSHIN
def calc_cgpa(records, student_id):
    # need to find all courses this student have (current +past)
    student_courses = []
    for r in records:
        if r["student_id"] == student_id:
            student_courses.append(r)

    total_points = 0
    for course in student_courses:
        marks = course["marks"]
        letter_grade = grade_conversion_letter(marks)
        points_grade = grade_conversion_point(letter_grade)
        total_points += points_grade

    number_of_courses = len(student_courses)
    if number_of_courses > 0:
        cgpa = total_points / number_of_courses
    else:
        cgpa = 0

    return round(cgpa, 2)

def display_performance(records): # highest, lowest, average marks
    course_marks = {}
    for r in records:
        course_id = r["course_id"]
        marks = r["marks"]

        if course_id not in course_marks:
            course_marks[course_id] = []

        course_marks[course_id].append(marks)
        #tuple sort out the data
    for course_id, marks_list in course_marks.items():
        marks_max = max(marks_list)
        marks_min = min(marks_list)

        total_marks = sum(marks_list)
        average_marks = round(total_marks / len(marks_list),2)

        print(f"Course: {course_id}: Highest = {marks_max}, Lowest = {marks_min}, Average = {average_marks}")


def save_data(records): # when saving txt will also incl grade letter after marks
    with open(file_path("grades.txt"), "w") as file:
        for r in records:
            letter_grade = grade_conversion_letter(r["marks"])
            file.write(f"{r["student_id"]},{r["semester"]},{r["course_id"]},{r["marks"]},{letter_grade}\n")
        print("Data saved!")

def main():
    records = load_data()
    save_data(records)

if __name__ == "__main__":
    main()

# only for overwriting grade.txt with grade letter (automation)