import os


def load_data():
    grade_record = []

    try:
        with open("grades.txt", "r") as file:
            for line in file:

                parts = [p.strip() for p in line.split(',')]
                student_id, semester, course_id, marks = parts[:4]

                marks = float(marks)

                grade_record.append({"student_id": student_id, "semester": semester, "course_id": course_id, "marks": marks})

        print("Loaded successfully!")
        return grade_record

    except FileNotFoundError:
        print("File not found!")
        return []

def save_data(records):
    with open("grades.txt", "w") as file:
        for r in records:
            file.write(f"{r["student_id"]},{r["semester"]},{r["course_id"]},{r["marks"]}\n")
            print("Data saved!")

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

def update_grade(records, student_id, semester, course_id, marks):
    for r in records:
        if r["student_id"] == student_id and r["course_id"] == course_id:
            r["marks"] = marks
            save_data(records)
            return True

    return False

def delete_grade(records, student_id, semester, course_id, marks):
    for r in records:
        if r["student_id"] == student_id and r["course_id"] == course_id:
            records.remove(r)
            save_data(records)
            return True

    return False

def calc_gpa(records, student_id, semester):
    selected_list = []
    for r in records:
        if r["student_id"] == student_id and r["semester"] == semester:
            selected_list.append(r)

    if not selected_list:
        return None

    points_list = []

    for r in selected_list:
        letter = grade_conversion_point(r["marks"])
        points = grade_conversion_point(letter)
        points_list.append(points)

    total_points = sum(points_list)
    gpa = total_points / len(points_list)
    return round(gpa, 2)

def calc_cgpa(records, student_id, semester):
    all_list = []

