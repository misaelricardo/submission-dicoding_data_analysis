import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
 
orders_complete_df = pd.read_csv('orders_complete.csv') #import csv to df

def create_most_cities_order_df(df):
    most_cities_orders_df = df.groupby('customer_city').agg({
    'customer_state':'first',
    'customer_id':'nunique',
    'order_id':'nunique'
    }).sort_values(by='order_id',ascending=False).reset_index()

    most_cities_orders_df.rename(columns={
    'customer_id':'customer_count',
    'order_id':'order_count'
    },inplace=True)

    return most_cities_orders_df 

def create_most_sold_monthly_2017_df(df):
    orders_2017_df = df[df['order_purchase_timestamp'].str.startswith('2017')]

    most_sold_monthly_2017_df = orders_2017_df.groupby('order_purchase_timestamp').agg({
    'item_count':'sum',
    'order_id':'count',
    'payment_value':'sum'
    }).sort_values(by='order_purchase_timestamp',ascending=True).reset_index()

    most_sold_monthly_2017_df.rename(columns={
    "order_id": "order_count"
    }, inplace=True)

    return most_sold_monthly_2017_df

def create_avg_review_score_df(df):
    avg_review_score_df = df.groupby('product_category_name').agg({
    'product_category_name_english':'first',
    'review_id':'count',
    'review_score':'mean'
    }).sort_values(by='review_score',ascending=False).reset_index()

    avg_review_score_df.rename(columns={
    'review_id':'review_count',
    'review_score':'avg_review_score'
    },inplace=True)

    avg_review_count = avg_review_score_df['review_count'].mean()
    avg_review_score_df = avg_review_score_df[avg_review_score_df['review_count'] > avg_review_count].sort_values(by='avg_review_score',ascending=False)    

    return avg_review_score_df

most_cities_orders_df = create_most_cities_order_df(orders_complete_df)
most_sold_monthly_2017_df = create_most_sold_monthly_2017_df(orders_complete_df)
avg_review_score_df= create_avg_review_score_df(orders_complete_df)


st.header('Brazilian E-Commerce Public Dataset Analysis')

####Visualisasi 1####
st.subheader("Cities with Most Order")

most_order_city = most_cities_orders_df['customer_city'].iloc[0]
most_order_count = most_cities_orders_df['order_count'].iloc[0]

col1, col2 = st.columns(2)
with col1:
    st.metric("City with the most order",value=most_order_city)
with col2:
    st.metric("Total orders in "+most_order_city,value=most_order_count)


plt.figure(figsize=(16, 8))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
plot = sns.barplot(x="customer_city", y="order_count", hue="customer_city", data=most_cities_orders_df.head(5), palette=colors)
plot.set_xlabel("Customer's City", fontsize=16) 
plot.set_ylabel("Order Count", fontsize=20)  
plt.xticks(size=16)
plt.yticks(size=20)
st.pyplot(plt)


####Visualisasi 2####
most_sold_monthly_2017_df['order_purchase_timestamp'] = pd.to_datetime(most_sold_monthly_2017_df['order_purchase_timestamp'], format='%Y-%m')
most_sold_monthly_2017_df['order_purchase_timestamp'] = most_sold_monthly_2017_df['order_purchase_timestamp'].dt.strftime('%B')

sorted_monthly_2017_df = most_sold_monthly_2017_df.sort_values(by="order_count",ascending=False).reset_index()
most_order_month_2017 = sorted_monthly_2017_df['order_purchase_timestamp'].iloc[0]
most_order_count_2017 = sorted_monthly_2017_df['order_count'].iloc[0]
least_order_month_2017 = sorted_monthly_2017_df['order_purchase_timestamp'].iloc[-1]
least_order_count_2017 = sorted_monthly_2017_df['order_count'].iloc[-1]

st.subheader("Monthly Order Totals in 2017")

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"Most Monthly Order ({most_order_month_2017}) : **{most_order_count_2017}**")
with col2:
    st.markdown(f"Least Monthly Order ({least_order_month_2017}) : **{least_order_count_2017}**")

plt.figure(figsize=(16, 8))
plot = sns.lineplot(x="order_purchase_timestamp", y="order_count", data=most_sold_monthly_2017_df, marker='o')
plot.set_xlabel("Year & Month", fontsize=16) 
plot.set_ylabel("Order Count", fontsize=20)
plt.xticks(size=16)
plt.yticks(size=16)
plt.xticks(rotation=45)
st.pyplot(plt)

####Visualisasi 3####
st.subheader("Product Categories Review")
tab1, tab2 = st.tabs(["Average Review Score", "Total Count of Review"])
with tab1:
    highest_reviewed_product = avg_review_score_df['product_category_name_english'].iloc[0]
    highest_reviewed_score = avg_review_score_df['avg_review_score'].iloc[0]
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Product with the highest average score",value=highest_reviewed_product)
    with col2:
        st.metric("Average review score of "+highest_reviewed_product,value=round(highest_reviewed_score,3))
    
    plt.figure(figsize=(16, 8))
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    plot = sns.barplot(x="product_category_name_english", y="avg_review_score", hue="product_category_name_english", data=avg_review_score_df.head(5), palette=colors)
    plot.set_xlabel("Product Category", fontsize=20) 
    plot.set_ylabel("Average Score of Review", fontsize=20)
    plt.xticks(size=16)
    plt.yticks(size=16)
    plt.title("Product Categories with The Highest Average Score", loc="center", fontsize=20)
    st.pyplot(plt)

with tab2:
    total_reviews_product_df = avg_review_score_df.sort_values(by="review_count",ascending=False).reset_index()
    most_reviewed_product = total_reviews_product_df['product_category_name_english'].iloc[0]
    total_most_review_product = total_reviews_product_df['review_count'].iloc[0]
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Product category with the most reviews",value=most_reviewed_product)
    with col2:
        st.metric("Total reviews of "+most_reviewed_product,value=total_most_review_product)
    
    plt.figure(figsize=(16, 8))
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    plot = sns.barplot(x="product_category_name_english", y="review_count", hue="product_category_name_english", data=total_reviews_product_df.head(5), palette=colors)
    plot.set_xlabel("Product Category", fontsize=20) 
    plot.set_ylabel("Total Count of Review", fontsize=20)
    plt.xticks(size=16)
    plt.yticks(size=16)
    plt.title("Product Categories with The Most Reviews", loc="center", fontsize=20)
    st.pyplot(plt)

with st.expander("See explanation"):
    st.write(
        """
        The charts above display product categories with total reviews surpassing the average. I applied this filter to account for numerous product categories with exceptionally high average scores but a limited number of reviews.
        """
    )