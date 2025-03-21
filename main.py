import customtkinter as ctk
from utils import add_transaction, get_balance, load_data, remove_transaction, update_transaction
import tkinter as tk  

# Theme configuration
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")  

# Function to update the transaction list
def update_transaction_list():
    for widget in transaction_frame.winfo_children():
        widget.destroy()

    transactions = load_data()["transactions"]
    for tx in transactions:
        frame = ctk.CTkFrame(transaction_frame, fg_color="#2E3B4E", corner_radius=10)  # Blu scuro con bordi arrotondati
        frame.pack(fill="x", pady=5, padx=5)

        label = ctk.CTkLabel(frame, text=f"{tx['category']} - {tx['amount']}€ ({tx['date']}) - Nota: {tx.get('note', 'Nessuna nota')}", 
                             anchor="w", text_color="white", font=("Arial", 12))
        label.pack(side="left", padx=10, pady=5)

        edit_btn = ctk.CTkButton(frame, text="✏️ Modifica", width=30, fg_color="#1F78D4", hover_color="#165A9C", 
                                 font=("Arial", 12), corner_radius=8, command=lambda tx=tx: edit_transaction(tx))
        edit_btn.pack(side="right", padx=5, pady=5)

        delete_btn = ctk.CTkButton(frame, text="🗑️ Elimina", width=30, fg_color="#E74C3C", hover_color="#C0392B", 
                                   font=("Arial", 12), corner_radius=8, command=lambda tx=tx: delete_transaction(tx["id"]))
        delete_btn.pack(side="right", padx=5, pady=5)

# function to delete a transaction
def delete_transaction(tx_id):
    remove_transaction(tx_id)
    update_transaction_list()
    balance_label.configure(text=f"Saldo: {get_balance()}€")

# function to edit a transaction
def edit_transaction(tx):
    category_var.set(tx["category"])
    amount_entry.delete(0, "end")
    amount_entry.insert(0, str(tx["amount"]))

    type_var.set(tx["type"])

    note_entry.delete(0, "end")
    note_entry.insert(0, tx.get("note", "")) 

    add_button.configure(text="Modifica", command=lambda: update_existing_transaction(tx["id"]))

# function to save the edit
def update_existing_transaction(tx_id):
    category = category_var.get()
    amount = float(amount_entry.get())
    tx_type = type_var.get()
    note = note_entry.get()

    update_transaction(tx_id, category, amount, tx_type, note)
    update_transaction_list()
    balance_label.configure(text=f"Saldo: {get_balance()}€")
    add_button.configure(text="Aggiungi Transazione", command=submit_transaction)

# function to add a transaction
def submit_transaction():
    category = category_var.get()
    amount = float(amount_entry.get())
    tx_type = type_var.get()
    note = note_entry.get()

    add_transaction(tx_type, category, amount, "2025-03-21", note) 
    update_transaction_list()
    balance_label.configure(text=f"Saldo: {get_balance()}€")

# function to add a new category
def add_new_category():
    new_category = new_category_entry.get()
    if new_category:
        categories.append(new_category)
        category_var.set(new_category)  
        new_category_window.destroy()  


def open_add_category_window():
    global new_category_window, new_category_entry
    new_category_window = ctk.CTkToplevel()
    new_category_window.title("Aggiungi Categoria")
    new_category_window.geometry("300x150")

    new_category_label = ctk.CTkLabel(new_category_window, text="Inserisci nome categoria:", font=("Arial", 14))
    new_category_label.pack(pady=10)

    new_category_entry = ctk.CTkEntry(new_category_window, placeholder_text="Nome categoria", font=("Arial", 12))
    new_category_entry.pack(pady=10)

    add_category_button = ctk.CTkButton(new_category_window, text="Aggiungi", command=add_new_category, 
                                        fg_color="#1F78D4", hover_color="#165A9C", font=("Arial", 12), corner_radius=8)
    add_category_button.pack(pady=10)

# Main app
app = ctk.CTk()
app.title("Budgeter")
app.geometry("1000x700")  

