import requests
import psycopg2
import pandas as pd
import json
import plotly.express as px
import streamlit as st
import numpy as np
from babel.numbers import format_currency


# Connecting to Postgres database
db_1=psycopg2.connect(host='localhost',
                        user='postgres',
                        password='@122Madras',
                        database='Phonepe',
                        port= '5432')
cursor = db_1.cursor()

# URL to plot India map 
url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"



# function to create geo visualization for transactions amount
def transactions_amount(year,quarter):
    query= f''' SELECT states,SUM(transaction_count),sum(transaction_amount) FROM aggre_trans_table
                WHERE year = {year} and quarter = {quarter}
                GROUP BY states 
                ORDER BY states '''

    cursor.execute(query)
    db_1.commit()

    df1= pd.DataFrame(cursor.fetchall(),columns=["States","Transaction_count","Transaction_amount"])

    df1.Transaction_count = df1.Transaction_count.astype(np.int64)
    df1.Transaction_amount = df1.Transaction_amount.astype(np.int64)

    df1.rename(columns={'Transaction_count': 'Transaction count','Transaction_amount':'Transaction amount'}, inplace=True)

    fig_1 = px.choropleth(
            df1,
            geojson=url,
            featureidkey='properties.ST_NM',
            locations='States',
            color='Transaction amount',
            title="TRANSACTION AMOUNT",
            color_continuous_scale="Sunsetdark", 
            hover_name= "States",
            width =700, height= 700
            )

    fig_1.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_1,use_container_width=True)

# function to create geo visualization for transactions count
def transactions_count(year,quarter):
    query= f''' SELECT states,SUM(transaction_count),sum(transaction_amount) FROM aggre_trans_table
                WHERE year = {year} and quarter = {quarter}
                GROUP BY states 
                ORDER BY states '''

    cursor.execute(query)
    db_1.commit()

    df1= pd.DataFrame(cursor.fetchall(),columns=["States","Transaction_count","Transaction_amount"])

    df1.Transaction_count = df1.Transaction_count.astype(np.int64)
    df1.Transaction_amount = df1.Transaction_amount.astype(np.int64)

    df1.rename(columns={'Transaction_count': 'Transaction count','Transaction_amount':'Transaction amount'}, inplace=True)

    fig_2 = px.choropleth(
            df1,
            geojson=url,
            featureidkey='properties.ST_NM',
            locations='States',
            color='Transaction count',
            title="TRANSACTION COUNT",
            color_continuous_scale="Sunsetdark", 
            hover_name= "States",
            width =700, height= 700
            )

    fig_2.update_geos(fitbounds="locations", visible=False)

    st.plotly_chart(fig_2,use_container_width=True)


# Transactions type - count
def transactions_type_count(year,quarter):


    query= f''' SELECT transaction_name,SUM(transaction_count) as transaction_count,sum(transaction_amount) as transaction_amount FROM aggre_trans_table
                    WHERE year = {year} and quarter = {quarter}
                    GROUP BY transaction_name 
                    ORDER BY transaction_count desc'''

    cursor.execute(query)
    db_1.commit()

    df1= pd.DataFrame(cursor.fetchall(),columns=["Transaction_name","Transaction_count","Transaction_amount"])

    df1.Transaction_count = df1.Transaction_count.astype(np.int64)
    df1.Transaction_amount = df1.Transaction_amount.astype(np.int64)

    fig = px.bar(df1,
                title='Transaction Types vs Total Transactions Count',
                x="Transaction_name",
                y="Transaction_count",
                color_discrete_sequence=px.colors.sequential.Purples_r,
                labels={'Transaction_name': 'Transaction type', 'Transaction_count': 'Transaction Count'}
                )

    st.plotly_chart(fig,use_container_width=False)

