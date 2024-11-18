import streamlit as st
import sys
import subprocess

# Replace the speech recognition import with this try-except block
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_ENABLED = True
except ImportError:
    SPEECH_RECOGNITION_ENABLED = False
    st.warning("Speech recognition is not available in the cloud deployment.")

from datetime import datetime
import requests  # Add this import
import os
from openai import OpenAI
from dotenv import load_dotenv
from safety_tips import SafetyTipsGenerator
import pandas as pd
import numpy as np
import ssl
import json
from datetime import datetime
import random
import time
from pygame import mixer
from gtts import gTTS
import plotly.express as px
ssl._create_default_https_context = ssl._create_unverified_context

# Load environment variables
load_dotenv()

# Your existing functions here
@st.cache_data
def load_and_prepare_data():
    """Load and prepare multiple data sources"""
    try:
        # Check if file exists
        if not os.path.exists("synthetic_traffic_fatalities.csv"):
            # Create some dummy data for testing
            dummy_data = pd.DataFrame({
                'DayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                'WeatherCondition': ['Clear', 'Rain', 'Clear', 'Snow', 'Clear'],
                'Fatality': [0, 1, 0, 1, 0]
            })
            return dummy_data
        
        # Primary driving data
        driving_data = pd.read_csv("synthetic_traffic_fatalities.csv")
        
        # Synthetic weather data
        weather_data = generate_synthetic_weather_data(len(driving_data))
        
        # Merge datasets
        combined_data = pd.merge(driving_data, weather_data, left_index=True, right_index=True)
        
        return combined_data
    except Exception as e:
        # Return dummy data as fallback
        return pd.DataFrame({
            'DayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
            'WeatherCondition': ['Clear', 'Rain', 'Clear', 'Snow', 'Clear'],
            'Fatality': [0, 1, 0, 1, 0]
        })

def generate_synthetic_weather_data(size):
    """Generate synthetic weather data for analysis"""
    weather_conditions = ['Clear', 'Rain', 'Snow', 'Fog']
    temperatures = np.random.normal(20, 5, size)
    conditions = np.random.choice(weather_conditions, size)
    
    
    return pd.DataFrame({
        'temperature': temperatures,
        'weather_condition': conditions
    })

def analyze_driving_patterns(df):
    """Comprehensive driving pattern analysis"""
    st.subheader("🔍 Driving Pattern Analysis")
    
    # Convert Fatality to numeric
    df['Fatality'] = pd.to_numeric(df['Fatality'], errors='coerce').fillna(0)
    
    # Key metrics at the top
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Incidents", len(df))
    with col2:
        fatal_count = df['Fatality'].sum()
        st.metric("Fatal Incidents", int(fatal_count))
    with col3:
        fatality_rate = (fatal_count / len(df)) * 100
        st.metric("Fatality Rate", f"{fatality_rate:.1f}%")
    
    # Time-based analysis
    col1, col2 = st.columns(2)
    
    with col1:
        daily_counts = df.groupby('DayOfWeek').size()
        fig_daily = px.bar(daily_counts, 
                          title='Incidents by Day of Week',
                          labels={'value': 'Number of Incidents', 'index': 'Day'})
        st.plotly_chart(fig_daily)
    
    with col2:
        weather_counts = df.groupby('WeatherCondition').size()
        fig_weather = px.pie(values=weather_counts.values, 
                           names=weather_counts.index,
                           title='Incidents by Weather Condition')
        st.plotly_chart(fig_weather)

def save_quiz_score(score, total_questions):
    try:
        # Load existing scores
        try:
            with open('quiz_scores.json', 'r') as f:
                scores = json.load(f)
        except FileNotFoundError:
            scores = []
        
        # Add new score
        scores.append({
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'score': score,
            'total': total_questions,
            'percentage': (score/total_questions) * 100
        })
        
        # Save updated scores
        with open('quiz_scores.json', 'w') as f:
            json.dump(scores, f)
        
        return scores
    except Exception as e:
        st.error(f"Error saving score: {e}")
        return None

