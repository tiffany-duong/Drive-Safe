BOB - Your Teen Driving Report Generator

What is this?
This is an AI-powered application that creates detailed teen driving reports and generates related images. It uses OpenAI's GPT for writing reports and DALL-E for creating images.

Features:
- Generates detailed driving performance reports
- Creates AI images related to the driving scenario
- Easy-to-use web interface
- Secure API key handling

Quick Setup:
1. Clone this repository:
   git clone https://github.com/Reenamjot/boblol.git
   cd boblol

2. Install all requirements:
   pip install -r requirements.txt

3. Set up your API key:
   - Copy .env.example to a new file named .env
   - Add your OpenAI API key to the .env file

4. Run the app:
   streamlit run App_UI.py

How to Use:
1. Open the app in your web browser
2. Type your driving scenario or question
3. Click "Generate Report and Images"
4. View your report and AI-generated images

Files Included:
- App_UI.py: Main application interface
- App_Pic.py: Image generation handler
- requirements.txt: List of required packages
- .env.example: Template for API key setup
- README.md: This guide

Requirements:
- Python 3.8+
- OpenAI API key
- Internet connection


