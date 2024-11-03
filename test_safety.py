from safety_tips import SafetyTipsGenerator

# Create an instance of the generator
generator = SafetyTipsGenerator()

# Test with a sample driving report
test_report = """
The driver was going too fast around corners and 
frequently checking their phone while driving. 
Multiple sudden brake applications were observed.
"""

# Generate and format safety tips
tips = generator.generate_safety_tips(test_report)
formatted_output = generator.format_tips(tips)

# Print the results
print(formatted_output) 