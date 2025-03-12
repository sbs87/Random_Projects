
# This script extracts and summarizes a YouTube transcript using CHatGPT. 
# Idea from https://medium.com/towards-data-science/5-ai-projects-you-can-build-this-weekend-with-python-c57724e9c461

import openai
from generic_openai_key import API_KEY
openai.api_key = API_KEY
import re
from youtube_transcript_api import YouTubeTranscriptApi
import markdown
import argparse

parser = argparse.ArgumentParser(
                    prog='summarize_youtube',
                    description='Summarizes a YouTube video')

parser.add_argument('-l','--link',help="The full html to YouTube video")
parser.add_argument('-o','--output',help="Filename to write summary",default="summarized_video.html",required=False)

args = parser.parse_args()
# TODO run validity check
youtube_url = args.link
output_fn = args.output


# extract YouTube transcript
# extract video ID with regex
video_id_regex = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
match = re.search(video_id_regex, youtube_url)

# Get YT object API
ytt_api = YouTubeTranscriptApi()
ytt_api.fetch(match.group(1))

# Extract trx
transcript = ytt_api.get_transcript(match.group(1))
text_list = [transcript[i]['text'] for i in range(len(transcript))]
transcript_text = '\n'.join(text_list)


# Summarize trasncript with CGPT
# TODO make this a generic function to apply to other scripts. 
# TODO change the prompt a bit
prompt = f"""I have a Youtube transcript. \
Please summarize the transcript. 


### Here is the job description:
{transcript_text}

Return the summary in markdown format."""


    
#TODO add verbose/feedback to stdout
# make api call
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ], 
    temperature = 0.25
)
    
# extract response
trasncript_output = response.choices[0].message.content

print(trasncript_output)


output_yt_sum_html = markdown.markdown(trasncript_output)

with open(output_fn, "w") as f:
    f.write(output_yt_sum_html)