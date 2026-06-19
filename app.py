import streamlit as st
import pandas as pd
from datetime import datetime, date
from io import StringIO

# Page configuration
st.set_page_config(page_title="💰 Personal Expense Tracker", layout="centered")

st.title("💰 Personal Expense Tracker")

# Initialize session state for expenses
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# Input form
with st.form("expense_form", clear_on_submit=True):
    expense = st.number_input("Enter your expense amount (Rs.)", min_value=0.0, format="%.2f")
    category = st.selectbox("Select Category:", ["Food", "Transport", "Books", "Home", "Entertainment", "Others"])
    note = st.text_input("Note (Optional)")
    exp_date = st.date_input("Date", value=date.today())
    submitted = st.form_submit_button("Add Expense")

if submitted:
    entry = {
        "amount": float(expense),
        "category": category,
        "note": note,
        "date": exp_date.isoformat(),
        "added_at": datetime.now().isoformat(timespec="seconds"),
    }
    st.session_state.expenses.append(entry)
    st.success(f"Added Rs. {expense:,.2f} to {category}!")

# Display and Analysis
if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    
    st.subheader("Expense History")
    st.dataframe(df[["date", "category", "amount", "note"]].sort_values(by="date", ascending=False), use_container_width=True)

    total = df["amount"].sum()
    count = len(df)
    
    col1, col2 = st.columns(2)
    col1.metric("Total Expense (Rs.)", f"{total:,.2f}")
    col2.metric("Total Entries", f"{count}")

    # Summary and Chart
    cat_summary = df.groupby("category", as_index=False)["amount"].sum().sort_values("amount", ascending=False)
    st.subheader("Expenses by Category")
    st.bar_chart(data=cat_summary.set_index("category"))

    # CSV Download
    csv_buf = StringIO()
    df.to_csv(csv_buf, index=False)
    st.download_button("Download CSV", data=csv_buf.getvalue(), file_name="expenses.csv", mime="text/csv")

    # Clear all data
    if st.button("Clear All Data"):
        st.session_state.expenses = []
        st.rerun()
else:
    st.info("No expenses added yet. Fill out the form above to get started!")
