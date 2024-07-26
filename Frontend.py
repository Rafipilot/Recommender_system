import streamlit as st
import openai
from youtube_transcript_api import YouTubeTranscriptApi
import creds 
import re

openai.api_key = creds.api_key

def summarize_text(text):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"what is the genre of the video in one or two words:\n\n{text}"}
        ],
        max_tokens=10  # adjust based on how concise we want the summary
    )
    summary = response.choices[0].message.content
    return summary

def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    full_transcript = ' '.join([entry['text'] for entry in transcript])
    return full_transcript

def get_youtube_video_id(url):
    # Define the regular expression pattern to match YouTube URLs
    pattern = re.compile(
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    # Use the pattern to search the URL
    match = pattern.search(url)
    
    # If a match is found, return the video ID
    if match:
        return match.group(6)
    return None

# Initialize session state for links if it doesn't exist
if 'links' not in st.session_state:
    st.session_state.links = []  # Creating the array of links the user "likes"

# Initialize session state for transcripts if it doesn't exist
if 'transcripts' not in st.session_state:
    st.session_state.transcripts = {}  # Storing transcripts with video ID as key

st.title('Recommender System', anchor='center')

# Create columns
main_col, vid_col = st.columns([1, 3])

with main_col:
    # Create a text input
    user_input = st.text_input('Enter a YouTube URL for the video that you like:')

    # Handle adding the new link
    if user_input:
        VID = get_youtube_video_id(user_input)
        if VID and VID not in st.session_state.links:
            st.session_state.links.append(VID)
        st.write('You entered:', VID)

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
                st.write("Summarizing")
                summary = summarize_text(transcript)
                st.write(f"Summary for video ID {video_id}:")
                st.write(summary)
            except Exception as e:
                st.write(f"An error occurred for video ID {video_id}: {e}")

    # Handle the RESET button
    if st.button("RESET"):
        st.session_state.links = []  # Clear the links list
        st.session_state.transcripts = {}  # Clear the transcripts dictionary
        st.write("All data has been reset.")

with vid_col:
    # Example video
    VIDEO_URL = "https://www.youtube.com/watch?v=Vn_9lVvMkX4&ab_channel=SkyNews"
    st.video(VIDEO_URL)
    st.button("Like")
    st.button("Dislike")







