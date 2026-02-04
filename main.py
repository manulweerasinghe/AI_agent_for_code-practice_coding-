import argparse
import os
from dotenv import load_dotenv
from google import genai

parser = argparse.ArgumentParser(description = "Chatbot")
parser.add_argument("user_prompt", type = str, help = "User prompt")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("The api key not found")

client = genai.Client(api_key = api_key)
generate_content = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = args.user_prompt
        )
usage_metadata = generate_content.usage_metadata
if usage_metadata == None:
    raise RuntimeError("Failed API request")
prompt_token_count = usage_metadata.prompt_token_count
response_token_count = usage_metadata.candidates_token_count
print("Prompt tokens: ", prompt_token_count)
print("Response tokens: ", response_token_count)
print(generate_content.text)
