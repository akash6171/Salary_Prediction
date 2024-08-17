import streamlit as st 
import pickle 
import numpy as np

def load_model():
    with open('saved_steps.pkl','rb') as file:
        data = pickle.load(file)
    return data
    
data = load_model()

regressor = data['model']
le_country = data['le_country']
le_education = data['le_education']

def showPredictPage():
    st.title('Salary prediction')
    st.write(''' ### We need some information to predict the salary''')
    
    countries = {
        'United States',
        'India',
        'United Kingdom',
        'Germany',
        'Australia',
        'Canada',
        'Brazil',
        'France',
        'China',
        'Russia',
        'Poland',
        'Japan',
        'Italy',
        'Spain',
        'South Africa',
        'South Korea',
        'Mexico',
        'Sweden',
        'Switzerland',
        'Netherlands',
        'Norway',
    }
    education = {
        "Less than a Bachelor's degree", 
        "Bachelor's degree",
        "Master's degree",
        "Postgraduate degree",
    }
    
    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)
    
    experience = st.slider("Years of Experience", 0, 50, 3)
    
    ok = st.button("Calculate Salary")
    if ok:
        X = np.array([[country, education, experience]])
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 0] = le_education.transform(X[:,1])
        X = X.astype(float)
        
        salary = regressor.predict(X)
        st.subheader(f"the estimated salary is ${salary[0]:2f}")
        
        
showPredictPage() 

# streamlit run predictionPage.py