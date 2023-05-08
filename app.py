import argparse
import re
from datetime import timedelta
import openai
import os
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def validate_video_url(url):
    if not url.startswith('https://www.youtube.com/watch?v='):
        raise argparse.ArgumentTypeError('Invalid video URL')
    return url

def clean_text(text):
    text = re.sub(r'(?<!^)(\d{1,2}:\d{2}:\d{2})|(\d{1,2}:\d{2})', '', text)
    return text

def process_chunk(current_text_chunk, chunk_start_time, file):
    prompt = f"You are a YouTube timestamp description expert. Write a max=7 words, single line timestamp description, do not mention timestamp description: '{current_text_chunk}'"
    messages = [{"role": "system", "content": "You are a YouTube timestamp description expert."},
                {"role": "user", "content": prompt}]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=80,
        n=1,
        temperature=0.0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    description = clean_text(response.choices[0].message['content']).strip()
    
    timestamp_string = str(timedelta(seconds=int(chunk_start_time)))
    polished_timestamp = f"{timestamp_string} - {description}".replace("\n", " ").replace("Timestamp Description: ", "").replace('"', '').replace(" - -", " -")
    print(polished_timestamp)

    
    
    file.write(polished_timestamp + '\n')
    return polished_timestamp

def generate_ultra_summary(timestamp_descriptions):
    ultra_summary_prompt = f"You are a Youtube summarizer expert. Summarize the following: '{' '.join(timestamp_descriptions)}' combine the following into one description of events:"
    messages = [{"role": "system", "content": "You are a YouTube summarizer expert."},
                {"role": "user", "content": ultra_summary_prompt}]

    ultra_summary = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=350,
        n=1,
        temperature=0.0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return ultra_summary.choices[0].message['content']


def process_transcript(whole_transcript, video_id):
    current_text_chunk = []
    timestamp_descriptions = []
    chunk_start_time = None

    os.makedirs("timestamps", exist_ok=True)

    with open(f"timestamps/{video_id}.txt", "w", encoding="utf-8") as file:
        file.write("Timestamps:\n\n")

        current_text_chunk = []
        for current_line in whole_transcript:
            if chunk_start_time is None:
                chunk_start_time = current_line['start']

            current_text_chunk.append(current_line['text'])

            if len(current_text_chunk) > 50:
                timestamp_descriptions.append(process_chunk(current_text_chunk, chunk_start_time, file))
                chunk_start_time = None
                current_text_chunk = []

        if current_text_chunk:
            timestamp_descriptions.append(process_chunk(current_text_chunk, chunk_start_time, file))

        ultra_summary = generate_ultra_summary(timestamp_descriptions)

        print(ultra_summary)
        file.write("\nSummary:\n\n")
        file.write(ultra_summary)
        


def get_transcript_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        transcript_lines = file.readlines()

    transcript = []

    for line in transcript_lines:
        time_pattern = r'\[\d{2}:\d{2}\.\d{3} -> \d{2}:\d{2}\.\d{3}\]'
        timestamp_match = re.search(time_pattern, line)

        if timestamp_match:
            timestamp = timestamp_match.group()
            start_time_str = re.search(r'\d{2}:\d{2}\.\d{3}', timestamp).group()
            start_time = sum(float(x) * 60 ** i for i, x in enumerate(reversed(start_time_str.split(":")))) 
            text = re.sub(time_pattern, '', line).strip()
            transcript.append({"start": start_time, "duration": 0, "text": text})

    return transcript



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process YouTube video transcript")
    parser.add_argument("video_id", help="YouTube video ID")

    args = parser.parse_args()

    video_id = args.video_id

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        process_transcript(transcript, video_id)
    except TranscriptsDisabled:
        print("Transcript not found")
