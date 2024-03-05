import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

dataset = pd.read_csv('./dataset/all_dataset_2.csv')
payment = pd.read_csv('./dataset/customers_dataset.csv')

def revenueGroupByCategory(sort):
  dataframe = dataset.groupby('product_category_name_english').agg({
      "order_id": "nunique",
      "price": ["sum", "min", "max", "mean"]
  })
  dataframe.columns = ['order_count', 'total_price', 'min_price', 'max_price', 'mean_price']
  if sort == 'count':
    return dataframe.sort_values(by='order_count', ascending=False).head()
  elif sort == 'price':
    return dataframe.sort_values(by='total_price', ascending=False).head()
  return 'wrong parameter'
  
def revenueGroupbyState(sort):
  dataframe =  dataset.groupby('customer_state').agg({
    "price": ["sum", "min", "max", "mean"],
    "order_id": "nunique"
  })

  dataframe.columns = [
      'Total',
      'Minimum',
      'Maximum',
      'Average',
      'Transaction Count'
  ]

  if sort == 'total':
    return dataframe.sort_values(by=dataframe.columns[0], ascending=False)
  elif sort == 'avg':
    return dataframe.sort_values(by=dataframe.columns[3], ascending=False)
  elif sort == 'count':
    return dataframe.sort_values(by=dataframe.columns[4], ascending=False)
  return 'wrong parameter'

def revenueGroupbyPayment(sort):
  dataframe = dataset.groupby(by='payment_type').agg({
    "order_id": "nunique",
    "payment_value": ["sum", "min", "max", "mean"]
  })

  dataframe.columns = [
    'Transaction',
    'Total Amount',
    'Minimum',
    'Maximum',
    'Average'
  ]

  if sort == 'total':
    return dataframe.sort_values(by=dataframe.columns[1], ascending=False)
  elif sort == 'count':
    return dataframe.sort_values(by=dataframe.columns[0], ascending=False)


st.title('e-Commerce Performance')

tabProduct, tabPayment = st.tabs(['Product', 'Payment'])

with tabProduct:
  st.header('Performance by Product Category (Top 5)')
  datasrc = revenueGroupByCategory('count')
  fig, [ax1, ax2] = plt.subplots(2, 1, figsize= [10, 10], facecolor='none')
  colors = ['#d63631', '#f2a49f', '#f2a49f', '#f2a49f', '#f2a49f']
  sns.barplot(
      data = datasrc,
      y = datasrc.index.values,
      x = 'order_count',
      ax = ax1,
      palette=colors,
      edgecolor='none'
  )
  for i, value in enumerate(datasrc['order_count']):
      ax1.text(value, i, str(value), ha='left', va='center', color='white')


  datasrc = revenueGroupByCategory('price')

  sns.barplot(
      data = datasrc,
      y = datasrc.index.values,
      x = 'total_price',
      ax = ax2,
      palette=colors,
      edgecolor='none'
  )
  for i, value in enumerate(datasrc['total_price']):
      ax2.text(value, i, str(value), ha='left', va='center', color='white')

  ax1.set_xlabel('')
  ax1.set_title('Order Count', color='white', fontweight='bold', fontsize=12)
  ax1.set_facecolor('none')
  ax1.tick_params(axis='x', colors='none')
  ax1.tick_params(axis='y', colors='white')
  ax1.spines['top'].set_visible(False)
  ax1.spines['right'].set_visible(False)
  ax1.spines['bottom'].set_visible(False)
  ax1.spines['left'].set_visible(False)

  ax2.set_xlabel('')
  ax2.set_title('Revenue', color='white', fontweight='bold', fontsize=12)
  ax2.set_facecolor('none')
  ax2.tick_params(axis='x', colors='none')
  ax2.tick_params(axis='y', colors='white')
  ax2.spines['top'].set_visible(False)
  ax2.spines['right'].set_visible(False)
  ax2.spines['bottom'].set_visible(False)
  ax2.spines['left'].set_visible(False)

  st.pyplot(fig)

with tabPayment:
  st.header('Payment Method Analytics')
  datasrc = revenueGroupbyPayment('total')

  fig, [ax1, ax2] = plt.subplots(2, 1, figsize=[10, 10], facecolor='none')

  sns.barplot(
      x = datasrc['Transaction'].sort_values(ascending=False),
      y = datasrc.index.values,
      ax=ax1,
      palette = colors,
      edgecolor = 'none'
  )
  for i, value in enumerate(datasrc['Transaction'].sort_values(ascending=False)):
      ax1.text(value, i, str(value), ha='left', va='center', color='white')

  sns.barplot(
      x = datasrc['Total Amount'].sort_values(ascending=False),
      y = datasrc.index.values,
      ax=ax2,
      palette = colors,
      edgecolor = 'none'
  )
  for i, value in enumerate(datasrc['Total Amount'].sort_values(ascending=False)):
      ax2.text(value, i, str(value), ha='left', va='center', color='white')

  ax1.set_xlabel('')
  ax1.set_title('Most Popular Payment Method', color='white', fontweight='bold', fontsize=12)
  ax1.set_facecolor('none')
  ax1.tick_params(axis='x', colors='none')
  ax1.tick_params(axis='y', colors='white')
  ax1.spines['top'].set_visible(False)
  ax1.spines['right'].set_visible(False)
  ax1.spines['bottom'].set_visible(False)
  ax1.spines['left'].set_visible(False)

  ax2.set_xlabel('')
  ax2.set_title('Transaction Value', color='white', fontweight='bold', fontsize=12)
  ax2.set_facecolor('none')
  ax2.tick_params(axis='x', colors='none')
  ax2.tick_params(axis='y', colors='white')
  ax2.spines['top'].set_visible(False)
  ax2.spines['right'].set_visible(False)
  ax2.spines['bottom'].set_visible(False)
  ax2.spines['left'].set_visible(False)

  st.pyplot(fig)
  st.table(datasrc)
