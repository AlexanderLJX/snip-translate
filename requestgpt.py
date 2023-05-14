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

    response = requests.post(url, data=json.dumps(payload), headers=headers)

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