# Transactions type - amount
def transactions_type_amount(year,quarter):

    query= f''' SELECT transaction_name,SUM(transaction_count) as transaction_count,sum(transaction_amount) as transaction_amount FROM aggre_trans_table
                    WHERE year = {year} and quarter = {quarter}
                    GROUP BY transaction_name 
                    ORDER BY transaction_amount desc'''

    cursor.execute(query)
    db_1.commit()

    df1= pd.DataFrame(cursor.fetchall(),columns=["Transaction_name","Transaction_count","Transaction_amount"])

    df1.Transaction_count = df1.Transaction_count.astype(np.int64)
    df1.Transaction_amount = df1.Transaction_amount.astype(np.int64)

    fig = px.bar(df1,
                title='Transaction Types vs Total Transactions Amount',
                x="Transaction_name",
                y="Transaction_amount",
                color_discrete_sequence=px.colors.sequential.Purples_r,
                labels={'Transaction_name': 'Transaction type', 'Transaction_amount': 'Transaction amount'}
                )

    st.plotly_chart(fig,use_container_width=False)

# Top 10 states - transactions (count)
def top_trans_states_count(year,quarter):

    query_1= f''' SELECT states,SUM(Transaction_count)as transaction_count FROM aggre_trans_table
                        WHERE year = {year} and quarter = {quarter}
                        GROUP BY states 
                        ORDER BY transaction_count desc
                        LIMIT 10'''

    cursor.execute(query_1)
    db_1.commit()

    df1= pd.DataFrame(cursor.fetchall(),columns=["States","Transaction_count"])

    fig_1 = px.bar(df1,
                title='Top 10 states with highest transaction count',
                x="States",
                y="Transaction_count",
                color_discrete_sequence=px.colors.sequential.Purples_r,
                labels={'Transaction_count': 'Transaction Count'}
                    )
    st.plotly_chart(fig_1,use_container_width=False)

# Top 10 states - transactions (amount)
def top_trans_states_amount(year,quarter):

    query_2= f''' SELECT states,SUM(Transaction_amount)as Transaction_amount FROM aggre_trans_table
                        WHERE year = {year} and quarter = {quarter}
                        GROUP BY states 
                        ORDER BY Transaction_amount desc
                        LIMIT 10'''

    cursor.execute(query_2)
    db_1.commit()

    df2= pd.DataFrame(cursor.fetchall(),columns=["States","Transaction_amount"])

    fig_2 = px.bar(df2,
                title='Top 10 states with highest Transaction amount',
                x="States",
                y="Transaction_amount",
                color_discrete_sequence=px.colors.sequential.Purples_r,
                labels={'Transaction_amount': 'Transaction Amount'}
                    )

    st.plotly_chart(fig_2,use_container_width=False)

# Top 10 districts - transactions (count)
def top_trans_districts_count(year,quarter):
    
    query_1= f''' SELECT district,transaction_count FROM map_trans_table
                WHERE year = {year} and quarter = {quarter}
                ORDER BY transaction_count desc
                LIMIT 10'''

    cursor.execute(query_1)
    db_1.commit()

    df1= pd.DataFrame(cursor.fetchall(),columns=["Districts","Transaction_count"])

    fig_1 = px.bar(df1,
                title='Top 10 districts with highest PhonePe transaction count',
                x="Districts",
                y="Transaction_count",
                color_discrete_sequence=px.colors.sequential.Purples_r,
                labels={'Transaction_count': 'Transaction Count'}
                    )
    st.plotly_chart(fig_1,use_container_width=False)


# Top 10 districts - transactions (amount)
def top_trans_districts_amount(year,quarter):

    query_2= f''' SELECT district,transaction_amount FROM map_trans_table
                WHERE year = {year} and quarter = {quarter}
                ORDER BY transaction_amount desc
                LIMIT 10'''

    cursor.execute(query_2)
    db_1.commit()

    df2= pd.DataFrame(cursor.fetchall(),columns=["Districts","Transaction_amount"])

    fig_2 = px.bar(df2,
                title='Top 10 districts with highest PhonePe transaction amount',
                x="Districts",
                y="Transaction_amount",
                color_discrete_sequence=px.colors.sequential.Purples_r,
                labels={'Transaction_amount': 'Transaction amount'}
                    )
    st.plotly_chart(fig_2,use_container_width=False)

