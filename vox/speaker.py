"""TTS speaker using spd-say (Speech Dispatcher with Piper backend)."""

import subprocess
import sys
import termios
import tty
import threading
import time
from typing import Dict, List


class PiperSpeaker:
    def __init__(self, rate: float = 1.0, voice: str = "en_US-male1"):
        self.rate = rate
        self.voice = voice

    def list_voices(self) -> List[Dict[str, str]]:
        try:
            result = subprocess.run(
                ["spd-say", "-L"], capture_output=True, text=True, timeout=5
            )
            voices = []
            for line in result.stdout.strip().split("\n")[1:]:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) >= 3:
                    voices.append(
                        {"id": f"{parts[1]}-{parts[2].lower()}", "name": line.strip()}
                    )
            if not voices:
                voices = [{"id": "en_US-male1", "name": "Piper en_US MALE1 (default)"}]
            return voices
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return [{"id": "en_US-male1", "name": "Piper (default)"}]

    def _say(self, text: str):
        subprocess.run(
            ["spd-say", "-o", "piper", "-r", str(int(self.rate * 100)), "-w", text],
            timeout=30,
        )

    def speak(self, paragraphs: List[str], start: int = 0, quiet: bool = False):
        if not paragraphs:
            return
        stopped = threading.Event()
        paused = threading.Event()
        idx = start

        def input_thread():
            nonlocal idx
            if not sys.stdin.isatty():
                return
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                while not stopped.is_set():
                    ch = sys.stdin.read(1)
                    if ch == " ":
                        if paused.is_set():
                            paused.clear()
                            if not quiet:
                                print(f"\r[SPEAKING] Paragraph {idx + 1}/{len(paragraphs)}    ")
                        else:
                            paused.set()
                            if not quiet:
                                print(f"\r[PAUSED] Paragraph {idx + 1}/{len(paragraphs)}    ")
                    elif ch == "q":
                        stopped.set()
                        paused.clear()
                        if not quiet:
                            print(f"\r[STOPPED] at paragraph {idx + 1}/{len(paragraphs)}")
                    elif ch == "\x1b":
                        seq = sys.stdin.read(2)
                        if seq == "[C":
                            idx = min(idx + 1, len(paragraphs) - 1)
                            paused.set()
                            stopped.set()
                            if not quiet:
                                print(f"\r[SEEK→] Paragraph {idx + 1}/{len(paragraphs)}")
                        elif seq == "[D":
                            idx = max(idx - 1, 0)
                            paused.set()
                            stopped.set()
                            if not quiet:
                                print(f"\r[SEEK←] Paragraph {idx + 1}/{len(paragraphs)}")
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)

        thread = threading.Thread(target=input_thread, daemon=True)
        thread.start()

        while idx < len(paragraphs):
            if stopped.is_set():
                break
            if paused.is_set():
                time.sleep(0.1)
                continue
            if not quiet:
                print(f"\r[SPEAKING] Paragraph {idx + 1}/{len(paragraphs)}    ", end="")
                sys.stdout.flush()
            self._say(paragraphs[idx])
            idx += 1

        stopped.set()
        thread.join(timeout=0.5)
        if not quiet:
            print("")
