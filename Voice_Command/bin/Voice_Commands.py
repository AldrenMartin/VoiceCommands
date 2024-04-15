'''
For Version 1 and 2 of the code
import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
import pyttsx3
import datetime
import os.path
'''
import os
import time
import playsound
from gtts import gTTS
import datetime
import os.path
import sched
from datetime import datetime, timedelta
from plyer import notification
import speech_recognition as sr
'''
First code: Just Audio 

def speak(text): 
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)  # Remove the temporary audio file after playing


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        
        try: 
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print ("Exception: " + str(e))
            
    return said

text = get_audio()


speak("Hello World")

if "hello" in text:
    speak("hello, how may I assist you.")



if "what is your name" in text:
    speak ("I am here to assist you")

'''

'''
Second Version of the Code: Audio + Add Event
class EventScheduler:
    def __init__(self):
        self.events = []

    def add_event(self, name, date, time):
        self.events.append({'name': name, 'date': date, 'time': time})
        print(f"Event '{name}' added on {date} at {time}")

    def edit_event(self, index, name, date, time):
        if 0 <= index < len(self.events):
            self.events[index] = {'name': name, 'date': date, 'time': time}
            print(f"Event at index {index} edited: '{name}' on {date} at {time}")
        else:
            print("Invalid index")

    def view_events(self):
        if self.events:
            print("Events:")
            for i, event in enumerate(self.events):
                print(f"{i}: {event['name']} on {event['date']} at {event['time']}")
        else:
            print("No events")

    def delete_event(self, index):
        if 0 <= index < len(self.events):
            deleted_event = self.events.pop(index)
            print(f"Event at index {index} deleted: '{deleted_event['name']}' on {deleted_event['date']} at {deleted_event['time']}")
        else:
            print("Invalid index")


def speak(text): 
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)  # Remove the temporary audio file after playing


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = r.listen(source)
        
    try: 
        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except Exception as e:
        print("Exception:", str(e))
        return ""


scheduler = EventScheduler()

while True:
    command = get_audio()
    if "add event" in command:
        speak("What's the name of the event?")
        event_name = get_audio()
        speak("On which date?")
        event_date = get_audio()
        speak("At what time?")
        event_time = get_audio()
        scheduler.add_event(event_name, event_date, event_time)
    elif "edit event" in command:
        speak("Please specify the index of the event you want to edit.")
        event_index = int(get_audio())
        speak("What's the new name of the event?")
        event_name = get_audio()
        speak("On which date?")
        event_date = get_audio()
        speak("At what time?")
        event_time = get_audio()
        scheduler.edit_event(event_index, event_name, event_date, event_time)
    elif "view events" in command:
        scheduler.view_events()
    elif "delete event" in command:
        speak("Please specify the index of the event you want to delete.")
        event_index = int(get_audio())
        scheduler.delete_event(event_index)
        '''
        
#Version 3; Audio + Events + Notification. To use with no interface

class EventScheduler:
    def __init__(self):
        self.events = []
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def add_event(self, name, date, time):
        self.events.append({'name': name, 'date': date, 'time': time})
        print(f"Event '{name}' added on {date} at {time}")
        # Schedule reminders for the added event
        event_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        self.set_reminders(name, event_datetime)

    def edit_event(self, index, name, date, time):
        if 0 <= index < len(self.events):
            self.events[index] = {'name': name, 'date': date, 'time': time}
            print(f"Event at index {index} edited: '{name}' on {date} at {time}")
            # Reschedule reminders for the edited event
            event_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            self.set_reminders(name, event_datetime)
        else:
            print("Invalid index")

    def view_events(self):
        if self.events:
            print("Events:")
            for i, event in enumerate(self.events):
                print(f"{i}: {event['name']} on {event['date']} at {event['time']}")
        else:
            print("No events")

    def delete_event(self, index):
        if 0 <= index < len(self.events):
            deleted_event = self.events.pop(index)
            print(f"Event at index {index} deleted: '{deleted_event['name']}' on {deleted_event['date']} at {deleted_event['time']}")
        else:
            print("Invalid index")

    def set_reminders(self, event_name, event_datetime):
        """ Set multiple reminders for an event. """
        reminders = [15, 60, 120]  # Reminders in minutes before the event
        for reminder_delta in reminders:
            reminder_time = event_datetime - timedelta(minutes=reminder_delta)
            self.schedule_notification(f"Reminder for {event_name}", reminder_time)

    def schedule_notification(self, event_name, event_time):
        """ Schedule a notification for the event. """
        self.scheduler.enterabs(event_time.timestamp(), 1, self.notify, argument=(event_name,))
        self.scheduler.run()

    def notify(self, event_name):
        """ Send a desktop notification about the event. """
        notification.notify(
            title='Event Reminder',
            message=f'Remember your event: {event_name}',
            app_icon=None,  # Path to an .ico file can be added here
            timeout=10,  # Notification duration in seconds
        )


def speak(text): 
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)  # Remove the temporary audio file after playing


def manual_input(prompt):
    return input(prompt)


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = r.listen(source)
        
    try: 
        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except Exception as e:
        print("Exception:", str(e))
        return ""


scheduler = EventScheduler()

while True:
    print("1. Add Event")
    print("2. Edit Event")
    print("3. View Events")
    print("4. Delete Event")
    print("5. Voice Command")
    print("6. Stop")

    choice = manual_input("Select an option: ")

    if choice == "1":
        event_name = manual_input("Enter event name: ")
        event_date = manual_input("Enter event date (YYYY-MM-DD): ")
        event_time = manual_input("Enter event time (HH:MM): ")
        scheduler.add_event(event_name, event_date, event_time)
    elif choice == "2":
        # Implement edit event functionality
        pass
    elif choice == "3":
        scheduler.view_events()
    elif choice == "4":
        # Implement delete event functionality
        pass
    elif choice == "5":
        # Voice command functionality
        command = get_audio()
        if "add event" in command:
            speak("What's the name of the event?")
            event_name = get_audio()
            speak("On which date?")
            event_date = get_audio()
            speak("At what time?")
            event_time = get_audio()
            scheduler.add_event(event_name, event_date, event_time)
        elif "edit event" in command:
            # Implement edit event functionality
            pass
        elif "view events" in command:
            scheduler.view_events()
        elif "delete event" in command:
            # Implement delete event functionality
            pass
        elif "stop" in command:
            break
    elif choice == "6":
        break