# Top 10 pincode - transactions (count)
def top_trans_pincode_count(year,quarter):

	query_1= f'''SELECT pin_code, transaction_count FROM top_trans_table
				WHERE year = {year} and quarter = {quarter}
				ORDER BY transaction_count desc
				LIMIT 10'''

	cursor.execute(query_1)
	db_1.commit()

	df1= pd.DataFrame(cursor.fetchall(),columns=["pin_code",'transaction_count'])

	fig=px.bar(df1,
			title='Top 10 pin codes with highest PhonePe transaction count',
			x='pin_code',
			y="transaction_count",
			color_discrete_sequence=px.colors.sequential.Purples_r,
			labels={'pin_code': 'Pin code',"transaction_count":"Transaction count"}
			)
	fig.update_layout(xaxis_type='category')
	st.plotly_chart(fig,use_container_width=False)

# Top 10 pincode - transactions (amount)
def top_trans_pincode_amount(year,quarter):

	query_1= f'''SELECT pin_code, transaction_amount as transaction_amount FROM top_trans_table
				WHERE year = {year} and quarter = {quarter}
				ORDER BY transaction_amount desc
				LIMIT 10'''

	cursor.execute(query_1)
	db_1.commit()

	df1= pd.DataFrame(cursor.fetchall(),columns=["pin_code",'transaction_amount'])

	fig=px.bar(df1,
				title='Top 10 pin codes with highest PhonePe transaction amount',
				x= 'pin_code',
				y="transaction_amount",
				color_discrete_sequence=px.colors.sequential.Purples_r,
				labels={'pin_code': 'Pin code',"transaction_amount":"Transaction amount"}
				)

	fig.update_layout(xaxis_type='category')
	st.plotly_chart(fig,use_container_width=False)

#Function to get the registered users
def user(year,quarter):
	query= f''' SELECT states,SUM(registered_users) as registered_users ,SUM(app_opens) as app_opens FROM map_user_table
					WHERE year = {year} and quarter = {quarter}
					GROUP BY states 
					ORDER BY states '''

	cursor.execute(query)
	db_1.commit()

	df1= pd.DataFrame(cursor.fetchall(),columns=["States","registered_users","app_opens"])

	df1.registered_users = df1.registered_users.astype(np.int64)
	df1.app_opens = df1.app_opens.astype(np.int64)

	df1.rename(columns={'registered_users': 'Registered users','app_opens':'App opens'}, inplace=True)


	fig_1 = px.choropleth(
			df1,
			geojson=url,
			featureidkey='properties.ST_NM',
			locations='States',
			color='Registered users',
			title="Registered Users",
			color_continuous_scale="Sunsetdark", 
			hover_name= "States",
			hover_data='App opens',
            width=700,height=700
			)

	fig_1.update_geos(fitbounds="locations", visible=False)

	st.plotly_chart(fig_1,use_container_width=True)

#Top 10 states - registered users 

def top_users_states_registered_users(year,quarter):

    query_1= f''' SELECT states,SUM(registered_users)as registered_users FROM map_user_table
                        WHERE year = {year} and quarter = {quarter}
                        GROUP BY states 
                        ORDER BY registered_users desc
                        LIMIT 10'''

    cursor.execute(query_1)
    db_1.commit()

    df1= pd.DataFrame(cursor.fetchall(),columns=["States","registered_users"])

    fig_1 = px.bar(df1,
                title='Top 10 states with highest Registered PhonePe users ',
                x="States",
                y="registered_users",
                color_discrete_sequence=px.colors.sequential.Purples_r,
                labels={'registered_users': 'Registered users'}
                    )
    st.plotly_chart(fig_1,use_container_width=False)

#Top 10 states - app_opens

