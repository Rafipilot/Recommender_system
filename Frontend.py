import streamlit as st
import openai
from youtube_transcript_api import YouTubeTranscriptApi

# Set up OpenAI API key
openai.api_key = 'your_openai_api_key'

def summarize_text(text):
    response = openai.Completion.create(
        engine="davinci",  # or use "gpt-4" if you have access
        prompt=f"Summarize the following text:\n\n{text}",
        max_tokens=150  # adjust based on how concise you want the summary
    )
    summary = response.choices[0].text.strip()
    return summary

def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    full_transcript = ' '.join([entry['text'] for entry in transcript])
    return full_transcript

# Initialize session state for links if it doesn't exist
if 'links' not in st.session_state:
    st.session_state.links = []  # Creating the array of links the user "likes"

# Initialize session state for transcripts if it doesn't exist
if 'transcripts' not in st.session_state:
    st.session_state.transcripts = {}  # Storing transcripts with video ID as key

# Set the title of the app
st.title('Recommender System')

# Create a text input
user_input = st.text_input('Enter a YouTube ID for the video that you like:')

# Handle adding the new link
if user_input:
    if user_input not in st.session_state.links:
        st.session_state.links.append(user_input)
    st.write('You entered:', user_input)

# Display the list of links
st.write('All YouTube IDs:', st.session_state.links)

# Handle the RUN button
if st.button("RUN"):
    st.write("Running")
    for video_id in st.session_state.links:
        try:
            # Fetch transcript
            transcript = get_transcript(video_id)
            st.session_state.transcripts[video_id] = transcript  # Save transcript
            # Display results
            st.write(f"Transcript for video ID {video_id}:")
            st.write(transcript)
        except Exception as e:
            st.write(f"An error occurred for video ID {video_id}: {e}")

# Handle the RESET button
if st.button("RESET"):
    st.session_state.links = []  # Clear the links list
    st.session_state.transcripts = {}  # Clear the transcripts dictionary
    st.write("All data has been reset.")












