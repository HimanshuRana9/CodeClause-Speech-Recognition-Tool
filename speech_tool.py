import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import threading


class SpeechRecognitionTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Speech Recognition Tool - Project #CC3603")
        self.root.geometry("600x400")
        self.root.configure(bg="#0A1D2E")

        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.running = False

        # ===== Title =====
        title = tk.Label(root, text="Basic Speech Recognition Tool",
                         font=("Arial", 20, "bold"), fg="cyan", bg="#0A1D2E")
        title.pack(pady=10)

        # Middle Panel - Recognized Speech
        mid_frame = tk.Frame(root, bg="#0A1D2E", bd=2, relief="groove")
        mid_frame.pack(pady=20, fill="both", expand=True, padx=20)

        tk.Label(mid_frame, text="Recognized Speech",
                 font=("Arial", 12, "bold"), fg="cyan", bg="#0A1D2E").pack(pady=5)

        self.recognized_text = scrolledtext.ScrolledText(
            mid_frame, wrap=tk.WORD, width=60, height=10,
            bg="#102030", fg="white", font=("Arial", 11)
        )
        self.recognized_text.pack(pady=5)

        # ===== Buttons =====
        btn_frame = tk.Frame(root, bg="#0A1D2E")
        btn_frame.pack(pady=10)

        self.listen_btn = tk.Button(btn_frame, text="Start Listening",
                                    command=self.start_listening,
                                    font=("Arial", 12), bg="cyan", fg="black")
        self.listen_btn.grid(row=0, column=0, padx=20)

        stop_btn = tk.Button(btn_frame, text="Stop Listening",
                             command=self.stop_listening,
                             font=("Arial", 12), bg="red", fg="white")
        stop_btn.grid(row=0, column=1, padx=20)

        clear_btn = tk.Button(btn_frame, text="Clear History",
                              command=self.clear_history,
                              font=("Arial", 12), bg="cyan", fg="black")
        clear_btn.grid(row=0, column=2, padx=20)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.running:
                try:
                    audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=7)
                    text = self.recognizer.recognize_google(audio)
                    self.recognized_text.insert(tk.END, f"You said: {text}\n")
                    self.recognized_text.see(tk.END)
                    self.speak(text)
                    if text.lower() == "stop":
                        self.running = False
                        self.recognized_text.insert(tk.END, "🛑 Listening stopped.\n")
                        break
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    self.recognized_text.insert(tk.END, "❌ Could not understand.\n")
                    self.recognized_text.see(tk.END)
                except sr.RequestError:
                    self.recognized_text.insert(tk.END, "⚠️ Internet error.\n")
                    self.recognized_text.see(tk.END)

    def start_listening(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.listen, daemon=True).start()
            self.recognized_text.insert(tk.END, "🎙️ Listening started...\n")

    def stop_listening(self):
        self.running = False
        self.recognized_text.insert(tk.END, "🛑 Listening stopped manually.\n")

    def clear_history(self):
        self.recognized_text.delete(1.0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechRecognitionTool(root)
    root.mainloop()
