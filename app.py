import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title= 'Indian-Startup-Analysis')

df = pd.read_csv('startup_cleaned-by-rajeev.csv')

# convert it into pandas datetime object
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['date'] = df['date'].dt.date

# Cleaning Cities Name
# df.replace('Ahmedabad','Ahemdabad',inplace = True)
# df.replace(['Bengaluru','Bangalore / SFO','Bangalore / San Mateo','Bangalore/ Bangkok','Banglore'],'Bangalore',inplace = True)
# df.replace('Bhubneswar','bhubaneswar',inplace = True)
# df.replace(['Delhi','New Delhi / US','New Delhi/ Houston','Nw Delhi'],'New Delhi',inplace = True)
# df.replace(['Mumbai / Global','Mumbai/Bengaluru'],'Mumbai',inplace = True)
# df.replace(['Pune / Dubai','Pune / Singapore','Pune / US','Pune/Seattle'],'Pune',inplace = True)
# df.replace('Gurgaon','Gurugram',inplace=True)

# Cleaning Rounds Names
# df.replace(['Pre Series A', 'Pre-series A', 'pre-Series A', 'pre-series A'], 'Pre-Series A', inplace=True)
# df.replace(['Angel / Seed Funding', 'Seed/ Angel Funding', 'Seed / Angle Funding', 'Seed/ Angel Funding', 'Seed/Angel Funding','Seed / Angel Funding'], 'Seed/Angel Funding', inplace=True)
# df.replace(['Seed Round','Seed','Seed funding'], 'Seed Funding', inplace=True)
# df.replace('Debt-Funding','Debt Funding',inplace = True)
# df.replace('Private','Private Funding',inplace = True)
# df.replace('Angel','Angel Round',inplace = True)
# df.replace('Private Equity Round','Private Equity',inplace = True)


# cleaning vertical name
# df.replace(['ECommerce', 'eCommerce', 'Ecommerce', 'E-commerce'],'E-Commerce', inplace=True)
# df.replace(['E-Tech', 'EdTech'],'Ed-Tech', inplace=True)
# df.replace('FinTech','Fin-Tech', inplace=True)

# cleaning company name
# df.replace('DST Global and Lightspeed Venture Partners\\\\xe2\\\\x80\\\\x99 global fund.','DST Global',inplace = True)
# df.replace(['SoftBank Group','Softbank Group','Softbank Group Corp'],'Softbank',inplace = True)

#df.replace(["Byju\\xe2\\x80\\x99s",""BYJU\\'S""],"BYJU'S",inplace = True)
df.drop(index=2,inplace= True)

def load_overall_analysis_details():
    st.title('Overall Analysis')

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        # Total amount invested
        total = round(df['amount'].sum())
        st.metric(label='Total Amount Invested',value = '₹'+str(total)+'cr')

    with col2:
        # maximum amount infused in a startup
        max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
        st.metric(label='Maximum Funding size ',value = '₹'+str(round(max_funding))+'cr')

    with col3:
        # average funding amount
        avg_funding = round((df.groupby('startup')['amount'].sum()).mean())
        st.metric(label='Average Funding size ', value = '₹'+str(avg_funding)+'cr')

    with col4:
        # total funded startup
        count = df['startup'].nunique()
        st.metric(label='Total funded StartUps',value=count)


    col5,col6 = st.columns(2)

    with col5:
    #MoM chart -> Total + Count

        st.header('Month on Month Investment Graph')
        selected_option = st.selectbox('Select Type',['Total Amount',' StartUp Count'])

        if selected_option == 'Total Amount':
            temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
            temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

            fig5, ax5 = plt.subplots()
            ax5.plot(temp_df['x_axis'], temp_df['amount'])
            st.pyplot(fig5)

        else:
            temp_df = df.groupby(['year', 'month'])['startup'].count().reset_index()
            temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

            fig5, ax5 = plt.subplots()
            ax5.plot(temp_df['x_axis'], temp_df['startup'])
            st.pyplot(fig5)


    with col6:
    # Sector Analysis Pie- top sectors(count+sum)

        st.header('Sector Analysis')
        option2 = st.selectbox('Select Type',['Total Amount','Count'])

        if option2 == 'Total Amount':
            sector_series = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(8)
        else:
            sector_series = df.groupby('vertical')['amount'].count().sort_values(ascending=False).head(8)

        fig6,ax6 = plt.subplots()
        ax6.pie(sector_series,labels = sector_series.index,autopct = '%0.01f')
        st.pyplot(fig6)

    # Type of funding

    col7,col8 = st.columns(2)

    with col7:

        st.subheader('Different types of Funding')
        l = sorted(df['round'].unique())
        type_of_funding = pd.DataFrame(l, columns=['Type'])
        st.dataframe(type_of_funding)

    # City wise funding

    with col8:
        st.subheader('Cities with most Funding')
        city_series = df.groupby('city')['amount'].sum().sort_values(ascending=False).head(10)

        fig7,ax7 = plt.subplots()
        ax7.pie(city_series,labels = city_series.index)
        st.pyplot(fig7)


    col9,col10 = st.columns(2)

    with col9:
        # Top Startups -> year wise -> Overall
        st.subheader('Top StartUps')
        selected_type = st.selectbox('Select One',['Year-Wise','Overall'])

        if selected_type == 'Year-Wise':
            top_df = df.groupby(['year','startup'])['amount'].sum().reset_index().sort_values(by=['year','amount'],ascending = [True,False]).drop_duplicates(subset=['year'],keep='first',ignore_index = True)

            top_df['year'] = top_df['year'].astype('str')
            top_df['year'] = top_df['year'].str.replace(',','')
            st.dataframe(top_df)

        else:
            st.dataframe(df.groupby(['startup'])['amount'].sum().sort_values(ascending=False).reset_index().head(15))

    with col10:
        # Top investors
        st.subheader('Top Investors')
        top_investors = df.groupby(['investors'])['amount'].sum().sort_values(ascending=False).reset_index().head(20)
        l = sorted(set(top_investors['investors'].str.split(',').sum()))
        st.dataframe(df[df['investors'].isin(l)].groupby('investors')['amount'].sum().sort_values(ascending=False).reset_index())


