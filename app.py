!pip -q install google-genai gradio gtts pillow
import gradio as gr
from google import genai
from google.genai import types
from gtts import gTTS
import tempfile

client = genai.Client(
    api_key="AQ.Ab8RN6IEF6KXhqVcG0xDN0_0b0Efsq_RDwGRMNtQalsm3zgZpA"
)

def extract_text(file):
  if file is None:
    return "Please upload a file first.", None

  uploaded_file_ref = client.files.upload(file=file.name)
  response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=[uploaded_file_ref, "Extract all text excatly as written."]
  )
  return response.text, None
def summarize(file):
  if file is None:
    return "Please upload a file first,", None

    uploaded_file_ref = client.files.upload(file=file.name)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[uploaded_file_ref,"Summarize this document in simple language."]
    )

    return response.text, None

def answer_question(file, question):
  if file is None:
    return "Please upload a file first,", None
  if not question.strip():
    return "Please enter a question.", None

  uploaded_file_ref = client.files.upload(file=file.name)
  response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=[
          uploaded_file_ref,
          f"Answer the following question using ONLY this document.\n\n"
      ]
  )
  return response.text, None

def audio_summary(file):
  if file is None:
    return "Please upload a file first.", None

  uploaded_file_ref = client.files.upload(file=file.name)
  response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=[uploaded_file_ref, "Summarize this document in simple language."]
  )
  summmary = response.text

  audio_file = tempfile.NamedTemporaryFile(
      suffix = ".mp3",
      delete = False
  ).name

  gTTS(summmary).save(audio_file)

  return summmary,audio_file

with gr.Blocks() as demo:
  gr.Markdown("# Gemini Document Analyzer")

  with gr.Row():
    with gr.Column(scale=1):
      file = gr.File(label = "Upload PDF/Image")

    with gr.Column(scale = 2):
      gr.Markdown("### Choose an Action")

      with gr.Row():
        btn_extract = gr.Button("Extract Text", variant = "Secondary")
        btn_summarize = gr.Button("Summarize", variant = "Secondary")
        btn_audio = gr.Button("Generate Audio Summary", variant = "Secondary")

      gr.Markdown("---")
      gr.Markdown("### Document Q & A")
      question = gr.Textbox(
          label = "Ask a specific question from the document",
          placeholder = "Type your question here...")
      btn_answer = gr.Button("Answer", variant = "Primary")

  gr.Markdown("---")
  gr.Markdown("### Outputs")

  with gr.Row():
    output = gr.Textbox(label = "Text Output", lines = 12, scale = 2)
    audio = gr.Audio(label = "Audio Output", scale = 1)

  btn_extract.click(
      fn = extract_text,
      inputs = [file],
      outputs = [output, audio]
  )

  btn_summarize.click(
      fn = summarize,
      inputs = [file],
      outputs = [output, audio]
  )

  btn_audio.click(
      fn = audio_summary,
      inputs = [file],
      outputs = [output, audio]
  )


  btn_answer.click(
      fn = answer_question,
      inputs = [file, question],
      outputs = [output, audio]
  )


demo.launch(debug = True)
