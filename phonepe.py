import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import plotly.express as px
import json
import requests
from PIL import Image

#to create mysql dataframe

#mysql connection

mydb = mysql.connector.connect(

  host="localhost",

  user="root",

  password="",

  database="Phonepe_data"

)
mycursor=mydb.cursor(buffered=True)

mycursor.execute("use Phonepe_data")


#for agg_transaction

mycursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table1=mycursor.fetchall()

Agg_transaction=pd.DataFrame(table1,columns=("States","Year","Quarter","Transaction_type",
                                              "Transaction_count","Transaction_amount"))

#for aggregated_user

mycursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table2=mycursor.fetchall()

Agg_user=pd.DataFrame(table2,columns=("States","Year","Quarter","Brands",
                                              "Transaction_count","Percentage"))

#for map_transaction

mycursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table3=mycursor.fetchall()

Map_transaction=pd.DataFrame(table3,columns=("States","Year","Quarter","Districts",
                                              "Transaction_count","Transaction_amount"))

#for map_user

mycursor.execute("SELECT * FROM map_user")
mydb.commit()
table4=mycursor.fetchall()

Map_user=pd.DataFrame(table4,columns=("States","Year","Quarter","Districts",
                                              "RegisteredUsers","Appopens"))

#for top_transaction

mycursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table5=mycursor.fetchall()

Top_transaction=pd.DataFrame(table5,columns=("States","Year","Quarter","Pincodes",
                                              "Transaction_count","Transaction_amount"))

#for top_user

mycursor.execute("SELECT * FROM top_user")
mydb.commit()
table6=mycursor.fetchall()

Top_user=pd.DataFrame(table6,columns=("States","Year","Quarter","Pincodes",
                                              "RegisteredUsers"))

#function creation

