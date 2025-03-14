# This script tailors my resume to a job description  using CHatGPT. 
# Idea from https://medium.com/towards-data-science/5-ai-projects-you-can-build-this-weekend-with-python-c57724e9c461

import markdown
import chatgpt_handler
import argparse

parser = argparse.ArgumentParser(
                    prog='tailor_resume',
                    description='Tailor a resume to a job description')

parser.add_argument('-r','--resume',help="The resume in MARKDOWN. Default 'resume.md'",default="resume.md",required=False)
parser.add_argument('-rh','--resume-html',help="Output filename for original resume as HTML. Optional. Default 'original_resume.html'",default="original_resume.html",required=False)
parser.add_argument('-j','--job-description',help="The job description in txt")
parser.add_argument('-o','--output',help="Filename to write tailored resume in html. Optional. Default 'tailored_resume.html'",default="tailored_resume.html",required=False)
parser.add_argument('-t','--temperature',help="Temperature to use in ChatGPT response. Optional. Default 0.25",default=0.25,required=False)
args = parser.parse_args()

resume_file = args.resume
resume_html_file = args.resume_html
job_desciption_file = args.job_description
output_file = args.output
temperature = args.temperature

# Read in resume as markdown
#TODO get chatgpt to convert to markdown if not in MD
with open(resume_file, "r") as file:
    input_resume = file.read()

# Read in JD
with open(job_desciption_file, "r") as file:
    job_desciption = file.read()

# Open AI/ChatGPT prompt:
prompt = f"""
I have a resume formatted in Markdown and a job description. \
Please adapt my resume to better align with the job requirements while \
maintaining a professional tone. Tailor my skills, experiences, and \
achievements to highlight the most relevant points for the position. \
Ensure that my resume still reflects my unique qualifications and strengths \
but emphasizes the skills and experiences that match the job description.

### Here is my resume in Markdown:
{input_resume}

### Here is the job description:
{job_desciption}

Please modify the resume to:
- Use keywords and phrases from the job description.
- Adjust the bullet points under each role to emphasize relevant skills and achievements.
- Make sure my experiences are presented in a way that matches the required qualifications.
- Maintain clarity, conciseness, and professionalism throughout.

Return the updated resume in Markdown format.

"""
    
output_resume_md = chatgpt_handler.call_chatgpt(prompt,temperature=temperature)

# Write original and tailored resume to html 
# TODO remove the ChatGPT response not part of resume
inout_resume_html = markdown.markdown(input_resume)
with open(resume_html_file, "w") as f:
    f.write(inout_resume_html)


output_resume_html = markdown.markdown(output_resume_md)

with open(output_file, "w") as f:
    f.write(output_resume_html)


# TODO: get PDF coversion to work. Missing dependency, no longer supported?

# import pdfkit

# # Convert an HTML file to PDF
# pdfkit.from_file("output.html", "output.pdf")

#TODO get resturn value of chatgpt to verify something happened. 
print(f"Tailored resume at {output_file} using temperature {temperature}. Original resume at {resume_html_file}")