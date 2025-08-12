import time
import threading
import tkinter as tk
from tkinter import messagebox, filedialog
import pygame

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock with Snooze")
        self.root.geometry("400x300")

        pygame.mixer.init()

        self.alarm_time = ""
        self.ringtone_path = ""
        self.snooze_minutes = 5
        self.alarm_on = False

        # Time entry
        tk.Label(root, text="Set Alarm Time (HH:MM:SS)").pack(pady=5)
        self.time_entry = tk.Entry(root, font=("Arial", 14))
        self.time_entry.pack()

        # Select ringtone
        self.ringtone_label = tk.Label(root, text="No ringtone selected", fg="gray")
        self.ringtone_label.pack(pady=5)
        tk.Button(root, text="Choose Ringtone", command=self.choose_ringtone).pack()

        # Snooze time
        tk.Label(root, text="Snooze Minutes:").pack(pady=5)
        self.snooze_entry = tk.Entry(root)
        self.snooze_entry.insert(0, str(self.snooze_minutes))
        self.snooze_entry.pack()

        # Set alarm button
        tk.Button(root, text="Set Alarm", command=self.set_alarm).pack(pady=10)

        # Cancel alarm button
        tk.Button(root, text="Cancel Alarm", command=self.cancel_alarm).pack()

    def choose_ringtone(self):
        path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if path:
            self.ringtone_path = path
            self.ringtone_label.config(text=f"Ringtone: {path.split('/')[-1]}", fg="green")

    def set_alarm(self):
        self.alarm_time = self.time_entry.get()
        try:
            self.snooze_minutes = int(self.snooze_entry.get())
        except ValueError:
            self.snooze_minutes = 5

        if not self.alarm_time or not self.ringtone_path:
            messagebox.showerror("Error", "Please set time and select a ringtone!")
            return

        self.alarm_on = True
        threading.Thread(target=self.check_alarm, daemon=True).start()
        messagebox.showinfo("Alarm Set", f"Alarm set for {self.alarm_time}")

    def cancel_alarm(self):
        self.alarm_on = False
        pygame.mixer.music.stop()
        messagebox.showinfo("Alarm Cancelled", "Alarm has been cancelled.")

    def check_alarm(self):
        while self.alarm_on:
            current_time = time.strftime("%H:%M:%S")
            if current_time == self.alarm_time:
                self.ring_alarm()
            time.sleep(1)

    def ring_alarm(self):
        pygame.mixer.music.load(self.ringtone_path)
        pygame.mixer.music.play(-1)  # Loop until stopped

        choice = messagebox.askquestion("Alarm", "Snooze?")
        if choice == 'yes':
            pygame.mixer.music.stop()
            snooze_seconds = self.snooze_minutes * 60
            time.sleep(snooze_seconds)
            self.ring_alarm()
        else:
            self.cancel_alarm()

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()
