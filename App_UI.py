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
ssl._create_default_https_context = ssl._create_unverified_context

# Load environment variables
load_dotenv()

# Your existing functions here
@st.cache_data
def load_and_prepare_data():
    """Load and prepare multiple data sources"""
    try:
        # Primary driving data
        driving_data = pd.read_csv("synthetic_traffic_fatalities.csv")
        
        # Synthetic weather data
        weather_data = generate_synthetic_weather_data(len(driving_data))
        
        # Merge datasets
        combined_data = pd.merge(driving_data, weather_data, left_index=True, right_index=True)
        
        return combined_data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

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

def main():
    st.title("🚗 Bob - Advanced Teen Driving Analysis")
    
    # Add custom CSS for emergency button styling
    st.markdown("""
    <style>
        div[data-testid="stButton"] button {
            background-color: #ff4b4b;
            color: white;
            font-weight: bold;
            padding: 0.5rem 1rem;
            font-size: 1.2rem;
        }
        div[data-testid="stButton"] button:hover {
            background-color: #ff0000;
            border-color: #ff0000;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar for navigation
    page = st.sidebar.selectbox(
        "Navigate to",
        ["Dashboard", "Detailed Analysis", "Safety Tips", "Data Explorer", "Emergency Services"]
    )
    
    # Load data
    try:
        df = load_and_prepare_data()
        
        if page == "Dashboard":
            st.header("📊 Dashboard")
            analyze_driving_patterns(df)
            
        elif page == "Detailed Analysis":
            st.header("🔍 Detailed Analysis")
            
            # Load and display the data structure first
            road_data = load_road_data()
            if road_data is not None:
                st.write("Data Structure Check:")
                st.write(road_data.head())
                st.write("Column Names:", road_data.columns.tolist())
                
                # Overview statistics
                st.subheader("📊 Road Safety Overview")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    total_roads = len(road_data['RoadID'].unique())
                    st.metric("Total Roads", total_roads)
                    
                with col2:
                    total_accidents = len(road_data)
                    st.metric("Total Incidents", total_accidents)
                
                with col3:
                    fatal_accidents = road_data['FatalAccidents'].sum()
                    st.metric("Fatal Incidents", fatal_accidents)
                
                with col4:
                    avg_accidents = round(total_accidents / total_roads, 1)
                    st.metric("Avg Incidents per Road", avg_accidents)
                
                # Road Condition Analysis
                st.subheader("🛣️ Road Condition Analysis")
                col1, col2 = st.columns(2)
                
                with col1:
                    condition_data = road_data['RoadCondition'].value_counts()
                    fig_condition = px.pie(values=condition_data.values, 
                                         names=condition_data.index,
                                         title='Incidents by Road Condition')
                    st.plotly_chart(fig_condition)
                    
                with col2:
                    weather_data = road_data['WeatherCondition'].value_counts()
                    fig_weather = px.bar(x=weather_data.index, 
                                       y=weather_data.values,
                                       title='Incidents by Weather Condition')
                    st.plotly_chart(fig_weather)
                
                # Time Analysis
                st.subheader("⏰ Time-based Analysis")
                col1, col2 = st.columns(2)
                
                with col1:
                    time_data = road_data['TimeOfDay'].value_counts()
                    fig_time = px.pie(values=time_data.values, 
                                    names=time_data.index,
                                    title='Incidents by Time of Day')
                    st.plotly_chart(fig_time)
                    
                with col2:
                    day_data = road_data['DayOfWeek'].value_counts()
                    fig_day = px.bar(x=day_data.index, 
                                   y=day_data.values,
                                   title='Incidents by Day of Week')
                    st.plotly_chart(fig_day)
                
                # Interactive Road Selection
                st.subheader("🔎 Individual Road Analysis")
                selected_road = st.selectbox("Select a road for detailed analysis:", 
                                           road_data['RoadName'].unique())
                
                road_details = road_data[road_data['RoadName'] == selected_road].iloc[0]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    ### Road Details
                    - **Speed Limit:** {road_details['SpeedLimit']} mph
                    - **Road Type:** {road_details['RoadType']}
                    - **Surface Type:** {road_details['SurfaceType']}
                    - **Lighting:** {road_details['Lighting']}
                    """)
                    
                with col2:
                    st.markdown(f"""
                    ### Safety Statistics
                    - **Total Incidents:** {len(road_data[road_data['RoadName'] == selected_road])}
                    - **Common Weather Condition:** {road_data[road_data['RoadName'] == selected_road]['WeatherCondition'].mode().iloc[0]}
                    - **Common Time of Day:** {road_data[road_data['RoadName'] == selected_road]['TimeOfDay'].mode().iloc[0]}
                    - **Most Common Day:** {road_data[road_data['RoadName'] == selected_road]['DayOfWeek'].mode().iloc[0]}
                    """)
            
        elif page == "Safety Tips":
            st.header("🛡️ Safety Tips Generator")
            
            tab1, tab2, tab3, tab4 = st.tabs(["General Safety", "Interactive Scenarios", "Safety Quiz", "Progress Tracker"])
            
            with tab1:
                st.subheader("Essential Driving Safety Tips")
                st.markdown("""
                ### 🚗 Basic Driving Safety
                1. **Always wear your seatbelt**
                2. **Follow speed limits**
                3. **Maintain safe following distance**
                4. **No phone use while driving**
                
                ### 🌦️ Weather-Related Safety
                1. **Reduce speed in bad weather**
                2. **Use headlights in poor visibility**
                3. **Increase following distance in rain**
                
                ### 🌙 Night Driving Tips
                1. **Use high beams appropriately**
                2. **Keep windshield clean**
                3. **Take breaks on long trips**
                """)
            
            with tab2:
                st.subheader("🚗 Interactive Driving Scenarios")
                
                # Scenario selector
                scenario_type = st.selectbox(
                    "Choose a scenario type:",
                    ["Highway Driving", "Urban Traffic", "Weather Conditions", "Emergency Situations"]
                )
                
                # Different scenarios based on selection
                scenarios = {
                    "Highway Driving": {
                        "scenario": """You're driving on the highway and notice a vehicle quickly 
                        approaching in your blind spot while you're planning to change lanes. What should you do?""",
                        "options": [
                            "Quickly change lanes before they reach you",
                            "Maintain your current position and speed, let them pass",
                            "Speed up to change lanes faster",
                            "Slow down abruptly to let them pass"
                        ],
                        "correct": 1,
                        "explanation": """The safest action is to maintain your position and speed. 
                        Sudden lane changes or speed adjustments can be dangerous. Let the other vehicle 
                        pass and then make your lane change when safe."""
                    },
                    "Urban Traffic": {
                        "scenario": """You're approaching a yellow light at an intersection with heavy pedestrian traffic. 
                        You're unsure if you can make it through before it turns red. What's the best action?""",
                        "options": [
                            "Speed up to make it through",
                            "Continue at the same speed",
                            "Begin slowing down to stop",
                            "Slam on the brakes"
                        ],
                        "correct": 2,
                        "explanation": """When in doubt at a yellow light, especially with pedestrians present, 
                        the safest option is to begin slowing down to stop. This prevents rushing through the 
                        intersection and reduces the risk of accidents."""
                    },
                    # Add more scenarios here...
                }
                
                if scenario_type in scenarios:
                    current_scenario = scenarios[scenario_type]
                    st.markdown(f"### Scenario: {scenario_type}")
                    st.markdown(current_scenario["scenario"])
                    
                    choice = st.radio("What would you do?", current_scenario["options"])
                    
                    if st.button("Check Response"):
                        if choice == current_scenario["options"][current_scenario["correct"]]:
                            st.success("✅ Correct! Great decision!")
                            st.markdown(current_scenario["explanation"])
                        else:
                            st.error("❌ That might not be the safest choice.")
                            st.markdown(current_scenario["explanation"])
            
            with tab3:
                st.subheader("📝 Safety Knowledge Quiz")
                
                # Enhanced quiz with more questions
                questions = [
                    {
                        "question": "What is the recommended following distance in good weather?",
                        "options": ["1 second", "2 seconds", "3 seconds", "4 seconds"],
                        "correct": 2
                    },
                    {
                        "question": "When should you turn on your headlights?",
                        "options": ["Only at night", "When it's raining", "30 minutes after sunset", "All of the above"],
                        "correct": 3
                    },
                    {
                        "question": "What should you do if your vehicle starts to skid?",
                        "options": ["Slam on the brakes", "Turn the wheel in the opposite direction", 
                                  "Steer in the direction you want to go", "Accelerate out of it"],
                        "correct": 2
                    }
                ]
                
                st.markdown("### Test Your Safety Knowledge!")
                
                quiz_responses = []
                for i, q in enumerate(questions):
                    response = st.radio(q["question"], q["options"], key=f"q_{i}")
                    quiz_responses.append(response == q["options"][q["correct"]])
                
                if st.button("Submit Quiz"):
                    score = sum(quiz_responses)
                    save_quiz_score(score, len(questions))
                    
                    st.markdown(f"""
                    ### Your Score: {score}/{len(questions)}
                    #### {score/len(questions)*100}%
                    
                    {'🌟 Excellent knowledge!' if score == len(questions) else 
                     '👍 Good effort!' if score >= len(questions)/2 else 
                     '📚 Keep learning about safety!'}
                    """)
            
            with tab4:
                st.subheader("📊 Your Progress")
                try:
                    with open('quiz_scores.json', 'r') as f:
                        scores = json.load(f)
                    
                    if scores:
                        # Convert scores to DataFrame for visualization
                        df_scores = pd.DataFrame(scores)
                        
                        # Show progress chart
                        fig = px.line(df_scores, x='date', y='percentage', 
                                    title='Your Safety Knowledge Progress',
                                    labels={'percentage': 'Score (%)', 'date': 'Quiz Date'})
                        st.plotly_chart(fig)
                        
                        # Show statistics
                        st.markdown(f"""
                        ### Your Statistics
                        - Average Score: {df_scores['percentage'].mean():.1f}%
                        - Highest Score: {df_scores['percentage'].max():.1f}%
                        - Total Quizzes Taken: {len(scores)}
                        """)
                    else:
                        st.info("Take some quizzes to see your progress!")
                except FileNotFoundError:
                    st.info("Take your first quiz to start tracking progress!")
            
        elif page == "Data Explorer":
            st.header("🔎 Data Explorer")
            st.dataframe(df)
            
            # Add interactive filters
            selected_columns = st.multiselect("Select columns to view:", df.columns)
            if selected_columns:
                st.dataframe(df[selected_columns])
                
        elif page == "Emergency Services":
            # Emergency Services section
            st.header("🚨 Emergency Services")
            
            # Create two columns
            col1, col2 = st.columns([2,1])
            
            with col1:
                st.markdown("""
                ### Emergency Guidelines
                1. **Stay Calm** - Take deep breaths and try to remain calm
                2. **Assess the Situation** - Check for injuries and immediate dangers
                3. **Move to Safety** - If possible, move to a safe location away from traffic
                4. **Turn on Hazard Lights** - Make your vehicle visible to others
                
                ### Important Information to Provide:
                - Your exact location (street names, landmarks)
                - Number of people involved
                - Any visible injuries
                - Any immediate dangers (fire, fuel leak, etc.)
                """)
                
                # Add a location finder
                if st.button("📍 Find My Location"):
                    st.info("For actual implementation, this would access the user's GPS location")
                    
            with col2:
                st.markdown("""
                ### Emergency Contacts
                """)
                
                # Emergency call button
                if st.button("🚨 CALL 911", use_container_width=True):
                    st.markdown("""
                    <div style="padding: 10px; background-color: #ff4b4b; border-radius: 5px; text-align: center;">
                        <h3 style="color: white;">Dialing 911...</h3>
                        <p style="color: white;">If this was a real emergency, your phone would now be calling 911.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Additional emergency numbers
                st.markdown("""
                #### Other Emergency Numbers:
                - Police (non-emergency): XXX-XXX-XXXX
                - Road Assistance: XXX-XXX-XXXX
                - Insurance Hotline: XXX-XXX-XXXX
                """)
    
    except Exception as e:
        st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
