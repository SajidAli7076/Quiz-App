import tkinter as tk
from tkinter import messagebox, ttk
from questions import QUIZ_DATA

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Knowledge Assessment")
        self.root.geometry("640x540")
        self.root.configure(bg="#1e1e24")
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TProgressbar", thickness=8, troughcolor="#2b2b36", background="#00adb5")
        
        self.topic = "Python Programming"
        self.current_question_idx = 0
        self.score = 0
        self.selected_ans = tk.StringVar()
        
        self.show_welcome_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_welcome_screen(self):
        self.clear_screen()
        
        title = tk.Label(self.root, text="Python Core Challenge", font=("Segoe UI", 24, "bold"), bg="#1e1e24", fg="#00adb5")
        title.pack(pady=(60, 10))
        
        tagline = tk.Label(self.root, text="Test your core skills and evaluate your runtime knowledge", font=("Segoe UI", 11), bg="#1e1e24", fg="#aaaaaa")
        tagline.pack(pady=(0, 30))
        
        card = tk.Frame(self.root, bg="#25252d", bd=0)
        card.pack(pady=10, padx=60, fill="both", expand=True)
        
        subtitle = tk.Label(card, text="Assessment Parameters", font=("Segoe UI", 14, "bold"), bg="#25252d", fg="#eeeeee")
        subtitle.pack(pady=(35, 15))
        
        desc = tk.Label(card, text="• Total Questions: 5 Core Concepts\n• Target Score: 70% to Pass\n• Features: Real-time accuracy metrics", font=("Segoe UI", 11), bg="#25252d", fg="#b6b6b6", justify="left")
        desc.pack(pady=10)
        
        start_btn = tk.Button(card, text="Launch Challenge 🚀", font=("Segoe UI", 12, "bold"), bg="#00adb5", fg="#ffffff", 
                              activebackground="#008086", activeforeground="#ffffff", relief="flat", bd=0, cursor="hand2")
        start_btn.configure(command=self.start_quiz, padx=20, pady=10)
        start_btn.pack(pady=35)

    def start_quiz(self):
        self.current_question_idx = 0
        self.score = 0
        self.show_question_screen()

    def show_question_screen(self):
        self.clear_screen()
        self.selected_ans.set("")
        
        questions = QUIZ_DATA[self.topic]
        q_data = questions[self.current_question_idx]
        total_q = len(questions)
        
        meta_frame = tk.Frame(self.root, bg="#1e1e24")
        meta_frame.pack(pady=(25, 8), fill="x", padx=50)
        
        progress_lbl = tk.Label(meta_frame, text=f"Progress: Question {self.current_question_idx + 1} of {total_q}", 
                                font=("Segoe UI", 10, "bold"), bg="#1e1e24", fg="#888888")
        progress_lbl.pack(side="left")
        
        pct_done = int((self.current_question_idx / total_q) * 100)
        progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=540, mode="determinate", style="TProgressbar")
        progress_bar.pack(pady=(0, 25))
        progress_bar["value"] = pct_done
        
        q_card = tk.Frame(self.root, bg="#25252d", bd=0)
        q_card.pack(fill="both", expand=True, padx=50, pady=5)
        
        q_lbl = tk.Label(q_card, text=q_data["question"], font=("Segoe UI", 14, "bold"), bg="#25252d", fg="#eeeeee", wraplength=500, justify="center")
        q_lbl.pack(pady=(30, 25), padx=25)
        
        options_frame = tk.Frame(q_card, bg="#25252d")
        options_frame.pack(anchor="w", padx=50, fill="x")
        
        for option in q_data["options"]:
            rb = tk.Radiobutton(options_frame, text=option, variable=self.selected_ans, value=option, 
                                font=("Segoe UI", 11), bg="#25252d", fg="#cccccc", activebackground="#25252d", 
                                activeforeground="#00adb5", selectcolor="#1e1e24", anchor="w", pady=8, cursor="hand2")
            rb.pack(fill="x")
            
        nav_frame = tk.Frame(self.root, bg="#1e1e24")
        nav_frame.pack(fill="x", padx=50, pady=30)
        
        quit_btn = tk.Button(nav_frame, text="Abort Test", font=("Segoe UI", 10, "bold"), bg="#393e46", fg="#eeeeee",
                             activebackground="#2b2b36", activeforeground="#eeeeee", relief="flat", bd=0, padx=15, pady=8, cursor="hand2", command=self.show_welcome_screen)
        quit_btn.pack(side="left")
        
        is_last = (self.current_question_idx == total_q - 1)
        next_text = "Compute Final Score 💾" if is_last else "Lock Alternative ➡️"
        next_bg = "#00adb5" if not is_last else "#393e46"
        
        self.next_btn = tk.Button(nav_frame, text=next_text, font=("Segoe UI", 10, "bold"), bg=next_bg, fg="#ffffff", 
                                  activebackground="#008086", relief="flat", bd=0, padx=20, pady=8, cursor="hand2", command=self.handle_next)
        self.next_btn.pack(side="right")

    def handle_next(self):
        if not self.selected_ans.get():
            messagebox.showwarning("Input Missing", "Please select an alternative option before jumping forward.")
            return
            
        questions = QUIZ_DATA[self.topic]
        correct_answer = questions[self.current_question_idx]["answer"]
        
        if self.selected_ans.get() == correct_answer:
            self.score += 1
            
        if self.current_question_idx < len(questions) - 1:
            self.current_question_idx += 1
            self.show_question_screen()
        else:
            self.show_results_screen()

    def show_results_screen(self):
        self.clear_screen()
        
        questions = QUIZ_DATA[self.topic]
        total = len(questions)
        pct = (self.score / total) * 100
        
        title = tk.Label(self.root, text="Evaluation Complete", font=("Segoe UI", 24, "bold"), bg="#1e1e24", fg="#00adb5")
        title.pack(pady=(50, 15))
        
        card = tk.Frame(self.root, bg="#25252d", bd=0)
        card.pack(pady=10, padx=60, fill="both", expand=True)
        
        score_lbl = tk.Label(card, text=f"Total Tally: {self.score} / {total}", font=("Segoe UI", 18, "bold"), bg="#25252d", fg="#eeeeee")
        score_lbl.pack(pady=(35, 8))
        
        pct_lbl = tk.Label(card, text=f"Performance Rating: {pct:.1f}%", font=("Segoe UI", 12), bg="#25252d", fg="#aaaaaa")
        pct_lbl.pack(pady=5)
        
        passed = pct >= 70
        msg = "VERDICT: SUCCESS (PASSED)" if passed else "VERDICT: CONDITIONAL REVIEW REQUIRED"
        msg_color = "#4caf50" if passed else "#f44336"
        
        msg_lbl = tk.Label(card, text=msg, font=("Segoe UI", 11, "bold"), bg="#25252d", fg=msg_color)
        msg_lbl.pack(pady=25)
        
        restart_btn = tk.Button(card, text="Restart Evaluation 🔄", font=("Segoe UI", 11, "bold"), bg="#393e46", fg="#ffffff", 
                                activebackground="#2b2b36", relief="flat", bd=0, padx=20, pady=10, cursor="hand2", command=self.show_welcome_screen)
        restart_btn.pack(pady=(10, 35))

if __name__ == "__main__":
    window = tk.Tk()
    app = QuizApp(window)
    window.mainloop()