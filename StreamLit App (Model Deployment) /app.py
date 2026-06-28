import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("flight_model.pkl")

st.title("✈️ Flight Delay Prediction App")

st.write("Enter flight details to predict delay")

# -------------------------------
# INPUTS
# -------------------------------

airline = st.selectbox("Select Airline", ["United Express", "Southwest", "American","Commutair Aka Champlain Enterprises, Inc.","Envoy Air","ExpressJet Airlines Inc.","Frontier Airlines Inc.","Hawaiian Airlines Inc.","JetBlue Airways","Mesa Airlines Inc.","SkyWest Airlines Inc.","Spirit Air Lines","Sun Country Airlines","Virgin America"])

origin = st.selectbox("Origin Airport", ["JFK", "GJT", "DEN", "ORD", "ATL", "SFO", "SEA", "MIA", "BOS", "PHX"])

dest = st.selectbox("Destination Airport", ["JFK", "GJT", "DEN", "ORD", "ATL", "SFO", "SEA", "MIA", "BOS", "PHX"])

day_of_week = st.slider("Day of Week (1=Mon, 7=Sun)", 1, 7, 3)

month = st.slider("Month", 1, 12, 5)

hour = st.slider("Departure Hour", 0, 23, 10)

is_weekend = st.selectbox("Is Weekend?", [0,1])

# -------------------------------
# FEATURE ENGINEERING
# -------------------------------

timeslot = "Morning" if hour < 12 else "Afternoon" if hour < 18 else "Evening"

peak_hour = 1 if (7 <= hour <= 10 or 17 <= hour <= 20) else 0

# -------------------------------
# CREATE INPUT DATA
# -------------------------------

input_data = pd.DataFrame({
    'Airline': [airline],
    'Origin': [origin],
    'Dest': [dest],
    'DayOfWeek': [day_of_week],
    'Hour': [hour],
    'TimeSlot': [timeslot],
    'Month': [month],
    'IsWeekend': [is_weekend],
    'PeakHour': [peak_hour]
})

# Convert categorical
for col in ['Airline','Origin','Dest','TimeSlot']:
    input_data[col] = input_data[col].astype('category')

# -------------------------------
# PREDICTION
# -------------------------------

if st.button("Predict Delay"):

    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.error("⚠️ Flight will be DELAYED")
    else:
        st.success("✅ Flight will be ON TIME")

#st.write(input_data)
#st.write(input_data.shape)
