import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout = 'wide',page_title = 'Startup Analysis')

df = pd.read_csv('startup_cleaned_data (1).csv')
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year 
df['month'] = df['date'].dt.month

def load_overall_analysis():
    st.title('Overall Analysis')
    # total amount
    total = round(df['amount'].sum())
    # max amount infused in startup
    max_funding = round(df.groupby('startup')['amount'].sum().sort_values(ascending= False).head(1).values[0])
    # avg ticket size
    avg_funding = round(df.groupby('startup')['amount'].sum().mean())
    # total funded startup
    num_startups = df['startup'].nunique()

    col1, col2 ,col3, col4 = st.columns(4)
    with col1:
      st.metric('Total',str(total) + 'Cr')
    with col2:
      st.metric('Max',str(max_funding) + 'Cr')
    with col3:
      st.metric('Avg Funding',str(avg_funding) + 'Cr')
    with col4:
      st.metric('Funded Startups',num_startups)
    
    st.header('MOM Graph')
    selected_option = st.selectbox('Select one',['Total','Count'])
    if selected_option == 'Total':
      temp_df = df.groupby(['year','month'])['amount'].sum().reset_index()

    else:
      temp_df = df.groupby(['year','month'])['amount'].count().reset_index()
    temp_df['x-axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig5 , ax5 = plt.subplots()
    ax5.plot(temp_df['x-axis'],temp_df['amount'])

    st.pyplot(fig5)

def load_investors_detail(investor):
    st.title(investor)
    #load recent 5 investment of investors
    last_5df = df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investment')
    st.dataframe(last_5df)


    col1,col2= st.columns(2)
    with col1:
    #biggest investments
      big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum(
      ).sort_values(ascending = False).head()
      st.subheader('Biggest Recent Investment')
      fig,ax = plt.subplots()
      ax.bar(big_series.index,big_series.values)
      st.pyplot(fig)

    with col2:
      vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
      st.subheader('Sectors Invested in')
      fig1,ax1 = plt.subplots()
      ax1.pie(vertical_series,labels = vertical_series.index,autopct="%0.01f%%")
      st.pyplot(fig1)

    col3,col4 = st.columns(2)
    with col3:
      vertical_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
      st.subheader('Stages Invested in')
      fig2,ax2 = plt.subplots()
      ax2.pie(vertical_series,labels = vertical_series.index,autopct="%0.01f%%")
      st.pyplot(fig2)
    
    with col4:
      vertical_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
      st.subheader('Cities Invested in')
      fig3,ax3 = plt.subplots()
      ax3.pie(vertical_series,labels = vertical_series.index,autopct="%0.01f%%")
      st.pyplot(fig3)

    col5,col6 = st.columns(2)
    with col5:    
     df['year'] = df['date'].dt.year
     year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
     st.subheader('YOY Investment')
     fig4,ax4 = plt.subplots()
     ax4.plot(year_series.index,year_series.values)
     st.pyplot(fig4)

st.sidebar.title('Startup analysis')
option = st.sidebar.selectbox('select one',['Overall','Investor','Startup'])

if option == 'Overall':
    load_overall_analysis()
elif option == 'Investor':
    selected_investors = st.sidebar.selectbox('select one',sorted(set((df['investors'].str.split(',').sum()))))
    btn1 = st.sidebar.button('Find Investor Details')
    if btn1:
        load_investors_detail(selected_investors)
else: 
    st.sidebar.selectbox('select one',sorted(df['startup'].unique().tolist()))
    st.title('Startup Analysis')
    btn2 = st.sidebar.button('Find Startup Details')

st.sidebar.markdown("""
- add
""")