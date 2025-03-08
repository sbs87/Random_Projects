# This script taylors my resume to a job description  using CHatGPT. 
# Idea from https://medium.com/towards-data-science/5-ai-projects-you-can-build-this-weekend-with-python-c57724e9c461

import openai
import markdown

from generic_openai_key import API_KEY

openai.api_key = API_KEY

with open("resume.md", "r") as file:
    input_resume = file.read()


job_desciption="""POSITION SUMMARY:

The Lead Bioinformatician participates in the development and validation of cutting-edge technologies for analysis of genetic data. Designs and implements algorithms of varying complexity in the context of research, development, product validations, clinical trials, regulatory submissions, and scientific publications.

PRIMARY RESPONSIBILITIES:

Provide technical leadership in the design and execution of complex experiments and all phases of product development.
Design and review statistical methodology in statistical analysis plans and protocols.
Develop algorithms and models for complex data analysis.
Produce high quality written documentation including study protocols, statistical analysis plans and reports, and regulatory submissions
Act as an internal technical consultant to other functional groups or their members by providing expert advice on bioinformatics methodology
Performs other duties as assigned
QUALIFICATIONS:

Master’s degree in bioinformatics with 6 years post-graduate experience, or PhD with 3 years of post-graduate experience (preferred)
At least 4 years practical experience with data analysis software such as Python or R
KNOWLEDGE, SKILLS, AND ABILITIES:

Expert knowledge of bioinformatics tools in mapping, variant calling, CNV analysis and statistical methods
Familiarity with typical approaches, best practices, and regulatory standards in CLIA product development design
Ability to produce high quality written documentation for varying audiences
Ability to work independently while managing multiple objectives and timelines
Desire to work in a fast-paced environment with potential for high impact in a small team"""

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
output_resume_md = response.choices[0].message.content


# Write original and tailored resume to html 
# TODO remove the ChatGPT response not part of resume
inout_resume_html = markdown.markdown(input_resume)
with open("original_resume.html", "w") as f:
    f.write(inout_resume_html)


output_resume_html = markdown.markdown(output_resume_md)

with open("tailored_resume.html", "w") as f:
    f.write(output_resume_html)


# TODO: get PDF coversion to work. Missing dependency, no longer supported?

# import pdfkit

# # Convert an HTML file to PDF
# pdfkit.from_file("output.html", "output.pdf")


