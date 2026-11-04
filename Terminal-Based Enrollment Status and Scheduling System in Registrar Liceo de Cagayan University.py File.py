
# Enrollment Status and Schedule System

import re

admins = {"admin1": "admin123"}
students = {}


# Checks Student ID
def valid_id(stud_id):
    return re.fullmatch(r"\d{2}-\d{4}-\d{6}", stud_id) is not None


# Checks name
def valid_name(name):
    parts = name.split(",")

    return (
        len(parts) == 2
        and parts[0].strip() != ""
        and len(parts[1].split()) >= 2
    )


# Checks course
def valid_course(course):
    return re.fullmatch(r"[A-Z]{2,}(?:-[A-Z]+)*", course) is not None


# Checks day
def valid_day(day):
    day = day.upper().replace(" ", "")
    days = []

    while day:
        if day.startswith("TH"):
            current = "TH"
            day = day[2:]
        elif day[0] in "MTWFS":
            current = day[0]
            day = day[1:]
        else:
            return False

        if current in days:
            return False

        days.append(current)

    return len(days) > 0


# Converts day keywords into a list
def get_day_list(day):
    day = day.upper().replace(" ", "")
    days = []

    while day:
        if day.startswith("TH"):
            days.append("TH")
            day = day[2:]
        else:
            days.append(day[0])
            day = day[1:]

    return days


# Checks time format and time order
def valid_time(time):
    pattern = (
        r"^(0?[1-9]|1[0-2]):([0-5][0-9])\s*(AM|PM)\s*-\s*"
        r"(0?[1-9]|1[0-2]):([0-5][0-9])\s*(AM|PM)$"
    )

    match = re.fullmatch(pattern, time.upper().strip())

    if not match:
        return False

    start_hour = int(match.group(1)) % 12
    start_minute = int(match.group(2))
    start_period = match.group(3)

    end_hour = int(match.group(4)) % 12
    end_minute = int(match.group(5))
    end_period = match.group(6)

    start_total = start_hour * 60 + start_minute
    end_total = end_hour * 60 + end_minute

    if start_period == "PM":
        start_total += 720

    if end_period == "PM":
        end_total += 720

    if start_period == "PM" and end_period == "AM":
        return False

    return end_total > start_total


# Checks if the same day and time already exist
def schedule_exists(day, time, subjects):
    new_days = get_day_list(day)

    for subject in subjects:
        old_days = get_day_list(subject["day"])

        if any(d in old_days for d in new_days):
            if time.upper().replace(" ", "") == subject["time"].upper().replace(" ", ""):
                return True

    return False


# Gets a valid Student ID
def get_valid_id():
    while True:
        stud_id = input("Enter Student ID (00-0000-000000): ").strip()

        if not valid_id(stud_id):
            print("Invalid Student ID. Please try again.")
        elif stud_id in students:
            print("Student ID already exists. Please try again.")
        else:
            return stud_id


# Gets a valid name
def get_valid_name():
    while True:
        name = input("Enter Name (Last name, First name(s)): ").strip()

        if valid_name(name):
            return name

        print("Invalid name. Please try again.")


# Gets a valid course
def get_valid_course():
    while True:
        course = input("Enter Course (e.g., BSIT): ").strip().upper()

        if valid_course(course):
            return course

        print("Invalid course. Please try again.")


# Gets a valid year level
def get_valid_year():
    while True:
        year = input("Enter Year Level (1-4): ").strip()

        if year in ["1", "2", "3", "4"]:
            return year

        print("Invalid year level. Enter 1-4.")


# Gets a valid day
def get_valid_day():
    while True:
        day = input("Enter Day (M, T, W, TH, F, S; e.g., MWF): ").strip().upper()

        if valid_day(day):
            return day

        print("Invalid day. Please try again.")


# Gets a valid time
def get_valid_time():
    while True:
        time = input("Enter Time (e.g., 9:00AM-11:00AM): ").strip().upper()

        if valid_time(time):
            return time

        print("Invalid time. Use standard time, e.g., 9:00AM-11:00AM.")


# Gets subjects and schedules
def get_subjects():
    subjects = []

    while True:
        print("\n--- ADD SUBJECT ---")

        while True:
            code = input("Enter Subject Code (e.g., IT101): ").strip().upper()

            if re.fullmatch(r"[A-Z]{2,}\d+[A-Z]*", code):
                if any(subject["code"] == code for subject in subjects):
                    print("Subject already exists. Please try again.")
                else:
                    break
            else:
                print("Invalid subject code. Please try again.")

        while True:
            day = get_valid_day()
            time = get_valid_time()

            if schedule_exists(day, time, subjects):
                print("The time is already existing. Please try again.")
                continue

            break

        subjects.append({
            "code": code,
            "day": day,
            "time": time
        })

        print("Subject added successfully!")

        while True:
            choice = input("Add another subject? (Y/N): ").strip().upper()

            if choice in ["Y", "N"]:
                break

            print("Invalid choice. Enter Y or N.")

        if choice == "N":
            break

    return subjects


