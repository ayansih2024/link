import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Define the file path for the CSV file
csv_file_path = 'book_inventory.csv'

# Sample book inventory to be used only if the CSV file doesn't exist
sample_inventory = {
    "Book ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    "Title": ["Harry Potter", "The Hobbit", "1984", "Percy Jackson", "Theory of Everything", 
              "The Castle of Adventure", "Diary of a Wimpy Kid", "Rodrick Rules", 
              "Long Haul", "Double Down", "The Third Wheel", "Dog Days", "Hard Luck", "Konnichiwa Izumi"],
    "Author": ["J.K. Rowling", "J.R.R. Tolkien", "George Orwell", "Rick Riordan", "Stephen Hawking", 
               "Enid Blyton", "Jeff Kinney", "Jeff Kinney", "Jeff Kinney", "Jeff Kinney", 
               "Jeff Kinney", "Jeff Kinney", "Jeff Kinney", "N/A"],
    "Available": [True, True, False, True, True, True, True, True, True, True, True, True, True, True],
    "Rented By": ["", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    "Return Date": ["", "", "", "", "", "", "", "", "", "", "", "", "", ""]
}

# Load the inventory from the CSV file, or initialize with the sample inventory if the file doesn't exist
if os.path.exists(csv_file_path):
    df = pd.read_csv(csv_file_path)
else:
    df = pd.DataFrame(sample_inventory)
    df.to_csv(csv_file_path, index=False)

# Function to save the DataFrame to the CSV file
def save_inventory(df):
    df.to_csv(csv_file_path, index=False)

# Streamlit app
st.title("Book Rental Service")

# Display available books
st.header("Available Books")
st.table(df[df["Available"]])

# Rent a book section
st.header("Rent a Book")

with st.form("rent_form"):
    book_id = st.number_input("Enter Book ID to Rent", min_value=1, max_value=len(df))
    user_name = st.text_input("Your Name")
    days_to_rent = st.number_input("Number of Days to Rent", min_value=1, max_value=30, value=7)
    submit = st.form_submit_button("Rent")
      
    if submit:
        if book_id in df["Book ID"].values:
            if df.loc[df["Book ID"] == book_id, "Available"].values[0]:
                return_date = datetime.now() + pd.Timedelta(days=days_to_rent)
                df.loc[df["Book ID"] == book_id, "Available"] = False
                df.loc[df["Book ID"] == book_id, "Rented By"] = user_name
                df.loc[df["Book ID"] == book_id, "Return Date"] = return_date.strftime("%Y-%m-%d")
                save_inventory(df)
                st.success(f"Book rented successfully by {user_name} until {return_date.strftime('%Y-%m-%d')}!")
            else:
                st.error("This book is currently not available.")
        else:
            st.error("Invalid Book ID.")

# Return a book section
st.header("Return a Book")

with st.form("return_form"):
    return_book_id = st.number_input("Enter Book ID to Return", min_value=1, max_value=len(df), key="return")
    return_user_name = st.text_input("Your Name", key="return_name")
    return_submit = st.form_submit_button("Return")

    if return_submit:
        if return_book_id in df["Book ID"].values:
            if not df.loc[df["Book ID"] == return_book_id, "Available"].values[0] and df.loc[df["Book ID"] == return_book_id, "Rented By"].values[0] == return_user_name:
                df.loc[df["Book ID"] == return_book_id, "Available"] = True
                df.loc[df["Book ID"] == return_book_id, "Rented By"] = ""
                df.loc[df["Book ID"] == return_book_id, "Return Date"] = ""
                save_inventory(df)
                st.success(f"Book returned successfully by {return_user_name}!")
            else:
                st.error("This book is either not rented out or the name does not match.")
        else:
            st.error("Invalid Book ID.")

# Add a new book section
st.header("Add a New Book")

with st.form("add_book_form"):
    new_book_title = st.text_input("Book Title")
    new_book_author = st.text_input("Book Author")
    add_book_submit = st.form_submit_button("Add Book")

    if add_book_submit:
        if new_book_title and new_book_author:
            new_book_id = df["Book ID"].max() + 1
            new_book_entry = pd.DataFrame({
                "Book ID": [new_book_id],
                "Title": [new_book_title],
                "Author": [new_book_author],
                "Available": [True],
                "Rented By": [""],
                "Return Date": [""]
            })
            df = pd.concat([df, new_book_entry], ignore_index=True)
            save_inventory(df)
            st.success(f"Book '{new_book_title}' by {new_book_author} added successfully!")
        else:
            st.error("Both title and author fields must be filled.")

# Display current inventory
st.header("Current Inventory")
st.table(df)
