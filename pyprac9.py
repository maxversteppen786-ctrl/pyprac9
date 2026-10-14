# =====================================================================
# Practical No 9: Python GUI Application with Local SQLite Database
# File: student_management.py
# =====================================================================

# ----------------- Step 2: Import Required Modules -----------------
import sqlite3
import tkinter as tk
from tkinter import messagebox

# ----------------- Step 3: Create the Database -----------------
connection = sqlite3.connect("students.db")
cursor = connection.cursor()

# ----------------- Step 4: Create the Student Table -----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    name TEXT,
    course TEXT,
    email TEXT
)
""")
connection.commit()

# ----------------- Step 8: Create the Add Function -----------------
def add_student():
    student_id = id_entry.get().strip()
    name = name_entry.get().strip()
    course = course_entry.get().strip()
    email = email_entry.get().strip()

    if student_id == "" or name == "" or course == "" or email == "":
        messagebox.showwarning("Warning", "Please fill all fields.")
        return

    try:
        cursor.execute(
            """
            INSERT INTO students (student_id, name, course, email)
            VALUES (?, ?, ?, ?)
            """,
            (student_id, name, course, email)
        )
        connection.commit()
        messagebox.showinfo("Success", "Student record added successfully.")
        clear_fields()
        display_students()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Student ID already exists.")

# ----------------- Step 9: Create the Display Function -----------------
def display_students():
    text_area.delete("1.0", tk.END)
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    if len(records) == 0:
        text_area.insert(tk.END, "No student records found.\n")
    else:
        for record in records:
            text_area.insert(
                tk.END,
                f"Student ID: {record[0]}\n"
                f"Name: {record[1]}\n"
                f"Course: {record[2]}\n"
                f"Email: {record[3]}\n"
                f"{'-' * 35}\n"
            )

# ----------------- Step 10: Create the Update Function -----------------
def update_student():
    student_id = id_entry.get().strip()
    name = name_entry.get().strip()
    course = course_entry.get().strip()
    email = email_entry.get().strip()

    if student_id == "":
        messagebox.showwarning("Warning", "Enter Student ID.")
        return

    cursor.execute(
        """
        UPDATE students
        SET name=?, course=?, email=?
        WHERE student_id=?
        """,
        (name, course, email, student_id)
    )
    connection.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo("Success", "Student record updated successfully.")
        clear_fields()
        display_students()
    else:
        messagebox.showwarning("Warning", "Student ID not found.")

# ----------------- Step 11: Create the Delete Function -----------------
def delete_student():
    student_id = id_entry.get().strip()

    if student_id == "":
        messagebox.showwarning("Warning", "Enter Student ID.")
        return

    cursor.execute("DELETE FROM students WHERE student_id=?", (student_id,))
    connection.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo("Success", "Student record deleted successfully.")
        clear_fields()
        display_students()
    else:
        messagebox.showwarning("Warning", "Student ID not found.")

# ----------------- Step 12: Create Clear Function -----------------
def clear_fields():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

# ----------------- Step 5: Create the Main Window -----------------
root = tk.Tk()
root.title("Student Management System")
root.geometry("600x550")
root.resizable(False, False)

# ----------------- Step 6: Add the Heading -----------------
heading = tk.Label(
    root,
    text="Student Management System",
    font=("Arial", 20, "bold")
)
heading.pack(pady=20)

# ----------------- Step 7: Create the Form -----------------
form_frame = tk.Frame(root)
form_frame.pack()

# Student ID Field
tk.Label(
    form_frame,
    text="Student ID:",
    font=("Arial", 12)
).grid(row=0, column=0, padx=10, pady=5, sticky="w")
id_entry = tk.Entry(form_frame, width=30)
id_entry.grid(row=0, column=1, pady=5)

# Student Name Field
tk.Label(
    form_frame,
    text="Name:",
    font=("Arial", 12)
).grid(row=1, column=0, padx=10, pady=5, sticky="w")
name_entry = tk.Entry(form_frame, width=30)
name_entry.grid(row=1, column=1, pady=5)

# Course Field
tk.Label(
    form_frame,
    text="Course:",
    font=("Arial", 12)
).grid(row=2, column=0, padx=10, pady=5, sticky="w")
course_entry = tk.Entry(form_frame, width=30)
course_entry.grid(row=2, column=1, pady=5)

# Email Field
tk.Label(
    form_frame,
    text="Email:",
    font=("Arial", 12)
).grid(row=3, column=0, padx=10, pady=5, sticky="w")
email_entry = tk.Entry(form_frame, width=30)
email_entry.grid(row=3, column=1, pady=5)

# ----------------- Step 13: Create Buttons -----------------
button_frame = tk.Frame(root)
button_frame.pack(pady=15)

# Add Button
tk.Button(
    button_frame,
    text="Add",
    width=12,
    command=add_student
).grid(row=0, column=0, padx=5, pady=5)

# Display Button
tk.Button(
    button_frame,
    text="Display",
    width=12,
    command=display_students
).grid(row=0, column=1, padx=5, pady=5)

# Update Button
tk.Button(
    button_frame,
    text="Update",
    width=12,
    command=update_student
).grid(row=0, column=2, padx=5, pady=5)

# Delete Button
tk.Button(
    button_frame,
    text="Delete",
    width=12,
    command=delete_student
).grid(row=1, column=0, padx=5, pady=5)

# Clear Button
tk.Button(
    button_frame,
    text="Clear",
    width=12,
    command=clear_fields
).grid(row=1, column=1, padx=5, pady=5)

# ----------------- Step 14: Create the Display Area -----------------
text_area = tk.Text(root, width=65, height=12)
text_area.pack(pady=10)

# ----------------- Step 15: Run the Application -----------------
root.mainloop()

# Close the database connection when the GUI is closed
connection.close()
