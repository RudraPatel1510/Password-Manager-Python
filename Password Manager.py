import os
import random
import json
import re
import string
from tkinter import *
from tkinter import messagebox



# --- Constants ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "passwords.json")
LOGO_FILE = os.path.join(BASE_DIR, "MyPassLogo.png")

# --- Functions ---

def generate_password():
    """Generate a random strong password."""
    password_length = 14
    characters = string.ascii_letters + string.digits + "!#$%&()*+"
    generated_password = ''.join(random.choice(characters) for _ in range(password_length))

    password_entry.delete(0, END)
    password_entry.insert(0, generated_password)


def search_credentials():
    """Search the JSON file for the entered website and display stored credentials."""
    website = website_entry.get()
    try:
        with open(DATA_FILE, "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="Password data file not found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Not Found", message="No details found for the entered website.")


def save_credentials():
    """Save the entered website, email, and password to the JSON file."""
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showwarning(title="Input Error", message="Please do not leave any fields empty.")
    elif re.fullmatch(r"^\w+@\w+\.(com|edu|gov|net|org|in)$", email, re.IGNORECASE):
        is_ok = messagebox.askokcancel(
            title="Confirm Details",
            message=f"Please confirm the details:\n\nWebsite: {website}\nEmail: {email}\nPassword: {password}\n\nSave these details?"
        )
        if is_ok:
            try:
                with open(DATA_FILE, "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open(DATA_FILE, "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open(DATA_FILE, "w") as data_file:
                    json.dump(data, data_file, indent=4)

            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)
    else:
        messagebox.showerror(title="Invalid Email", message="Please enter a valid email address.")


# --- UI Setup ---

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Logo
logo_image = PhotoImage(file=LOGO_FILE)
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entry Fields
website_entry = Entry(width=27)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_entry = Entry(width=52)
email_entry.grid(column=1, row=2, columnspan=2)

password_entry = Entry(width=27)
password_entry.grid(column=1, row=3)

# Buttons
generate_password_button = Button(text="Generate Password", width=20, command=generate_password)
generate_password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=38, command=save_credentials)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=20, command=search_credentials)
search_button.grid(column=2, row=1)

# Start the application
window.mainloop()
