# Lab 4: VibeCoding

**Project:** Catch the Falling Objects (Pygame)
**AI tool used:** Claude

## Contents
- `before.mp4`: gameplay before any changes (shows the bugs)
- `after.mp4`: gameplay after all fixes and features
- `catch-falling/`: updated source code
- `Claude chat history.pdf`: exported chat history
- Chat link: https://claude.ai/share/19ccc204-a6b1-4aa4-93fd-0696772d224d

## What was done
1. **Collision fix:** catches now require the object to reach basket height, and the catch loop no longer mutates the list it iterates over.
2. **Basket control:** the boundary clamp accounts for the basket's width, so it stays fully on screen.
3. **Controlled spawning:** randomized intervals, varied x positions with a minimum distance from the last spawn, kept inside the screen, with a cap on objects on screen.
4. **Speed boost:** SPACE gives a temporary boost, shown by a gold basket and a HUD bar, followed by a cooldown.

## How to run
cd Lab-4/catch-falling
pip install -r requirements.txt
python main.py