def load_road_data():
    """Load road safety data from GitHub"""
    try:
        github_csv_url = "https://raw.githubusercontent.com/Reenamjot/boblol/main/detailed_analysis.csv"
        road_data = pd.read_csv(github_csv_url)
        
        # Debug: Print column names
        print("Available columns:", road_data.columns.tolist())
        st.write("Available columns:", road_data.columns.tolist())
        
        # Clean column names - make them consistent
        road_data.columns = road_data.columns.str.strip().str.replace(' ', '_')
        
        # Show cleaned column names
        st.write("Cleaned column names:", road_data.columns.tolist())
        
        return road_data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Add this at the beginning after your imports
st.set_page_config(
    page_title="DriveSafe - Advanced Driving Analysis",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for better styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 2rem;
    }
    
    /* Headers styling */
    h1, h2, h3 {
        color: #1E3D59;
        padding-bottom: 1rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f5f5f5;
    }
    
    /* Cards styling */
    div.stMetric {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Button styling */
    div[data-testid="stButton"] button {
        background-color: #1E3D59;
        color: white;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stButton"] button:hover {
        background-color: #2E5D79;
        border-color: #2E5D79;
        transform: translateY(-2px);
    }
    
    /* Emergency button specific styling */
    .emergency-button button {
        background-color: #ff4b4b !important;
        font-weight: bold;
        padding: 0.5rem 1rem;
        font-size: 1.2rem;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #ffffff;
        border-radius: 5px;
        padding: 0 16px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* DataFrames styling */
    .dataframe {
        border: none !important;
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Metrics styling */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
        color: #1E3D59;
    }
    
    /* Card container styling */
    .card-container {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Modify the main function to use the new styling
def main():
    try:
        # Load data silently without debug messages
        df = load_and_prepare_data()
        
        # Custom CSS for better styling
        st.markdown("""
            <style>
            .welcome-header {
                text-align: center;
                padding: 2rem;
                background: linear-gradient(to right, #1E3D59, #2E5D79);
                color: white;
                border-radius: 10px;
                margin-bottom: 2rem;
            }
            .route-card {
                background: white;
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                margin: 1rem 0;
                transition: transform 0.3s ease;
            }
            .route-card:hover {
                transform: translateY(-5px);
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Title with custom styling
        st.markdown("""
            <div style='text-align: center;'>
                <h1>🚗 DriveSafe - Advanced Driving Analysis</h1>
            </div>
        """, unsafe_allow_html=True)
        
        # Sidebar navigation
        with st.sidebar:
            page = st.selectbox(
                "Navigation",
                ["Profile", "Dashboard", "Detailed Analysis", "Safety Tips", "Emergency Services"]
            )
        
        # Voice Control System
        st.sidebar.markdown("### 🎙️ Voice Control")
        voice_active = st.sidebar.checkbox("Enable Voice Control")
        
        if voice_active:
            st.sidebar.info("Say 'Hey DriveSafe' to activate")
            if listen_for_wake_word():
                st.sidebar.success("Wake word detected! Listening for command...")
                command = process_voice_command()
                
                # Handle commands
                if command == "emergency":
                    page = "Emergency Services"
                elif command == "report":
                    page = "Detailed Analysis"
                elif command == "tips":
                    page = "Safety Tips"
        
        # Page content
        if page == "Profile":
            tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
            
            with tab1:
                st.markdown("""
                <div style='text-align: center; padding: 20px;'>
                    <h2>👤 Welcome Back!</h2>
                </div>
                """, unsafe_allow_html=True)
                
                with st.form("login_form"):
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    col1, col2, col3 = st.columns([1,2,1])
                    with col2:
                        login_button = st.form_submit_button("Sign In", use_container_width=True)
                    
                    st.markdown("""
                    <div style='text-align: center;'>
                        <p><a href='#'>Forgot Password?</a></p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with tab2:
                st.markdown("""
                <div style='text-align: center; padding: 20px;'>
                    <h2>🚗 Create Your Account</h2>
                </div>
                """, unsafe_allow_html=True)
                
                with st.form("signup_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        first_name = st.text_input("First Name")
                        email = st.text_input("Email Address")
                        password = st.text_input("Password", type="password")
                    
                    with col2:
                        last_name = st.text_input("Last Name")
                        phone = st.text_input("Phone Number")
                        confirm_password = st.text_input("Confirm Password", type="password")
                    
                    st.markdown("### Vehicle Information (Optional)")
                    col3, col4 = st.columns(2)
                    
                    with col3:
                        vehicle_make = st.text_input("Vehicle Make")
                        vehicle_year = st.text_input("Vehicle Year")
                    
                    with col4:
                        vehicle_model = st.text_input("Vehicle Model")
                        license_plate = st.text_input("License Plate")
                    
                    agree = st.checkbox("I agree to the Terms and Conditions")
                    
                    col5, col6, col7 = st.columns([1,2,1])
                    with col6:
                        signup_button = st.form_submit_button("Create Account", use_container_width=True)
                    
                    if signup_button and agree:
                        st.success("Account created successfully! Please check your email for verification.")
                    elif signup_button and not agree:
                        st.error("Please agree to the Terms and Conditions")

        elif page == "Dashboard":
            # Welcome Section
            st.markdown("""
                <div class="welcome-header">
                    <h1 style="color: white;">👋 Welcome to DriveSafe</h1>
                    <p style="color: white;">Your Professional Driving Companion</p>
                    <h3 style="color: white; font-style: italic; margin-top: 10px;">🛡️ Drive Smart. Drive Safe. 🚦</h3>
                    <div style="margin-top: 20px;">
                        <span style="color: white; font-size: 24px; margin: 0 10px;">✅ Plan</span>
                        <span style="color: white; font-size: 24px; margin: 0 10px;">🛡️ Protect</span>
                        <span style="color: white; font-size: 24px; margin: 0 10px;">🚦 Prevent</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Quick Stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Active Users", "1,234", "+12%")
            with col2:
                st.metric("Safe Trips", "5,678", "+8%")
            with col3:
                st.metric("Safety Score", "92%", "+3%")
            
            # Featured Routes
            st.markdown("### 🚗 Choose Your Route")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                    <div class="route-card">
                        <h4>🎓 New Driver</h4>
                        <p>Start with the basics and build your confidence</p>
                        <ul>
                            <li>Basic safety tips</li>
                            <li>Parking tutorials</li>
                            <li>Traffic rules</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                    <div class="route-card">
                        <h4>🌟 Advanced Skills</h4>
                        <p>Ready to level up your driving skills?</p>
                        <ul>
                            <li>Advanced techniques</li>
                            <li>Weather conditions</li>
                            <li>Night driving</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
            
            # Daily Tip
            st.markdown("### 💡 Today's Driving Tip")
            tips_generator = SafetyTipsGenerator()
            st.info(tips_generator.get_random_tip())
            
            # Weather Alert
            st.markdown("### 🌤️ Weather Alert")
            st.warning("Light rain expected this afternoon. Remember to maintain safe following distance!")

        elif page == "Detailed Analysis":
            # Initialize distraction_rating at the start
            distraction_rating = 0
            
            st.subheader("📊 Road Safety Analysis")
            
            # Add voice input option
            method = st.radio(
                "Choose reporting method:",
                ["🎙️ Voice Report", "⌨️ Manual Entry"]
            )
            
            if method == "🎙️ Voice Report":
                st.markdown("""
                    <style>
                    .stButton > button {
                        width: 120px !important;
                        height: 120px !important;
                        border-radius: 12px !important;
                        background-color: #1E3D59 !important;
                        color: white !important;
                        font-size: 40px !important;
                        margin: 20px auto !important;
                        border: none !important;
                    }
                    </style>
                """, unsafe_allow_html=True)
                
                # Simple questions list
                st.markdown("""
                    ### Please answer:
                    1. What type of incident?
                    2. Where did it happen?
                    3. When did it happen?
                    4. Any injuries?
                    5. Need emergency assistance?
                """)

                # Example
                st.caption("Example: 'Minor accident on Main Street, happened 10 minutes ago, no injuries, no emergency needed.'")
                
                # Recording button
                if st.button("🎙️", key="record_button"):
                    if not SPEECH_RECOGNITION_ENABLED:
                        st.error("Speech recognition is not available in this environment.")
                        return
                    r = sr.Recognizer()
                    with sr.Microphone() as source:
                        st.write("Recording...")
                        try:
                            audio = r.listen(source, timeout=15)
                            st.write("Processing...")
                            
                            # Convert speech to text
                            text = r.recognize_google(audio)
                            edited_text = st.text_area("Review and edit if needed:", text)
                            
                            # Simple confirmation
                            incident_type = st.selectbox("Type:", ["Minor", "Major", "Hazard", "Emergency"])
                            location = st.text_input("Location:")
                            needs_emergency = st.radio("Emergency needed?", ["No", "Yes"])

                            if st.button("Submit"):
                                st.success("Report submitted!")
                            
                        except sr.WaitTimeoutError:
                            st.error("No speech detected. Please try again.")
                        except sr.UnknownValueError:
                            st.error("Could not understand audio. Please try again.")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            else:
                # Your existing manual entry form
                with st.expander("Click to Report an Accident or Near-Miss"):
                    col1, col2 = st.columns(2)
                    with col1:
                        incident_date = st.date_input("Date of Incident")
                        incident_time = st.time_input("Time of Incident")
                        incident_type = st.selectbox("Type of Incident", 
                            ["Near Miss", "Minor Accident", "Major Accident"])
                    with col2:
                        location = st.text_input("Location")
                        weather = st.selectbox("Weather Conditions", 
                            ["Clear", "Rain", "Snow", "Fog", "Other"])
                
                # Distraction Factors
                st.markdown("### 📱 Distraction Factors")
                distractions = st.multiselect("Select all that apply:",
                    ["Phone Use", "Eating/Drinking", "Adjusting Music", 
                     "Passengers", "External Distraction", "Fatigue"])
                
                # Calculate distraction rating
                if distractions:
                    distraction_rating = len(distractions) * 20
                    st.warning(f"️ Distraction Rating: {distraction_rating}/100")
                    if distraction_rating > 60:
                        st.error("HIGH RISK: Multiple distractions significantly increase accident risk!")
                        
                if st.button("Submit Report"):
                    st.success("Report submitted successfully! Drive safely!")

            # Distraction Analysis Table
            st.markdown("### 📊 Distraction Risk Analysis")
            distraction_data = {
                'Distraction Type': ['Phone Use', 'Eating/Drinking', 'Passenger Interaction', 
                                   'Music Adjustment', 'External Factors'],
                'Risk Level': ['Very High', 'Moderate', 'High', 'Moderate', 'High'],
                'Reaction Time Impact': ['+0.8s', '+0.3s', '+0.5s', '+0.3s', '+0.4s'],
                'Accident Risk Increase': ['23x', '8x', '12x', '7x', '10x']
            }
            df_distractions = pd.DataFrame(distraction_data)
            st.table(df_distractions)

            # Enhanced Risk Factor Pie Chart with larger size
            st.markdown("### 🎯 Risk Factor Distribution")
            risk_data = {
                'Risk Factor': ['Distracted Driving', 'Speeding', 'Weather Conditions', 
                               'Fatigue', 'Vehicle Maintenance', 'Traffic Violations'],
                'Risk Percentage': [30, 25, 15, 12, 10, 8]
            }
            df_risks = pd.DataFrame(risk_data)
            
            fig = px.pie(df_risks, 
                         values='Risk Percentage', 
                         names='Risk Factor',
                         title='Common Driving Risk Factors',
                         color_discrete_sequence=px.colors.qualitative.Set3)
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(
                showlegend=False,
                height=700,  # Increased height
                title_x=0.5,
                title_font_size=24
            )
            st.plotly_chart(fig, use_container_width=True)

            # Add navigation buttons based on risk factors
            st.markdown("### 🚦 Recommended Safety Resources")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📱 View Distracted Driving Tips", use_container_width=True):
                    st.session_state.page = "Safety Tips"
                    st.session_state.safety_topic = "distracted_driving"
                    st.rerun()
                    
                if st.button("🌧️ Weather Safety Guidelines", use_container_width=True):
                    st.session_state.page = "Safety Tips"
                    st.session_state.safety_topic = "weather"
                    st.rerun()
                    
                if st.button("⚡ Emergency Response Tips", use_container_width=True):
                    st.session_state.page = "Safety Tips"
                    st.session_state.safety_topic = "emergency"
                    st.rerun()
            
            with col2:
                if st.button("🚗 Speed Management Tips", use_container_width=True):
                    st.session_state.page = "Safety Tips"
                    st.session_state.safety_topic = "speed"
                    st.rerun()
                    
                if st.button("😴 Fatigue Management", use_container_width=True):
                    st.session_state.page = "Safety Tips"
                    st.session_state.safety_topic = "fatigue"
                    st.rerun()
                    
                if st.button("🔧 Vehicle Maintenance Guide", use_container_width=True):
                    st.session_state.page = "Safety Tips"
                    st.session_state.safety_topic = "maintenance"
                    st.rerun()

            # Add a note about the data
            st.info("👆 Click on any button above to view detailed safety tips and guidelines for each risk factor.")

        elif page == "Safety Tips":
            st.subheader("🚦 Safety Tips for Drivers")
            
            # Create columns for better layout
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### Essential Safety Tips:
                1.  Always wear your seatbelt
                2. 🚫 Never text while driving
                3. ⏰ Maintain a 3-second following distance
                4. 🌧️ Slow down in bad weather
                5. 🛑 Obey all traffic signs and signals
                """)
                
            with col2:
                st.markdown("""
                ### Additional Safety Guidelines:
                6. 🔄 Check mirrors regularly
                7. ↔️ Use turn signals consistently
                8. 🎵 Minimize distractions (music, food)
                9. 🔧 Keep your vehicle maintained
                10. 🌙 Extra caution at night
                """)
            
            # Add a random daily tip feature
            st.markdown("---")
            st.markdown("### 💡 Tip of the Day")
            tips_generator = SafetyTipsGenerator()
            daily_tip = tips_generator.get_random_tip()
            st.info(daily_tip)
            
            # Real-time Alert Simulation (moved before Test Your Knowledge)
            st.markdown("### 🎯 Real-time Alert Simulation")
            st.markdown("Select different scenarios to hear how the alert system works:")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🚨 Simulate Speeding"):
                    play_alert("speeding")
                if st.button(" Simulate Phone Use"):
                    play_alert("phone_use")
                if st.button("↔️ Simulate Lane Departure"):
                    play_alert("lane_departure")
            with col2:
                if st.button("↩ Simulate Sharp Turn"):
                    play_alert("sharp_turn")
                if st.button("🛑 Simulate Sudden Brake"):
                    play_alert("sudden_brake")
                if st.button("😴 Simulate Fatigue"):
                    play_alert("fatigue")
            
            # Test Your Knowledge section after alerts
            st.markdown("### 📝 Test Your Knowledge")
            if st.button("Take Safety Quiz"):
                questions = [
                    {
                        "question": "What is the recommended following distance in seconds?",
                        "options": ["1 second", "2 seconds", "3 seconds", "4 seconds"],
                        "correct": 2
                    },
                    {
                        "question": "What should you do in heavy rain?",
                        "options": ["Drive normally", "Increase speed", "Reduce speed", "Turn off lights"],
                        "correct": 2
                    }
                ]
                
                score = 0
                for i, q in enumerate(questions):
                    answer = st.radio(q["question"], q["options"], key=f"q_{i}")
                    if answer == q["options"][q["correct"]]:
                        score += 1
                
                if st.button("Submit Quiz"):
                    st.write(f"Your score: {score}/{len(questions)}")
                    save_quiz_score(score, len(questions))

        elif page == "Emergency Services":
            st.subheader("Emergency Services")
            
            # Emergency Button moved to top
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                st.markdown(
                    """
                    <style>
                    div.stButton > button:first-child {
                        background-color: #ff4b4b;
                        color: white;
                        font-size: 20px;
                        font-weight: bold;
                        padding: 20px 40px;
                        border-radius: 10px;
                        border: none;
                        width: 100%;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(" EMERGENCY - CALL 911 🚨"):
                    st.warning("⚠️ This is a demo button. In a real emergency, directly dial 911 on your phone.")
            
            # Emergency Action Plan
            st.markdown("---")
            st.markdown("""
                ### 🚨 In Case of Emergency:
                1. **Stay Calm and Assess the Situation**
                2. **If Anyone is Injured:**
                   - Call 911 immediately
                   - Don't move injured persons unless they're in immediate danger
                   - Stay on the line with emergency services
                3. **Move to Safety:**
                   - If possible, move vehicles to the side of the road
                   - Turn on hazard lights
                   - Set up emergency reflectors/flares if available
            """)
            
            # Create columns for contact information
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 📞 Emergency Contacts
                - **Emergency Services**: 911
                - **Highway Patrol**: 1-800-835-5247
                - **Poison Control**: 1-800-222-1222
                - **Road Conditions**: 511
                """)
                
                st.markdown("""
                ### 🚗 Roadside Assistance
                - **AAA**: 1-800-222-4357
                - **National Highway Traffic Safety**: 1-888-327-4236
                """)
            
            with col2:
                st.markdown("""
                ### 🏥 Local Emergency Facilities
                - **Nearest Hospital**: 
                  Memorial Hospital
                  123 Medical Center Dr
                  (555) 555-1234
                
                - **Urgent Care**: 
                  CityHealth Urgent Care
                  456 Health Ave
                  (555) 555-5678
                """)
            
            # Important Information Checklist
            st.markdown("---")
            st.markdown("### 📝 Important Information to Gather")
            
            checklist = """
            - [ ] Location (cross streets, mile markers, or landmarks)
            - [ ] Vehicle information (make, model, color)
            - [ ] License plate numbers
            - [ ] Insurance information
            - [ ] Photos of the scene (if safe to do so)
            - [ ] Names and contact information of any witnesses
            """
            st.markdown(checklist)
            
            # Emergency Kit Reminder
            st.markdown("---")
            st.markdown("""
            ### 🛠️ Emergency Kit Checklist
            Make sure your car has these essential items:
            - First aid kit
            - Flashlight with extra batteries
            - Jumper cables
            - Basic tool kit
            - Blanket
            - Phone charger
            - Small fire extinguisher
            - Warning devices (flares or reflective triangles)
            - Basic repair items (duct tape, zip ties)
            - Small bottle of water and non-perishable snacks
            """)
            
            # Disclaimer
            st.markdown("---")
            st.caption("""
                ⚠️ Disclaimer: This is an emergency reference guide. In case of a real emergency, 
                always call 911 first. The information provided here is for general guidance only. 
                Local emergency numbers and facilities may vary by location.
            """)

    except Exception as e:
        st.error(f"Error: {str(e)}")

def render_analysis():
    st.subheader("📊 Advanced Driving Analysis")
    
    # Enhanced Risk Factor Pie Chart with larger size
    st.markdown("### 🎯 Risk Factor Distribution")
    risk_data = {
        'Risk Factor': ['Distracted Driving', 'Speeding', 'Weather Conditions', 
                       'Fatigue', 'Vehicle Maintenance', 'Traffic Violations'],
        'Risk Percentage': [30, 25, 15, 12, 10, 8]
    }
    df_risks = pd.DataFrame(risk_data)
    
    fig = px.pie(df_risks, 
                 values='Risk Percentage', 
                 names='Risk Factor',
                 title='Common Driving Risk Factors',
                 color_discrete_sequence=px.colors.qualitative.Set3)
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        showlegend=False,
        height=700,  # Increased height
        title_x=0.5,
        title_font_size=24
    )
    st.plotly_chart(fig, use_container_width=True)

    # Navigation buttons based on risk factors
    st.markdown("### 🚦 Recommended Safety Resources")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📱 View Distracted Driving Tips", use_container_width=True):
            st.session_state.page = "Safety Tips"
            st.session_state.safety_topic = "distracted_driving"
            st.rerun()
            
        if st.button("🌧️ Weather Safety Guidelines", use_container_width=True):
            st.session_state.page = "Safety Tips"
            st.session_state.safety_topic = "weather"
            st.rerun()
            
        if st.button("⚡ Emergency Response Tips", use_container_width=True):
            st.session_state.page = "Safety Tips"
            st.session_state.safety_topic = "emergency"
            st.rerun()
    
    with col2:
        if st.button("🚗 Speed Management Tips", use_container_width=True):
            st.session_state.page = "Safety Tips"
            st.session_state.safety_topic = "speed"
            st.rerun()
            
        if st.button("😴 Fatigue Management", use_container_width=True):
            st.session_state.page = "Safety Tips"
            st.session_state.safety_topic = "fatigue"
            st.rerun()
            
        if st.button("🔧 Vehicle Maintenance Guide", use_container_width=True):
            st.session_state.page = "Safety Tips"
            st.session_state.safety_topic = "maintenance"
            st.rerun()

    st.info("👆 Click on any button above to view detailed safety tips and guidelines for each risk factor.")

def create_accident_trend_chart():
    # Create dummy data for demonstration
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='M')
    values = np.random.normal(10, 2, len(dates))
    df = pd.DataFrame({'Date': dates, 'Accidents': values})
    
    fig = px.line(df, x='Date', y='Accidents', 
                  title='Accident Trends Over Time',
                  template='plotly_white')
    return fig

def create_safety_score_chart():
    categories = ['Speed', 'Braking', 'Turns', 'Following Distance']
    scores = np.random.uniform(70, 95, len(categories))
    
    fig = px.bar(x=categories, y=scores,
                 title='Safety Scores by Category',
                 template='plotly_white')
    return fig

def play_alert(alert_type):
    """Play audio alert based on the type of alert"""
    try:
        mixer.init()
        alert_file = f"alerts/{alert_type.lower().replace(' ', '_')}.mp3"
        if os.path.exists(alert_file):
            mixer.music.load(alert_file)
            mixer.music.play()
            time.sleep(2)  # Wait for audio to finish
            mixer.music.stop()  # Stop the audio after playing
        else:
            st.warning(f"⚠️ Alert: {alert_type}")
    except Exception as e:
        st.error(f"Audio alert system unavailable: {str(e)}")

# Optional: Script to generate audio files using gTTS
def create_alert_files():
    alerts = {
        "speeding": "Warning: Speed exceeds limit. Please slow down.",
        "sharp_turn": "Caution: Sharp turn ahead. Reduce speed.",
        "phone_use": "Alert: Phone use detected. Keep eyes on road.",
        "sudden_brake": "Notice: Sudden braking detected. Maintain safe distance.",
        "lane_departure": "Warning: Lane departure detected. Stay in lane."
    }
    
    # Create alerts directory if it doesn't exist
    if not os.path.exists("alerts"):
        os.makedirs("alerts")
    
    # Generate audio files
    for filename, text in alerts.items():
        tts = gTTS(text=text, lang='en')
        tts.save(f"alerts/{filename}.mp3")

# Run this once to create the audio files
# create_alert_files()

# Add this function for voice input
def voice_input_report():
    # Remove all previous content and styling
    st.markdown("""
        <style>
        /* Override default button styling */
        .stButton > button {
            width: 300px !important;
            height: 300px !important;
            border-radius: 50% !important;
            background-color: #FF4B4B !important;
            color: white !important;
            font-size: 100px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            margin: 50px auto !important;
            border: none !important;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2) !important;
        }
        
        .stButton > button:hover {
            background-color: #FF6B6B !important;
            transform: scale(1.05);
        }
        
        .big-title {
            font-size: 40px !important;
            text-align: center;
            margin-bottom: 30px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 class='big-title'>🎙️ Voice Command Center</h1>", unsafe_allow_html=True)
    
    # Single large button
    if st.button("🎙️", key="mega_mic"):
        if not SPEECH_RECOGNITION_ENABLED:
            st.error("Speech recognition is not available in this environment.")
            return
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.markdown("<h2 style='text-align: center; color: red;'>🔴 Recording...</h2>", unsafe_allow_html=True)
            try:
                audio = r.listen(source, timeout=5)
                st.write("Processing your command...")
                
                # Convert speech to text
                text = r.recognize_google(audio)
                st.success(f"Recorded: {text}")
                
            except sr.WaitTimeoutError:
                st.error("No speech detected. Please try again.")
            except sr.UnknownValueError:
                st.error("Could not understand audio. Please try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    # Command list below the button
    st.markdown("""
        <div style='text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px; margin-top: 30px;'>
            <h2 style='color: #1E3D59; margin-bottom: 20px;'>Available Commands:</h2>
            <p style='font-size: 20px; margin: 10px 0;'>🚨 "Report accident at [location]"</p>
            <p style='font-size: 20px; margin: 10px 0;'>⚠️ "Report hazard at [location]"</p>
            <p style='font-size: 20px; margin: 10px 0;'>🆘 "Emergency assistance needed"</p>
            <p style='font-size: 20px; margin: 10px 0;'>🌤️ "Weather conditions at [location]"</p>
        </div>
    """, unsafe_allow_html=True)

def test_microphone():
    """Test if microphone is working correctly"""
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Microphone test successful! Your microphone is working.")
            return True
    except Exception as e:
        st.error(f"Microphone test failed: {str(e)}")
        st.info("If you're on macOS, make sure you've granted microphone permissions to your terminal/IDE")
        return False

# Add this to your voice_input_report function at the start:
def voice_input_report():
    if not test_microphone():
        return
    
    # ... rest of your existing voice_input_report code ...

def save_report(report):
    """Save voice report to a file"""
    try:
        # Load existing reports
        try:
            with open('voice_reports.json', 'r') as f:
                reports = json.load(f)
        except FileNotFoundError:
            reports = []
        
        # Add new report
        reports.append({
            'timestamp': report['timestamp'].strftime("%Y-%m-%d %H:%M:%S"),
            'description': report['description'],
            'location': report['location'],
            'type': report['type']
        })
        
        # Save updated reports
        with open('voice_reports.json', 'w') as f:
            json.dump(reports, f, indent=4)
            
    except Exception as e:
        st.error(f"Error saving report: {str(e)}")

def emergency_mode():
    """Simplified emergency interface with large buttons and voice commands"""
    st.markdown("""
        <div style='text-align: center'>
        <h1 style='color: red; font-size: 48px'>🚨 EMERGENCY MODE 🚨</h1>
        <p style='font-size: 24px'>Please pull over safely before using this app</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button(" CALL 911", key="emergency"):
        # Integrate with phone's emergency calling system
        pass

def listen_for_wake_word():
    """Listen for the wake word 'hey drivesafe'"""
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio).lower()
            return "hey drivesafe" in text or "hey drive safe" in text
    except:
        return False

def process_voice_command():
    """Process voice command after wake word is detected"""
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Listening for command...")
            audio = r.listen(source, timeout=5)
            command = r.recognize_google(audio).lower()
            
            # Simple command processing
            if "emergency" in command:
                st.error("🚨 Initiating emergency protocol!")
                return "emergency"
            elif "report accident" in command:
                st.warning("📝 Starting accident report...")
                return "report"
            elif "safety tips" in command:
                st.info("💡 Opening safety tips...")
                return "tips"
            else:
                st.info(f"Command not recognized: {command}")
                return None
    except:
        st.error("Could not process command. Please try again.")
        return None

def render_login():
    st.markdown("### 🔐 User Authentication")
    
    # Create tabs for Sign In and Sign Up
    login_tab, signup_tab = st.tabs(["Sign In", "Sign Up"])
    
    with login_tab:
        st.markdown("#### Sign In")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        col1, col2 = st.columns([1,2])
        with col1:
            if st.button("Sign In", use_container_width=True):
                # Add authentication logic here
                st.success("Successfully signed in!")
        with col2:
            st.markdown("[Forgot Password?](#)")
    
    with signup_tab:
        st.markdown("#### Create Account")
        new_email = st.text_input("Email", key="new_email")
        new_password = st.text_input("Create Password", type="password", key="new_pass")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        # Additional user info
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
            driving_experience = st.selectbox("Driving Experience", 
                ["< 1 year", "1-3 years", "3-5 years", "5+ years"])
        with col2:
            last_name = st.text_input("Last Name")
            vehicle_type = st.selectbox("Vehicle Type", 
                ["Sedan", "SUV", "Truck", "Motorcycle", "Other"])
        
        if st.button("Create Account", use_container_width=True):
            # Add account creation logic here
            st.success("Account created successfully!")

if __name__ == "__main__":
    main()
