import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Load the dataset
data = pd.read_csv("Imports_Exports_Dataset.csv")

# Set the title of the app
st.title("Imports and Exports Data Dashboard")

# Sidebar filters
st.sidebar.header("Filters")

# Category filter
categories = data['Category'].unique()
selected_category = st.sidebar.multiselect("Select Categories", options=categories, default=categories)

# Shipping method filter
shipping_methods = data['Shipping_Method'].unique()
selected_shipping_method = st.sidebar.multiselect("Select Shipping Method", options=shipping_methods, default=shipping_methods)

# Filter data based on selected filters
filtered_data = data[
    (data['Category'].isin(selected_category)) & 
    (data['Shipping_Method'].isin(selected_shipping_method))
]

# Create two columns for side-by-side layout
col1, col2 = st.columns(2)

# Import Values Visualization
with col1:
    import_values = filtered_data[filtered_data['Import_Export'] == 'Import'].groupby('Category')['Value'].sum().sort_values(ascending=False).head(10)
    fig_imports = plt.figure(figsize=(9, 5))
    import_values.plot(kind='bar', color='lightcoral', edgecolor='black')
    plt.title('Top 10 Categories by Import Value')
    plt.xlabel('Category')
    plt.ylabel('Import Value (in USD)')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig_imports)
    plt.clf()  # Clear the figure after displaying

# Export Values Visualization
with col2:
    export_values = filtered_data[filtered_data['Import_Export'] == 'Export'].groupby('Category')['Value'].sum().sort_values(ascending=False).head(10)
    fig_exports = plt.figure(figsize=(9, 5))
    export_values.plot(kind='bar', color='lightblue', edgecolor='black')
    plt.title('Top 10 Categories by Export Value')
    plt.xlabel('Category')
    plt.ylabel('Export Value (in USD)')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig_exports)
    plt.clf()  # Clear the figure after displaying

# Pie chart for Shipping Method
st.subheader("Proportion of Transactions by Shipping Method")
shipping_method_counts = filtered_data['Shipping_Method'].value_counts()
fig_shipping = plt.figure(figsize=(5, 5))
plt.pie(shipping_method_counts, labels=shipping_method_counts.index, autopct='%1.1f%%', colors=plt.cm.Paired.colors, startangle=90)
plt.title('Proportion of Transactions by Shipping Method')
plt.axis('equal')
st.pyplot(fig_shipping)
plt.clf()  # Clear the figure after displaying

# Pie chart for Import/Export type
import_export_counts = filtered_data['Import_Export'].value_counts()
fig_import_export = plt.figure(figsize=(5, 5))
plt.pie(import_export_counts, labels=import_export_counts.index, autopct='%1.1f%%', colors=plt.cm.Set3.colors, startangle=90)
plt.title('Proportion of Transactions by Import/Export Type')
plt.axis('equal')
st.pyplot(fig_import_export)
plt.clf()  # Clear the figure after displaying

# Customer-wise Transactions
st.subheader("Customer-wise Highest Import/Export Transactions")
customer_values = filtered_data.groupby(['Customer', 'Import_Export'])['Value'].sum().unstack().fillna(0)
top_customers = customer_values.sum(axis=1).sort_values(ascending=False).head(10)
top_customer_values = customer_values.loc[top_customers.index]
fig_customers = plt.figure(figsize=(7, 5))
top_customer_values.plot(kind='bar', stacked=True, color=['lightcoral', 'lightblue'], edgecolor='black')
plt.title('Customer-wise Highest Import/Export Transactions')
plt.xlabel('Customer')
plt.ylabel('Transaction Value (in USD)')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Transaction Type', loc='upper right')
st.pyplot(fig_customers)
plt.clf()  # Clear the figure after displaying

# Heatmap of Correlation
st.subheader("Correlation Heatmap of Numerical Features")
fig_heatmap = plt.figure(figsize=(8, 6))
correlation_matrix = filtered_data[['Quantity', 'Value', 'Weight']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap of Numerical Features')
st.pyplot(fig_heatmap)
plt.clf()  # Clear the figure after displaying

# Box plot for Shipping Method
st.subheader("Box Plot of Transaction Value by Shipping Method")
fig_box = plt.figure(figsize=(7, 5))
sns.boxplot(x='Shipping_Method', y='Value', data=filtered_data)
plt.title('Box Plot of Transaction Value by Shipping Method')
plt.ylabel('Transaction Value')
plt.xlabel('Shipping Method')
plt.xticks(rotation=45)
st.pyplot(fig_box)
plt.clf()  # Clear the figure after displaying

# Show treemap using Plotly
st.subheader("Treemap of Total Import/Export Values by Category")
category_values = filtered_data.groupby('Category')['Value'].sum().reset_index()
fig_treemap = px.treemap(category_values, 
                         path=['Category'],  
                         values='Value',     
                         title='Treemap of Total Import/Export Values by Category',
                         color='Value',      
                         color_continuous_scale='Viridis')
st.plotly_chart(fig_treemap)

# Bubble chart
st.subheader("Bubble Chart of Transaction Count vs Total Value by Category")
bubble_data = filtered_data.groupby('Category').agg({
    'Value': 'sum',         
    'Import_Export': 'count' 
}).reset_index()
bubble_data.rename(columns={'Import_Export': 'Transaction Count', 'Value': 'Total Value'}, inplace=True)

fig_bubble = px.scatter(bubble_data, 
                         x='Total Value', 
                         y='Transaction Count', 
                         size='Transaction Count', 
                         color='Category', 
                         hover_name='Category',
                         title='Bubble Chart of Transaction Count vs Total Value by Category',
                         size_max=60)  

st.plotly_chart(fig_bubble)

# Sunburst chart
st.subheader("Sunburst Chart of Import/Export Values by Category")
sunburst_data = filtered_data.groupby(['Category', 'Import_Export']).agg({'Value': 'sum'}).reset_index()

fig_sunburst = px.sunburst(sunburst_data, 
                           path=['Category', 'Import_Export'],  
                           values='Value',                       
                           title='Sunburst Chart of Import/Export Values by Category',
                           color='Value',                        
                           color_continuous_scale='Viridis')    
st.plotly_chart(fig_sunburst)
