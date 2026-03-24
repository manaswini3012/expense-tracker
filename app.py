
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Expense Tracker", layout="wide")

# Title
st.title("💰 Smart Expense Tracker")
st.caption("Manage your daily expenses in a simple and smart way")

file = "data.csv"

# Create file if not exists
if not os.path.exists(file):
    df = pd.DataFrame(columns=["Amount", "Category", "Date", "Description"])
    df.to_csv(file, index=False)

# Load data
data = pd.read_csv(file)

# ------------------ ADD EXPENSE ------------------
st.markdown("---")
st.subheader("➕ Add Expense")

col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("Enter amount")
    category = st.selectbox("Select category", ["Food", "Travel", "Shopping", "Other"])

with col2:
    date = st.date_input("Select date")
    description = st.text_input("Description")

if st.button("➕ Add Expense"):
    new_data = pd.DataFrame([[amount, category, date, description]],
                            columns=["Amount", "Category", "Date", "Description"])
    
    new_data.to_csv(file, mode='a', header=False, index=False)
    st.success("✅ Expense Saved!")
    st.rerun()

# ------------------ SHOW DATA ------------------
st.markdown("---")
st.subheader("📋 All Expenses")
st.dataframe(data, use_container_width=True)

# ------------------ SUMMARY ------------------
st.markdown("---")
st.subheader("📊 Expense Summary")

if not data.empty:
    summary = data.groupby("Category")["Amount"].sum()

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.bar(summary.index, summary.values)

        ax.set_title("Category-wise Expenses")
        ax.set_xlabel("Category")
        ax.set_ylabel("Amount")

        plt.xticks(rotation=30)
        plt.tight_layout()

        st.pyplot(fig)

    # Insight
    top_category = summary.idxmax()
    top_value = summary.max()
    st.info(f"💡 Highest spending is on **{top_category}** (₹ {top_value})")

# ------------------ BUDGET ------------------
st.markdown("---")
st.subheader("💡 Budget Check")

budget = st.number_input("Enter your monthly budget")

total_spent = data["Amount"].sum()

col1, col2 = st.columns(2)

with col1:
    st.metric("💸 Total Spent", f"₹ {total_spent}")

with col2:
    if total_spent > budget:
        st.metric("⚠️ Status", "Over Budget")
    else:
        st.metric("✅ Status", "Safe")

if total_spent > budget:
    st.error("⚠️ You exceeded your budget!")
else:
    st.success("✅ You are within budget")

# ------------------ DELETE ------------------
st.markdown("---")
st.subheader("🧹 Delete Expense")

if not data.empty:
    index_to_delete = st.number_input(
        "Enter index to delete", min_value=0, max_value=len(data)-1, step=1
    )

    if st.button("🗑 Delete Expense"):
        data = data.drop(index_to_delete)
        data.to_csv(file, index=False)
        st.success("🗑️ Expense Deleted!")
        st.rerun()