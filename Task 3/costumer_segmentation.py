# Abdul Rafay Kalim, Task 3 customer_segmentation.py, Elevvo Pathways

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

print("📂 Loading dataset... please wait.")
# Loading data
df = pd.read_excel("Online Retail.xlsx", engine='openpyxl')

# Cleaning dataset
df = df[df['InvoiceNo'].astype(str).str.startswith('C') == False]  # remove cancellations
df.dropna(subset=['CustomerID'], inplace=True)  # remove missing IDs

# Calculating TotalPrice before grouping
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

print("📊 Calculating RFM metrics...")
# Reference date
current_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

# Calculating RFM (Recency, Frequency, Monetary)
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (current_date - x.max()).days,  # Recency
    'InvoiceNo': 'nunique',                                 # Frequency
    'TotalPrice': 'sum'                                     # Monetary
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

# RFM Segmentation
rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, labels=[4, 3, 2, 1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method="first"), 4, labels=[1, 2, 3, 4])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 4, labels=[1, 2, 3, 4])

rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

# Map segments
def segment_customer(score):
    if score == '444':
        return 'Champions'
    elif score[0] == '4':
        return 'Loyal Customers'
    elif score[1] == '4':
        return 'Frequent Buyers'
    elif score[2] == '4':
        return 'Big Spenders'
    else:
        return 'Others'

rfm['Segment'] = rfm['RFM_Score'].apply(segment_customer)

print("✅ Data processed successfully.")

# Marketing ideas for each segment
marketing_strategies = {
    "Champions - frequent, recent & high spenders": "Offer exclusive discounts & early product access.",
    "Loyal Customers - buy regularly & spend well": "Reward with loyalty programs & thank-you offers.",
    "Potential Loyalists - could become champions soon": "Provide special offers to encourage more purchases.",
    "At Risk - used to buy often but not anymore": "Send win-back campaigns & personalized offers.",
    "Hibernating - low spenders & inactive": "Run awareness campaigns to re-engage.",
    "Lost Customers - haven’t purchased in a long time": "Offer steep discounts to bring them back.",
    "New Customers - recently joined": "Send welcome emails & first-purchase discounts."
}

# 📊 VISUALIZING

# Bar chart - Customer count by segment (Vertical)
plt.figure(figsize=(10, 6))
sns.countplot(
    x='Segment',
    data=rfm,
    order=rfm['Segment'].value_counts().index,
    palette='viridis'
)
plt.title("Customer Count by Segment")
plt.ylabel("Count")
plt.xlabel("Segment")

# Pie chart - Segment proportion
plt.figure(figsize=(6, 6))
segment_counts = rfm['Segment'].value_counts()
plt.pie(
    segment_counts, 
    labels=segment_counts.index, 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=sns.color_palette("pastel")
)
plt.title("Segment Proportion")

# Line chart - Average Monetary value by segment
plt.figure(figsize=(10, 6))
avg_monetary = rfm.groupby('Segment')['Monetary'].mean().sort_values()
plt.plot(avg_monetary.index, avg_monetary.values, marker='o', color='orange')
plt.title("Average Monetary Value by Segment")
plt.xlabel("Segment")
plt.ylabel("Average Monetary (£)")
plt.grid(True)

plt.tight_layout()
plt.show()


# Customer Segments Count Plot
plt.figure(figsize=(10, 6))
sns.countplot(
    y='Segment',
    data=rfm,
    order=rfm['Segment'].value_counts().index,
    palette='viridis'
)
plt.title("Number of Customers in Each Segment")
plt.xlabel("Number of Customers")
plt.ylabel("Customer Segment")
plt.tight_layout()
plt.show()

# Average Spend Per Segment Plot
plt.figure(figsize=(10, 6))
avg_spend = rfm.groupby('Segment')['Monetary'].mean().sort_values()
sns.barplot(
    x=avg_spend.values,
    y=avg_spend.index,
    palette='coolwarm'
)
plt.title("Average Spending by Customer Segment")
plt.xlabel("Average Spend")
plt.ylabel("Customer Segment")
plt.tight_layout()
plt.show()

# Show marketing strategies
print("\n💡 Suggested Marketing Strategies:")
for seg, strategy in marketing_strategies.items():
    print(f"- {seg}: {strategy}")