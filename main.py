#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BLK-REV Extractor Pro
Main entry point with support for both Tkinter and PyQt5 interfaces

Usage:
    python main.py           # Launch default GUI (PyQt5 if available, else Tkinter)
    python main.py --tk      # Force Tkinter interface
    python main.py --cli     # Command line interface
"""

import sys
import os
import argparse

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def check_pyqt5():
    """Check if PyQt5 is available"""
    try:
        import PyQt5
        return True
    except ImportError:
        return False


def run_pyqt5():
    """Run PyQt5 interface"""
    try:
        from frontend.main_window_pyqt5 import main as pyqt_main
        return pyqt_main()
    except Exception as e:
        print(f"Error starting PyQt5 interface: {e}")
        return 1


def run_tkinter():
    """Run Tkinter interface"""
    try:
        import tkinter as tk
        from tkinter import messagebox
        from frontend.main_window import MainWindow
        from utils.config_manager import ConfigManager
        from utils.logger import AppLogger

        root = tk.Tk()
        root.title("BLK-REV Extractor Pro v1.0")

        # Initialize systems
        config = ConfigManager()
        logger = AppLogger()
        logger.info("Starting BLK-REV Extractor Pro (Tkinter mode)")

        # Create main window
        try:
            app = MainWindow(root)
            logger.info("Main window created successfully")
            root.mainloop()
        except Exception as e:
            logger.error(f"Failed to create main window: {e}")
            messagebox.showerror("Fatal Error", str(e))
            return 1
        finally:
            logger.info("Application closing")

        return 0

    except Exception as e:
        print(f"Error starting Tkinter interface: {e}")
        return 1


def run_cli():
    """Run command line interface"""
    try:
        import cli
        return cli.main()
    except Exception as e:
        print(f"Error starting CLI: {e}")
        return 1


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="BLK-REV Extractor Pro - Data extraction tool"
    )
    parser.add_argument(
        "--tk", "--tkinter",
        action="store_true",
        help="Use Tkinter interface (default: auto-detect)"
    )
    parser.add_argument(
        "--qt", "--pyqt",
        action="store_true",
        help="Use PyQt5 interface (default: auto-detect)"
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Use command line interface"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    args = parser.parse_args()

    # Determine interface to use
    if args.cli:
        return run_cli()
    elif args.tk:
        return run_tkinter()
    elif args.qt:
        if check_pyqt5():
            return run_pyqt5()
        else:
            print("PyQt5 not installed. Falling back to Tkinter...")
            return run_tkinter()
    else:
        # Auto-detect: prefer PyQt5 if available
        if check_pyqt5():
            print("Starting PyQt5 interface...")
            return run_pyqt5()
        else:
            print("PyQt5 not found. Starting Tkinter interface...")
            return run_tkinter()


if __name__ == "__main__":
    sys.exit(main())
