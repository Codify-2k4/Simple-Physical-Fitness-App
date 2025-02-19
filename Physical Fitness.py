import tkinter as tk
import random
import pyttsx3
import time
from threading import Thread

class StudyFitnessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Active Study Companion")
        self.root.geometry("400x500")

        self.study_time = 25  # Minutes before break
        self.exercise_time = 30  # Seconds per break
        self.points = 0
        self.difficulty = "Medium"
        self.timer_running = False
        self.exercise_list = {
            "Easy": ["Neck Rolls", "Wrist Stretch", "Shoulder Shrugs", "Deep Breathing"],
            "Medium": ["Jumping Jacks", "Squats", "Lunges", "Wall Sit"],
            "Hard": ["Burpees", "Push-ups", "Plank Hold", "Mountain Climbers"]
        }

        self.engine = pyttsx3.init()
        
        self.label = tk.Label(root, text="👨‍💻 Study & Stay Active!", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)

        self.timer_label = tk.Label(root, text="Time Until Next Break: 25:00", font=("Arial", 12))
        self.timer_label.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Studying", command=self.start_timer, font=("Arial", 12), bg="lightblue")
        self.start_button.pack(pady=10)

        self.exercise_label = tk.Label(root, text="Exercise will appear here!", font=("Arial", 12))
        self.exercise_label.pack(pady=10)

        self.points_label = tk.Label(root, text=f"Points: {self.points}", font=("Arial", 12, "bold"))
        self.points_label.pack(pady=10)

        self.difficulty_label = tk.Label(root, text="Set Difficulty:", font=("Arial", 12))
        self.difficulty_label.pack()

        self.difficulty_menu = tk.StringVar(value="Medium")
        self.difficulty_dropdown = tk.OptionMenu(root, self.difficulty_menu, "Easy", "Medium", "Hard", self.set_difficulty)
        self.difficulty_dropdown.pack(pady=5)

        self.break_button = tk.Button(root, text="Take a Break Now", command=self.start_exercise, font=("Arial", 12), bg="lightgreen")
        self.break_button.pack(pady=10)

        self.message_label = tk.Label(root, text="", font=("Arial", 12, "italic"))
        self.message_label.pack(pady=10)

    def set_difficulty(self, value):
        self.difficulty = value

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            Thread(target=self.countdown_timer, args=(self.study_time * 60,)).start()

    def countdown_timer(self, seconds):
        while seconds > 0 and self.timer_running:
            mins, secs = divmod(seconds, 60)
            self.timer_label.config(text=f"Time Until Next Break: {mins:02d}:{secs:02d}")
            time.sleep(1)
            seconds -= 1
        
        if self.timer_running:
            self.start_exercise()

    def start_exercise(self):
        self.timer_running = False
        exercise = random.choice(self.exercise_list[self.difficulty])
        self.exercise_label.config(text=f"💪 Do: {exercise} for {self.exercise_time} sec")
        self.points += 10
        self.points_label.config(text=f"Points: {self.points}")
        self.speak(f"Time for a break! Do {exercise} for {self.exercise_time} seconds.")

    def speak(self, text):
        Thread(target=self._speak_thread, args=(text,)).start()

    def _speak_thread(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudyFitnessApp(root)
    root.mainloop()
