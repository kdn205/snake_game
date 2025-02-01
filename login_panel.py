import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
import sys

class LoginPanel:
    def __init__(self):
        try:
            self.root = tk.Tk()
            self.root.title("Snake Game Login")
            self.root.geometry("400x300")
            self.root.configure(bg="#2C3E50")
            
            # Add protocol handler for window close button (X)
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            # Center the window
            self.center_window()
            
            # Create main frame
            self.main_frame = tk.Frame(self.root, bg="#2C3E50")
            self.main_frame.pack(pady=20)
            
            # Title
            tk.Label(self.main_frame, text="Snake Game", font=("Helvetica", 24, "bold"), 
                    bg="#2C3E50", fg="white").pack(pady=10)
            
            # Username entry
            tk.Label(self.main_frame, text="Username:", font=("Helvetica", 12), 
                    bg="#2C3E50", fg="white").pack()
            self.username_entry = tk.Entry(self.main_frame, font=("Helvetica", 12))
            self.username_entry.pack(pady=5)
            
            # Add a frame for the buttons
            button_frame = tk.Frame(self.main_frame, bg="#2C3E50")
            button_frame.pack(pady=10)
            
            # Login button (moved to button frame)
            tk.Button(button_frame, text="Start Game", command=self.start_game,
                     font=("Helvetica", 12), bg="#27AE60", fg="white",
                     activebackground="#219A52").pack(side=tk.LEFT, padx=5)
            
            # High scores button (moved to button frame)
            tk.Button(button_frame, text="View High Scores", command=self.show_high_scores,
                     font=("Helvetica", 12), bg="#3498DB", fg="white",
                     activebackground="#2980B9").pack(side=tk.LEFT, padx=5)
            
            # Quit button
            tk.Button(button_frame, text="Quit", command=self.quit_game,
                     font=("Helvetica", 12), bg="#E74C3C", fg="white",
                     activebackground="#C0392B").pack(side=tk.LEFT, padx=5)
            
            self.player_name = None
        except Exception as e:
            print(f"Error initializing login panel: {e}")
            self.root = None
        
    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 300) // 2
        self.root.geometry(f"400x300+{x}+{y}")
        
    def start_game(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username!")
            return
        
        # Check for duplicate username
        try:
            with open("high_scores.txt", "r") as file:
                scores = json.load(file)
                existing_players = {score['player'] for score in scores}
                if username in existing_players:
                    messagebox.showerror("Error", "This username already exists! Please choose another name.")
                    return
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is empty, no need to check for duplicates
            pass
        
        self.player_name = username
        self.root.destroy()
        
    def show_high_scores(self):
        try:
            with open("high_scores.txt", "r") as file:
                scores = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            scores = []
            
        scores_window = tk.Toplevel(self.root)
        scores_window.title("High Scores")
        scores_window.geometry("400x400")
        scores_window.configure(bg="#2C3E50")
        
        tk.Label(scores_window, text="Top Players", font=("Helvetica", 20, "bold"),
                bg="#2C3E50", fg="white").pack(pady=10)
        
        scores_frame = tk.Frame(scores_window, bg="#2C3E50")
        scores_frame.pack(pady=10)
        
        # Headers
        tk.Label(scores_frame, text="Rank", font=("Helvetica", 12, "bold"),
                bg="#2C3E50", fg="white").grid(row=0, column=0, padx=10)
        tk.Label(scores_frame, text="Player", font=("Helvetica", 12, "bold"),
                bg="#2C3E50", fg="white").grid(row=0, column=1, padx=10)
        tk.Label(scores_frame, text="Score", font=("Helvetica", 12, "bold"),
                bg="#2C3E50", fg="white").grid(row=0, column=2, padx=10)
        tk.Label(scores_frame, text="Date", font=("Helvetica", 12, "bold"),
                bg="#2C3E50", fg="white").grid(row=0, column=3, padx=10)
        
        # Sort scores and display top 10
        scores.sort(key=lambda x: x['score'], reverse=True)
        for i, score in enumerate(scores[:10], 1):
            tk.Label(scores_frame, text=str(i), font=("Helvetica", 12),
                    bg="#2C3E50", fg="white").grid(row=i, column=0)
            tk.Label(scores_frame, text=score['player'], font=("Helvetica", 12),
                    bg="#2C3E50", fg="white").grid(row=i, column=1)
            tk.Label(scores_frame, text=str(score['score']), font=("Helvetica", 12),
                    bg="#2C3E50", fg="white").grid(row=i, column=2)
            tk.Label(scores_frame, text=score['date'], font=("Helvetica", 12),
                    bg="#2C3E50", fg="white").grid(row=i, column=3)
            
    def on_closing(self):
        self.player_name = None
        self.root.destroy()
        
    def quit_game(self):
        self.root.quit()
        self.root.destroy()
        sys.exit()
        
    def run(self):
        try:
            if self.root:
                self.root.mainloop()
            return self.player_name
        except Exception as e:
            print(f"Error running login panel: {e}")
            return None 