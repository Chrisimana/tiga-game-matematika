import matplotlib.pyplot as plt
import numpy as np
import random
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

"""Scatter Plot Game"""

class SimpleScatterPlotGame:
    def __init__(self, root):
        self.root = root
        self.graph_size = 10
        self.points_to_guess = 5
        self.points = []
        self.correct = 0
        self.attempted = 0
        
        self.setup_gui()
        self.setup_game()

    def setup_gui(self):
        # Main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(self.main_frame, text="🎮 Scatter Plot Coordinate Game", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Instructions
        instructions = ttk.Label(self.main_frame, 
                                text="Guess the coordinates of the points on the graph!",
                                font=('Arial', 10))
        instructions.pack(pady=5)
        
        # Matplotlib figure
        self.fig = Figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, self.main_frame)
        self.canvas.get_tk_widget().pack(pady=10)
        
        # Controls frame
        controls_frame = ttk.Frame(self.main_frame)
        controls_frame.pack(pady=10)
        
        # Point number selection
        point_frame = ttk.Frame(controls_frame)
        point_frame.pack(pady=5)
        ttk.Label(point_frame, text="Point number (1-5):").pack(side='left')
        self.point_var = tk.StringVar(value="1")
        point_spinbox = ttk.Spinbox(point_frame, from_=1, to=5, textvariable=self.point_var, width=5)
        point_spinbox.pack(side='left', padx=5)
        
        # Coordinate inputs
        coord_frame = ttk.Frame(controls_frame)
        coord_frame.pack(pady=5)
        ttk.Label(coord_frame, text="X coordinate:").pack(side='left')
        self.x_var = tk.StringVar()
        x_entry = ttk.Entry(coord_frame, textvariable=self.x_var, width=8)
        x_entry.pack(side='left', padx=5)
        
        ttk.Label(coord_frame, text="Y coordinate:").pack(side='left')
        self.y_var = tk.StringVar()
        y_entry = ttk.Entry(coord_frame, textvariable=self.y_var, width=8)
        y_entry.pack(side='left', padx=5)
        
        # Buttons
        button_frame = ttk.Frame(controls_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Guess", command=self.guess).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Increase Difficulty", command=self.increase_difficulty).pack(side='left', padx=5)
        ttk.Button(button_frame, text="New Game", command=self.new_game).pack(side='left', padx=5)
        
        # Score display
        self.score_var = tk.StringVar(value="Score: 0/0")
        score_label = ttk.Label(self.main_frame, textvariable=self.score_var, font=('Arial', 12, 'bold'))
        score_label.pack(pady=5)

    def setup_game(self):
        # Generate random points
        self.points = []
        for _ in range(self.points_to_guess):
            x = random.randint(-self.graph_size + 1, self.graph_size - 1)
            y = random.randint(-self.graph_size + 1, self.graph_size - 1)
            self.points.append((x, y))
        
        self.display_plot()

    def display_plot(self):
        self.ax.clear()
        self.ax.set_xlim(-self.graph_size, self.graph_size)
        self.ax.set_ylim(-self.graph_size, self.graph_size)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_title(f"Identify the Coordinates (Graph Size: ±{self.graph_size})", fontsize=14)

        # Plot points
        x_vals = [p[0] for p in self.points]
        y_vals = [p[1] for p in self.points]
        self.ax.scatter(x_vals, y_vals, color='red', s=100, alpha=0.7)

        # Number the points
        for i, (x, y) in enumerate(self.points, 1):
            self.ax.text(x, y + 0.3, str(i), fontsize=12, ha='center', va='bottom',
                        bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.7))

        self.ax.set_xlabel('X coordinate')
        self.ax.set_ylabel('Y coordinate')
        self.canvas.draw()

    def guess(self):
        try:
            point_num = int(self.point_var.get())
            if point_num < 1 or point_num > self.points_to_guess:
                messagebox.showwarning("Warning", "Invalid point number!")
                return

            x_guess = float(self.x_var.get())
            y_guess = float(self.y_var.get())

            actual_x, actual_y = self.points[point_num - 1]
            self.attempted += 1

            if abs(x_guess - actual_x) < 0.1 and abs(y_guess - actual_y) < 0.1:
                self.correct += 1
                messagebox.showinfo("Correct!", f"✅ Correct! The coordinates are ({actual_x}, {actual_y})")
            else:
                messagebox.showinfo("Incorrect", f"❌ Incorrect. The correct coordinates are ({actual_x}, {actual_y})")

            self.update_score()
            self.x_var.set("")
            self.y_var.set("")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")

    def increase_difficulty(self):
        self.graph_size += 5
        self.points_to_guess = min(8, self.points_to_guess + 1)
        messagebox.showinfo("Difficulty Increased", f"🎯 Difficulty increased! Graph size: ±{self.graph_size}")
        self.setup_game()

    def new_game(self):
        self.correct = 0
        self.attempted = 0
        self.graph_size = 10
        self.points_to_guess = 5
        self.setup_game()
        self.update_score()

    def update_score(self):
        accuracy = (self.correct / self.attempted * 100) if self.attempted > 0 else 0
        self.score_var.set(f"Score: {self.correct}/{self.attempted} | Accuracy: {accuracy:.1f}%")

