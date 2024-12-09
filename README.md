# Drive Safe: A Helping Hand to Improve Your Driving Safety 🚗

<img width="823" alt="Screen Shot 2024-12-08 at 4 19 04 PM" src="https://github.com/user-attachments/assets/cc648d12-b49f-4d5e-8418-c7c4c4430a4d">

## Project Summary
Drive Safe is a web application built with Python, Streamlit, pandas, Plotly, OpenAI, and JSON that helps drivers improve their driving safety through real-time analysis, interactive learning, and safety alerts. The platform features multiple interactive dashboards for safety monitoring, AI-powered assistance, 911 emergency button, login/create account page with consent check box, report accident, stimulation accident, and voice command. My contribution includes developing the 911 Emergency Service web page, and the AI Assistant web page while implementing ML and NLP data and models to strengthen the prompt engineering responses for the AI Assistant. A high priority was ensuring that Drive Safe would be user friendly and accessible to everyone while providing accurate, reliable, and consensual data to users. By making analytics accessible to users, Drive Safe addresses the social issue of traffic fatality within Santa Clara County to help reduce the amount of traffic accidents, making drivers more aware of past accidents, and help improve citizen's driving safety and abilities.

## Drive Safe: What is it?
Drive Safe is designed to help drivers be more alerted of recent traffic accidents so that they can be more aware of hazard intersections and areas using past data to help provide new tips and strategies to help drivers avoid the same accident, hoping to save future lives! Drive Safe features advance AI tools with tips and helpful solutions to help enhance citizen's driving safety and insights.

## Overview:



https://github.com/user-attachments/assets/40d42037-cf4f-4525-91cc-3c8a3d3b4346






## Key Features
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
  - Best practices
  - Emergency guidelines

- 🚨 **Emergency Services**
  - Quick access to emergency contacts
  - Location-based services
  - Incident reporting
  - Emergency response protocols

- 👤 **User Authentication**
  - Secure sign-up/sign-in system
  - Profile management
  - Vehicle information tracking
  - Activity history

- 🤖 **AI Assistant**
  - Real-time driving advice
  - Voice command button interface
  - Natural language interaction
  - Personalized responses
  - OpenAI GPT-3.5 powered responses

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

## Features in Detail

### Interactive Dashboard
- Real-time data visualization
- Custom chart configurations
- Downloadable reports
- Trend analysis

### Safety Analysis
- Risk factor identification
- Performance scoring
- Historical comparisons
- Safety recommendations

### User Authentication
- Secure login system
- Profile customization
- Vehicle management
- Activity tracking

### AI Assistant
- Real-time driving advice
- Voice command button interface
- Natural language interaction
- Personalized responses
- OpenAI GPT-3.5 powered responses

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

