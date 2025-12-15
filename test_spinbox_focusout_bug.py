"""
Unit test for the spinbox focusout validation bug.

This test demonstrates that without a focusout event binding,
invalid values typed into the spinbox persist when the user
tabs away or clicks elsewhere.

EXPECTED BEHAVIOR:
- Before patch: This test will FAIL because focusout doesn't trigger validation
- After patch: This test will PASS because focusout binding enforces validation
"""

import unittest
import tkinter as tk
from matrix_inverse_gui import MatrixInverseApp


class TestSpinboxFocusOutBug(unittest.TestCase):
    def setUp(self):
        """Set up a test root window and app for each test."""
        try:
            self.root = tk.Tk()
        except tk.TclError as e:
            self.skipTest(f"Tkinter not available in this environment: {e}")
            return
        self.root.withdraw()
        self.addCleanup(self._safe_destroy_root)
        self.app = MatrixInverseApp(self.root)
    
    def _safe_destroy_root(self):
        """Safely destroy the Tk root if it exists."""
        try:
            if getattr(self, "root", None):
                self.root.destroy()
        except Exception:
            pass

    def test_focusout_enforces_validation_for_value_too_high(self):
        """
        Test that focusout event enforces validation for values above maximum.
        
        BUG: Without focusout binding, typing "10" and focusing out leaves 
        the IntVar with value 10 (invalid). 
        
        FIX: Adding focusout binding should clamp to 5 (max valid value).
        """
        # Manually set an invalid value (above max of 5)
        self.app.size_spin.delete(0, tk.END)
        self.app.size_spin.insert(0, "10")
        
        # Simulate user focusing out (tabbing away or clicking elsewhere)
        self.app.size_spin.event_generate('<FocusOut>')
        self.root.update()
        
        # After focusout, the value should be corrected to max (5)
        actual_value = self.app.size_var.get()
        self.assertEqual(actual_value, 5, 
                        f"After focusout with value 10, expected 5 but got {actual_value}")
    
    def test_focusout_enforces_validation_for_value_too_low(self):
        """
        Test that focusout event enforces validation for values below minimum.
        
        BUG: Without focusout binding, typing "1" and focusing out leaves 
        the IntVar with value 1 (invalid).
        
        FIX: Adding focusout binding should clamp to 2 (min valid value).
        """
        # Manually set an invalid value (below min of 2)
        self.app.size_spin.delete(0, tk.END)
        self.app.size_spin.insert(0, "1")
        
        # Simulate user focusing out
        self.app.size_spin.event_generate('<FocusOut>')
        self.root.update()
        
        # After focusout, the value should be corrected to min (2)
        actual_value = self.app.size_var.get()
        self.assertEqual(actual_value, 2,
                        f"After focusout with value 1, expected 2 but got {actual_value}")
    
    def test_focusout_allows_valid_values(self):
        """
        Test that focusout doesn't modify valid values.
        """
        # Set a valid value
        self.app.size_spin.delete(0, tk.END)
        self.app.size_spin.insert(0, "4")
        
        # Simulate user focusing out
        self.app.size_spin.event_generate('<FocusOut>')
        self.root.update()
        
        # Value should remain unchanged
        actual_value = self.app.size_var.get()
        self.assertEqual(actual_value, 4,
                        f"After focusout with valid value 4, expected 4 but got {actual_value}")


if __name__ == "__main__":
    unittest.main()