"""Algebra Practice Game"""

class TextAlgebraGame:
    def __init__(self, root):
        self.root = root
        self.difficulty = 1
        self.correct = 0
        self.attempted = 0
        self.streak = 0
        self.max_streak = 0
        
        self.setup_gui()

    def setup_gui(self):
        # Main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(self.main_frame, text="🧮 Algebra Practice Game", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Stats frame
        stats_frame = ttk.Frame(self.main_frame)
        stats_frame.pack(pady=10)
        
        self.stats_var = tk.StringVar(value="Difficulty: Easy | Score: 0/0 | Streak: 0 | Max Streak: 0")
        stats_label = ttk.Label(stats_frame, textvariable=self.stats_var, font=('Arial', 10))
        stats_label.pack()
        
        # Problem display
        self.problem_var = tk.StringVar(value="Click 'New Problem' to start!")
        problem_label = ttk.Label(self.main_frame, textvariable=self.problem_var, 
                                 font=('Arial', 14, 'bold'), background='white', relief='solid', padding=10)
        problem_label.pack(pady=20)
        
        # Answer input
        answer_frame = ttk.Frame(self.main_frame)
        answer_frame.pack(pady=10)
        
        ttk.Label(answer_frame, text="Your answer for x:").pack(side='left')
        self.answer_var = tk.StringVar()
        answer_entry = ttk.Entry(answer_frame, textvariable=self.answer_var, width=10, font=('Arial', 12))
        answer_entry.pack(side='left', padx=5)
        answer_entry.bind('<Return>', lambda e: self.check_answer())
        
        # Buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="New Problem", command=self.new_problem).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Check Answer", command=self.check_answer).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Change Difficulty", command=self.change_difficulty).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Reset Game", command=self.reset_game).pack(side='left', padx=5)
        
        # Feedback
        self.feedback_var = tk.StringVar()
        feedback_label = ttk.Label(self.main_frame, textvariable=self.feedback_var, 
                                  font=('Arial', 12), foreground='blue')
        feedback_label.pack(pady=10)

    def get_difficulty_name(self):
        return {1: "Easy", 2: "Medium", 3: "Hard"}[self.difficulty]

    def new_problem(self):
        problem_type = random.choice(["one-step", "two-step"])

        if problem_type == "one-step":
            equation, answer = self.create_one_step_problem()
        else:
            equation, answer = self.create_two_step_problem()

        self.current_answer = answer
        self.problem_var.set(f"Solve for x:\n{equation}")
        self.answer_var.set("")
        self.feedback_var.set("")

    def create_one_step_problem(self):
        if self.difficulty == 1:
            a = 1
            b = random.randint(-10, 10)
            c = random.randint(-10, 10)
        elif self.difficulty == 2:
            a = random.choice([1, -1, 2, -2])
            b = random.randint(-20, 20)
            c = random.randint(-20, 20)
        else:
            a = random.randint(-5, 5)
            if a == 0: a = 1
            b = random.randint(-50, 50)
            c = random.randint(-50, 50)

        equation = ""
        if a == 1:
            equation += "x"
        elif a == -1:
            equation += "-x"
        else:
            equation += f"{a}x"

        if b >= 0:
            equation += f" + {b}"
        else:
            equation += f" - {-b}"

        equation += f" = {c}"

        answer = round((c - b) / a, 2)
        return equation, answer

    def create_two_step_problem(self):
        if self.difficulty == 1:
            a = random.randint(1, 5)
            b = random.randint(-10, 10)
            c = random.randint(1, 5)
            d = random.randint(-10, 10)
        elif self.difficulty == 2:
            a = random.randint(-5, 5)
            b = random.randint(-20, 20)
            c = random.randint(-5, 5)
            d = random.randint(-20, 20)
        else:
            a = random.randint(-10, 10)
            b = random.randint(-50, 50)
            c = random.randint(-10, 10)
            d = random.randint(-50, 50)

        while a == c:
            a = random.randint(-10, 10) if self.difficulty == 3 else random.randint(-5, 5)

        left_side = ""
        if a == 1:
            left_side = "x"
        elif a == -1:
            left_side = "-x"
        else:
            left_side = f"{a}x"

        if b >= 0:
            left_side += f" + {b}"
        else:
            left_side += f" - {-b}"

        right_side = ""
        if c == 1:
            right_side = "x"
        elif c == -1:
            right_side = "-x"
        else:
            right_side = f"{c}x"

        if d >= 0:
            right_side += f" + {d}"
        else:
            right_side += f" - {-d}"

        equation = f"{left_side} = {right_side}"
        answer = round((d - b) / (a - c), 2)
        return equation, answer

    def check_answer(self):
        if not hasattr(self, 'current_answer'):
            messagebox.showwarning("Warning", "Please generate a problem first!")
            return

        try:
            user_answer = float(self.answer_var.get())
            self.attempted += 1

            if abs(user_answer - self.current_answer) < 0.01:
                self.correct += 1
                self.streak += 1
                self.max_streak = max(self.max_streak, self.streak)
                self.feedback_var.set(f"✅ Correct! x = {self.current_answer}")
                if self.streak >= 3:
                    self.feedback_var.set(f"✅ Correct! x = {self.current_answer}\n🔥 Hot streak! {self.streak} correct in a row!")
            else:
                self.streak = 0
                self.feedback_var.set(f"❌ Incorrect. The correct answer is x = {self.current_answer}")

            self.update_stats()
            self.new_problem()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")

    def change_difficulty(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Change Difficulty")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select Difficulty:", font=('Arial', 12)).pack(pady=20)
        
        difficulty_var = tk.IntVar(value=self.difficulty)
        
        ttk.Radiobutton(dialog, text="Easy (simple one-step equations)", 
                       variable=difficulty_var, value=1).pack(pady=5)
        ttk.Radiobutton(dialog, text="Medium (negative numbers, two-step)", 
                       variable=difficulty_var, value=2).pack(pady=5)
        ttk.Radiobutton(dialog, text="Hard (complex coefficients)", 
                       variable=difficulty_var, value=3).pack(pady=5)
        
        def apply_difficulty():
            self.difficulty = difficulty_var.get()
            self.update_stats()
            dialog.destroy()
            self.new_problem()
        
        ttk.Button(dialog, text="Apply", command=apply_difficulty).pack(pady=20)

    def reset_game(self):
        self.correct = 0
        self.attempted = 0
        self.streak = 0
        self.max_streak = 0
        self.update_stats()
        self.new_problem()

    def update_stats(self):
        accuracy = (self.correct / self.attempted * 100) if self.attempted > 0 else 0
        self.stats_var.set(f"Difficulty: {self.get_difficulty_name()} | Score: {self.correct}/{self.attempted} | Streak: {self.streak} | Max Streak: {self.max_streak} | Accuracy: {accuracy:.1f}%")

