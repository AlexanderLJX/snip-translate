# translation.py
import requests
import json

def get_gpt_translation(input, length="medium", timeout=7):
    url = "https://free.churchless.tech/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload_short = {
        "messages": [
            {
                "role": "user",
                "content": "translate the following to English:\"さっきからこいつの思考が全く読めない\" \n Reply with only the translation, do not add any additional words or explanations."
            },
            {
                "role": "assistant",
                "content": "I haven't been able to read this person's thoughts at all since a while ago."
            },
            {
                "role": "user",
                "content": "translate the following to English:\"球磨川が目の前にいるってのに！どうしてブルってんだよ俺の身体！！\" \n Reply with only the translation, do not add any additional words or explanations."
            },
            {
                "role": "assistant",
                "content": "Even though Kumagawa is right in front of me! Why is my body trembling?!"
            },
            {
                "role": "user",
                "content": "translate the following to English:\"これは僕が己の過ちに対して支払った代償であり\" \n Reply with only the translation, do not add any additional words or explanations."
            },
            {
                "role": "assistant",
                "content": "This is the price I paid for my own mistakes."
            },
            {
                "role": "user",
                "content": "translate the following to English:\"" + input + "\" \n Reply with only the translation, do not add any additional words or explanations."
            }
        ],
        "model": "gpt-3.5-turbo",
        "temperature": 1,
        "presence_penalty": 0,
        "top_p": 1,
        "frequency_penalty": 0,
        "stream": True
    }
    payload_medium = {
        "messages": [
            {
                "role": "user",
                "content": "translate the following to English:\"さっきからこいつの思考が全く読めない\" \n Reply with only the translation, followed by a full explanation starting with \"Full explanation:\"."
            },
            {
                "role": "assistant",
                "content": "I haven't been able to read this person's thoughts at all since a while ago. \nFull explanation: The speaker is expressing their inability to understand or predict what someone else is thinking."
            },
            {
                "role": "user",
                "content": "translate the following to English:\"球磨川が目の前にいるってのに！どうしてブルってんだよ俺の身体！！\" \n Reply with only the translation, followed by a full explanation starting with \"Full explanation:\"."
            },
            {
                "role": "assistant",
                "content": "Even though Kumagawa is right in front of me! Why is my body trembling?! \nFull explanation: The speaker is expressing their surprise and frustration about their body trembling despite being in the presence of Kumagawa."
            },
            {
                "role": "user",
                "content": "translate the following to English:\"これは僕が己の過ちに対して支払った代償であり\" \n Reply with only the translation, followed by a full explanation starting with \"Full explanation:\"."
            },
            {
                "role": "assistant",
                "content": "This is the price I paid for my own mistakes. \nFull explanation: The speaker is acknowledging that the situation they are facing is a consequence or payment they have to bear for their own errors or wrongdoings. It suggests a sense of personal accountability and responsibility for the negative outcome they are experiencing."
            },
            {
                "role": "user",
                "content": "translate the following to English:\"" + input + "\" \n Reply with only the translation, followed by a full explanation starting with \"Full explanation:\"."
            }
        ],
        "model": "gpt-3.5-turbo",
        "temperature": 1,
        "presence_penalty": 0,
        "top_p": 1,
        "frequency_penalty": 0,
        "stream": True
    }

    payload_long = {
        "messages": [
            {
                "role": "user",
                "content": "translate the following to English:\"さっきからこいつの思考が全く読めない\" \n Reply with only the translation, followed by a full in depth explanation starting with \"Full explanation:\"."
            },
            {
                "role": "assistant",
                "content": """I haven't been able to read this person's thoughts at all since a while ago. \nFull explanation: 
1. さっきから (sakki kara): "since a while ago" or "for some time now"
2. こいつ (koitsu): "this guy" or "this person" (informal and somewhat rude)
3. の (no): possessive particle, similar to "'s" or "of" in English
4. 思考 (shikō): "thought" or "thinking"
5. が (ga): subject particle
6. 全く (mattaku): "completely" or "entirely"
7. 読めない (yomenai): negative potential form of the verb 読む (yomu, "to read"), meaning "can't read"
The speaker is expressing their inability to understand or predict what the other person is thinking."""
            },
            # {
            #     "role": "user",
            #     "content": "translate the following to English:\"球磨川が目の前にいるってのに！どうしてブルってんだよ俺の身体！！\" \n Reply with only the translation, followed by a full in depth explanation starting with \"Full explanation:\"."
            # },
            # {
            #     "role": "assistant",
            #     "content": "Even though Kumagawa is right in front of me! Why is my body trembling?! \nFull explanation: The speaker is expressing their surprise and frustration about their body trembling despite being in the presence of Kumagawa."
            # },
            {
                "role": "user",
                "content": "translate the following to English:\"これは僕が己の過ちに対して支払った代償であり\" \n Reply with only the translation, followed by a full in depth explanation starting with \"Full explanation:\"."
            },
            {
                "role": "assistant",
                "content": """This is the price I paid for my own mistakes. \nFull explanation: 
1. これは (Kore wa): This means "this is" and is used to refer to something that has been mentioned or is being discussed.
2. 僕が (boku ga): "僕" (boku) is a first-person pronoun meaning "I" or "me," and "が" (ga) is a subject marker. Together, they mean "I" as the subject of the sentence.
3. 己の過ちに対して (onore no ayamachi ni taishite): "己" (onore) is a pronoun meaning "oneself" or "myself." "過ち" (ayamachi) means "mistake" or "error." "に対して" (ni taishite) is a preposition meaning "toward" or "in relation to." So, this phrase means "toward my own mistakes."
4. 支払った代償であり (shiharatta daishou de ari): "支払った" (shiharatta) is the past tense of the verb "支払う" (shiharau), which means "to pay" or "to compensate." "代償" (daishou) means "price" or "compensation." "であり" (de ari) is a formal way to say "is" or "to be." This phrase means "the price I paid."
The speaker is acknowledging that the situation they are facing is a consequence or payment they have to bear for their own errors or wrongdoings. It suggests a sense of personal accountability and responsibility for the negative outcome they are experiencing."""
            },
            {
                "role": "user",
                "content": "translate the following to English:\"" + input + "\" \n Reply with only the translation, followed by a full in depth explanation starting with \"Full explanation:\"."
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
        if length == "short":
            response = requests.post(url, data=json.dumps(payload_short), headers=headers, timeout=timeout)
            response.raise_for_status()
        elif length == "medium":
            response = requests.post(url, data=json.dumps(payload_medium), headers=headers, timeout=timeout)
            response.raise_for_status()
        elif length == "long":
            response = requests.post(url, data=json.dumps(payload_long), headers=headers, timeout=timeout)
            response.raise_for_status()
        else:
            return "Invalid length. Please choose a valid length."

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
