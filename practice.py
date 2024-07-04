import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import cv2
import numpy as np

# Initialize recognizer and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command(command_label):
    command = ""
    try:
        with sr.Microphone() as source:
            print('Listening...')
            command_label.config(text="Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
                command_label.config(text=command)
    except:
        pass
    return command

def get_user_input():
    return simpledialog.askstring("Input", "I didn't catch that. Please type your command:")

def run_alexa(command_label):
    command = take_command(command_label)
    if not command:
        command = get_user_input()

    print(command)
    response = ""
    if 'play' in command:
        song = command.replace('play', '')
        response = 'Playing ' + song
        talk(response)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M:%S %p')
        response = 'Current time is ' + time
        talk(response)
    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person, 1)
        response = info
        talk(info)
    elif 'who is our python sir' in command:
        response = 'Mr. Gagandeep is our mentor'
        talk(response)
    elif 'date' in command:
        response = 'Sorry, I have a headache'
        talk(response)
    elif 'are you single' in command:
        response = 'Yes, but I am ready to mingle'
        talk(response)
    elif 'jokes' in command:
        response = pyjokes.get_joke()
        talk(response)
    elif 'where are you from' in command:
        response = 'From the bottom of your heart'
        talk(response)
    elif 'what is your age' in command:
        response = "Don't ask age from girls and salary from boys"
        talk(response)
    else:
        response = 'Please say it again.'
        talk(response)
    command_label.config(text=response)
    show_feedback(response)

def on_button_click(command_label):
    run_alexa(command_label)

# Set up OpenCV window for visual feedback
def show_feedback(response):
    feedback_img = np.zeros((300, 800, 3), dtype=np.uint8)
    cv2.putText(feedback_img, response, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("Voice Assistant Feedback", feedback_img)
    cv2.waitKey(1000)  # Display the feedback for 1 second

window = tk.Tk()
window.title('Voice Assistant')
window.geometry('1000x600')

# Add an attractive background image
background_image_path = r"C:\Users\ASUS\Downloads\new_background.jpeg"  # Replace with your image path
background_image = Image.open(background_image_path)
background_image = background_image.resize((1000, 600), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

command_label = tk.Label(window, text='', wraplength=350, bg='white', font=('Helvetica', 12))
command_label.pack(pady=20)

start_button = tk.Button(window, text='Start Voice Assistant', bg='blue', fg='white', font=('Helvetica', 14, 'bold'), command=lambda: on_button_click(command_label))
start_button.pack()

window.mainloop()
cv2.destroyAllWindows()