"""Projectile Game"""

class ProjectileGame:
    def __init__(self, root):
        self.root = root
        self.level = 1
        self.max_height = 10
        self.wall_x = 0
        self.wall_height = 0
        self.score = 0
        self.attempts = 0
        
        self.setup_gui()
        self.new_level()

    def setup_gui(self):
        # Main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(self.main_frame, text="🎯 Projectile Motion Game", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Instructions
        instructions = ttk.Label(self.main_frame, 
                                text="Adjust the parabola to make the projectile clear the wall!",
                                font=('Arial', 10))
        instructions.pack(pady=5)
        
        # Score display
        self.score_var = tk.StringVar(value="Score: 0 | Attempts: 0 | Accuracy: 0%")
        score_label = ttk.Label(self.main_frame, textvariable=self.score_var, font=('Arial', 10))
        score_label.pack(pady=5)
        
        # Level selection
        level_frame = ttk.Frame(self.main_frame)
        level_frame.pack(pady=10)
        
        ttk.Label(level_frame, text="Level:").pack(side='left')
        self.level_var = tk.IntVar(value=1)
        ttk.Radiobutton(level_frame, text="Basic (Sliders)", 
                       variable=self.level_var, value=1, command=self.on_level_change).pack(side='left', padx=10)
        ttk.Radiobutton(level_frame, text="Advanced (Input)", 
                       variable=self.level_var, value=2, command=self.on_level_change).pack(side='left', padx=10)
        
        # Basic controls (sliders)
        self.basic_frame = ttk.Frame(self.main_frame)
        self.basic_frame.pack(pady=10)
        
        ttk.Label(self.basic_frame, text="Adjust the sliders to clear the wall:").pack()
        
        self.a_slider = tk.Scale(self.basic_frame, from_=-2, to=2, resolution=0.1, 
                                orient='horizontal', label='a:', length=300)
        self.a_slider.pack(pady=5)
        self.a_slider.set(0)
        
        self.b_slider = tk.Scale(self.basic_frame, from_=-5, to=5, resolution=0.1,
                                orient='horizontal', label='b:', length=300)
        self.b_slider.pack(pady=5)
        self.b_slider.set(0)
        
        self.c_slider = tk.Scale(self.basic_frame, from_=0, to=self.max_height, resolution=0.1,
                                orient='horizontal', label='c:', length=300)
        self.c_slider.pack(pady=5)
        self.c_slider.set(0)
        
        # Advanced controls (text inputs)
        self.advanced_frame = ttk.Frame(self.main_frame)
        
        ttk.Label(self.advanced_frame, text="Enter coefficients for y = ax² + bx + c:").pack()
        
        coeff_frame = ttk.Frame(self.advanced_frame)
        coeff_frame.pack(pady=10)
        
        ttk.Label(coeff_frame, text="a:").pack(side='left')
        self.a_var = tk.StringVar(value="0")
        a_entry = ttk.Entry(coeff_frame, textvariable=self.a_var, width=8)
        a_entry.pack(side='left', padx=5)
        
        ttk.Label(coeff_frame, text="b:").pack(side='left')
        self.b_var = tk.StringVar(value="0")
        b_entry = ttk.Entry(coeff_frame, textvariable=self.b_var, width=8)
        b_entry.pack(side='left', padx=5)
        
        ttk.Label(coeff_frame, text="c:").pack(side='left')
        self.c_var = tk.StringVar(value="0")
        c_entry = ttk.Entry(coeff_frame, textvariable=self.c_var, width=8)
        c_entry.pack(side='left', padx=5)
        
        # Connect events
        self.a_slider.configure(command=self.on_slider_change)
        self.b_slider.configure(command=self.on_slider_change)
        self.c_slider.configure(command=self.on_slider_change)
        
        self.a_var.trace('w', self.on_input_change)
        self.b_var.trace('w', self.on_input_change)
        self.c_var.trace('w', self.on_input_change)
        
        # Matplotlib figure
        self.fig = Figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, self.main_frame)
        self.canvas.get_tk_widget().pack(pady=10)
        
        # Buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Check Solution", command=self.check_solution).pack(side='left', padx=5)
        ttk.Button(button_frame, text="New Level", command=self.new_level).pack(side='left', padx=5)
        
        # Feedback
        self.feedback_var = tk.StringVar()
        feedback_label = ttk.Label(self.main_frame, textvariable=self.feedback_var, 
                                  font=('Arial', 11), wraplength=500)
        feedback_label.pack(pady=10)

    def on_level_change(self):
        self.level = self.level_var.get()
        if self.level == 1:
            self.advanced_frame.pack_forget()
            self.basic_frame.pack(pady=10)
        else:
            self.basic_frame.pack_forget()
            self.advanced_frame.pack(pady=10)
        self.new_level()

    def on_slider_change(self, event=None):
        if self.level == 1:
            self.update_plot()

    def on_input_change(self, *args):
        if self.level == 2:
            self.update_plot()

    def new_level(self):
        # Generate random wall position and height
        self.wall_x = random.uniform(3, 7)
        self.wall_height = random.uniform(1, self.max_height - 1)

        # Set random starting positions
        if self.level == 1:
            self.a_slider.set(random.uniform(-1, 1))
            self.b_slider.set(random.uniform(-2, 2))
            self.c_slider.set(random.uniform(0, self.max_height/2))
        else:
            self.a_var.set("0")
            self.b_var.set("0")
            self.c_var.set("0")

        self.feedback_var.set("🎯 New level! Adjust the parabola to clear the wall.")
        self.update_plot()

    def update_plot(self):
        self.ax.clear()
        
        # Get current values
        if self.level == 1:
            a = self.a_slider.get()
            b = self.b_slider.get()
            c = self.c_slider.get()
        else:
            try:
                a = float(self.a_var.get())
                b = float(self.b_var.get())
                c = float(self.c_var.get())
            except ValueError:
                a, b, c = 0, 0, 0

        # Set up the plot
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, self.max_height)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel('Distance')
        self.ax.set_ylabel('Height')
        self.ax.set_title('Adjust the Projectile Path to Clear the Wall')

        # Draw wall
        self.ax.plot([self.wall_x, self.wall_x], [0, self.wall_height], 'k-', linewidth=15, alpha=0.7)
        self.ax.text(self.wall_x, self.wall_height/2, f"Wall Height: {self.wall_height:.1f}",
                    ha='center', va='center', color='white', fontweight='bold', fontsize=10)

        # Plot the parabola
        x = np.linspace(0, 10, 100)
        y = a * x**2 + b * x + c

        # Only plot valid ranges (positive y)
        valid_mask = y >= 0
        x_valid = x[valid_mask]
        y_valid = y[valid_mask]

        if len(x_valid) > 0:
            self.ax.plot(x_valid, y_valid, 'r-', linewidth=2, label=f'y = {a:.1f}x² + {b:.1f}x + {c:.1f}')

            # Mark the point at the wall
            y_at_wall = a * self.wall_x**2 + b * self.wall_x + c
            if y_at_wall >= 0:
                self.ax.plot(self.wall_x, y_at_wall, 'ro', markersize=8)
                self.ax.text(self.wall_x, y_at_wall + 0.3, f'{y_at_wall:.1f}',
                           ha='center', va='bottom', fontweight='bold')

        self.ax.legend()
        self.canvas.draw()

    def check_solution(self):
        self.attempts += 1

        # Get current values
        if self.level == 1:
            a = self.a_slider.get()
            b = self.b_slider.get()
            c = self.c_slider.get()
        else:
            try:
                a = float(self.a_var.get())
                b = float(self.b_var.get())
                c = float(self.c_var.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers!")
                return

        # Calculate height at wall position
        y_at_wall = a * self.wall_x**2 + b * self.wall_x + c

        if y_at_wall > self.wall_height + 0.1:  # Small buffer
            self.score += 1
            self.feedback_var.set(f"🎉 SUCCESS! You cleared the wall!\nAt x = {self.wall_x:.1f}, your height was {y_at_wall:.1f}\nWall height was {self.wall_height:.1f}\n🎯 Perfect! The projectile cleared by {y_at_wall - self.wall_height:.1f} units!")
            # Auto-generate new level after success
            self.new_level()
        else:
            self.feedback_var.set(f"❌ Try again! The projectile didn't clear the wall.\nAt x = {self.wall_x:.1f}, your height was {y_at_wall:.1f}\nBut you needed at least {self.wall_height:.1f}\n💡 Tip: Adjust the coefficients to make the parabola higher at x = {self.wall_x:.1f}")

        self.update_score()

    def update_score(self):
        accuracy = (self.score / self.attempts * 100) if self.attempts > 0 else 0
        self.score_var.set(f"Score: {self.score} | Attempts: {self.attempts} | Accuracy: {accuracy:.1f}%")

"""Main Application"""

class MathGamesApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Three Math Games")
        self.root.geometry("800x700")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        
        # Create tabs for each game
        self.scatter_frame = ttk.Frame(self.notebook)
        self.algebra_frame = ttk.Frame(self.notebook)
        self.projectile_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.scatter_frame, text="Scatter Plot Game")
        self.notebook.add(self.algebra_frame, text="Algebra Game")
        self.notebook.add(self.projectile_frame, text="Projectile Game")
        
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Initialize games
        self.scatter_game = SimpleScatterPlotGame(self.scatter_frame)
        self.algebra_game = TextAlgebraGame(self.algebra_frame)
        self.projectile_game = ProjectileGame(self.projectile_frame)

    def run(self):
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    print("🎮 Three Math Games")
    print("=====================================")
    print("1. Scatter Plot Coordinate Game")
    print("2. Algebra Practice Game") 
    print("3. Projectile Motion Game")
    print()
    
    app = MathGamesApp()
    app.run()