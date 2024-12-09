# Tiffany Duong - worked on lines ~532-900. Worked on AI Assistant and 911 emergency features

import streamlit as st
from openai import OpenAI

# This MUST be the first Streamlit command
st.set_page_config(
    page_title="DriveSafe - Advanced Driving Analysis",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Regular imports without speech recognition
import sys
import subprocess
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
from safety_tips import SafetyTipsGenerator
import pandas as pd
import numpy as np
import ssl
import json
import random
import time
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
            # Add custom CSS for the sidebar speech button
            st.markdown("""
                <style>
                .sidebar-speech-button {
                    background-color: #1E3D59;
                    color: white;
                    padding: 12px 20px;
                    text-align: center;
                    text-decoration: none;
                    display: block;
                    font-size: 16px;
                    margin: 10px 0;
                    border-radius: 12px;
                    border: 2px solid #ffffff;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }
                .sidebar-speech-button:hover {
                    background-color: #2E5D79;
                    transform: translateY(-2px);
                }
                .voice-hint {
                    text-align: center;
                    color: #666;
                    font-size: 0.9em;
                    font-style: italic;
                    margin-top: 5px;
                }
                </style>
            """, unsafe_allow_html=True)
            
            # Navigation selectbox
            page = st.selectbox(
                "Navigation",
                ["Profile", "Dashboard", "Detailed Analysis", "Safety Tips", "Emergency Services", "AI Assistant"]
            )
            
            # Add speech button and hint text
            st.markdown("""
                <div class='sidebar-speech-button'>
                    🎤 Voice Commands
                </div>
                <div class='voice-hint'>
                    Say "Hey DriveSafe" to start
                </div>
            """, unsafe_allow_html=True)
        
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
            
            # Weather Alert
            st.markdown("### 🌤️ Weather Alert")
            st.warning("Light rain expected this afternoon. Remember to maintain safe following distance!")

        elif page == "Detailed Analysis":
            create_detailed_analysis()

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
            
            # Real-time Alert Simulation
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
                ###  Roadside Assistance
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

        elif page == "AI Assistant":
            st.subheader("🤖 AI Driving Assistant")
            
            # Container for chat interface
            chat_container = st.container()
            
            # Speech button (non-functional placeholder)
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                st.markdown(
                    """
                    <style>
                    .speech-button {
                        background-color: #1E3D59;
                        color: white;
                        padding: 15px 32px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 4px 2px;
                        border-radius: 12px;
                        width: 100%;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                st.button("🎤 Hold to Speak", key="speech_button", help="Speech functionality coming soon!")
            
            # Text input for questions
            with chat_container:
                user_question = st.text_input("Ask me anything about driving safety:", 
                                            placeholder="e.g., How should I handle hydroplaning?")
                if user_question:
                    with st.spinner("Thinking..."):
                        response = ai_driving_assistant(user_question)
                        
                        # Create a message-like container for the response
                        st.markdown(
                            f"""
                            <div style="
                                background-color: #f0f2f6;
                                border-radius: 10px;
                                padding: 15px;
                                margin: 10px 0;
                            ">
                                {response}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

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
    """Display alert based on the type of alert"""
    alert_messages = {
        "speeding": "⚠️ Warning: Speed exceeds limit. Please slow down.",
        "sharp_turn": "⚠️ Caution: Sharp turn ahead. Reduce speed.",
        "phone_use": "⚠️ Alert: Phone use detected. Keep eyes on road.",
        "sudden_brake": "⚠️ Notice: Sudden braking detected. Maintain safe distance.",
        "lane_departure": "⚠️ Warning: Lane departure detected. Stay in lane.",
        "fatigue": "⚠️ Warning: Signs of fatigue detected. Consider taking a break."
    }
    
    message = alert_messages.get(alert_type, f"⚠️ Alert: {alert_type}")
    st.warning(message)

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
        <h1 style='color: red; font-size: 48px'> EMERGENCY MODE 🚨</h1>
        <p style='font-size: 24px'>Please pull over safely before using this app</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button(" CALL 911", key="emergency"):
        # Integrate with phone's emergency calling system
        pass

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

def ai_driving_assistant(user_query):
    """
    AI assistant that answers driving-related questions using OpenAI's API
    """
    client = OpenAI()
    system_prompt = """You are a helpful driving assistant. Provide clear, accurate advice about:
    - Traffic rules and regulations
    - Safe driving practices
    - Vehicle maintenance
    - Emergency situations
    Always prioritize safety and include relevant disclaimers when necessary."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def create_detailed_analysis():
    # Header with proper spacing
    st.markdown("""
        <div style='text-align: center; padding: 1rem; margin-bottom: 2rem;'>
            <h1 style='color: #1E3D59;'>📊 Detailed Driving Analysis</h1>
            <p style='color: #666; font-size: 1.1em;'>Comprehensive analysis of driving patterns and safety metrics</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create the pie chart with adjusted layout
    incident_types = {
        'Speed Related': 30,
        'Weather Related': 25,
        'Distracted Driving': 20,
        'Vehicle Malfunction': 15,
        'Other': 10
    }
    
    fig = px.pie(
        values=list(incident_types.values()),
        names=list(incident_types.keys()),
        title='Incident Distribution by Type',  # Shortened title
        color_discrete_sequence=['#66B2B2', '#FFE5B4', '#B4B4FF', '#FFB4B4', '#E5E5E5'],
        hole=0.4
    )
    
    # Update layout with better responsiveness
    fig.update_layout(
        title={
            'text': 'Incident Distribution by Type',
            'x': 0.5,  # Center the title
            'xanchor': 'center',
            'y': 0.95,
            'font': {'size': 24, 'color': '#1E3D59'}
        },
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        height=500,
        margin=dict(t=100, b=100, l=50, r=50)  # Adjust margins
    )
    
    # Use columns for better spacing
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.plotly_chart(fig, use_container_width=True)
    
    # Create two columns for metrics and findings
    col1, col2 = st.columns(2)
    
    with col1:
        # Add styled metrics container
        st.markdown("""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <h3 style='color: #1E3D59; margin-bottom: 15px;'>Safety Metrics</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Add metrics with improved styling
        st.metric(
            label="Overall Safety Score",
            value="85%",
            delta="↑ 5%",
            help="Based on last 30 days of driving data"
        )
        st.metric(
            label="Incident-Free Days",
            value="45",
            delta="↑ 12",
            help="Consecutive days without incidents"
        )
    
    with col2:
        # Add styled findings container
        st.markdown("""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <h3 style='color: #1E3D59; margin-bottom: 15px;'>Key Findings</h3>
                <ul style='color: #444; margin-left: 20px;'>
                    <li>Speed remains the leading factor in incidents (30%)</li>
                    <li>Weather conditions significantly impact safety (25%)</li>
                    <li>Distracted driving continues to be a major concern (20%)</li>
                    <li>Regular maintenance could prevent 15% of incidents</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    # Add recommendations section at the bottom
    st.markdown("""
        <div style='margin-top: 2rem; padding: 20px; background-color: #f0f7ff; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h3 style='color: #1E3D59; margin-bottom: 15px;'>💡 Recommendations</h3>
            <ul style='color: #444; margin-left: 20px;'>
                <li>Consider implementing speed monitoring systems</li>
                <li>Enhance weather alert notifications</li>
                <li>Schedule regular vehicle maintenance checks</li>
                <li>Provide additional training for distraction prevention</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 
    
