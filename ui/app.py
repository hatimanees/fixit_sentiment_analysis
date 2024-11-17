# app.py (Streamlit frontend)
import streamlit as st
import requests
from PyPDF2 import PdfReader
import io

API_URL = "http://127.0.0.1:5000/upload"


def main():
    st.title("Sentiment Analysis on Call Transcripts")

    uploaded_file = st.file_uploader("Upload your call transcript", type=["txt", "pdf"])

    if uploaded_file:
        try:
            # Process the uploaded file
            if uploaded_file.name.endswith(".txt"):
                transcript = uploaded_file.read().decode('utf-8')
            elif uploaded_file.name.endswith(".pdf"):
                reader = PdfReader(uploaded_file)
                transcript = ""
                for page in reader.pages:
                    transcript += page.extract_text()

            # Display the extracted text
            st.text_area("Uploaded Transcript", transcript, height=300)

            # Send the transcript for sentiment analysis
            if st.button("Analyze Sentiment"):
                with st.spinner("Analyzing sentiment..."):
                    try:
                        # Send the transcript directly as form data
                        response = requests.post(
                            API_URL,
                            data={'transcript': transcript},
                            timeout=10
                        )

                        if response.status_code == 200:
                            sentiment = response.json().get('sentiment', [])
                            st.success("Analysis complete!")

                            # Create a nice display for results
                            st.subheader("Sentiment Results")
                            for result in sentiment:
                                score = result['score']
                                label = result['label']

                                # Create a progress bar for visualization
                                st.write(f"{label}:")
                                st.progress(score)
                                st.write(f"Score: {score:.2f}")

                                # Add interpretation
                                if label == 'Overall Sentiment':
                                    if score > 0.6:
                                        st.info("📈 This text is predominantly positive")
                                    elif score < 0.4:
                                        st.info("📉 This text is predominantly negative")
                                    else:
                                        st.info("📊 This text is relatively neutral")
                                elif label == 'Confidence':
                                    if score > 0.8:
                                        st.info("✨ High confidence in this analysis")
                                    elif score < 0.5:
                                        st.warning("⚠️ Take this analysis with a grain of salt")
                        else:
                            st.error(f"Error: {response.json().get('error', 'Unknown error')}")

                    except requests.exceptions.ConnectionError:
                        st.error("Could not connect to the server. Please make sure the Flask backend is running.")
                    except requests.exceptions.Timeout:
                        st.error("Request timed out. Please try again.")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")


if __name__ == "__main__":
    main()




