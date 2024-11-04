import sqlite3
from tkinter import *

# Create the main window
root = Tk()
root.title('My Project')
root.geometry("500x600")

# Connect to database
conn = sqlite3.connect('data.db')

# Create cursor
c = conn.cursor()

# Create table if it doesn't exist
c.execute("""CREATE TABLE IF NOT EXISTS student (
    f_name TEXT,
    l_name TEXT,
    age INTEGER,
    address TEXT,
    email TEXT
)""")
conn.commit()

# Function to submit the form data to the database
def submit():
    c.execute("INSERT INTO student (f_name, l_name, age, address, email) VALUES (?, ?, ?, ?, ?)",
              (f_name.get(), l_name.get(), age.get(), address.get(), email.get()))
    conn.commit()
    clear_entries()

# Function to query and show records
def query():
    records_text.delete(1.0, END)
    c.execute("SELECT rowid, * FROM student")  # Including rowid for deletion
    records = c.fetchall()
    for record in records:
        records_text.insert(END, f"ID: {record[0]}, First Name: {record[1]}, Last Name: {record[2]}, Age: {record[3]}, Address: {record[4]}, Email: {record[5]}\n")

# Function to clear entry fields
def clear_entries():
    f_name.delete(0, END)
    l_name.delete(0, END)
    age.delete(0, END)
    address.delete(0, END)
    email.delete(0, END)

# Function to delete a record
def delete_record():
    try:
        c.execute("DELETE FROM student WHERE rowid=?", (delete_box.get(),))  # Use rowid for deletion
        conn.commit()
        delete_box.delete(0, END)
    except sqlite3.Error as e:
        print(f"Error deleting record: {e}")

# Entry fields
f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20)
l_name = Entry(root, width=30)
l_name.grid(row=1, column=1, padx=20)
age = Entry(root, width=30)
age.grid(row=2, column=1, padx=20)
address = Entry(root, width=30)
address.grid(row=3, column=1, padx=20)
email = Entry(root, width=30)
email.grid(row=4, column=1, padx=20)

# Entry for deleting records
delete_box = Entry(root, width=30)
delete_box.grid(row=5, column=1, padx=20)

# Labels
f_name_label = Label(root, text="First Name")
f_name_label.grid(row=0, column=0)
l_name_label = Label(root, text="Last Name")
l_name_label.grid(row=1, column=0)
age_label = Label(root, text="Age")
age_label.grid(row=2, column=0)
address_label = Label(root, text="Address")
address_label.grid(row=3, column=0)
email_label = Label(root, text="Email")
email_label.grid(row=4, column=0)
delete_label = Label(root, text="Record ID to delete:")
delete_label.grid(row=5, column=0)  # Adjusted to row 5 for better spacing

# Buttons
submit_btn = Button(root, text="Add Record to Database", command=submit)
submit_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

query_btn = Button(root, text="Show Records", command=query)
query_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

delete_btn = Button(root, text="Delete Record", command=delete_record)
delete_btn.grid(row=6, column=2, pady=10, padx=10)  # Aligned with delete_box

# Text box to display records
records_text = Text(root, width=60, height=15)
records_text.grid(row=9, column=0, columnspan=3, padx=20, pady=10)  # Updated row number

# Label for records display
records_label = Label(root, text="Records:")
records_label.grid(row=9, column=0, sticky=W, padx=20)

# Close connection when the program ends
def on_closing():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter main loop
root.mainloop()
