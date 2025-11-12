"""Matrix Inverse Calculator - Tkinter GUI Skeleton (refactored)

This module provides the initial GUI scaffolding only. No computation
or validation is implemented in this ticket.

Enhancements:
- Clear, self-contained layout using Tkinter's grid geometry manager
- A resizable root window with a sensible minsize and a default geometry
- Size selector (Spinbox) restricted to matrix sizes 2–5 with validation
- Placeholder controls: "Compute Inverse" and "Clear"
- Distinct sections: Input Matrix and Inverse (Result) with labeled headings
- Results area uses a disabled Text widget as a placeholder
- Layout weights ensure input and result sections expand gracefully
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
        self.size_spin.bind('<Return>', lambda e: self._ensure_valid_size())

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
        Validates the proposed spinbox value.
        
        This method is called by the `validatecommand` when the spinbox's content changes
        or loses focus (due to `validate='focusout'`). It checks if the `value_if_allowed`
        is a valid integer within the allowed range (2-5).
        
        Args:
            value_if_allowed: The proposed value as a string.
            
        Returns:
            True if the value is valid or temporarily acceptable (e.g., empty string during editing).
            False if the value is invalid, which will cause Tkinter to revert the spinbox
            to its last valid state and also revert the `textvariable`.
        """
        if value_if_allowed == "":
            # Allow empty string during editing. Tkinter will revert on focus out if not filled.
            return True
        
        try:
            val = int(value_if_allowed)
            return 2 <= val <= 5
        except ValueError:
            # Not a valid integer
            return False
    
    def _ensure_valid_size(self) -> None:
        """
        Ensures the `size_var` (and thus the spinbox value) is within the valid range (2-5).
        
        This method is typically called after a user action (e.g., pressing Enter)
        to explicitly correct an out-of-range or non-integer value that might have
        been temporarily set in the `IntVar` or not caught by `validatecommand` during
        a `focusout` event.
        If the `IntVar` holds a non-integer value (e.g., user typed "abc" and pressed Enter
        before `focusout` validation), it resets it to the default (3).
        """
        try:
            current_value = self.size_var.get()
            # Correct if current value is outside the allowed range
            if current_value < 2:
                self.size_var.set(2)
            elif current_value > 5:
                self.size_var.set(5)
        except tk.TclError:
            # If size_var holds a non-integer string (e.g., from direct entry not caught by validation)
            # Reset to default.
            self.size_var.set(3)


def main() -> None:
    root = tk.Tk()
    app = MatrixInverseApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()