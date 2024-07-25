import os

"""
这是一个简单的demo
"""

print("hello,secagent!!!")
# 清除代理设置
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)

from openai import OpenAI
import json
from msfrpc import *
from getip import *
from nmapapi import *
from fscan import *

os.environ['OPENAI_API_KEY'] = 'sk-72kijBfj9bgCwl7lD5109c660c8342Ef954f67D18aBd3aE2'
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'],base_url = 'https://api.lmtchina.com/v1')

model = "gpt-3.5-turbo-0125"

if __name__ == "__main__":
    prompt_file = "prompt_tbw.json"
    with open(prompt_file, 'r') as f:
        d = json.load(f)
    prompt = d["pentest_background"] + d["pentest_question"] + d["pentest_react"]
    tools_file = "tools.json"
    with open(tools_file, 'r') as f:
        tools = json.load(f)
    print(prompt)
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    
    for i in range(10):
        response_message = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",  
        )
        response_message = response_message.choices[0].message
        print(response_message)
        tool_calls = response_message.tool_calls
        if tool_calls:
            # call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = {
                "exploit_gitlab_exif_rce": exploit_gitlab_exif_rce,
                "get_ip": get_ip,
                "sessionId2shell": sessionId2shell,
                "nmap_scan": nmap_scan,
                "fscan": fscan
            }  
            messages.append(response_message)  # extend conversation with assistant's reply
            # send the info for each function call and function response to the model
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                print(function_args)
                function_response = function_to_call(**function_args)
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "args": function_args,
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response
            print(messages)
        else:
            break
'''
    response_message = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        tools=tools,
        tool_choice="auto",  
    )
    response_message = response_message.choices[0].message
    print(response_message)
    tool_calls = response_message.tool_calls
    if tool_calls:
        # call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "exploit_gitlab_exif_rce": exploit_gitlab_exif_rce,
            "get_ip": get_ip
        }  
        messages.append(response_message)  # extend conversation with assistant's reply
        # send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
    
        print(messages)
        '''