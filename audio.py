import winsound
import os
import threading

class SoundManager:
    def __init__(self, filename="level_music.wav"):
        self.filename = filename
        self._stop_event = threading.Event()
        self._thread = None
        self.is_playing = False

    def _play_loop(self):
        while not self._stop_event.is_set():
            if os.path.exists(self.filename):
                # Проигрываем .wav файл синхронно в отдельном потоке, не мешая Tkinter
                winsound.PlaySound(self.filename, winsound.SND_FILENAME)
            else:
                break

    def play_level_music(self):
        if self.is_playing:
            return
        if os.path.exists(self.filename):
            self.is_playing = True
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._play_loop, daemon=True)
            self._thread.start()

    def pause_music(self):
        if self.is_playing:
            self._stop_event.set()
            winsound.PlaySound(None, winsound.SND_ASYNC)
            self.is_playing = False

    def resume_music(self):
        self.play_level_music()

    def stop_music(self):
        if self.is_playing:
            self._stop_event.set()
            winsound.PlaySound(None, winsound.SND_ASYNC)
            self.is_playing = False