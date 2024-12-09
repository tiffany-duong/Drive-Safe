# Drive Safe: A Helping Hand to Improve Your Driving Safety 🚗

<img width="249" alt="Drive Safe Logo" src="https://github.com/user-attachments/assets/fdea65ce-0e58-41d1-b8a5-6c720e2b65c8">

<img width="823" alt="Screen Shot 2024-12-08 at 4 19 04 PM" src="https://github.com/user-attachments/assets/cc648d12-b49f-4d5e-8418-c7c4c4430a4d">

<img width="1661" alt="Screen Shot 2024-12-08 at 7 07 46 PM" src="https://github.com/user-attachments/assets/1f0a992a-15af-4874-911e-5c194ea33cc3">

<img width="1665" alt="Screen Shot 2024-12-08 at 7 07 57 PM" src="https://github.com/user-attachments/assets/4dea293b-561a-4962-a3ec-fdfe1e02526c">

<img width="1674" alt="Screen Shot 2024-12-08 at 7 08 14 PM" src="https://github.com/user-attachments/assets/8760a763-2365-43c0-b7e3-c5bce99f0efb">

<img width="1675" alt="Screen Shot 2024-12-08 at 7 08 29 PM" src="https://github.com/user-attachments/assets/6b7161e2-fa43-4be7-b357-c71c1e0ba1db">

<img width="1674" alt="Screen Shot 2024-12-08 at 7 08 37 PM" src="https://github.com/user-attachments/assets/59565f5d-143b-43b4-93f5-b901c9d6b5f2">

## Project Summary
Drive Safe is a web application built with Python, Streamlit, pandas, Plotly, OpenAI, and JSON that helps drivers improve their driving safety through real-time analysis, interactive learning, and safety alerts. The platform features multiple interactive dashboards for safety monitoring, AI-powered assistance, 911 emergency button, login/create account page with consent checkbox, report accident, stimulation accident, and voice command. My contribution includes developing the 911 Emergency Service web page, and the AI Assistant web page while implementing ML and NLP data and models to strengthen the prompt engineering responses for the AI Assistant. A high priority was ensuring that Drive Safe would be user friendly and accessible to everyone while providing accurate, reliable, and consensual data to users. By making analytics accessible to users, Drive Safe addresses the social issue of traffic fatality within Santa Clara County to help reduce the amount of traffic accidents, making drivers more aware of past accidents, and help improve citizen's driving safety and abilities.

## Introduction to Drive Safe: What is it?
Drive Safe is designed to help drivers be more alerted of recent traffic accidents so that they can be more aware of hazard intersections and areas using past data to help provide new tips and strategies to help drivers avoid the same accident, hoping to save future lives! Drive Safe features advance AI tools with tips and helpful solutions to help enhance citizen's driving safety and insights.

## Demo Video:

https://github.com/user-attachments/assets/40d42037-cf4f-4525-91cc-3c8a3d3b4346

## Why Drive Safe?
Driving has it's pros and cons and there is nothing worst than experiencing a traffic accident. unfortunately, there are no real time monitoring or data tracking applications drivers can use at the moment that features real time update. This can be hard on inexperienced drivers, parents who have their love ones on the road, and corporations. 

With Drive Safe, it offers a real time dashboard, detailed analysis of data, safety tips, 911 emergency button, secure user authentication, AI Assistant, learning quizzes and much more! 

Drive smart, drive safe, with Drive Safe!

## Our Solution With Feature Explanation
Drive Safe includes the latest technology with a user friendly platform to help provide insightful tips and suggestions for users.

- 📊 **Dashboard**
  - Real-time speed monitoring 
  - Driving pattern analysis
  - Interactive charts and visualizations
  - Safety score tracking

- 📈 **Detailed Analysis**
  - Comprehensive driving statistics
  - Historical data trends
  - Performance metrics
  - Risk assessment

- 🛡️ **Safety Tips**
  - Interactive safety quizzes
  - Educational content
  - Safety tips recommendations
  - Emergency guidelines

- 🚨 **Emergency Services**
  - Quick access to emergency contacts
  - Location-based services
  - Incident reporting
  - Emergency response protocols

- 👤 **User Authentication**
  - Secure sign-up/sign-in system
  - Profile customization
  - Vehicle information tracking
  - Activity history

- 🤖 **AI Assistant**
  - Real-time driving advice
  - Voice command button interface
  - Natural language interaction
  - Personalized responses
  - OpenAI GPT-3.5 powered responses
 
## What Matters With Drive Safe?
Drive Safe makes analytics approachable and helps Safe tackles the critical issue of traffic fatalities in Santa Clara County. Drive Safe can help reduce accidents by increasing driver awareness of past incidents and improving overall driving safety and skills.

## Tech Stack
- Python 3.8+
- Streamlit
- Pandas
- Plotly
- OpenAI GPT-3.5
- Speech Recognition (coming soon)
- JSON for data storage
- Plotly for interactive visualizations

## Installation & Setup

### Requirements
- Python 3.8+
- pip package manager
- Virtual environment (recommended)

### Installation Steps
1. Clone the repository
```bash
git clone https://github.com/Reenamjot/boblol.git
cd boblol
```

2. Create and activate virtual environment (optional but recommended)
```bash
python -m venv myenv
source myenv/bin/activate  # For Unix/macOS
myenv\Scripts\activate     # For Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
Create a `.env` file in the root directory and add:
```
OPENAI_API_KEY=your_api_key_here
```

5. Run the application
```bash
streamlit run App_UI.py
```

## Project Structure
```
boblol/
├── App_UI.py                    # Main application interface with AI Assistant
├── App_Pic.py                   # Image processing functionality
├── safety_tips.py               # Safety tips and quiz module
├── create_alerts.py             # Alert system
├── check_dependencies.py        # Dependency checker
├── test_safety.py              # Test cases
├── data/
│   ├── data_analysis.csv       # Analysis data
│   ├── detailed_analysis.csv   # Detailed metrics
│   └── quiz_scores.json        # User quiz results
├── .env                        # Environment variables (OpenAI API key)
└── requirements.txt            # Project dependencies
```

## Running Tests
```bash
python -m pytest test_safety.py
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.
