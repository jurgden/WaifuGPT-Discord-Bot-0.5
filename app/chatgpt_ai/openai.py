from dotenv import load_dotenv
import openai
import os


load_dotenv()
openai.api_key = os.getenv('OPENAI_KEY')



def chatgpt_response(prompt, context):
  context_prompt = ""
  if context:
    context_prompt = "\n".join([f"{k}: {v}"
                                for k, v in context.items()]) + "\n\n"

  response = openai.Completion.create(model="text-davinci-003",
                                      prompt=context_prompt + prompt,
                                      temperature=.70,
                                      max_tokens=3000)
  response_dict = response.get("choices")
  if response_dict and len(response_dict) > 0:
    prompt_reponse = response_dict[0]["text"]
  return prompt_reponse
