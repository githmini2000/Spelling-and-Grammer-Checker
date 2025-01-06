import re
import google.generativeai as genai
import streamlit as st

# Configure the Gemini API
genai.configure(api_key="AIzaSyCqoVQ_sY6Ytsxc7bJ5cvPzUc8u4u886rM")  # Replace with your actual API key

# Function to apply grammar rules locally
def apply_grammar_rules(text):
    corrections = {
        "මම": {
            "ටා": "ටෙමි", "නා": "නෙමි", "තා": "තෙමි", "මු":"මි", "දා": "දෙමි",
            "බා": "බෙමි", "මා": "මෙමි", "යා": "යෙමි", "නවා": "මි", "වා": "වෙමි",
            "සා": "සෙමි", "ටේය": "ටෙමි", "ටී": "ටිමි", "ටෙහි": "ටෙමි",
        },
        "අපි": {
            "ටාය": "ටෙමු", "නාය": "නෙමු", "මි":"මු", "තාය": "තෙමු", "දාය": "දෙමු",
            "බාය": "බෙමු", "මාය": "මෙමු", "යාය": "යෙමු", "වාය": "වෙමු",
            "සාය": "සෙමු", "ටේය": "ටෙමු", "ටී": "ටිමු", "ටෙහි": "ටෙමු", 
        }
    }

    corrected_paragraph = []
    sentences = re.split(r'(?<=\.)\s*', text)

    for sentence in sentences:
        sentence = sentence.strip()
        if sentence.startswith("මම"):
            for key, value in corrections["මම"].items():
                if sentence.endswith(key):
                    sentence = sentence.replace(key, value)
            if not sentence.endswith("මි"):
                sentence = sentence + "මි"
        elif sentence.startswith("අපි"):
            for key, value in corrections["අපි"].items():
                if sentence.endswith(key):
                    sentence = sentence.replace(key, value)
            if not sentence.endswith("මු"):
                sentence = sentence + "මු"

        corrected_paragraph.append(sentence)

    return " ".join(corrected_paragraph)

# Function to get corrections from Gemini API
def get_correction_from_gemini(text):
    try:
        # Create a GenerativeModel instance
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Generate content using the Gemini model
        response = model.generate_content(
            f"Correct the following Sinhala paragraph for grammar: {text}"
        )
        return response.result
    except Exception as e:
        return f"Error with AI correction: {e}"

# Main function to check grammar
def check_paragraph(paragraph):
    # Apply grammar rules locally
    rule_corrected = apply_grammar_rules(paragraph)
    
    # Get further corrections from Gemini API
    gemini_corrected = get_correction_from_gemini(rule_corrected)
    
    return rule_corrected, gemini_corrected

# Streamlit Interface
st.title("Sinhala Grammar Checker")
st.write("This tool checks Sinhala grammar using custom rules and the Gemini AI model.")

# Input paragraph
paragraph = st.text_area("Enter your paragraph in Sinhala:", height=200)

if st.button("Check Grammar"):
    if paragraph.strip():
        st.write("Processing...")

        # Process the paragraph
        rule_corrected, gemini_corrected = check_paragraph(paragraph)

        # Display results
        st.subheader("Results")
        st.write("### Corrected sentence:")
        st.write(rule_corrected)
        st.write("### AI-Based Corrections (Gemini):")
        st.write(gemini_corrected)
    else:
        st.error("Please enter a paragraph to check.")