def load_investor_details(investor):

    st.title(investor)

    # 1. load recent 10 investments of the investor

    st.subheader('Most Recent Investments')
    last10_df = df[df['investors'].str.contains(investor)].sort_values(by='date', ascending=False,ignore_index=True).head(10)[['date','startup','vertical','city','round','amount']]
    st.dataframe(last10_df)

    # 2. biggest investments

    col1,col2 = st.columns(2)

    with col1:
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')

        fig,ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)

    # 3. Generally invests in ...
    # sector -> pie
    with col2:
         vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values(ascending=False).head(10)

         st.subheader('Sectors Invested')
         fig1,ax1 = plt.subplots()
         ax1.pie(vertical_series,labels = vertical_series.index,autopct = '%0.01f' )
         st.pyplot(fig1)


    col3,col4 = st.columns(2)

    # stage -> pie
    with col3:
        stage_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Stages Invested')
        fig2,ax2 = plt.subplots()
        ax2.pie(stage_series,labels = stage_series.index)
        st.pyplot(fig2)

    # city -> pie
    with col4:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum().sort_values(ascending=False).head(7)
        st.subheader('Cities with most Investments')
        fig3,ax3 = plt.subplots()
        ax3.pie(city_series,labels = city_series.index)
        st.pyplot(fig3)

    col5,col6 = st.columns(2)

    with col5:
    # YoY investment graph

        yoy_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
        st.subheader('Year on Year Investment')
        fig4,ax4 = plt.subplots()
        ax4.plot(yoy_series.index,yoy_series.values)
        st.pyplot(fig4)

    with col6:
    # Similar Investors

        st.subheader('Similar Investors')
        l = df[df['investors'].str.contains(investor)]['vertical'].value_counts().head(3).index.tolist()

        undis1 = df[df['investors'].str.contains('Undisclosed Investors', case=False)]
        undis2 = df[df['investors'].str.contains('Undisclosed', case=False)]
        undis3 = df[df['investors'].str.contains('Undisclosed investor', case=False)]

        undisclosed_indices = set(undis1.index).union(undis2.index).union(undis3.index)

        new_df = df.drop(index = undisclosed_indices)
        new = new_df[new_df['vertical'].isin(l)]['investors'].value_counts().reset_index().head(10).drop(columns = 'count')
        st.dataframe(new)


def load_startup_details(startup_name):

    # Name
    st.title(startup_name)

    # industry , sub-industry
    industry_name = df[df['startup'] == startup_name].groupby('vertical')['amount'].sum().sort_values(ascending=False).index[0]
    sub_industry_name = df[df['startup'] == startup_name].groupby('subvertical')['amount'].sum().sort_values(ascending=False).index[0].title()

    st.metric(label='Industry',value= industry_name)
    st.markdown("---")

    st.metric(label='Sub-Industry', value= sub_industry_name)
    st.markdown("---")

    # city
    city = df[df['startup'] == startup_name]['city'].unique()[0]
    st.metric(label='Location',value=city)
    st.markdown("---")

    # Funding Rounds

    st.header('Funding Rounds')
    funding_df = df[df['startup'] == 'Flipkart'][['round', 'investors', 'date','amount']].rename(columns={'round':'funding round','amount':'amount in cr'}).reset_index().drop(columns='index')
    st.dataframe(funding_df)
    st.markdown("---")


    # Similiar Company
    st.header('Similiar Companies')

    l1 = df[df['startup'] == startup_name].dropna(subset='vertical')['vertical'].tolist()
    l2 = df[df['startup'] == startup_name].dropna(subset='subvertical')['subvertical'].tolist()
    vertical_list = l1 + l2

    new_df = df[df['startup'] != startup_name]
    temp = pd.Series(new_df[new_df['vertical'].isin(vertical_list)]['startup'].drop_duplicates().unique()).reset_index().drop(columns=['index']).rename(columns={0: 'name'}).head(15)
    st.dataframe(temp)

st.sidebar.title('Indian StartUps Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp Analysis','Investor Analysis'])

if option == 'Overall Analysis':
    # btn1 = st.sidebar.button('Go')
    # if btn1:
        load_overall_analysis_details()

elif option == 'StartUp Analysis':

    df.drop(index=[33, 593], inplace=True)
    startup_name = st.sidebar.selectbox('Select StartUp',sorted(df['startup'].unique().tolist()))
    btn2 = st.sidebar.button('Find Startup Details')

    if btn2:
        load_startup_details(startup_name)


else:
    df.replace(['SoftBank Group', 'Softbank Group', 'Softbank Group Corp'], 'Softbank', inplace=True)
    investors_list = sorted(set(df['investors'].str.split(',').sum()))
    investors_list.pop(0)

    selected_investor = st.sidebar.selectbox('Select Investor',investors_list)
    btn3 = st.sidebar.button('Go')

    if btn3:
        load_investor_details(selected_investor)






