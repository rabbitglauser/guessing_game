students = ["Harry 25 26.5 28",
            "Sammy 55 22 45",
            "Gregory 95 22 45",
            "Peter 75 22 45",
            "Andre 26 28 30"]
num_students = len(students)
selected_student = "Peter"


def run_me():
    n = num_students  # int(input("give me something to do ?>"))
    student_marks = {}
    for i in range(n):
        name, *line = students[i].split()  # input("").split()
        scores = list(map(float, line))
        student_marks[name] = scores
    query_name = selected_student  # input()

    students_scores = student_marks[query_name]

    total_score = 0
    for score in students_scores:
        total_score = total_score + score

    average_score = total_score/len(students_scores)
    print(round(average_score, 2))


if __name__ == '__main__':
    run_me()
