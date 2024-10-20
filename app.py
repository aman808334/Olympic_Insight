import streamlit as st
import  pandas as pd
import plotly.express as pl
import matplotlib.pyplot as plt
import seaborn as sb
import plotly.figure_factory as ff

import preprocessor, helper
from helper import medal_tally

# For Styling
st.markdown("""
    <style>
    .custom-title {
        font-size: 42px;
        color: #317d9b; /* Green */
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

df_till_2016 = pd.read_csv('Olympics_Till_2016.csv')
df_2020 = pd.read_csv('Olympics_2020.csv')
df_2024 = pd.read_csv('Olympics_2024.csv')

df = preprocessor.preprocess(df_till_2016,df_2020,df_2024)

# st.dataframe(df)

st.sidebar.title("Olympics Analysis")

# Four Radio Button
user_menu = st.sidebar.radio(
   'Select an Option',
   ('Medal Tally', 'Overall Analysis', 'Country-Wise Analysis', 'Athlete wise Analysis', 'Interesting Facts')
)

#  If Radio Button 'Medal Tally' is chick
if user_menu == 'Medal Tally':

   st.sidebar.header("Medal Tally")
   years,country = helper.country_year_list(df)

   selected_year = st.sidebar.selectbox("Select Year", years)
   selected_country = st.sidebar.selectbox("Select Country", country)

   medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

   st.markdown('<div class="custom-title">Medal Tally</div>', unsafe_allow_html=True)

   if(selected_year == 'Overall' and selected_country == 'Overall'):
        st.header("Overall Tally")
   if(selected_year != 'Overall' and selected_country == 'Overall'):
        st.header("Medal Tally in " + str(selected_year))
   if(selected_year == 'Overall' and selected_country != 'Overall'):
        st.header("Overall Performance of " + selected_country)
   if(selected_year != 'Overall' and selected_country != 'Overall'):
      st.header("Performance of " + selected_country + " in " + str(selected_year))

   medal_tally = medal_tally.rename(columns={'region': 'Region'}) # Rename

   # To start from '1' instead of '0'
   medal_tally.index = medal_tally.index + 1

   st.dataframe(medal_tally)


# If Radio Button 'Overall Analysis' is chick
if user_menu == 'Overall Analysis':

   #st.header("Overall Olympic Statistics")
   st.markdown('<div class="custom-title">Overall Olympic Statistics</div>', unsafe_allow_html=True)

   st.text("")  # For a Gap

   editions = df['Year'].unique().shape[0]-1 # 1906 isn't recog.
   cities = df['City'].unique().shape[0]
   sports = df['Sport'].unique().shape[0]
   events = df['Event'].unique().shape[0]
   athletes = df['Name'].unique().shape[0]
   nations = df['region'].unique().shape[0]

   col1, col2, col3 = st.columns(3)
   with col1:
      st.title("Editions")
      st.header(editions)
   with col2:
      st.title("Hosts")
      st.header(cities)
   with col3:
      st.title("Sports")
      st.header(sports)

   col1, col2, col3 = st.columns(3)
   with col1:
      st.title("Events")
      st.header(events)
   with col2:
      st.title("Nations")
      st.header(nations-2)
   with col3:
      st.title("Athletes")
      st.header(athletes)

   st.text("")  # For a Gap

   # Graph of Participating Nations Over the Years

   #st.header("Participating Nations Over the Years")
   st.markdown('<div class="custom-title">Participating Nations Over the Years</div>', unsafe_allow_html=True)
   nations_over_time = helper.data_over_time(df,'region')
   figure = pl.line(nations_over_time, x="Edition", y="region")
   st.plotly_chart(figure)

   st.write("")  # For a Gap

   # Graph of Events Over the Years

   #st.header("Events Over the Years")
   st.markdown('<div class="custom-title">Events Over the Years</div>', unsafe_allow_html=True)
   events_over_time = helper.data_over_time(df, 'Event')
   figure = pl.line(events_over_time, x="Edition", y="Event")
   st.plotly_chart(figure)

   st.write("")  # For a Gap

   # Graph of Athletes Over the Years

   #st.header("Athletes Over the Years")
   st.markdown('<div class="custom-title">Athletes Over the Years</div>', unsafe_allow_html=True)
   athletes_over_time = helper.data_over_time(df, 'Name')
   figure = pl.line(athletes_over_time, x="Edition", y="Name")
   st.plotly_chart(figure)

   st.write("")  # For a Gap

   # HeatMap of No. of Events Over the Years

   #st.header("No of Events Over the Years")
   st.markdown('<div class="custom-title">No of Events Over the Years</div>', unsafe_allow_html=True)
   figure,ax = plt.subplots(figsize=(21,21))
   x = df.drop_duplicates(['Year', 'Sport', 'Event'])
   ax = sb.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
   st.pyplot(figure)

   st.write("")  # For a Gap

   # Data of Most Successful Athletes

   #st.header("Most Successful Athletes")
   st.markdown('<div class="custom-title">Most Successful Athletes</div>', unsafe_allow_html=True)

   sport_list = df['Sport'].unique().tolist()
   sport_list.insert(0,'Overall')

   selected_sport = st.selectbox('Select a Sport', sport_list)
   x = helper.most_successful(df,selected_sport)

   # Start with a particular value
   start_value = 1
   x.index = range(start_value, start_value + len(x))

   x = x.rename(columns={'region': 'Region'}) # Rename

   st.dataframe(x)

# If Radio Button 'Country-Wise Analysis' is click
if user_menu == 'Country-Wise Analysis':

   st.sidebar.title("Country-Wise Analysis")

   country_list = df['region'].dropna().unique().tolist()
   country_list.sort()

   selected_country = st.sidebar.selectbox('Select a Country',country_list)

   # First - Medal Tally Over the Years
   #st.header(selected_country + " Medal Tally Over the Years")
   st.markdown(f'<div class="custom-title">{selected_country} Medal Tally Over the Years</div>', unsafe_allow_html=True)

   # Table
   country_df = helper.year_wise_medal_tally(df,selected_country)
   # To start from '1' instead of '0'
   country_df.index = country_df.index + 1

   st.dataframe(country_df)

   # Graph
   figure = pl.line(country_df, x="Year", y="Medal")
   st.plotly_chart(figure)

   st.write("")  # For a Gap

   # Second - HeatMap will say that in a particular year & sport which country has won how many medals
   st.markdown(f'<div class="custom-title">{selected_country} Medals in All Sports Over the Year</div>', unsafe_allow_html=True)
   st.write("") # For a Graph

   pt = helper.country_event_heatmap(df,selected_country)
   figure, ax = plt.subplots(figsize=(21, 21))
   ax = sb.heatmap(pt,annot=True)
   st.pyplot(figure)

   st.write("")  # For a Graph

   # Third - Most Successful Athletes Country-Wise
   st.markdown(f'<div class="custom-title">Top 10 Athletes of {selected_country}</div>', unsafe_allow_html=True)
   st.write("")  # For a Graph

   top_df = helper.most_successful_country_wise(df,selected_country)

   # Start with a particular value
   start_value = 1
   top_df.index = range(start_value, start_value + len(top_df))

   st.dataframe(top_df)

# If Radio Button 'Athlete wise Analysis' is click
if user_menu == 'Athlete wise Analysis':

   athlete_df = df.drop_duplicates(subset=['Name', 'region'])

   # Graph of Probability of winning medals VS Age
   x1 = athlete_df['Age'].dropna().tolist()
   x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna().tolist()
   x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna().tolist()
   x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna().tolist()

   figure = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
   figure.update_layout(autosize=False,width=1000,height=600)

   #st.header("Probability of Winning VS Age")
   st.markdown(f'<div class="custom-title">Probability of Winning VS Age</div>', unsafe_allow_html=True)
   st.write("")  # For a Gap
   st.plotly_chart(figure)

   # Graph of Men Participation Vs Women Participation Over Years

   #st.header("Men Participation Vs Women Participation")
   st.markdown(f'<div class="custom-title">Men Participation Vs Women Participation</div>', unsafe_allow_html=True)
   st.write("") # For a Gap

   final = helper.men_vs_women(df)
   figure = pl.line(final, x="Year", y=["Male", "Female"])
   st.plotly_chart(figure)


#  If Radio Button 'Interesting Facts' is chick
if user_menu == 'Interesting Facts':

   # st.header("10 Interesting Facts About the Olympics") -> Simple
   #  Instead of st.title(), will use -
   st.markdown('<div class="custom-title">Interesting Facts About the Olympics</div>', unsafe_allow_html=True)
   st.write("")  # For a Gap

   # Facts
   st.write("""
   1. The first modern Olympics were held in 1896 in Athens, Greece.
   2. Women have been allowed to compete in the Olympics since 1900.
   3. In the 1936 Berlin Olympics, two Japanese athletes had a half-silver and half-bronze medal.
   4. The 2012 London Olympics were the first Olympics in which all participating countries sent female athletes.
   5. Cricket has been part of the Olympics only once, in 1900.
   6. In 1906, a proper Olympics was organized but it wasn't officially recognized by the IOC.
   7. The 2020 Olympics were held in 2021 due to the COVID-19 pandemic but were still called the 2020 Olympics.
   8. The USA has hosted the most number of Olympics.
   9. In the 2016 Rio Olympics, Brazil held the record for the most athletes.
   10. The 2024 Olympics were the first to have an equal number of male and female participants.
   11. Russia & Belarus were not allowed participate in 2024 Olympics
   12. Djankeu Ngamba is the first-ever medalist for the Refugee Olympic Team, having won bronze in 2024 Olympics
   """)