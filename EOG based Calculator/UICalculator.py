import tkinter as tk
import time

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"

CURSOR_COLOR = "#FFCCCC"



class Calculator:
    def __init__(self):
        # EYE
        self.buttons = {}
        # Initialization
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(0, 0)
        self.window.title("Calculator")
        # Frames
        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()

        # number and its position in the grid
        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        self.total_label, self.label = self.create_display_labels()
        # creating button grid
        self.buttons_frame = self.create_buttons_frame()
        # make them fill the empty spaces (giving them 0<weight allows that!)
        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()

        # last to apply for all the buttons
        self.update_button_color()
        # set the cursor to "5"
        self.blink_state = False
        self.cursor = (2, 2)
        self.set_cursor(self.cursor)

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def update_button_color(self):
        for button in self.buttons.values():
            button[0].bind("<Enter>", self.on_enter)
            button[0].bind("<Leave>", self.on_leave)

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR,
                               font=DIGITS_FONT_STYLE,
                               borderwidth=0,
                               command=lambda x=digit: self.add_to_expression(x)
                               )
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)  # sticky to fill all dir
            self.buttons[str(digit)] = (button, WHITE)

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            self.buttons[symbol] = (button, OFF_WHITE)
            i += 1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)
        self.buttons["C"] = (button, OFF_WHITE)

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)
        self.buttons["x\u00b2"] = (button, OFF_WHITE, LABEL_COLOR)

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)
        self.buttons["\u221ax"] = (button, OFF_WHITE)

    # evaluate any py valid expression
    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))

            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0,
                           command=self.evaluate
                           )
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)
        self.buttons["="] = (button, LIGHT_BLUE)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        # to display the operator on the original form.
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    def on_enter(self, event):
        event.widget.config(bg=CURSOR_COLOR)

    def on_leave(self, event):
        button_info = self.buttons[event.widget.cget("text")]
        event.widget.config(bg=button_info[1])
        # event.widget.config(bg=WHITE)

    def set_cursor(self, position):
        # Remove cursor from all buttons
        for button in self.buttons.values():
            button[0].config(bg=button[1])
        button = self.buttons_frame.grid_slaves(row=position[0], column=position[1])[0]
        # Set cursor to the specified button
        button.config(bg=CURSOR_COLOR)
        self.cursor = position

    def show_direction_popup(self, direction):
        popup = tk.Toplevel(self.window)
        popup.geometry()  # Small size for the popup
        popup.wm_overrideredirect(True)  # Remove window decorations

        # Position the popup relative to the main window
        x = self.window.winfo_x()
        y = self.window.winfo_y()
        popup.geometry(f"+{x + 50}+{y + 50}")

        # Create a label inside the popup with the direction text
        label = tk.Label(popup, text=direction, font=SMALL_FONT_STYLE, bg=LIGHT_GRAY, fg=LABEL_COLOR)
        label.pack()

        # Schedule the popup to disappear after 1 second
        self.window.after(1000, popup.destroy)

    def process_directions(self, directions):
        for direction in directions:
            if direction in ('up', 'down', 'left', 'right'):
                self.move_cursor(direction)
                self.show_direction_popup(direction)
            elif direction == 'blink':
                self.blink()
                self.blink()
                self.show_direction_popup("blink")
                if self.cursor == (4, 3):
                    self.cursor = (2, 2)  # Reset cursor position
            self.window.update()
            time.sleep(1)

    def move_cursor(self, direction):
        row, col = self.cursor
        max_col = 4  # Updated to allow movement to the rightmost column
        if direction == 'up' and row > 0:
            self.set_cursor((row - 1, col))
        elif direction == 'down' and row < 4:
            new_col = col if row < 3 else min(col, 2)  # Last row has only 3 columns
            self.set_cursor((row + 1, new_col))
        elif direction == 'left' and col > 1:
            self.set_cursor((row, col - 1))
        elif direction == 'right' and col < max_col:
            self.set_cursor((row, col + 1))

    def blink(self):
        row, col = self.cursor
        button = self.buttons_frame.grid_slaves(row=row, column=col)[0]
        if not self.blink_state:
            self.blink_state = True
            button.config(bg=CURSOR_COLOR)
        else:
            button.invoke()  # invoke the button functionality
            self.blink_state = False
            if button.cget("text") == "=":
                self.set_cursor((2, 2))  #

    def run(self):
        self.window.after(1000, self.process_directions, ["up",
                                                          "right",
                                                          "blink",
                                                          "right",
                                                          "blink", "down", "left", "blink",
                                                          "down", "down", "right", "blink"
                                                          ])
        self.window.mainloop()


if __name__ == '__main__':
    calc = Calculator()
    calc.run()
