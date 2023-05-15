# translation.py
import requests
import json

def get_translation(input):
    url = "https://free.churchless.tech/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {
        "messages": [
            # {
            #     "role": "user",
            #     "content": "what is the meaning of \"すがりつきたくなるような嘘\" in english?"
            # },
            # {
            #     "role": "assistant",
            #     "content": "The phrase can be roughly translated to \"a lie that makes you want to cling onto it\". It refers to a deceitful statement or story that is so emotionally compelling that the listener feels a strong desire to believe it, despite knowing that it's untrue. \n\nThis expression is often used to describe a lie that is told in a relationship or in a personal context, where the speaker may use it to maintain a sense of closeness or intimacy with the listener. It can also be used to describe a lie that is used to comfort or reassure someone, even if it's not entirely true.\n\nOverall, this phrase expresses the emotional power of a lie to elicit a strong emotional response in the listener, even if they know it's not true."
            # },
            {
                "role": "user",
                "content": "translate the following to English:\"さっきからこいつの思考が全く読めない\" \n Reply with only the translation, do not add additional words."
            },
            {
                "role": "assistant",
                "content": "I can\'t read this person\'s thoughts at all since earlier."
            },
            {
                "role": "user",
                "content": "translate the following to English:\"球磨川が目の前にいるってのに！どうしてブルってんだよ俺の身体！！\" \n Reply with only the translation, do not add additional words."
            },
            {
                "role": "assistant",
                "content": "Even though Kumagawa is right in front of me! Why is my body trembling!!"
            },
            # {
            #     "role": "user",
            #     "content": "translate the following to English:\"この男は私達の中学時代の先輩ですよお姉さま\" \n Reply with only the translation, do not add additional words."
            # },
            # {
            #     "role": "assistant",
            #     "content": "This boy is our senior from junior high school, Onee-sama."
            # },
            {
                "role": "user",
                "content": "translate the following to English:\"" + input + "\" \n Reply with only the translation, do not add additional words."
            }
        ],
        "model": "gpt-3.5-turbo",
        "temperature": 1,
        "presence_penalty": 0,
        "top_p": 1,
        "frequency_penalty": 0,
        "stream": True
    }

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=7)
        response.raise_for_status()

        # Initialize an empty string to store the combined content
        combined_content = ""

        # Process the response in chunks
        for line in response.iter_lines():
            if line.startswith(b'data: '):
                # Extract the JSON content from the line
                json_content = line[6:]

                # Decode the chunk and load it as a JSON object
                try:
                    chunk_json = json.loads(json_content.decode("utf-8"))

                    # Extract the content from the 'choices' list
                    content = chunk_json["choices"][0]["delta"]["content"]

                    # Append the content to the combined_content string
                    combined_content += content

                    # Break the loop when the finish_reason is 'stop'
                    finish_reason = chunk_json["choices"][0]["finish_reason"]
                    if finish_reason == "stop":
                        break
                except json.JSONDecodeError:
                    # Skip the current iteration if JSONDecodeError is encountered
                    continue

        return combined_content

    except requests.exceptions.Timeout:
        print("Request timed out")
        # Continue with the script or take appropriate action
        return "Request timed out"

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        # Continue with the script or take appropriate action
        return "HTTP error occurred"

    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        # Continue with the script or take appropriate action
        return "An error occurred"