def top_users_states_app_opens(year,quarter):

    query_2= f''' SELECT states,SUM(app_opens)as app_opens FROM map_user_table
                        WHERE year = {year} and quarter = {quarter}
                        GROUP BY states 
                        ORDER BY app_opens desc
                        LIMIT 10'''

    cursor.execute(query_2)
    db_1.commit()

    df2= pd.DataFrame(cursor.fetchall(),columns=["States","app_opens"])

    fig_2 = px.bar(df2,
                title='Top 10 states with highest PhonePe app opens',
                x="States",
                y="app_opens",
                color_discrete_sequence=px.colors.sequential.Purples_r,
                labels={'app_opens': 'App opens'}
                )

    st.plotly_chart(fig_2,use_container_width=False)

# Top 10 districts - registered users

def top_users_districts_registered_users(year,quarter):

    query_1= f''' SELECT district,registered_users FROM map_user_table
                WHERE year = {year} and quarter = {quarter}
                ORDER BY registered_users desc
                LIMIT 10'''

    cursor.execute(query_1)
    db_1.commit()

    df1= pd.DataFrame(cursor.fetchall(),columns=["Districts","registered_users"])

    fig_1 = px.bar(df1,
                title='Top 10 districts with highest Registered PhonePe users',
                x="Districts",
                y="registered_users",
                color_discrete_sequence=px.colors.sequential.Purples_r,
                labels={'registered_users': 'Registered users'}
                    )
    st.plotly_chart(fig_1,use_container_width=False)

# Top 10 districts - app opens
    
def top_users_districts_app_opens(year,quarter):
    query_2= f''' SELECT district,app_opens FROM map_user_table
                WHERE year = {year} and quarter = {quarter}
                ORDER BY app_opens desc
                LIMIT 10'''

    cursor.execute(query_2)
    db_1.commit()

    df2= pd.DataFrame(cursor.fetchall(),columns=["Districts","app_opens"])

    fig_2 = px.bar(df2,
                title='Top 10 districts with highest PhonePe app opens',
                x="Districts",
                y="app_opens",
                color_discrete_sequence=px.colors.sequential.Purples_r,
                labels={'Transaction_amount': 'App opens'}
                    )

    st.plotly_chart(fig_2,use_container_width=False)

# Top 10 pincode - registered users

def top_users_pincode_count(year,quarter):
    
    query_1= f''' SELECT pin_code, registered_users FROM top_user_table
                WHERE year = {year} and quarter = {quarter}
                ORDER BY registered_users desc
                LIMIT 10'''

    cursor.execute(query_1)
    db_1.commit()

    df1= pd.DataFrame(cursor.fetchall(),columns=["pin_code","registered_users"])

    fig_1 = px.bar(df1,
                title='Top 10 pin code with highest Registered PhonePe users',
                x="pin_code",
                y="registered_users",
                color_discrete_sequence=px.colors.sequential.Purples_r,
                labels={'pin_code':'Pin code','registered_users': 'Registered users'}
                )
    fig_1.update_layout(xaxis_type= "category")
    st.plotly_chart(fig_1,use_container_width=False)

#Streamlit

st.set_page_config(
        page_title='PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION',
        layout="wide"
        )

st.title(':violet[PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION]')

transactions, users = st.tabs(['Transactions', 'Users'])


