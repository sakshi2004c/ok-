import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime, timedelta


class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.root.geometry("400x300")

        # Create a style object
        self.style = ttk.Style()

        # Configure styles for different elements
        # Background color for frames
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', font=('Arial', 14))    # Font for labels
        self.style.configure('TButton', font=(
            'Arial', 12))   # Font for buttons
        self.style.configure('TLabel', font=(
            'Arial', 20, 'bold'))  # Font for logo label
        # Background color for home page
        self.style.configure('HomePage.TFrame', background='#85C1E9')
        self.logo_image = tk.PhotoImage(file="logo.png").subsample(3)  # Change "logo.png" to the path of your logo image
        self.logo_label = ttk.Label(
            root, image=self.logo_image,foreground='blue')
        self.logo_label.pack(pady=10)
        # Background color for difficulty page
        self.style.configure('DifficultyPage.TFrame', background='#85C1E9')
        # Background color for question page
        self.style.configure('QuestionPage.TFrame', background='#85C1E9')

        # Home Page

      

        self.home_frame = ttk.Frame(self.root, style='HomePage.TFrame')
        self.home_frame.pack(fill="both", expand=True)

        self.logo_label = ttk.Label(
            self.home_frame, text="MIND BUSTERS ", style='Logo.TLabel')
        self.logo_label.pack(pady=20)

        self.play_button = ttk.Button(
            self.home_frame, text="Play", command=self.show_difficulty_selection)
        self.play_button.pack(pady=20)
        self.root.configure(bg='#85C1E9') 

        # Difficulty Selection Page
        self.difficulty_frame = ttk.Frame(
            self.root, style='DifficultyPage.TFrame')

        self.easy_button = ttk.Button(
            self.difficulty_frame, text="Easy", command=lambda: self.start_game("easy"))
        self.easy_button.pack(pady=10)

        self.medium_button = ttk.Button(
            self.difficulty_frame, text="Medium", command=lambda: self.start_game("medium"))
        self.medium_button.pack(pady=10)

        self.hard_button = ttk.Button(
            self.difficulty_frame, text="Hard", command=lambda: self.start_game("hard"))
        self.hard_button.pack(pady=10)

        # Flag to track if quiz is completed
        self.quiz_completed = False

    def show_difficulty_selection(self):
        self.home_frame.pack_forget()
        self.difficulty_frame.pack(fill="both", expand=True)

    def start_game(self, difficulty):
        self.difficulty_frame.pack_forget()

        # Fetch questions from API
        self.questions = self.fetch_computer_science_questions(difficulty)
        self.current_question_index = 0
        self.score = 0
        self.time_limit = 30  # Time limit for each question (in seconds)

        # Question Page
        self.question_frame = ttk.Frame(self.root, style='QuestionPage.TFrame')
        self.question_frame.pack(fill="both", expand=True)

        self.question_label = ttk.Label(
            self.question_frame, text=self.questions[self.current_question_index]['question'], font=('Arial', 16))
        self.question_label.pack(pady=20)

        # Fetch and display options for the question
        options = self.questions[self.current_question_index]['incorrect_answers']
        correct_answer = self.questions[self.current_question_index]['correct_answer']
        options.append(correct_answer)
        self.answer_var = tk.StringVar()
        self.answer_var.set('')  # Reset answer variable
        for option_text in options:
            option = ttk.Radiobutton(
                self.question_frame, text=option_text, variable=self.answer_var, value=option_text)
            option.pack(anchor='center',pady=10)

        self.submit_button = ttk.Button(
            self.question_frame, text="Submit", command=self.check_answer)
        self.submit_button.pack(pady=10,anchor='e')

        self.timer_label = ttk.Label(self.question_frame, text="")
        self.timer_label.pack(anchor='w')

        self.start_time = datetime.now()
        self.update_timer()

    def fetch_computer_science_questions(self, difficulty, amount=5):
        url = f"https://opentdb.com/api.php?amount={
            amount}&category=18&difficulty={difficulty.lower()}&type=multiple"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            questions = data["results"]
            return questions
        else:
            print("Failed to fetch questions.")
            return []

    def update_timer(self):
        elapsed_time = datetime.now() - self.start_time
        remaining_time = max(self.time_limit - elapsed_time.seconds, 0)
        self.timer_label.config(text="Time: " + str(remaining_time) + "s")
        if remaining_time == 0:
            self.check_answer()
        else:
            self.root.after(1000, self.update_timer)

    def check_answer(self):
        user_answer = self.answer_var.get().strip()
        correct_answer = self.questions[self.current_question_index]['correct_answer']
        if user_answer == correct_answer:
            self.score += 1
            messagebox.showinfo("Correct", "Your answer is correct!")
        else:
            messagebox.showerror("Incorrect", "Your answer is incorrect!")
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.show_next_question()
        else:
            messagebox.showinfo("Quiz Finished", f"Quiz finished. Your score: {
                                self.score}/{len(self.questions)}")
            self.quiz_completed = True
            self.show_difficulty_selection()

    def show_next_question(self):
        self.question_label.config(
            text=self.questions[self.current_question_index]['question'])

        # Fetch and display options for the question
        options = self.questions[self.current_question_index]['incorrect_answers']
        correct_answer = self.questions[self.current_question_index]['correct_answer']
        options.append(correct_answer)
        self.answer_var.set('')  # Reset answer variable
        for widget in self.question_frame.winfo_children():
            if isinstance(widget, ttk.Radiobutton):
                widget.destroy()
        for option_text in options:
            option = ttk.Radiobutton(
                self.question_frame, text=option_text, variable=self.answer_var, value=option_text)
            option.pack(anchor='center',pady=10)


    def back_to_home(self):
        self.question_frame.pack_forget()
        self.home_frame.pack(fill="both", expand=True)
        if self.quiz_completed:
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    quiz_game = QuizGame(root)
    root.mainloop()
