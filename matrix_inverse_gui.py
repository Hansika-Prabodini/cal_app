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
        )
        self.size_spin.grid(row=0, column=1, sticky="w")

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


def main() -> None:
    root = tk.Tk()
    app = MatrixInverseApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
