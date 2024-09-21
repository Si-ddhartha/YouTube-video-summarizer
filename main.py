import os
from dotenv import load_dotenv

import google.generativeai as genai

from pytubefix import YouTube
from pytubefix.exceptions import VideoUnavailable

load_dotenv()
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
genai.configure(api_key=GOOGLE_API_KEY)

def get_transcript(video_url):
    video = YouTube(video_url)

    for caption in video.caption_tracks:
        if caption.code == 'en' or caption.code == 'a.en':
            break
    
    if caption.code not in ['en', 'a.en']:
        raise ValueError('English caption not found!!!')

    transcript = caption.generate_srt_captions()

    return transcript

def generate_summary(model, transcript):
    prompt_template = '''
        You are an expert summarizer. I will provide you with the transcript of a YouTube video. Your task is to generate a detailed summary that covers all the key points discussed in the video. Make sure to include:

        1. The main topic of the video.
        2. Any important subtopics or sections discussed.
        3. Key points and explanations mentioned by the speaker.
        4. Any examples, data, or statistics that are highlighted.
        5. Conclusions or takeaways provided in the video.

        Be as thorough as possible and ensure the summary is coherent and captures all relevant information. Here is the transcript of the video:

        {transcript}

        Now, summarize the content based on the transcript provided.
    '''

    try:
        summary = model.generate_content(prompt_template.format(transcript=transcript))
    
    except Exception as e:
        raise e

    return summary.text


def main():
    video_url = input('Enter youtube video url: ')

    try:
        transcript = get_transcript(video_url)
    
    except VideoUnavailable as e:
        raise e
    
    else:
        model = genai.GenerativeModel(model_name='gemini-1.5-pro')
        video_summary = generate_summary(model, transcript)

        with open('Summary.txt', 'w') as f:
            f.write(video_summary)


if __name__ == '__main__':
    main()