# Sidebar
sidebar = ctk.CTkFrame(master=app, width=200, fg_color="#2E3B4E", corner_radius=10)  # Sidebar con bordi arrotondati
sidebar.pack(side="left", fill="y", padx=10, pady=10)

ctk.CTkLabel(master=sidebar, text="💸 Budgeter", font=("Arial", 24, "bold"), text_color="white").pack(pady=20)

balance_label = ctk.CTkLabel(master=sidebar, text=f"Saldo: {get_balance()}€", font=("Arial", 16), text_color="white")
balance_label.pack(pady=10)


add_category_button = ctk.CTkButton(master=sidebar, text="➕ Aggiungi Categoria", command=open_add_category_window, 
                                    fg_color="#1F78D4", hover_color="#165A9C", font=("Arial", 14), corner_radius=8)
add_category_button.pack(pady=10)


main_frame = ctk.CTkFrame(master=app, fg_color="#2E3B4E", corner_radius=10)
main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Form to add a transaction
form_frame = ctk.CTkFrame(master=main_frame, fg_color="#3B4E6D", corner_radius=10)
form_frame.pack(fill="x", pady=10, padx=10)

categories = ["Spesa 💰", "Stipendio 💼", "Regalo 🎁", "Trasporti 🚗", "Casa 🏠", "Bollette 💡", "Alimenti 🍞", "Salute 🏥", "Debiti 💳", 
              "Lavoro 🧑‍💻", "Istruzione 🎓", "Tecnologia 💻", "Libri 📚", "Gioielli 💍", "Svago 🎮", "Fitness 🏋️", "Progetti 📊", 
              "Ristoranti 🍽️", "Vacanze 🏖️", "Energia 🔋", "Assicurazione 🛡️", "Viaggi ✈️", "Donazioni ❤️", "Spedizioni 📦", 
              "Bambini 👶", "Arredamento 🛋️", "Eventi 🎉", "Festa 🎈", "Cinema 🍿", "Natura 🌳", "Animali 🐶", "Musica 🎵"]

category_var = ctk.StringVar(value="Categorie")  # Default 'Categorie'
category_dropdown = ctk.CTkOptionMenu(master=form_frame, variable=category_var, values=categories, 
                                      font=("Arial", 14), fg_color="#1F78D4", button_color="#165A9C", dropdown_font=("Arial", 14))
category_dropdown.pack(side="left", padx=10, pady=10)

amount_entry = ctk.CTkEntry(master=form_frame, placeholder_text="Importo", font=("Arial", 14))
amount_entry.pack(side="left", padx=10, pady=10)

# Function to validate the amount input
def validate_amount_input(char, value):
    if value == "" or value.replace('.', '', 1).isdigit():
        return True
    return False

amount_entry.configure(validate="key", validatecommand=(app.register(validate_amount_input), "%S", "%P"))

type_var = ctk.StringVar(value="income")
income_button = ctk.CTkRadioButton(master=form_frame, text="Entrata", variable=type_var, value="income", 
                                   font=("Arial", 14), fg_color="#1F78D4", hover_color="#165A9C")
expense_button = ctk.CTkRadioButton(master=form_frame, text="Uscita", variable=type_var, value="expense", 
                                    font=("Arial", 14), fg_color="#1F78D4", hover_color="#165A9C")
income_button.pack(side="left", padx=10, pady=10)
expense_button.pack(side="left", padx=10, pady=10)

note_entry = ctk.CTkEntry(master=form_frame, placeholder_text="Nota", font=("Arial", 14))
note_entry.pack(side="left", padx=10, pady=10)

add_button = ctk.CTkButton(master=form_frame, text="Aggiungi Transazione", command=submit_transaction, 
                           fg_color="#1F78D4", hover_color="#165A9C", font=("Arial", 14), corner_radius=8)
add_button.pack(side="left", padx=10, pady=10)

# Transaction list
transaction_frame = ctk.CTkFrame(master=main_frame, fg_color="#3B4E6D", corner_radius=10)
transaction_frame.pack(fill="both", expand=True, pady=10, padx=10)

update_transaction_list()

app.mainloop()