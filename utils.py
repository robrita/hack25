import streamlit as st

def render_sidebar():
    """
    Render the common sidebar navigation for all pages in the PMO Agent application.
    This function should be called on every page to maintain consistent navigation.
    """
    # Configure page
    st.set_page_config(
        page_title="App Generator",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.logo(
        "https://upload.wikimedia.org/wikipedia/commons/a/a8/Microsoft_Azure_Logo.svg",
        link="https://portal.azure.com/",
    )

    # Custom CSS to adjust padding and hide certain elements
    # This is useful to ensure the layout looks good across different pages
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 3rem;
            # padding-bottom: 1rem;
            # padding-left: 1rem;
            # padding-right: 1rem;
        }
        .stAppDeployButton {
            display: none;
        }
        .st-emotion-cache-15ecox0 {
            display: none;
        }
        .viewerBadge_container__r5tak {
            display: none;
        }
        .styles_viewerBadge__CvC9N {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.write("# AzTech - App Generator")

        with st.container(border=True):
            st.page_link("app.py", label="Dashboard", icon="📊")
            st.page_link("pages/1_App_Generator.py", label="Generator", icon="🎨")

        st.image("img/H25_banner.png", width='stretch')
        st.write("*Powered by **Azure AI Foundry.***")

def keep_state(state_object, state_name):
    """
    Keep the Streamlit session state alive across page navigations.
    This is useful to maintain stateful data like uploaded files or user inputs.
    """
    if state_object:
        st.session_state[state_name] = state_object
    elif state_name in st.session_state:
        return True
    return False
