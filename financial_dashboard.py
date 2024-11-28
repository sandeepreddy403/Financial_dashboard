#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# In[2]:


# File path
file_path = r"C:\Users\DELL\Documents\financial_dashboard\family_financial_and_transactions_data.xlsx"


# In[3]:


# Load the single sheet
data = pd.read_excel(file_path)

# Display data summary
print(data.head())


# In[4]:


#  Data Analysis
print(data.columns)


# In[5]:


# visualisations
# Spending Distribution by Category
st.subheader("Spending Distribution by Category")
category_plot = sns.barplot(data=data, x='Category', y='Amount', ci=None)
plt.title("Spending Distribution by Category")
plt.xlabel("Category")
plt.ylabel("Total Amount Spent")
st.pyplot(plt.gcf())
plt.clf() 


# In[6]:


# family summary
family_summary = data.groupby('Family ID').agg(
    Income=('Income', 'sum'),
    Savings=('Savings', 'sum'),
    Monthly_Expenses=('Monthly Expenses', 'sum'),
    Loan_Payments=('Loan Payments', 'sum'),
    Credit_Card_Spending=('Credit Card Spending', 'sum'),
    Goals_Achieved=('Financial Goals Met (%)', 'mean')
)
family_summary['Savings_to_Income'] = family_summary['Savings'] / family_summary['Income']
family_summary['Expenses_to_Income'] = family_summary['Monthly_Expenses'] / family_summary['Income']
family_summary['Loan_to_Income'] = family_summary['Loan_Payments'] / family_summary['Income']
family_summary['Credit_to_Income'] = family_summary['Credit_Card_Spending'] / family_summary['Income']

print("\nFamily Summary:")
print(family_summary.head())


# In[7]:


# Member-Level Spending Analysis
member_spending = data.groupby('Member ID').agg(
    Total_Spent=('Amount', 'sum'),
    Transaction_Count=('Amount', 'count')
)

print("\nMember Spending Summary:")
print(member_spending)


# In[8]:


# Financial Scoring Model
def calculate_financial_score(row):
    score = 100
    score += row['Savings_to_Income'] * 40  # Reward savings
    score -= row['Expenses_to_Income'] * 30  # Penalize high expenses
    score -= row['Loan_to_Income'] * 20  # Penalize high loan payments
    score -= row['Credit_to_Income'] * 10  # Penalize high credit card spending
    score += row['Goals_Achieved'] * 20  # Reward achieving financial goals
    return max(0, min(score, 100))  # Keep score within 0–100

family_summary['Financial_Score'] = family_summary.apply(calculate_financial_score, axis=1)
print("\nFamily Financial Scores:")
print(family_summary[['Income', 'Savings_to_Income', 'Expenses_to_Income', 'Loan_to_Income', 'Financial_Score']])


# In[9]:


import streamlit as st
st.header("Calculate Financial Score for a Family")

# Input fields for financial data
income = st.number_input("Income", min_value=0.0, value=5000.0)
savings = st.number_input("Savings", min_value=0.0, value=1000.0)
monthly_expenses = st.number_input("Monthly Expenses", min_value=0.0, value=2000.0)
loan_payments = st.number_input("Loan Payments", min_value=0.0, value=500.0)
credit_card_spending = st.number_input("Credit Card Spending", min_value=0.0, value=300.0)
goals_achieved = st.slider("Financial Goals Achieved (%)", min_value=0, max_value=100, value=50)

# Calculate and display the score
if st.button("Calculate Financial Score"):
    score = 100
    score += (savings / income) * 40
    score -= (monthly_expenses / income) * 30
    score -= (loan_payments / income) * 20
    score -= (credit_card_spending / income) * 10
    score += (goals_achieved / 100) * 20
    score = max(0, min(score, 100))
    st.success(f"Financial Score: {round(score, 2)}")

# Footer
st.write("Built with ❤️ using Streamlit")


# In[ ]:




