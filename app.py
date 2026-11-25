
import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get Gemini API key (supports local .env and Streamlit Community Cloud secrets)
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY and hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]

# Page configuration
st.set_page_config(
    page_title="AI Research Generator",
    page_icon="📚",
    layout="wide"
)

# Application title
st.title("📚 AI Research Title, Abstract & Keyword Generator")

st.write(
    "Turn your simple project idea into a professional "
    "research report outline using Artificial Intelligence."
)

st.divider()

# Sidebar
st.sidebar.title("About the Project")
st.sidebar.write(
    "This application helps students generate research "
    "titles, abstracts, keywords, objectives and future enhancements."
)

st.sidebar.info("Powered by Google Gemini AI")

# Main input section
st.header("Enter Your Project Details")

project_idea = st.text_area(
    "Project Idea (Explain in 2-3 lines)",
    placeholder="Example: Detect fake news using machine learning "
                "to identify misleading information.",
    height=120
)

domain = st.selectbox(
    "Select Your Project Domain",
    [
        "Artificial Intelligence (AI)",
        "Internet of Things (IoT)",
        "Web Development",
        "Cybersecurity",
        "Machine Learning",
        "Other"
    ]
)

# Generate button
if st.button("✨ Generate Research Content", use_container_width=True):

    if not project_idea.strip():
        st.warning("Please enter your project idea.")

    elif not API_KEY:
        st.error(
            "Gemini API key not found. Please add it to your .env file."
        )

    else:
        try:
            with st.spinner("Generating your research content..."):

                # Create prompt
                prompt = f"""
                You are an expert academic research assistant.

                Generate research content based on the following details.

                Project Idea: {project_idea}
                Domain: {domain}

                Follow these instructions carefully:

                1. Generate 3 professional research title options.
                2. Write one academic abstract between 150 and 200 words.
                3. Generate exactly 5 relevant keywords.
                4. Generate exactly 3 clear research objectives.
                5. Generate exactly 3 possible future enhancements.

                Use simple, professional academic English.

                Format your answer using these headings:

                ## 1. Research Title Options
                ## 2. Abstract
                ## 3. Keywords
                ## 4. Research Objectives
                ## 5. Future Enhancements

                Make the content relevant to the project idea.
                Do not invent experimental results or claim that
                the proposed project has already been completed.
                """

                # Generate AI response using verified active model
                import time
                result = None
                last_error = None

                for attempt in range(3):
                    try:
                        # Use HTTP/1.1 to prevent Windows SSL/HTTP2 unexpected EOF socket drops
                        client = genai.Client(
                            api_key=API_KEY,
                            http_options={
                                'timeout': 60000,
                                'client_args': {'http2': False}
                            }
                        )
                        response = client.models.generate_content(
                            model="gemini-3.6-flash",
                            contents=prompt
                        )
                        if response and response.text:
                            result = response.text
                            break
                    except Exception as err:
                        last_error = err
                        time.sleep(1.5)

                if not result:
                    raise last_error

            # Display generated content
            st.success("Research content generated successfully!")

            st.divider()

            st.subheader("📄 Generated Research Content")

            st.markdown(result)

            # Download generated content
            st.download_button(
                label="⬇️ Download Research Content",
                data=result,
                file_name="research_content.txt",
                mime="text/plain",
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# Footer
st.divider()

st.caption(
    "AI Research Generator | Built with Python, Streamlit "
    "and Google Gemini API"
)
