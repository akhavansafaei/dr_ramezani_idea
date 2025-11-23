#!/usr/bin/env python3
"""
Quick Launcher for Computer Vision System
Choose your preferred interface
"""

import sys
import os


def print_banner():
    """Print welcome banner"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║    🎥  Computer Vision System - Budget Friendly  🎥      ║
║                                                           ║
║         Multi-Feature Face Analysis with AI               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)


def print_menu():
    """Print menu options"""
    print("\nChoose an interface to launch:\n")
    print("  1. 🖥️  Desktop GUI      (Recommended for real-time)")
    print("                        - Professional dark theme interface")
    print("                        - Real-time video processing")
    print("                        - Live controls and statistics\n")

    print("  2. 🌐  Web Interface    (Modern & shareable)")
    print("                        - Beautiful browser-based UI")
    print("                        - Process images and videos")
    print("                        - Share with others\n")

    print("  3. ⌨️  Command Line     (Lightweight)")
    print("                        - Terminal-based processing")
    print("                        - Minimal resource usage")
    print("                        - Automation friendly\n")

    print("  4. ℹ️  Help & Docs      (Learn more)")
    print("  5. ❌  Exit\n")


def launch_desktop_gui():
    """Launch desktop GUI"""
    print("\n🚀 Launching Desktop GUI...")
    print("   Close the window to return here.\n")
    os.system("python gui_app.py")


def launch_web_interface():
    """Launch web interface"""
    print("\n🚀 Launching Web Interface...")
    print("   Opening on http://localhost:7860")
    print("   Press Ctrl+C to stop the server.\n")
    os.system("python web_app.py")


def launch_command_line():
    """Show command line options"""
    print("\n⌨️  Command Line Options:\n")
    print("Basic usage:")
    print("  python main.py\n")

    print("With webcam and auto-optimization:")
    print("  python main.py --auto-optimize --target-fps 15\n")

    print("Process a video file:")
    print("  python main.py --source video.mp4\n")

    print("Disable specific features:")
    print("  python main.py --disable emotion_detection pose_detection\n")

    print("All options:")
    print("  python main.py --help\n")

    input("Press Enter to return to menu...")


def show_help():
    """Show help and documentation"""
    print("\n📚 Documentation:\n")
    print("  README.md           - Complete project documentation")
    print("  UI_GUIDE.md         - User interface guide")
    print("  QUICKSTART.md       - Quick start guide")
    print("  PROJECT_SUMMARY.md  - Project overview\n")

    print("💡 Quick Tips:\n")
    print("  • Desktop GUI: Best for real-time webcam processing")
    print("  • Web Interface: Best for demos and sharing")
    print("  • Command Line: Best for batch processing\n")

    print("  • Enable auto-optimize for low-end systems")
    print("  • Disable heavy features (emotion, pose) for better FPS")
    print("  • Use GPU (CUDA) for best performance\n")

    print("🆘 Troubleshooting:\n")
    print("  • Low FPS? Enable auto-optimize")
    print("  • GPU not detected? Check PyTorch CUDA installation")
    print("  • Webcam not working? Try different source number (--source 1)\n")

    print("🔗 Online Resources:\n")
    print("  • GitHub: Check repository for updates")
    print("  • Issues: Report bugs on GitHub")
    print("  • Docs: Read markdown files in project folder\n")

    input("Press Enter to return to menu...")


def main():
    """Main launcher function"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner()
        print_menu()

        try:
            choice = input("Enter your choice (1-5): ").strip()

            if choice == '1':
                launch_desktop_gui()
            elif choice == '2':
                launch_web_interface()
            elif choice == '3':
                launch_command_line()
            elif choice == '4':
                show_help()
            elif choice == '5':
                print("\n👋 Goodbye! Thanks for using Computer Vision System.\n")
                sys.exit(0)
            else:
                print("\n❌ Invalid choice. Please enter a number between 1 and 5.")
                input("Press Enter to continue...")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using Computer Vision System.\n")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("Press Enter to continue...")


if __name__ == '__main__':
    main()
