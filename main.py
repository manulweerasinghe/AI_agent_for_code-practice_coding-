import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from functions.call_function import available_functions
from functions.call_function import call_function

def model_generate_content(client, messages):
    generate_content = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = messages,
            config = types.GenerateContentConfig(
                tools = [available_functions],
                system_instruction = system_prompt),
            )
    return generate_content
    
def main():
    # CLI argument
    parser = argparse.ArgumentParser(description = "Chatbot")
    parser.add_argument("user_prompt", type = str, help = "User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    #set messages
    messages = [types.Content(role="user", parts=[genai.types.Part(text = args.user_prompt)])]

    #get api key
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("The api key not found")

    #setup client and send request
    client = genai.Client(api_key = api_key)
    for i in range(20):
        generate_content = model_generate_content(client, messages)
        if generate_content.candidates:
            for msg in generate_content.candidates:
                messages.append(msg.content)

        #count token usage
        usage_metadata = generate_content.usage_metadata
        function_calls = generate_content.function_calls
        if not usage_metadata:
            raise RuntimeError("Failed API request")
        prompt_token_count = usage_metadata.prompt_token_count
        response_token_count = usage_metadata.candidates_token_count
        if not function_calls:
            if args.verbose:
                print("User prompt: ", generate_content.text)
                print("Prompt tokens: ", prompt_token_count)
                print("Response tokens: ", response_token_count)
            else:
                print("Final Result:")
                print(generate_content.text)
            break
        else:
            function_result_list = []
            for function_call in function_calls:
                #print(f"Calling function: {function_call.name}({function_call.args})")
                function_call_result = call_function(function_call, args.verbose)
                if function_call_result.parts == []:
                    raise RuntimeError("Empty parts list from called function") 
                if not function_call_result.parts[0].function_response:
                    raise RuntimeError("Empty parts list [0].function_response from called function")
                if not function_call_result.parts[0].function_response.response:
                    raise RuntimeError("Empty parts list [0].function_response.response from called function")
                function_result_list.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

                messages.append(types.Content(role = "user", parts = function_result_list))
        if i == 19:
            sys.exit(1)

if __name__ == "__main__":
    main()
