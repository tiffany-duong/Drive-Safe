import streamlit as st

# Add debug print to see if the file is running
st.write("Debug: App is running")

try:
    from safety_tips import SafetyTipsGenerator
    st.write("Debug: Successfully imported SafetyTipsGenerator")
except Exception as e:
    st.write(f"Debug: Error importing SafetyTipsGenerator - {str(e)}")

st.title("Driving Safety Tips Generator")

try:
    # Create an instance of the generator
    generator = SafetyTipsGenerator()
    st.write("Debug: Successfully created generator instance")

    # Create a text area for input
    user_input = st.text_area(
        "Enter driving report here:",
        """The driver was going too fast around corners and 
        frequently checking their phone while driving. 
        Multiple sudden brake applications were observed."""
    )

    # Add a button to generate tips
    if st.button("Generate Safety Tips"):
        # Generate and format safety tips
        tips = generator.generate_safety_tips(user_input)
        formatted_output = generator.format_tips(tips)
        
        # Display the results
        st.write(formatted_output)

except Exception as e:
    st.write(f"Debug: Error in main code - {str(e)}") 