# Displays subjects in a table
def show_subjects(subjects):
    print("-" * 60)
    print(f"{'Subject Code':<18}{'Day':<12}{'Time':<30}")
    print("-" * 60)

    for subject in subjects:
        print(
            f"{subject['code']:<18}"
            f"{subject['day']:<12}"
            f"{subject['time']:<30}"
        )

    print("-" * 60)


# Adds a student record
def add_student():
    print("\n--- ADD STUDENT RECORD ---")

    stud_id = get_valid_id()
    name = get_valid_name()
    course = get_valid_course()
    year = get_valid_year()
    subjects = get_subjects()

    students[stud_id] = {
        "name": name,
        "course": course,
        "year": year,
        "status": "Enrolled",
        "subjects": subjects
    }

    print("\nYOU ARE NOW ENROLLED!")
    print("Student Name:", name)
    print("Student Number:", stud_id)
    print("Course:", course)
    print("Year Level:", year)
    print("Enrollment Status: ENROLLED")
    print("\nSUBJECT SCHEDULE")
    show_subjects(subjects)


# Views all student records
def view_records():
    if not students:
        print("No student records found.")
        return

    for stud_id, data in students.items():
        print("\nStudent ID:", stud_id)
        print("Student Name:", data["name"])
        print("Course:", data["course"])
        print("Year Level:", data["year"])
        print("Enrollment Status:", data["status"])
        show_subjects(data["subjects"])


# Updates a student record
def update_student():
    if not students:
        print("No student records available.")
        return

    while True:
        stud_id = input("Enter Student ID: ").strip()

        if not valid_id(stud_id):
            print("Invalid Student ID. Please try again.")
        elif stud_id not in students:
            print("Student not found. Please try again.")
        else:
            break

    data = students[stud_id]

    while True:
        print("\n--- UPDATE MENU ---")
        print("1. Update Name")
        print("2. Update Course")
        print("3. Update Year Level")
        print("4. Replace Subjects")
        print("5. Return")

        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            data["name"] = get_valid_name()
            print("Name updated successfully!")

        elif choice == "2":
            data["course"] = get_valid_course()
            print("Course updated successfully!")

        elif choice == "3":
            data["year"] = get_valid_year()
            print("Year updated successfully!")

        elif choice == "4":
            new_subjects = get_subjects()
            if new_subjects:
                data["subjects"] = new_subjects
                print("Subjects updated successfully!")

        elif choice == "5":
            break

        else:
            print("Invalid choice. Enter 1-5.")


# Student portal
def student_portal():
    while True:
        stud_id = input("Enter Student ID: ").strip()

        if not valid_id(stud_id):
            print("Invalid Student ID. Please try again.")
        elif stud_id not in students:
            print("Student not found. Please try again.")
        else:
            break

    data = students[stud_id]

    print("\nStudent Name:", data["name"])
    print("Student Number:", stud_id)
    print("Course:", data["course"])
    print("Year Level:", data["year"])
    print("Enrollment Status:", data["status"])
    print("\nSUBJECT SCHEDULE")
    show_subjects(data["subjects"])


# Admin portal
def admin_portal():
    while True:
        print("\n--- ADMIN PORTAL ---")
        print("1. Add Student Record")
        print("2. View All Records")
        print("3. Update Student Record")
        print("4. Logout")

        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_records()
        elif choice == "3":
            update_student()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Enter 1-4.")


# Main menu
def main():
    while True:
        print("\nWELCOME TO ENROLLMENT STATUS AND SCHEDULE SYSTEM")
        print("1. Admin Login")
        print("2. Student Portal")
        print("3. Exit")

        choice = input("Enter choice (1-3): ").strip()

        if choice == "1":
            username = input("Enter Admin Username: ").strip()
            password = input("Enter Password: ")

            if username in admins and admins[username] == password:
                print("Welcome Admin!")
                admin_portal()
            else:
                print("Invalid username or password.")

        elif choice == "2":
            student_portal()

        elif choice == "3":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Enter 1-3.")


# Run the program
if __name__ == "__main__":
    main()
