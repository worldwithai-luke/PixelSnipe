PixelSnipe 🎯
Overview
PixelSnipe is a cutting-edge color-based aim assist tool designed to enhance your gaming experience by detecting green enemy outlines in games like Valorant. Unlike traditional aimbots, PixelSnipe operates without interacting with game memory, making it a safer alternative for players looking to explore aim assist technology. It uses a Raspberry Pi to process screen data and send input, ensuring minimal interference with game files.
This project serves as a proof of concept, demonstrating how color detection and hardware integration can create a seamless aiming experience. PixelSnipe is built for educational purposes and to showcase innovative approaches to gaming automation.



🚀 Getting Started
Prerequisites
To get started with PixelSnipe, you'll need the following:

Raspberry Pi 4
Python (Version 3.9 recommended)
A monitor with HDMI input for Raspberry Pi setup

Setup Instructions

Set Up Your Raspberry Pi:

Flash your Raspberry Pi with the latest Raspberry Pi OS.
Connect it to your monitor and ensure it has internet access.
Follow this guide for initial setup.


Install Python and Dependencies:

Install Python 3.9 on your Raspberry Pi.
Clone the PixelSnipe repository and install dependencies:git clone https://github.com/worldwithai-luke/PixelSnipe.git
cd PixelSnipe
pip install -r requirements.txt




Configure Raspberry Pi as an Input Device:

Use the provided script in the RPiScripts folder to configure your Raspberry Pi as a USB HID device.
Run the script on your Raspberry Pi:python RPiScripts/setup_hid.py


This will allow the Raspberry Pi to emulate a mouse for input.


Run PixelSnipe:

Execute the main script:python main.py


The script will start scanning for green enemy outlines and assist with aiming.



⚙️ Configuration
Customize PixelSnipe to fit your gaming setup:

Enemy Outline Color: Set enemy outlines to GREEN in your game settings.
Field of View (FOV): Adjust the FOV in main.py. The default is optimized for 60 FOV.
Keybinds: Modify keybinds in colorant.py. Check this list for virtual-key codes.

🛠️ Support
Need help? Join our community on Discord to connect with other users and get support:

Special thanks to the open-source community for inspiration, particularly projects like Colorant that paved the way for innovative aim assist tools.
🤝 Contributing
We welcome contributions! If you have ideas, suggestions, or bug reports, please:

Open an issue with detailed information.
Submit a pull request with your changes.
Star ⭐ the repository if you find it useful!

⚠️ Disclaimer

Educational Use OnlyPixelSnipe is intended for educational purposes only. Use it at your own risk.


Risk of BansWhile PixelSnipe avoids memory reading, it may still be detectable by anti-cheat systems. Using aim assist tools can lead to bans and negatively impact the gaming experience for others. We do not endorse cheating in games.


Modify for SafetyTo reduce detection risks, consider modifying the source code or creating your own implementation based on this concept.