def Trans_amount_count_Y(df, year):
    
    TCAY=df[df["Year"]==year]
    TCAY.reset_index(drop = True,inplace = True)
    TCAY_grouby=TCAY.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    TCAY_grouby.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:

        Trans_amount=px.bar(TCAY_grouby,x="States", y= "Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                                height=600,width=600)

        st.plotly_chart(Trans_amount)

  
    with col2:

        Trans_count=px.bar(TCAY_grouby,x="States", y= "Transaction_count", title=f"{year} TRANSACTION COUNT",
                            height=650,width=650)

        st.plotly_chart(Trans_count)

    
#geo part

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

    response=requests.get(url)
    data=json.loads(response.content)

    state_name=[]

    for feature in data["features"]:
        state_name.append(feature["properties"]["ST_NM"])


    state_name.sort()
#for transaction amount
    
    col1,col2=st.columns(2)
    with col1:

        fig1 = px.choropleth(TCAY_grouby,geojson=data, 
                            locations= "States", 
                            featureidkey= "properties.ST_NM",
                            color="Transaction_amount",
                            color_continuous_scale="Reds",
                            range_color=(TCAY_grouby["Transaction_amount"].min(),TCAY_grouby["Transaction_amount"].max()),
                            hover_name= "States",
                            title=f"{year} TRANSANCTION AMOUNT",
                            fitbounds="locations",
                            height=650,width=650)
        
        fig1.update_geos(visible=False)
        
        st.plotly_chart(fig1)

#for transaction count
    with col2:

        fig2 = px.choropleth(TCAY_grouby,geojson=data, 
                            locations= "States", 
                            featureidkey= "properties.ST_NM",
                            color="Transaction_count",
                            color_continuous_scale="Reds",
                            range_color=(TCAY_grouby["Transaction_count"].min(),TCAY_grouby["Transaction_count"].max()),
                            hover_name= "States",
                            title=f"{year} TRANSANCTION COUNT",
                            fitbounds="locations",
                            height=650,width=650)
        
        fig2.update_geos(visible=False)
        
        st.plotly_chart(fig2)

    return TCAY

# to get quarter details

def Trans_amount_count_Y_Q(df, quarter):
    
    TCAY=df[df["Quarter"]==quarter]
    TCAY.reset_index(drop = True,inplace = True)
    TCAY_grouby=TCAY.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    TCAY_grouby.reset_index(inplace=True)

    col1,col2=st.columns(2)
    
    with col1:

        Trans_amount=px.bar(TCAY_grouby,x="States", y= "Transaction_amount", title=f"{TCAY['Year'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                             height=650,width=650)

        st.plotly_chart(Trans_amount)
    
    with col2:

        Trans_count=px.bar(TCAY_grouby,x="States", y= "Transaction_count", title=f"{TCAY['Year'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                            height=650,width=650)

        st.plotly_chart(Trans_count)

    #geo part

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

    response=requests.get(url)
    data=json.loads(response.content)

    state_name=[]

    for feature in data["features"]:
        state_name.append(feature["properties"]["ST_NM"])


    state_name.sort()
    #for transaction amount

    col1,col2=st.columns(2)
    with col1:

        fig1 = px.choropleth(TCAY_grouby,geojson=data, 
                            locations= "States", 
                            featureidkey= "properties.ST_NM",
                            color="Transaction_amount",
                            color_continuous_scale="Reds",
                            range_color=(TCAY_grouby["Transaction_amount"].min(),TCAY_grouby["Transaction_amount"].max()),
                            hover_name= "States",
                            title=f"{TCAY['Year'].min()} YEAR {quarter} QUARTER TRANSANCTION AMOUNT",
                            fitbounds="locations",
                            height=650,width=650)
        
        fig1.update_geos(visible=False)
        
        st.plotly_chart(fig1)

    #for transaction count
        
    with col2:    

        fig2 = px.choropleth(TCAY_grouby,geojson=data, 
                            locations= "States", 
                            featureidkey= "properties.ST_NM",
                            color="Transaction_count",
                            color_continuous_scale="Reds",
                            range_color=(TCAY_grouby["Transaction_count"].min(),TCAY_grouby["Transaction_count"].max()),
                            hover_name= "States",
                            title=f"{TCAY['Year'].min()} YEAR {quarter} QUARTER TRANSANCTION COUNT",
                            fitbounds="locations",
                            height=650,width=650)
        
        fig2.update_geos(visible=False)
        
        st.plotly_chart(fig2)

    return TCAY

#to get transaction_type

def agg_transaction_type(df, State):
    
    TCAY1=df[df["States"]==State]
    TCAY1.reset_index(drop = True,inplace = True)
    TCAY_grouby=TCAY1.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    TCAY_grouby.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:

        trans_amount=px.pie(data_frame=TCAY_grouby, names="Transaction_type", values="Transaction_amount",
                        width=600,title= f"{State} TRANSACTION AMOUNT",hole=0.4)
        st.plotly_chart(trans_amount)

    with col2:

        trans_count=px.pie(data_frame=TCAY_grouby, names="Transaction_type", values="Transaction_count",
                        width=600,title=f"{State} TRANSACTION COUNT",hole=0.4)
        st.plotly_chart(trans_amount)

#to get Agg_user_year wise data

def Agg_u_year(df,year):

    Agg_user_year=df[df['Year']==year]
    Agg_user_year.reset_index(drop= True, inplace= True)

    Agg_user_year_G=pd.DataFrame(Agg_user_year.groupby("Brands")["Transaction_count"].sum())
    Agg_user_year_G.reset_index(inplace= True)

    Agg_user_count=px.bar(Agg_user_year_G, x= "Brands", y= "Transaction_count",title=f"{year} USER BRAND AND TRANSACTION COUNT",
                        height= 600, width= 600, color_discrete_sequence=px.colors.sequential.amp_r,hover_name="Brands")

    st.plotly_chart(Agg_user_count)

    return Agg_user_year

#Agg_user by Quarter wise data

def Agg_u_Q(df,quarter):
    Agg_user_Quarter=df[df["Quarter"]== quarter]
    Agg_user_Quarter.reset_index(drop= True, inplace= True)

    Agg_user_Quarter_G= pd.DataFrame(Agg_user_Quarter.groupby("Brands")["Transaction_count"].sum())
    Agg_user_Quarter_G.reset_index(inplace= True)

    Agg_user_count=px.line(Agg_user_Quarter_G, x= "Brands", y= "Transaction_count",title=f"{quarter} QUARTER, USER BRAND AND TRANSACTION COUNT",
                            height= 600, width= 600, color_discrete_sequence=px.colors.sequential.Bluered,hover_name="Brands",markers= True)

    st.plotly_chart(Agg_user_count)

    return Agg_user_Quarter



#map_transaction_district

def map_transaction_district(df, State):
    
    MTCAY=df[df["States"]==State]
    MTCAY.reset_index(drop = True,inplace = True)
    MTCAY_G=MTCAY.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    MTCAY_G.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        Map_trans_amount=px.bar(MTCAY_G, x= "Transaction_amount", 
                                y= "Districts", 
                                orientation="h",
                                title=f"{State.upper()} DISTRICT AND TRANSACTION AMOUNT",
                                color_discrete_sequence=px.colors.sequential.algae_r)
        st.plotly_chart(Map_trans_amount)
    
    with col2:

        Map_trans_count=px.bar(MTCAY_G, x= "Transaction_count", 
                                y= "Districts", 
                                orientation="h",
                                title=f"{State.upper()} DISTRICT AND TRANSACTION COUNT",
                                color_discrete_sequence=px.colors.sequential.algae_r)
        st.plotly_chart(Map_trans_count)

    return MTCAY


#map_user_year

def map_u_year(df, year):
    Map_user_year=df[df["Year"]==year]
    Map_user_year.reset_index(drop= True, inplace= True)

    Map_user_year_G=Map_user_year.groupby("States")[["RegisteredUsers","Appopens"]].sum()
    Map_user_year_G.reset_index(inplace= True)

    Map_user_count=px.line(Map_user_year_G, x= "States", y= ["RegisteredUsers","Appopens"],title= f"{year} REGISTERED USERS AND APPOPENS FOR MAP USERS",
                                height= 800, width= 1000,markers= True)


    st.plotly_chart(Map_user_count)

    return Map_user_year


#map_user_quarter

def map_u_quarter(df, quarter):
    Map_user_quarter=df[df["Quarter"]==quarter]
    Map_user_quarter.reset_index(drop= True, inplace= True)

    Map_user_quarter_G=Map_user_quarter.groupby("States")[["RegisteredUsers","Appopens"]].sum()
    Map_user_quarter_G.reset_index(inplace= True)

    Map_user_count=px.line(Map_user_quarter_G, x= "States", y= ["RegisteredUsers","Appopens"],title= f"{df['Year'].min()} {quarter} QUARTER REGISTERED USERS AND APPOPENS FOR MAP USERS",
                                height= 800, width= 1000,markers= True)


    st.plotly_chart(Map_user_count)

    return Map_user_quarter

#map_user_district wise data
def map_u_district(df, state):

    Map_user_district=df[df["States"]==state]
    Map_user_district.reset_index(drop= True, inplace= True)
    Map_user_district = Map_user_district.drop_duplicates(subset=["Districts"])


    map_fig_1=px.bar(Map_user_district, x="RegisteredUsers", y= "Districts", orientation= "h",height=800,
                    title= f"{state.upper()}MAP REGISTERED USERS-DISTRICT WISE")

    st.plotly_chart(map_fig_1)  


#top transaction(pincodes and transaction amount)

def top_transaction_state(df,state):

    Top_user_state=df[df["States"]==state]
    Top_user_state.reset_index(drop= True, inplace= True)


    col1,col2=st.columns(2)
    with col1:

        top_fig_1=px.bar(Top_user_state, x="Quarter", y= "Transaction_amount",height=600,width=600,
                        title= "TOP TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Aggrnyl,
                        hover_data="Pincodes")

        st.plotly_chart(top_fig_1)

    with col2: 

        top_fig_2=px.bar(Top_user_state, x="Quarter", y= "Transaction_count",height=600,width=600,
                        title= "TOP TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.deep_r,
                        hover_data="Pincodes")

        st.plotly_chart(top_fig_2)

#top user quarter and registered user

def top_u_year(df,year):

    Top_user_year=df[df['Year']==year]
    Top_user_year.reset_index(drop= True, inplace= True)


    Top_user_year_G=pd.DataFrame(Top_user_year.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    Top_user_year_G.reset_index(inplace= True)

    fig_1=px.bar(Top_user_year_G, x= "States", y="RegisteredUsers",
                color="Quarter", height=1000, width= 800,
                color_discrete_sequence=px.colors.sequential.amp_r,hover_name="States",
                title=F"{year} TOP USER-REGISTERED USER")

    st.plotly_chart(fig_1)

    return Top_user_year

#top_user state 

def top_u_state(df, state):

    Top_user_state=df[df["States"]==state]
    Top_user_state.reset_index(drop= True, inplace= True)

    fig_2=px.bar(Top_user_state, x="Quarter", y="RegisteredUsers", title= "REGISTERED USERS,PINCODES,QUARTERS FOR TOP USERS",
                height=1000, width= 800, color="RegisteredUsers", hover_data="Pincodes",
                color_continuous_scale=px.colors.sequential.amp_r)

    st.plotly_chart(fig_2)
  

#streamlit part

st.set_page_config(layout="wide")

st.title("PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:

    click=option_menu("MAIN MENU",["ABOUT","DATA EXPLORATION"])

if click=="ABOUT":
    
    col1,col2=st.columns(2)
    with col1:

        st.header("PHONEPE")
        st.subheader("NUMBER ONE MONEY TRANSFER APP IN INDIA")
        st.markdown("Phonepe is an India's financial company")
        st.write("****FEATURES****")
        st.write("****CREDIT AND DEBIT CARD ACCESS****")
        st.write("****CAN CHECK BALANCE****")
        st.write("****EASY TO ACCESS****")
        st.write("****SECURED****")
        

    with col2:
        st.image(Image.open("E:/my project/.venv/image.jpg"),width=600)

    col3,col4=st.columns(2)

    with col3:
        st.image(Image.open("E:/my project/phonepe.png"),width=600)

    with col4:

        st.write("****PROMINENT FEATURES OF PHONEPE APP:****")
        st.write("****Customer Support****")
        st.write("****UPI Mandates****")
        st.write("****Loan Payments****")
        st.write("****Insurance Premium Payments****")
        st.write("****Investments****")
        st.write("****QR Code Payments****")
        st.write("****Online Shopping****")
        st.write("****Mobile Recharge****")
        st.write("****Mobile RechargeBill Payments****")
        st.write("****Bill Payments****")
        
        



elif click=="DATA EXPLORATION":
    tab1,tab2,tab3=st.tabs(["Aggregated List","Map list","Top list"])

    with tab1:
        option=st.radio("SELECT YOUR OPTION",["Aggregated Transaction","Aggregated User"])

        if option=="Aggregated Transaction":

            col1,col2=st.columns(2)

            with col1:
              years = st.selectbox("SELECT THE YEAR", options=range(Agg_transaction["Year"].min(), Agg_transaction["Year"].max() +1), index=0)
        
            trac_y=Trans_amount_count_Y(Agg_transaction, years )

            col1,col2= st.columns(2)

            with col1:
                Quarter = st.selectbox("SELECT THE QUARTER", options=range(trac_y["Quarter"].min(), trac_y["Quarter"].max() +1), index=0)

            trac_y_Q=Trans_amount_count_Y_Q(trac_y,Quarter)

            col1,col2=st.columns(2)

        
            with col1:
                states=st.selectbox("SELECT STATES",trac_y["States"].unique())

            agg_transaction_type(trac_y,states)

           
        elif option=="Aggregated User":

            col1,col2=st.columns(2)

            with col1:
              years = st.selectbox("SELECT THE BRAND", options=range(Agg_user["Year"].min(), Agg_user["Year"].max() +1), index=0)
        
            Agg_user_year=Agg_u_year(Agg_user,years)

            col1,col2= st.columns(2)

            with col1:
                Quarter = st.selectbox("SELECt QUARTERS", options=range(Agg_user_year["Quarter"].min(), Agg_user_year["Quarter"].max() +1), index=0)

            Agg_user_Quarter=Agg_u_Q(Agg_user_year,Quarter)


          
    with tab2:
        option2=st.radio("SELECT YOUR OPTION",["Map Transaction","Map User"])

        if option2=="Map Transaction":
            col1,col2=st.columns(2)

            with col1:
               
                years = st.selectbox("SELECT YEARS", options=range(Map_transaction["Year"].min(), Map_transaction["Year"].max() +1),index=0) 
                                
        
            map_trac_y=Trans_amount_count_Y(Map_transaction, years)

            col1,col2=st.columns(2)


            with col1:
                states=st.selectbox("SELECT STATES OF MAP",map_trac_y["States"].unique())

            map_transaction_district(map_trac_y,states)

            col1,col2= st.columns(2)


            with col1:

                Quarter = st.selectbox("SELECT QUARTER", options=range(map_trac_y["Quarter"].min(), map_trac_y["Quarter"].max() +1), index=0)

            map_trac_y_Q=Trans_amount_count_Y_Q(map_trac_y,Quarter)

            col1,col2=st.columns(2)

        
            with col1:
                states=st.selectbox("SELECT ANY STATES",map_trac_y_Q["States"].unique())

            map_transaction_district(map_trac_y_Q,states)



        if option2=="Map User":
            col1,col2=st.columns(2)

            with col1:
               
                years = st.slider("YEARS",Map_user["Year"].min(), Map_user["Year"].max(), 
                                Map_user["Year"].min())
        
            map_user_year=map_u_year(Map_user, years)

            col1,col2=st.columns(2)

            with col1:
               
                quarters = st.slider("QUARTERS OF MAP USERS",map_user_year["Quarter"].min(), map_user_year["Quarter"].max(), 
                                map_user_year["Quarter"].min())
        
            map_user_quarter=map_u_quarter(map_user_year, quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("MAP USER-STATES",map_user_quarter["States"].unique())

            map_u_district(map_user_quarter, states)





    with tab3:
        option3=st.radio("SELECT YOUR OPTION",["Top Transaction","Top User"])

        if option3=="Top Transaction":

            col1,col2=st.columns(2)

            with col1:
              years = st.selectbox("TOP-YEAR", options=range(Top_transaction["Year"].min(), Top_transaction["Year"].max() +1), index=0)
        
            top_trac_y=Trans_amount_count_Y(Top_transaction,years)


            col1,col2=st.columns(2)


            with col1:
                states=st.selectbox("SELECT STATES OF MAP",top_trac_y["States"].unique())

            top_transaction_state(top_trac_y,states)

            col1,col2= st.columns(2)

            with col1:
                Quarter = st.selectbox("TOP QUARTERS", options=range(top_trac_y["Quarter"].min(), top_trac_y["Quarter"].max() +1), index=0)

            top_trac_y_Q=Trans_amount_count_Y_Q(top_trac_y,Quarter)


    
        if option3=="Top User":

            col1,col2=st.columns(2)

            with col1:
              years = st.selectbox("TOP_USER-YEAR", options=range(Top_user["Year"].min(), Top_user["Year"].max() +1), index=0)
        
            top_user_year=top_u_year(Top_user,years)

            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("TOP_USER-STATES",top_user_year["States"].unique())

            top_user_state=top_u_state(top_user_year, states)

        
