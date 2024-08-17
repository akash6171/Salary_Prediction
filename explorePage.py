import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]]='Other'
    return categorical_map

def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_education(x):
    if "Bachelor’s degree" in x:
        return "Bachelor’s degree"
    if "Master’s degree" in x:
        return "Master’s degree"
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

@st.cache
def load_data():
    survey = pd.read_csv('survey_results_public.csv')
    survey = survey[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    survey = survey.rename({"ConvertedComp": "Salary"}, axis=1)
    survey = survey[survey['Salary'].notnull()]
    survey = survey.dropna()
    survey = survey[survey["Employment"] == "Employed full-time"]
    survey = survey.drop("Employment", axis=1)
    
    country_map = shorten_categories(survey.Country.value_counts(), 400)
    survey['Country'] = survey['Country'].map(country_map)
    survey = survey[survey["Salary"] <= 250000]
    survey = survey[survey["Salary"] >= 10000]
    survey = survey[survey['Country'] != 'Other']
    
    survey['YearsCodePro'] = survey['YearsCodePro'].apply(clean_experience)
    survey['EdLevel'] = survey['EdLevel'].apply(clean_education)
    return survey

survey = load_data()

def showExplorePage():
    st.title('Explore Software Engineer salaries')
    st.write(
    """
    ### Stack Overflow Developer Survey 2020
    """
    )
    
    data = survey['Country'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    st.write("""### Number of data from different countries""")
    st.pyplot(fig1)
    
    st.write(
        """"
        #### Mean Salary Based on Country
        """
    )
    data = survey.groupby(['Country'])['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(data)
    
    st.write("""
             #### Mean Salary Based on Experience
             """)
    
    data = survey.groupby(['YearsCodePro'])['Salary'].mean().sort_values(ascending=True)
    st.line_chart(data)

    