with transactions:
    year= st.radio('**YEAR**',[2018,2019,2020,2021,2022,2023],horizontal=True)
    quarter= st.radio('**QUARTER**',[1,2,3,4],horizontal=True)
    

    if year == 2023 and  quarter== 4:
        st.header(":violet[***Not yet updated***]")
    else:
        query=f'''SELECT year,SUM(transaction_amount) as transaction_amount ,SUM(transaction_count) as transaction_count FROM aggre_trans_table
                WHERE year = {year} and quarter = {quarter}
                GROUP BY year'''
    
        cursor.execute(query)
        db_1.commit()

        df1= pd.DataFrame(cursor.fetchall(),columns=["year","transaction_amount",'transaction_count'])

        a= df1['transaction_amount'].iloc[0]
        transaction_amount= format_currency(a, 'INR', locale='en_IN')

        b= df1['transaction_count'].iloc[0]
        
        transaction_count= ('{:,}'.format(b)) 


        st.title(":violet[Transactions]")
        st.write(":violet[***All PhonePe transactions (UPI + Cards + Wallets)***]")
        st.write(transaction_count)
        st.write(":violet[***Total payment value***]")
        st.write(transaction_amount)

        option= st.selectbox('',("Transaction Count","Transaction Amount"))

        if option == "Transaction Count":
            transactions_count(year,quarter)
            col1,col2,col3=st.columns(3)
            with col1:
                transactions_type_count(year,quarter)
                top_trans_states_count(year,quarter)
                top_trans_districts_count(year,quarter)
                top_trans_pincode_count(year,quarter)
            with col2:
                st.markdown("# ")
                st.markdown("# ")
                st.markdown("# ")

            with col3:
                query_1= f''' SELECT transaction_name,SUM(transaction_count)as transaction_count FROM aggre_trans_table
                        WHERE year = {year} and quarter = {quarter}
                        GROUP BY transaction_name 
                        ORDER BY transaction_count desc'''

                cursor.execute(query_1)
                db_1.commit()

                df1= pd.DataFrame(cursor.fetchall(),columns=["Transaction_name","Transaction count"])
                st.markdown("# ")
                st.markdown("# ")
                st.write(df1)

        
        elif option == "Transaction Amount":
            transactions_amount(year,quarter)
            col1,col2,col3=st.columns(3)
            with col1:
                transactions_type_amount(year,quarter)
                top_trans_states_amount(year,quarter)
                top_trans_districts_amount(year,quarter)
                top_trans_pincode_amount(year,quarter)
            with col2:
                st.markdown("# ")
                st.markdown("# ")
                st.markdown("# ")

            with col3:
                query_1= f''' SELECT transaction_name,SUM(transaction_amount)as transaction_amount FROM aggre_trans_table
                        WHERE year = {year} and quarter = {quarter}
                        GROUP BY transaction_name 
                        ORDER BY transaction_amount desc'''

                cursor.execute(query_1)
                db_1.commit()

                df1= pd.DataFrame(cursor.fetchall(),columns=["Transaction_name","Transaction amount"])
                st.markdown("# ")
                st.markdown("# ")
                st.write(df1)
                


with users:
    year= st.radio('**Year**',[2018,2019,2020,2021,2022,2023],horizontal=True)
    quarter= st.radio('**Quarter**',[1,2,3,4],horizontal=True)
    if year == 2023 and  quarter== 4:
        st.header(":violet[***Not yet updated***]")
    else:
        query=f'''SELECT year,SUM(registered_users) as registered_users ,SUM(app_opens) as app_opens FROM map_user_table
                        WHERE year = {year} and quarter = {quarter}
                        GROUP BY year'''
            
        cursor.execute(query)
        db_1.commit()

        df1= pd.DataFrame(cursor.fetchall(),columns=["year","registered_users",'app_opens'])

        a= df1['registered_users'].iloc[0]
        registered_users= ('{:,}'.format(a)) 

        b= df1['app_opens'].iloc[0]

        app_opens= ('{:,}'.format(b)) 

        st.title(":violet[Users]")
        st.write(f":violet[***Registered PhonePe users till Q{quarter} {year}***]")
        st.write(registered_users)
        st.write(":violet[***Total payment value***]")
        if year==2018:
            st.write(":violet[*Data not available*]")
        elif year==2019 and quarter==1:
            st.write(":violet[*Data not available*]")
        else:
            st.write(app_opens)

        user(year,quarter)

        st.markdown(":violet[**TOP Chart**]")

        option= st.selectbox('',("Registered users","App opens"))

        if option == "Registered users":
            top_users_states_registered_users(year,quarter)
            top_users_districts_registered_users(year,quarter)
            top_users_pincode_count(year,quarter)

        if option == 'App opens':
            if year==2018:
                st.write(":violet[***Data not available***]")
            elif year==2019 and quarter==1:
                st.write(":violet[***Data not available***]")
            else:
                top_users_states_app_opens(year,quarter)
                top_users_districts_app_opens(year,quarter)





