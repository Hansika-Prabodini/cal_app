"""
Matrix Inverse Calculator - Tkinter GUI Skeleton

This module provides the initial GUI scaffolding only. No computation
or validation is implemented in this ticket.

Requirements addressed:
- Tk root window with title, resizable, geometry and minsize
- Top-level layout frames: controls, input grid area, results area
- Size selector (IntVar 2–5, default 3) via Spinbox
- Placeholder buttons: Compute Inverse, Clear
- Section labels: Matrix Size, Input Matrix, Inverse (Result)
- Results area uses a disabled Text widget placeholder
- Grid weights so input and results areas expand
- Run guard to start mainloop
"""

import tkinter as tk
from tkinter import ttk


class MatrixInverseApp:
    def __init__(self, master: tk.Tk):
        self.master = master
        self._configure_root()
        self._init_state()
        self._build_layout()

    # Root/window configuration
    def _configure_root(self) -> None:
        self.master.title("Matrix Inverse Calculator")
        # Suggested comfortable size for 5x5 grid area
        self.master.geometry("900x600")
        # Sensible minimum size to keep layout usable
        self.master.minsize(700, 450)
        # Ensure content can expand
        self.master.rowconfigure(0, weight=0)
        self.master.rowconfigure(1, weight=2)
        self.master.rowconfigure(2, weight=1)
        self.master.columnconfigure(0, weight=1)

    def _init_state(self) -> None:
        # IntVar for matrix size (2–5), default 3
        self.size_var = tk.IntVar(value=3)
        # Register validation command for spinbox
        self.validate_cmd = self.master.register(self._validate_size)

    def _build_layout(self) -> None:
        # Controls frame (top)
        controls = ttk.Frame(self.master, padding=(10, 10))
        controls.grid(row=0, column=0, sticky="ew")
        controls.columnconfigure(0, weight=0)
        controls.columnconfigure(1, weight=0)
        controls.columnconfigure(2, weight=0)
        controls.columnconfigure(3, weight=1)  # spacer/stretch
        controls.columnconfigure(4, weight=0)
        controls.columnconfigure(5, weight=0)

        # Matrix Size label
        size_label = ttk.Label(controls, text="Matrix Size")
        size_label.grid(row=0, column=0, sticky="w", padx=(0, 8))

        # Size selector Spinbox (2–5), default shown from IntVar=3
        self.size_spin = ttk.Spinbox(
            controls,
            from_=2,
            to=5,
            textvariable=self.size_var,
            width=5,
            wrap=False,
            justify="center",
            validate="focusout",
            validatecommand=(self.validate_cmd, '%P')
        )
        self.size_spin.grid(row=0, column=1, sticky="w")
        # Bind additional event to validate on Return key
        self.size_spin.bind('<Return>', lambda e: self._validate_and_correct())

        # Placeholder buttons
        self.compute_btn = ttk.Button(controls, text="Compute Inverse")
        self.compute_btn.grid(row=0, column=4, padx=(8, 8))

        self.clear_btn = ttk.Button(controls, text="Clear")
        self.clear_btn.grid(row=0, column=5)

        # Input section container
        input_section = ttk.Frame(self.master, padding=(10, 5))
        input_section.grid(row=1, column=0, sticky="nsew")
        input_section.rowconfigure(1, weight=1)  # grid area grows
        input_section.columnconfigure(0, weight=1)

        input_label = ttk.Label(input_section, text="Input Matrix")
        input_label.grid(row=0, column=0, sticky="w", pady=(0, 6))

        # Placeholder for future Entry grid
        self.input_grid_frame = ttk.Frame(input_section, relief="groove", padding=10)
        self.input_grid_frame.grid(row=1, column=0, sticky="nsew")
        self.input_grid_frame.rowconfigure(0, weight=1)
        self.input_grid_frame.columnconfigure(0, weight=1)

        # Results section container
        results_section = ttk.Frame(self.master, padding=(10, 5))
        results_section.grid(row=2, column=0, sticky="nsew")
        results_section.rowconfigure(1, weight=1)
        results_section.columnconfigure(0, weight=1)

        results_label = ttk.Label(results_section, text="Inverse (Result)")
        results_label.grid(row=0, column=0, sticky="w", pady=(0, 6))

        # Disabled Text widget as placeholder for results
        self.results_text = tk.Text(results_section, height=8, wrap="word")
        self.results_text.grid(row=1, column=0, sticky="nsew")

        # Insert placeholder text and disable editing
        self._set_results_placeholder(
            "Result will appear here after computation. This is a placeholder."
        )

    def _set_results_placeholder(self, text: str) -> None:
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert("1.0", text)
        self.results_text.configure(state="disabled")
    
    def _validate_size(self, value_if_allowed: str) -> bool:
        """
        Validate that the spinbox value is within the allowed range (2-5).
        
        Args:
            value_if_allowed: The proposed value as a string
            
        Returns:
            True if valid, False otherwise (which triggers correction)
        """
        if value_if_allowed == "":
            # Empty string during editing is allowed temporarily
            return True
        
        try:
            val = int(value_if_allowed)
            # Check if value is within valid range
            if 2 <= val <= 5:
                return True
            else:
                # Invalid value - will trigger correction
                self.master.after_idle(self._validate_and_correct)
                return False
        except ValueError:
            # Not a valid integer - will trigger correction
            self.master.after_idle(self._validate_and_correct)
            return False
    
    def _validate_and_correct(self) -> None:
        """
        Validate and correct the spinbox value to ensure it's within range.
        If the current value is invalid, reset it to the last valid value or default.
        """
        try:
            current = self.size_var.get()
            # If current value is outside range, correct it
            if current < 2:
                self.size_var.set(2)
            elif current > 5:
                self.size_var.set(5)
        except tk.TclError:
            # If IntVar has invalid value, reset to default
            self.size_var.set(3)


def main() -> None:
    root = tk.Tk()
    app = MatrixInverseApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
