from tkinter import messagebox


class Controller():


    def _numerical_validation(self, value: str, variable: str | None = None) -> float:
        try:
            new_val_float = float(value)

            if new_val_float < 0 and variable != "nu":
                raise ValueError

            return new_val_float

        except ValueError:
            messagebox.showwarning("Warning", "Invalid input")
            return