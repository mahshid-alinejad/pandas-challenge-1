#!/usr/bin/env python
# coding: utf-8

# ## Part 1: Explore the Data
# 
# Import the data and use Pandas to learn more about the dataset.

# In[2]:


import pandas as pd

df = pd.read_csv('Resources/client_dataset.csv')

df.head()


# In[3]:


# View the column names in the data

df.columns


# In[4]:


# Use the describe function to gather some basic statistics

df.describe()


# In[5]:


# Use this space to do any additional research
# and familiarize yourself with the data.
print(df.dtypes)
print(df.shape)
print(df.info())
print(df.isnull().sum())
for column in df.columns:
    unique_values = df[column].unique()
    print(f"Unique values in {column}: {unique_values}")


# In[6]:


# What three item categories had the most entries?

category_counts = df['category'].value_counts()

category_counts.head(3)




# In[7]:


# For the category with the most entries,
# which subcategory had the most entries?

subcategory_counts = df['subcategory'].value_counts()
print(subcategory_counts.head(1))


# In[8]:


# Which five clients had the most entries in the data?
top_clients = df['client_id'].value_counts()
top_clients.head(5)


# In[9]:


# Store the client ids of those top 5 clients in a list.
top_5_client_id=[33615,66037,46820,38378,24741]
top_5_client_id 


# In[10]:


# How many total units (the qty column) did the
# client with the most entries order ?
total_units_top_client = df[df['client_id'] == 33615]['qty'].sum()
total_units_top_client


# ## Part 2: Transform the Data
# Do we know that this client spent the more money than client 66037? If not, how would we find out? Transform the data using the steps below to prepare it for analysis.

# In[11]:


# Create a column that calculates the 
# subtotal for each line using the unit_price
# and the qty
df["subtotal"]= df["unit_price"] * df["qty"]
df[["subtotal", 'unit_price','qty']].head(2)


# In[12]:


# Create a column for shipping price.
# Assume a shipping price of $7 per pound
# for orders over 50 pounds and $10 per
# pound for items 50 pounds or under.
def calculate_shipping_price(unit_weight):
    if unit_weight > 50:
        return 7 * unit_weight
    else:
        return 10 * unit_weight
df['total_weight'] = df['unit_weight'] * df['qty']
df['shipping_price'] = df['total_weight'].apply(calculate_shipping_price)
df[['unit_price', 'unit_weight', 'qty', 'total_weight', 'shipping_price']].head(3)



# In[13]:


# Create a column for the total price
# using the subtotal and the shipping price
# along with a sales tax of 9.25%

df["total_price"] = ((df["subtotal"] + df["shipping_price"]) *1.0925).round(2)
df[['shipping_price', 'subtotal', 'total_price']].head(3)


# In[14]:


# Create a column for the cost
# of each line using unit cost, qty, and
# shipping price (assume the shipping cost
# is exactly what is charged to the client).
df['line_cost'] = df['unit_cost'] * df['qty'] + df['shipping_price']
df[["line_cost"]].head(3)



# In[15]:


# Create a column for the profit of
# each line using line cost and line price
df["line_profit"]=df["total_price"]- df["line_cost"]
df[["line_profit"]].head(3)


# ## Part 3: Confirm your work
# You have email receipts showing that the total prices for 3 orders. Confirm that your calculations match the receipts. Remember, each order has multiple lines.
# 
# Order ID 2742071 had a total price of \$152,811.89
# 
# Order ID 2173913 had a total price of \$162,388.71
# 
# Order ID 6128929 had a total price of \$923,441.25
# 

# In[20]:


# Check your work using the totals above
df_1 = df.loc[df["order_id"] == 2742071]["total_price"]
print(f"Order 2742071 total :${df_1.sum():0.2f}")
       
df_2 = df.loc[df["order_id"] == 2173913]["total_price"]
print(f"Order 2173913 total :${df_1.sum():0.2f}")  

df_3 = df.loc[df["order_id"] == 6128929]["total_price"]
print(f"Order 6128929 total :${df_1.sum():0.2f}") 


# ## Part 4: Summarize and Analyze
# Use the new columns with confirmed values to find the following information.

# In[45]:


# How much did each of the top 5 clients by quantity
# spend? Check your work from Part 1 for client ids.
df_1_client = df.loc[df["client_id"] == 33615]["total_price"]

print(f"33615 :${df_1_client.sum():0.2f}")


df_2_client = df.loc[df["client_id"] == 66037]["total_price"]

print(f"66037 :${df_2_client.sum():0.2f}")


df_3_client = df.loc[df["client_id"] ==  46820]["total_price"]

print(f" 46820 :${df_3_client.sum():0.2f}")


df_4_client = df.loc[df["client_id"] == 38378]["total_price"]

print(f"38378 :${df_1_client.sum():0.2f}")


df_5_client = df.loc[df["client_id"] == 24741]["total_price"]

print(f"24741 :${df_1_client.sum():0.2f}")


# In[67]:


# Create a summary DataFrame showing the totals for the
# for the top 5 clients with the following information:
# total units purchased, total shipping price,
# total revenue, and total profit. Sort by total profit.

summary_df = df.loc[df['client_id'].isin(top_5_client_id)].groupby('client_id').agg(
    total_qty=('qty', 'sum'),
    total_shipping_price=('shipping_price', 'sum'),
    total_price = ('total_price', 'sum'),
    line_cost =("line_cost", "sum"), 
    line_profit=('line_profit', 'sum')
)

summary_df = summary_df.sort_values(by='line_profit', ascending=False).astype(int).reset_index()
summary_df.head()







# In[70]:


# Format the data and rename the columns
# to names suitable for presentation.
# Currency should be in millions of dollars.
summary_df.columns =["Client ID", "Units", "Shipping", "Total Revenue", "Total Cost", "Total Profit"]
formatting_list = ["Shipping", "Total Revenue", "Total Cost", "Total Profit"]
for col in formatting_list:
    
    summary_df[col] = summary_df[col] / 1000000
    summary_df[col] = summary_df[col].map("${:,.2f}M".format)




# In[73]:


# Sort the updated data by "Total Profit" form highest to lowest
summary_df.sort_values("Total Profit", ascending = False)


# In[ ]:




