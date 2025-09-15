# pages/1_PRD_Generator.py
import os
import sys
import streamlit as st
from dotenv import load_dotenv
sys.path.append('..')
from utils import render_sidebar, keep_state

from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import (
    MessageRole,
)

# Load environment variables
load_dotenv()

# Create an instance of the AgentsClient using DefaultAzureCredential
agents_client = AgentsClient(
    endpoint=os.getenv("FOUNDRY_API_ENDPOINT"),
    credential=DefaultAzureCredential()
)

class PRDGenerator:
    def __init__(self):
        # Create a thread for the agent
        if "thread1" not in st.session_state:
            with st.spinner("Please wait while creating a thread..."):
                st.session_state.thread1 = agents_client.threads.create()

        self.thread = st.session_state.thread1

    def generate_prd(self, content):
        """Generate a Product Requirements Document for a given app description using Azure Foundry Agent"""
        try:
            # Create a message, with the prompt being the message content that is sent to the model
            agents_client.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=content,
            )
            
            # [START create_and_process]
            run = agents_client.runs.create_and_process(
                thread_id=self.thread.id,
                agent_id=os.getenv("AGENT_PRD_GENERATOR_ID"),
            )

            # [END create_and_process]
            if run.status == "failed":
                raise Exception(run.last_error)

            # Get the last message from the sender
            last_msg = agents_client.messages.get_last_message_text_by_role(
                thread_id=self.thread.id, role=MessageRole.AGENT
            )
 
            return last_msg.text.value
            
        except Exception as e:
            st.error(f"Error generating PRD: {str(e)}")
            return "Error generating PRD"

def main():
    # Render shared sidebar navigation
    render_sidebar()
    
    st.title("📋 PRD Generator")
    st.markdown("Generate comprehensive Product Requirements Documents (PRDs) for your app ideas using AI.")
    
    # Initialize the PRD generator
    prd_gen = PRDGenerator()
    container1 = st.container(border=True, key="container1")

    # Example data
    example_data_fitness = """An app for tracking personal fitness goals with social features to connect with friends and share achievements"""
    example_data_pdf = """A conversational AI application that allows users to upload PDF documents and chat with them using natural language queries to extract information, summarize content, and get answers based on the document content"""
    example_data_mining = """An intelligent document processing system that automatically extracts, categorizes, and indexes key information from unstructured documents like contracts, reports, and emails to create a searchable knowledge base"""

    saved_data = st.session_state.get("input_text", "")
    
    # Create radio button for example selection
    example_choice = container1.radio(
        "Choose an example or write your own:",
        options=["Custom", "Personal fitness tracker", "Chat with my PDF", "Document knowledge mining"],
        horizontal=True
    )
    
    # Determine which example to use
    example_data = ""
    if example_choice == "Personal fitness tracker":
        example_data = example_data_fitness
    elif example_choice == "Chat with my PDF":
        example_data = example_data_pdf
    elif example_choice == "Document knowledge mining":
        example_data = example_data_mining
    
    input_text = container1.text_area(
        "Describe your app idea in detail:",
        placeholder="An app for tracking personal fitness goals with social features...",
        height=150,
        value=example_data if example_choice != "Custom" else saved_data
    )

    if keep_state(input_text, "input_text"):
        input_text = st.session_state.input_text

    app_description = input_text.strip()

    # Show example or help
    with container1.expander("ℹ️ How this tool works?"):
        st.markdown("""
        ### How to Use the PRD Generator:
        
        1. **Describe Your App**: Provide a detailed description of your app idea, including key features and target audience
        2. **Click 'Generate PRD'**: The AI will analyze your description and create a comprehensive Product Requirements Document
        
        ### What You'll Get:
        - **Complete PRD**: A beautifully formatted markdown document with all essential sections for product development
        - **Actionable Requirements**: Clear guidance for development teams
        - **Download Option**: Download the PRD as a markdown file for easy sharing and documentation
        
        ### PRD Sections Generated:
        - Product Overview & Objectives
        - Target Audience Analysis
        - Key Features & User Stories
        - Technical Requirements
        - Success Metrics & Timeline
        - Risk Assessment
        
        ### Output Format:
        - **Markdown Structure**: Clean, professional formatting with proper headers and bullet points
        - **Easy to Read**: Native markdown rendering for optimal readability
        - **Shareable**: Download as .md file for integration with documentation systems
        """)

    # Generate button
    if st.button("🚀 Generate PRD", type="primary", disabled=app_description == ""):
        # Generate PRD
        with st.spinner("Generating Product Requirements Document..."):
            prd_content = prd_gen.generate_prd(app_description)
            st.session_state.prd_markdown = prd_content
            st.success("✅ PRD generated successfully!")

    # Get the PRD content from session state
    prd_markdown = st.session_state.get("prd_markdown", "")

    if prd_markdown:
        container2 = st.container(border=True, key="container2")
        
        # Display results
        container2.subheader("📊 Generated PRD")
        
        # Display the PRD with native copy functionality
        with container2.expander("📋 Product Requirements Document", expanded=True):
            st.code(prd_markdown, language="markdown", line_numbers=False)
        
        # Download option
        container2.download_button(
            label="📥 Download PRD as Markdown",
            data=prd_markdown,
            file_name="product_requirements_document.md",
            mime="text/markdown"
        )
        
        # PRD Refinement Section
        container2.subheader("🔄 Refine PRD")
        
        refinement_text = container2.text_area(
            "Describe how you'd like to refine or improve the PRD:",
            placeholder="Add more technical details, change the target audience, modify features, etc...",
            height=100,
            key="refinement_input"
        )
        
        # Update PRD button
        if container2.button("🔄 Update PRD", type="secondary", disabled=refinement_text.strip() == ""):
            # Generate updated PRD
            with st.spinner("Updating Product Requirements Document..."):
                updated_prd = prd_gen.generate_prd(refinement_text.strip())
                st.session_state.prd_markdown = updated_prd
                st.success("✅ PRD updated successfully!")
                st.rerun()

if __name__ == "__main__":
    main()