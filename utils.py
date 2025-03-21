import json

DB_FILE = "db.json"


def load_data():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"transactions": []}


def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_transaction(tx_type, category, amount, date, note=""):
    data = load_data()
    new_id = len(data["transactions"]) + 1
    data["transactions"].append({
        "id": new_id,
        "type": tx_type,  
        "category": category,
        "amount": amount,
        "date": date,
        "note": note  
    })
    save_data(data)


def get_balance():
    data = load_data()
    income = sum(tx["amount"] for tx in data["transactions"] if tx["type"] == "income")
    expenses = sum(tx["amount"] for tx in data["transactions"] if tx["type"] == "expense")
    return income - expenses

def remove_transaction(tx_id):
    data = load_data()
    data["transactions"] = [tx for tx in data["transactions"] if tx["id"] != tx_id]
    save_data(data)


def update_transaction(tx_id, category, amount, tx_type, note=""):
    data = load_data()
    for tx in data["transactions"]:
        if tx["id"] == tx_id:
            tx["category"] = category
            tx["amount"] = amount
            tx["type"] = tx_type
            tx["note"] = note 
            break
    save_data(data)
