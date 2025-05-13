import random
import string
import json
from pathlib import Path
import streamlit as st

class Bank:
    database = 'data.json'
    data = []

    @classmethod
    def load_data(cls):
        if Path(cls.database).exists():
            with open(cls.database, 'r') as file:
                cls.data = json.load(file)
        else:
            cls.data = []
            cls.update_data()

    @classmethod
    def update_data(cls):
        with open(cls.database, 'w') as file:
            json.dump(cls.data, file, indent=4)

    @staticmethod
    def generate_account_number():
        chars = random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=7)
        random.shuffle(chars)
        return "".join(chars)

    @classmethod
    def find_user(cls, accnum, pin):
        return [i for i in cls.data if i['accountnumber'] == accnum and str(i['pin']) == str(pin)]


# Load data at start
Bank.load_data()

st.title("🏦 Bank Management System")

menu = st.sidebar.selectbox("Select Action", (
    "Create Account", 
    "Deposit Money", 
    "Withdraw Money", 
    "View Account Details", 
    "Update Account Details", 
    "Delete Account"
))

# CREATE
if menu == "Create Account":
    st.subheader("📝 Create New Account")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    email = st.text_input("Email")
    pin = st.text_input("4-digit PIN", type='password')
    
    if st.button("Create Account"):
        if age < 18:
            st.error("Must be 18+ to create account.")
        elif not pin.isdigit() or len(pin) != 4:
            st.error("PIN must be a 4-digit number.")
        else:
            account = {
                "name": name,
                "age": age,
                "email": email,
                "pin": int(pin),
                "accountnumber": Bank.generate_account_number(),
                "balance": 0
            }
            Bank.data.append(account)
            Bank.update_data()
            st.success("Account created successfully!")
            st.info(f"Save this account number: {account['accountnumber']}")

# DEPOSIT
elif menu == "Deposit Money":
    st.subheader("💰 Deposit Money")
    accnum = st.text_input("Account Number")
    pin = st.text_input("PIN", type='password')
    amount = st.number_input("Deposit Amount", min_value=1)

    if st.button("Deposit"):
        user = Bank.find_user(accnum, pin)
        if user:
            if amount > 100000:
                st.warning("Amount must be ≤ 100000")
            else:
                user[0]['balance'] += amount
                Bank.update_data()
                st.success("Deposit successful.")
        else:
            st.error("Invalid account number or PIN.")

# WITHDRAW
elif menu == "Withdraw Money":
    st.subheader("🏧 Withdraw Money")
    accnum = st.text_input("Account Number")
    pin = st.text_input("PIN", type='password')
    amount = st.number_input("Withdraw Amount", min_value=1)

    if st.button("Withdraw"):
        user = Bank.find_user(accnum, pin)
        if user:
            if user[0]['balance'] < amount:
                st.warning("Insufficient balance.")
            else:
                user[0]['balance'] -= amount
                Bank.update_data()
                st.success("Withdrawal successful.")
        else:
            st.error("Invalid account number or PIN.")

# SHOW DETAILS
elif menu == "View Account Details":
    st.subheader("📄 Account Information")
    accnum = st.text_input("Account Number")
    pin = st.text_input("PIN", type='password')

    if st.button("Show Details"):
        user = Bank.find_user(accnum, pin)
        if user:
            st.json(user[0])
        else:
            st.error("Invalid credentials.")

# UPDATE
elif menu == "Update Account Details":
    st.subheader("🛠️ Update Account")
    accnum = st.text_input("Account Number")
    pin = st.text_input("Current PIN", type='password')

    user = Bank.find_user(accnum, pin)

    if user:
        name = st.text_input("New Name", value=user[0]['name'])
        email = st.text_input("New Email", value=user[0]['email'])
        new_pin = st.text_input("New PIN", type='password', value=str(user[0]['pin']))

        if st.button("Update"):
            user[0]['name'] = name
            user[0]['email'] = email
            user[0]['pin'] = int(new_pin) if new_pin else user[0]['pin']
            Bank.update_data()
            st.success("Account updated successfully.")
    elif accnum and pin:
        st.error("No account found.")

# DELETE
elif menu == "Delete Account":
    st.subheader("🗑️ Delete Account")
    accnum = st.text_input("Account Number")
    pin = st.text_input("PIN", type='password')

    if st.button("Delete Account"):
        user = Bank.find_user(accnum, pin)
        if user:
            Bank.data.remove(user[0])
            Bank.update_data()
            st.success("Account deleted successfully.")
        else:
            st.error("Invalid credentials.")
