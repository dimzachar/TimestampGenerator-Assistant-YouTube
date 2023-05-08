# TimestampGenerator-Assistant-YouTube

This Python script utilizes OpenAI's GPT-3.5-turbo model to generate timestamp descriptions and an ultra-summary of a YouTube video using its transcript. The timestamp descriptions are limited to a maximum of 7 words (can be changed).

Please be aware that using OpenAI's API key will incur costs. Using OpenAI's GPT-3.5-turbo model seems cheaper than text-davinci-003.


## Features

- Automatically fetches the YouTube transcript for a given video ID
- Generates a timestamped summary
- Generates an ultra-summary of the video content
- Supports input of transcripts from a text file

## Dependencies

- Python 3.x
- `openai` (install with `pip install openai`)
- `youtube_transcript_api` (install with `pip install youtube_transcript_api`)
- `python-dotenv` (install with `pip install python-dotenv`)

## Installation

1. Clone the repository:

```
git clone https://github.com/your-username/YouTube-Transcript-Summarizer.git
cd TimestampGenerator-Assistant-YouTube```


## Usage

1. Sign up and set up an OpenAI API key and save it in a `.env` file in the same directory as the script, with the following format:

OPENAI_API_KEY=your_api_key_here

2. Run the script, passing the YouTube video ID as a command-line argument:

```
python app.py <video_id>
```

## Output

The timestamped summary and ultra-summary will be printed to the console and saved to a text file in the `issues` folder, named `video_id.txt`.


## Function Overview

- `validate_video_url(url)`: Validates the provided YouTube video URL.
- `clean_text(text)`: Cleans up the text by removing any timestamp-like strings.
- `process_chunk(current_text_chunk, chunk_start_time, file)`: Processes a chunk of text, generating a timestamp description using GPT-3.5-turbo.
- `generate_ultra_summary(timestamp_descriptions)`: Generates an ultra-summary of the video using the list of timestamp descriptions.
- `process_transcript(whole_transcript, video_id)`: Processes the entire transcript, generating timestamp descriptions and the ultra-summary, and saves them in a file.
- `get_transcript_from_file(file_path)`: Reads a transcript from a file and returns it as a list of dictionaries containing start time, duration, and text.

## How It Works

The script first downloads the transcript of the specified YouTube video using the `youtube_transcript_api`. Then, it processes the transcript by breaking it into chunks of text and generating timestamp descriptions for each chunk using GPT-3.5-turbo. The generated timestamp descriptions are then used to create an ultra-summary of the video. Finally, the timestamp descriptions and the ultra-summary are saved in a file in the `timestamps` directory, with the filename format `<video_id>.txt`.


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

