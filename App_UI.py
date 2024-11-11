import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from safety_tips import SafetyTipsGenerator
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
import ssl
import json
from datetime import datetime
import random
import time
from pygame import mixer
from gtts import gTTS
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
    page_title="Bob - Teen Driving Analysis",
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
            <h1 style='text-align: center; color: #1E3D59; padding: 20px;'>
                🚗 Bob - Advanced Teen Driving Analysis
            </h1>
        """, unsafe_allow_html=True)
        
        # Sidebar navigation
        with st.sidebar:
            page = st.selectbox(
                "Navigation",
                ["Dashboard", "Detailed Analysis", "Safety Tips", "Emergency Services"]
            )
        
        # Page content
        if page == "Dashboard":
            # Welcome Section
            st.markdown("""
                <div class="welcome-header">
                    <h1>👋 Welcome to Bob</h1>
                    <p>Your Trusted Teen Driving Companion</p>
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
            st.subheader("📊 Road Safety Analysis")
            
            # Add Report Accident Button
            st.markdown("### 🚨 Report an Incident")
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
                    st.warning(f"⚠️ Distraction Rating: {distraction_rating}/100")
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

            # Speed vs Reaction Time Interactive Chart
            st.markdown("### 🚗 Speed Impact Analysis")
            speed = st.slider("Select Speed (mph)", 20, 80, 40)
            reaction_distance = speed * 1.467  # Convert mph to feet per second
            stopping_distance = (speed * 1.467) * (speed/20)  # Simplified stopping distance formula
            
            # Display reaction time visualization
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Reaction Distance (feet)", f"{reaction_distance:.1f}")
            with col2:
                st.metric("Stopping Distance (feet)", f"{stopping_distance:.1f}")
                
            # Voice Alert System (with audio)
            st.markdown("### 🎙️ Voice Alert System")
            alert_triggers = st.multiselect("Simulate Driving Behaviors:",
                ["Speeding", "Sharp Turn", "Sudden Brake", "Phone Use", "Lane Departure"])
            
            if alert_triggers:
                for trigger in alert_triggers:
                    play_alert(trigger)

            # Keep your existing visualizations and conclusions here

        elif page == "Safety Tips":
            st.subheader("🚦 Safety Tips for Teen Drivers")
            
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
            
            # Add an interactive quiz section
            st.markdown("---")
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
            st.subheader("🚨 Emergency Services")
            
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
                if st.button("🚨 EMERGENCY - CALL 911 🚨"):
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
        else:
            # Fallback to text alert if audio file not found
            alert_messages = {
                "Speeding": "🔊 Warning: Speed exceeds limit. Please slow down.",
                "Sharp Turn": "🔊 Caution: Sharp turn ahead. Reduce speed.",
                "Phone Use": "🔊 Alert: Phone use detected. Keep eyes on road.",
                "Sudden Brake": "🔊 Notice: Sudden braking detected. Maintain safe distance.",
                "Lane Departure": "🔊 Warning: Lane departure detected. Stay in lane."
            }
            st.warning(alert_messages.get(alert_type, "⚠️ Alert!"))
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

if __name__ == "__main__":
    main()
