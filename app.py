import streamlit as st
import pandas as pd
from datetime import date

# Page config
st.set_page_config(page_title="💰 Expense Tracker & Converter", layout="centered")

st.title("💰 Expense Tracker & Currency Converter")

# 1. Expense Tracker Part
if "expenses" not in st.session_state:
    st.session_state.expenses = []

with st.expander("➕ Add New Expense"):
    with st.form("expense_form", clear_on_submit=True):
        amount = st.number_input("Amount (INR)", min_value=0.0)
        category = st.selectbox("Category", ["Food", "Transport", "Books", "Others"])
        submitted = st.form_submit_button("Add")
        if submitted:
            st.session_state.expenses.append({"amount": amount, "category": category})

# 2. Currency Converter Part
st.subheader("💱 Quick Currency Converter")
amount_to_convert = st.number_input("Enter Amount in INR", min_value=0.0, value=100.0)
target_currency = st.selectbox("Convert to:", ["NPR (Nepal)", "USD (USA)", "EUR (Europe)"])

# Conversion rates
rates = {"NPR (Nepal)": 1.6, "USD (USA)": 0.012, "EUR (Europe)": 0.011}

if st.button("Convert"):
    converted = amount_to_convert * rates[target_currency]
    st.success(f"{amount_to_convert} INR = {converted:.2f} {target_currency.split(' ')[0]}")

# Display Expenses
if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)
    st.subheader("Your Expenses")
    st.dataframe(df)
