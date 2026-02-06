import argparse
import os
from dotenv import load_dotenv
from google import genai

# CLI argument
parser = argparse.ArgumentParser(description = "Chatbot")
parser.add_argument("user_prompt", type = str, help = "User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

#set messages
messages = [genai.types.Content(role="user", parts=[genai.types.Part(text = args.user_prompt)])]

#get api key
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("The api key not found")

#setup client and send request
client = genai.Client(api_key = api_key)
generate_content = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = messages
        )

#count token usage
usage_metadata = generate_content.usage_metadata
if usage_metadata == None:
    raise RuntimeError("Failed API request")
prompt_token_count = usage_metadata.prompt_token_count
response_token_count = usage_metadata.candidates_token_count
if args.verbose:
    print("User prompt: ", generate_content.text)
    print("Prompt tokens: ", prompt_token_count)
    print("Response tokens: ", response_token_count)
else:
    print(generate_content.text)
