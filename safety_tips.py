from typing import Dict, List
import re

class SafetyTipsGenerator:
    def __init__(self):
        # Dictionary of driving behaviors and corresponding safety tips
        self.safety_tips_database = {
            'speed': [
                "Maintain a consistent speed within posted limits",
                "Reduce speed in adverse weather conditions",
                "Allow extra distance for stopping at higher speeds"
            ],
            'braking': [
                "Practice smooth, gradual braking",
                "Maintain a safe following distance (3-second rule)",
                "Anticipate stops to avoid sudden braking"
            ],
            'lane_change': [
                "Always use turn signals when changing lanes",
                "Check blind spots before lane changes",
                "Avoid weaving between lanes unnecessarily"
            ],
            'distraction': [
                "Keep your phone out of reach while driving",
                "Set up GPS and music before starting your journey",
                "Pull over if you need to handle any distractions"
            ],
            'turning': [
                "Slow down before entering turns",
                "Use appropriate turn signals in advance",
                "Check for pedestrians when turning"
            ]
        }

    def analyze_report(self, report_text: str) -> List[str]:
        """
        Analyze the driving report and identify relevant behaviors
        """
        report_lower = report_text.lower()
        behavior_keywords = {
            'speed': r'speed|fast|slow|mph|acceleration',
            'braking': r'brake|stop|sudden|emergency',
            'lane_change': r'lane|merge|switch|changing lanes',
            'distraction': r'distract|phone|text|attention',
            'turning': r'turn|corner|intersection|curve'
        }
        
        return [behavior for behavior, pattern in behavior_keywords.items() 
                if re.search(pattern, report_lower)]

    def generate_safety_tips(self, report_text: str, max_tips: int = 3) -> List[str]:
        """
        Generate personalized safety tips based on the driving report
        """
        identified_behaviors = self.analyze_report(report_text)
        selected_tips = []
        
        for behavior in identified_behaviors:
            if behavior in self.safety_tips_database:
                selected_tips.extend(self.safety_tips_database[behavior])
        
        # If no behaviors were identified, add some general tips
        if not selected_tips:
            selected_tips = [
                "Always wear your seatbelt",
                "Stay focused on the road",
                "Follow traffic rules and signs"
            ]
            
        return selected_tips[:max_tips]

    def format_tips(self, tips: List[str]) -> str:
        """
        Format the safety tips into a presentable string
        """
        if not tips:
            return ""
            
        formatted_output = "\n🚗 Safety Tips & Recommendations:\n\n"
        for i, tip in enumerate(tips, 1):
            formatted_output += f"{i}. {tip}\n"
        
        return formatted_output

# Add this at the very end of safety_tips.py, after the class definition
__all__ = ['SafetyTipsGenerator']