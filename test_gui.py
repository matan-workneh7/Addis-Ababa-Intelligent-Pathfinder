#!/usr/bin/env python3
"""
Simple test for Tkinter GUI.
"""

import tkinter as tk
from tkinter import ttk

def main():
    root = tk.Tk()
    root.title("Test GUI")
    root.geometry("400x300")
    
    label = ttk.Label(root, text="GUI Test - If you see this, Tkinter works!", font=("Arial", 14))
    label.pack(pady=50)
    
    button = ttk.Button(root, text="Test Button", command=lambda: print("Button clicked!"))
    button.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    main()
