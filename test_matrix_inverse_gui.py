"""
Unit tests for Matrix Inverse Calculator GUI

This test file includes a test that verifies the Spinbox validation
bug is fixed - ensuring manual entry is restricted to valid range 2-5.
"""

import unittest
import tkinter as tk
from matrix_inverse_gui import MatrixInverseApp


class TestMatrixInverseApp(unittest.TestCase):
    def setUp(self):
        """Set up a test root window and app for each test."""
        self.root = tk.Tk()
        # Hide the GUI window during tests to avoid side effects in headless envs
        self.root.withdraw()
        self.app = MatrixInverseApp(self.root)
    
    def tearDown(self):
        """Clean up the test window."""
        self.root.destroy()
    
    def test_spinbox_validates_manual_entry(self):
        """
        Test that the Spinbox properly validates manual text entry.
        
        This test verifies that when a user manually types a value outside
        the valid range (2-5), the Spinbox rejects it and maintains a valid value.
        
        Before the patch: This test will FAIL because the Spinbox accepts any value.
        After the patch: This test will PASS because validation is enforced.
        """
        # Test 1: Try to set a value below minimum (1)
        self.app.size_spin.delete(0, tk.END)
        self.app.size_spin.insert(0, "1")
        self.root.update()  # Force GUI update
        # Trigger validation by simulating focus out or pressing return
        self.app.size_spin.event_generate('<FocusOut>')
        self.root.update()
        
        value = self.app.size_var.get()
        self.assertGreaterEqual(value, 2, 
                                f"Spinbox should reject value 1, but got {value}")
        
        # Test 2: Try to set a value above maximum (10)
        self.app.size_spin.delete(0, tk.END)
        self.app.size_spin.insert(0, "10")
        self.root.update()
        self.app.size_spin.event_generate('<FocusOut>')
        self.root.update()
        
        value = self.app.size_var.get()
        self.assertLessEqual(value, 5,
                             f"Spinbox should reject value 10, but got {value}")
        
        # Test 3: Try to set a negative value (-3)
        self.app.size_spin.delete(0, tk.END)
        self.app.size_spin.insert(0, "-3")
        self.root.update()
        self.app.size_spin.event_generate('<FocusOut>')
        self.root.update()
        
        value = self.app.size_var.get()
        self.assertGreaterEqual(value, 2,
                                f"Spinbox should reject value -3, but got {value}")
        
        # Test 4: Valid values should be accepted (3)
        self.app.size_spin.delete(0, tk.END)
        self.app.size_spin.insert(0, "3")
        self.root.update()
        self.app.size_spin.event_generate('<FocusOut>')
        self.root.update()
        
        value = self.app.size_var.get()
        self.assertEqual(value, 3,
                        f"Spinbox should accept value 3, but got {value}")
        
        # Test 5: Valid boundary values (2 and 5)
        self.app.size_spin.delete(0, tk.END)
        self.app.size_spin.insert(0, "2")
        self.root.update()
        self.app.size_spin.event_generate('<FocusOut>')
        self.root.update()
        
        value = self.app.size_var.get()
        self.assertEqual(value, 2,
                        f"Spinbox should accept value 2, but got {value}")
        
        self.app.size_spin.delete(0, tk.END)
        self.app.size_spin.insert(0, "5")
        self.root.update()
        self.app.size_spin.event_generate('<FocusOut>')
        self.root.update()
        
        value = self.app.size_var.get()
        self.assertEqual(value, 5,
                        f"Spinbox should accept value 5, but got {value}")

    def test_validate_size_logic_unit(self):
        """Directly test the _validate_size helper for edge cases."""
        self.assertTrue(self.app._validate_size(""))       # allow empty during edit
        self.assertTrue(self.app._validate_size("2"))
        self.assertTrue(self.app._validate_size("3"))
        self.assertTrue(self.app._validate_size("5"))
        self.assertFalse(self.app._validate_size("1"))
        self.assertFalse(self.app._validate_size("6"))
        self.assertFalse(self.app._validate_size("abc"))
        self.assertFalse(self.app._validate_size("-1"))

    def test_ensure_valid_size_enforces_bounds_and_resets_on_error(self):
        """Ensure _ensure_valid_size clamps values and handles TclError path."""
        # Below minimum -> clamped to 2
        self.app.size_var.set(1)
        self.app._ensure_valid_size()
        self.assertEqual(self.app.size_var.get(), 2)

        # Above maximum -> clamped to 5
        self.app.size_var.set(10)
        self.app._ensure_valid_size()
        self.assertEqual(self.app.size_var.get(), 5)

        # Non-integer value in IntVar -> triggers TclError on get, resets to default (3)
        self.app.size_var.set("abc")
        self.app._ensure_valid_size()
        self.assertEqual(self.app.size_var.get(), 3)


if __name__ == "__main__":
    unittest.main()
