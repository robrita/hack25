import streamlit as st
from dotenv import load_dotenv
from utils import render_sidebar

# Load environment variables
load_dotenv()

def main():
    # Render shared sidebar navigation
    render_sidebar()

    # Loading the CSS
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    st.title("🚀 AzTech - App Generator")
    st.markdown("Welcome to the AzTech - App Generator, your comprehensive tool for creating Azure Technology-Powered AI applications.")

    # Display hero banner image
    st.image("img/hero-banner.png", width='stretch')

if __name__ == "__main__":
    main()