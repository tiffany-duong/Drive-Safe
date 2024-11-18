# Teen Driving Safety Analysis Platform 🚗

## Overview
A comprehensive web application built with Streamlit that helps teen drivers improve their driving safety through real-time analysis, interactive learning, and safety alerts. The platform features multiple interactive dashboards for safety monitoring.

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

## Tech Stack
- Python 3.8+
- Streamlit
- Pandas
- Plotly

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

4. Run the application
```bash
streamlit run App_UI.py
```

## Project Structure
```
boblol/
├── App_UI.py                    # Main application interface
├── App_Pic.py                   # Image processing functionality
├── safety_tips.py               # Safety tips and quiz module
├── create_alerts.py             # Alert system
├── check_dependencies.py        # Dependency checker
├── test_safety.py              # Test cases
├── data/
│   ├── data_analysis.csv       # Analysis data
│   ├── detailed_analysis.csv   # Detailed metrics
│   └── quiz_scores.json        # User quiz results
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

