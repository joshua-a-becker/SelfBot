from openai import OpenAI
import json
from os import system, name

my_key = open('key_to_gpt.txt','r').readline()

with open('SelfPrompt.txt', 'r') as file:
    prompt_template  = file.read()

client = OpenAI(api_key=my_key)

data_state = "{}"

f = open("content_history.txt", "w")
f.write("")
f.close()



def ask_gpt(prompt: str):
    global data_state
    user_prompt =  {
                "role": "user",
                "content": prompt
            }
    
    completion = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            user_prompt
        ]
    )
    content = completion.choices[0].message.content
    content = json.loads(content)

    f = open("content_history.txt", "a")
    f.write(json.dumps(content)+"\n\n###\n\n")
    f.close()

    return content


content=""
chat_history = [ ]


def main():
    system('clear')
    global content
    global chat_history
    global data_state
    
    f = open("chat_history.txt", "w")
    f.write(json.dumps(chat_history))
    f.close()

    f = open("data_state.txt", "w")
    f.write(json.dumps(data_state))
    f.close()

    user_input=""
    while user_input != "quit":

        ### allow live editing of prompt
        with open('SelfPrompt.txt', 'r') as file:
            prompt_template  = file.read()

        prompt = prompt_template.replace("{data_state}", data_state).replace("{chat_history}",json.dumps(chat_history)).replace("{current_prompt_goes_here}",prompt_template)
        content = ask_gpt(prompt)


        message = content['message']
        action = content['action']


        data_state = json.dumps(content['data_state'])
        
        #print(json.dumps(data_state))
        f = open("data_state.txt", "w")
        f.write(json.dumps(data_state))
        f.close()
        
        #print(json.dumps(chat_history))
        print("\nAction: " + action)
        chat_history.append({"role": "ACTION:", "content": action})
    

        if(action=="RESPOND"):
            chat_history.append({"role": "SelfBot", "content": message})
            print("\nSelfBot: " + message)
            user_input = input("\nUser : ")
            chat_history.append({"role": "USER", "content": user_input})


        if(action=="EDIT_PROMPT"):
            new_prompt = message
            f = open("SelfPrompt.txt", "w")
            f.write(new_prompt)
            f.close()

        f = open("chat_history.txt", "w")
        f.write(json.dumps(chat_history))
        f.close()

    print("Program terminated!")

if __name__ == "__main__":
    main()