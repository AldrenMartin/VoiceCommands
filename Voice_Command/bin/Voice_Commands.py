import os
import sys
import time
import playsound
from gtts import gTTS
import datetime
import sched
from datetime import datetime, timedelta
import speech_recognition as sr
from plyer import notification

# Define a class to manage events and reminders
class EventScheduler:
    def __init__(self):
        # Initialize empty list to store events
        self.events = []
        # Initialize scheduler for scheduling reminders
        self.scheduler = sched.scheduler(time.time, time.sleep)

    # Method to add a new event
    def add_event(self, name, date, time):
        # Add the event to the list of events
        self.events.append({'name': name, 'date': date, 'time': time})
        print(f"Event '{name}' added on {date} at {time}")
        # Schedule reminders for the added event
        event_datetime = datetime.strptime(f"{date} {time}", "%Y %m/%d %H:%M")  # Updated format here
        self.set_reminders(name, event_datetime)

    # Method to edit an existing event
    def edit_event(self, index, name, date, time):
        if 0 <= index < len(self.events):
            # Update the event at the specified index
            self.events[index] = {'name': name, 'date': date, 'time': time}
            print(f"Event at index {index} edited: '{name}' on {date} at {time}")
            # Reschedule reminders for the edited event
            event_datetime = datetime.strptime(f"{date} {time}", "%Y %m/%d %H:%M")  # Updated format here
            self.set_reminders(name, event_datetime)
        else:
            print("Invalid index")

    # Method to view all events
    def view_events(self):
        if self.events:
            print("Events:")
            for i, event in enumerate(self.events):
                print(f"{i}: {event['name']} on {event['date']} at {event['time']}")
        else:
            print("No events")

    # Method to delete an event
    def delete_event(self, index):
        if 0 <= index < len(self.events):
            # Remove the event at the specified index
            deleted_event = self.events.pop(index)
            print(
                f"Event at index {index} deleted: '{deleted_event['name']}' on {deleted_event['date']} at {deleted_event['time']}")
        else:
            print("Invalid index")

    # Method to set reminders for an event
    def set_reminders(self, event_name, event_datetime):
        """ Set multiple reminders for an event. """
        reminders = [15, 60, 120]  # Reminders in minutes before the event
        for reminder_delta in reminders:
            # Calculate reminder time
            reminder_time = event_datetime - timedelta(minutes=reminder_delta)
            # Schedule notification for the reminder
            self.schedule_notification(f"Reminder for {event_name}", reminder_time)

    # Method to schedule a notification
    def schedule_notification(self, event_name, event_time):
        """ Schedule a notification for the event. """
        # Schedule notification using the scheduler
        self.scheduler.enterabs(event_time.timestamp(), 1, self.notify, argument=(event_name,))
        # Run the scheduler
        self.scheduler.run()

    # Method to send a notification
    def notify(self, event_name):
        """ Send a desktop notification about the event. """
        # Use plyer to send desktop notification
        notification.notify(
            title='Event Reminder',
            message=f'Remember your event: {event_name}',
            app_icon=None,  # Path to an .ico file can be added here
            timeout=10,  # Notification duration in seconds
        )

# Function to convert text to speech and play it
def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)  # Remove the temporary audio file after playing

# Function to get user input manually
def manual_input(prompt):
    return input(prompt)

# Function to get audio input using microphone and speech recognition
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return ""

# Function to validate date format
def validate_date(date_str):
    formats = ["%Y %m/%d", "%Y-%m-%d", "%Y %m/%d %H:%M", "%Y %m/%dth", "%Y-%m-%dth", "%Y %m/%d %H:%Mth" ]  # Add more formats as needed
    for fmt in formats:
        try:
            datetime.strptime(date_str, fmt)
            return True
        except ValueError:
            pass
    return False

# Function to validate time format
def validate_time(time_str):
    try:
        time.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

# Main function to run the program
def main():
    scheduler = EventScheduler()

    while True:
        # Display menu options
        print("1. Add Event")
        print("2. Edit Event")
        print("3. View Events")
        print("4. Delete Event")
        print("5. Voice Command")
        print("6. Stop")

        # Get user choice
        choice = manual_input("Select an option: ")

        if choice == "1":
            try:
                # Get event details from user
                event_name = manual_input("Enter event name: ")
                event_date = manual_input("Enter event date (YYYY MM/DD): ")
                event_time = manual_input("Enter event time (HH MM): ")
                # Add event to scheduler
                scheduler.add_event(event_name, event_date, event_time)
                print("Event added successfully")

            except ValueError:
                print("Invalid input. Please enter valid data.")

        elif choice == "2":
            if scheduler.events:
                # Display events for editing
                scheduler.view_events()
                try:
                    index = int(manual_input("Enter the index of the event you want to edit: "))
                    new_name = manual_input("Enter the new name of the event: ")
                    new_date = manual_input("Enter the new date of the event (YYYY-MM-DD): ")
                    new_time = manual_input("Enter the new time of the event (HH:MM): ")
                    # Edit event
                    scheduler.edit_event(index, new_name, new_date, new_time)
                except ValueError:
                    print("Invalid input. Please enter valid data.")
            else:
                print("No events to edit.")
        elif choice == "3":
            # View all events
            scheduler.view_events()
        elif choice == "4":
            if scheduler.events:
                # Display events for deletion
                scheduler.view_events()
                try:
                    index = int(manual_input("Enter the index of the event you want to delete: "))
                    # Delete event
                    scheduler.delete_event(index)
                except ValueError:
                    print("Invalid index. Please enter a valid index.")
            else:
                print("No events to delete.")
        elif choice == "5":
            # Get voice command from user
            command = get_audio()
            if "add event" in command:
                # Add event through voice input
                speak("What's the name of the event?")
                event_name = get_audio()
                
                while True:
                    speak("On which date? Please say the date in year. month. day format.")
                    event_date = get_audio()
                    if validate_date(event_date):
                        break
                    else:
                        speak("Invalid date format. Please try again.")

                while True:
                    speak("At what time? Please say the time in hour and minute format.")
                    event_time = get_audio()
                    if validate_time(event_time):
                        scheduler.add_event(event_name, event_date, event_time)
                        speak("Event added successfully.")
                        break
                    else:
                        speak("Invalid time format. Please try again.")
            elif "edit event" in command:
                # Inform user that edit functionality is not implemented for voice commands
                speak("Edit event implementation is not included in this version of VoiceCommands, we are sorry.")
                pass
            elif "view events" in command:
                # View all events
                scheduler.view_events()
            elif "delete event" in command:
                if scheduler.events:
                    speak("Here are the current events.")
                    # View events for deletion
                    scheduler.view_events()
                    speak("Please say the index of the event you want to delete.")
                    index_command = get_audio()  # Expecting a spoken number
                    try:
                        index = int(index_command)
                        if 0 <= index < len(scheduler.events):
                            speak(
                                f"Do you really want to delete the event: {scheduler.events[index]['name']}? Say yes to confirm.")
                            confirmation = get_audio()
                            if 'yes' in confirmation:
                                # Confirm deletion and delete event
                                scheduler.delete_event(index)
                                speak("Event deleted successfully.")
                            else:
                                speak("Deletion cancelled.")
                        else:
                            speak("Invalid index. Please try again.")
                    except ValueError:
                        speak("I did not understand the index. Please try again.")
                else:
                    speak("There are no events to delete.")
            elif "stop" in command:
                break
        elif choice == "6":
            sys.exit()

# Entry point of the program
if __name__ == '__main__':
    main()
