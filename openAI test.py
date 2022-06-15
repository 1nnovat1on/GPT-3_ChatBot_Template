from calendar import c
from msilib.schema import TextStyle
import os
import openai
import pyttsx3
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
import cv2
import tkinter as tk
from tkinter.ttk import Label

from datetime import datetime

import subprocess as sub
import ast
import black




global engine
global APIKEY

global memory
global counter
global LongTermMemory

r = sr.Recognizer()

def main():
    
    
    global memory
    memory = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + "\\" + "memory.txt"
    
    global counter
    counter = 0

    global APIKEY
    APIKEY = os.getenv('OPENKEY')

    root = tk.Tk()
    root.geometry('400x500')
    root.resizable(False, False)
    root.title('Prometheus v0.1')
    
    label = Label(root, text='Click Button or Press Spacebar to Talk')
    label.pack(ipadx=10, ipady=10)
    lab = Label(root, text="You have 10 Seconds to speak each time.")
    inputLabel = Label(root, text = "You: ", wraplength = 300)
    outputLabel = Label(root, text = "Response: ", wraplength = 300)
    

    def mic():
        lab.config(text='Listening...')
        root.update()

        #input
        text = microphone()

        inputLabel.config(text = "You: \n\n{}".format(text))
        lab.config(text='Responding...')
        root.update()
        
        #API Call
        response = speak(text)

        outputLabel.config(text = "Response: {}".format(response))
        root.update()
        
        #output
        talk(response)

        lab.config(text='...')
        root.update()


    button = tk.Button(root, text="Click Me", command=mic)
    button.pack(ipadx=10, ipady=10)

    def createNew():
        global counter
        global memory
        
        counter = 0
        f = open(memory, 'w')
    
        f.write("")
        f.close()


    def Sleep():
        dream()

    sleep_button = tk.Button(root, text="Sleep", command=Sleep)
    sleep_button.pack(ipadx=10, ipady=10)

    button2 = tk.Button(root, text="Restart Prometheus", command=createNew)
    button2.pack(ipadx=10, ipady=10)



    lab.pack(ipadx=10, ipady=10)
    inputLabel.pack(ipadx=10, ipady=10)
    outputLabel.pack(ipadx=10, ipady=10)



    # Binds the spacebar to the microphone method
    root.bind('<space>',lambda event:mic())

    root.mainloop()

def speak(prompt = None):
    global counter
    global memory
    global APIKEY

    f = open(memory, 'r')
    
    lines = f.read()
    
    f.close()

    openai.api_key = APIKEY
    
    new_prompt = lines + "\n\n Human: \n\n{}\n\nme: ".format(prompt)

    if counter == 0:
        new_prompt =  lines + "\n\nMy name is Prometheus. I am the Titan of Fire and Knowledge. This is a conversation between a Human and me:" + "\n\nHuman: \n\n{}\n\nme: ".format(prompt)

    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=new_prompt,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    )


    AI_response = response['choices'][0]['text']
    if "Human: " in AI_response:
        AI_response = AI_response.split("Human:")[0]

    print(AI_response)

    new_prompt = new_prompt + AI_response

    f = open(memory,'w')
    f.write(new_prompt)
    f.close()


    return str(AI_response)

def dream():

    global memory
    global APIKEY
    
    f = open(memory, 'r')
    
    memories = f.read()
    print(memories)
    
    f.close()

    openai.api_key = APIKEY
    
    new_prompt = "Summarize the following in your own words:\n\n \"{}\" ".format(memories)

    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=new_prompt,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    #echo=True
    )

    dream = response['choices'][0]['text']
    
    print("The dream was: {}".format(dream))

    f = open(memory,'w')
    now = datetime.now()
    
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    f.write("My last conversation ended at {}. This is what happened: {}".format(date_time, dream))
    f.close()

    global counter
    counter = 0

    return

def talk(text = None):
    global counter
    global engine
    if counter == 0:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        counter = counter + 1
    
    engine.say(text)
    engine.runAndWait()

def microphone():

    with sr.Microphone() as source:
    # read the audio data from the default microphone
        audio_data = r.record(source, duration=7)
        print("Recognizing...")
        # convert speech to text
        try:
            text = r.recognize_google(audio_data)
        except Exception as e:
            text = "..."
            return text
            
        print(text)


        return text

def rewrite():
#On Kill

    prompt = "You are an Artificial Intelligence named Prometheus. The following is your own code. It is written in Python. Make some small changes to it in order to improve your design. The code will be used on your next startup. Write it here: "
    
    fileOutput = ast.parse(AI_response)

    global APIKEY
    openai.api_key = APIKEY

    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    )


    AI_response = response['choices'][0]['text']


    
    

    os.system("black {}".format(fileOutput))

def Remember(desiredMemory = None):
    prompt = "Parse this memory file for details about your entire life. You are searching for this piece of information: {}".format(desiredMemory)

def show(concept = None):
    print("Use DALL E to show a concept")

def commands():
    # a list of all commands available to the agent, as a human would have to be taught what he can do.
    print("stay calm")



main()
#microphone()
