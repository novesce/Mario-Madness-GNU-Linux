"""Hold Paranoia's GNOME wallpaper until the game closes this process's stdin."""

import fcntl
import os
from pathlib import Path
import select
import signal
import sys

from gi.repository import Gio, GLib


def run(image_path):
    parent = os.getppid()

    def finished(timeout):
        readable, _, _ = select.select([sys.stdin], [], [], timeout)
        return bool(readable) or os.getppid() != parent

    image_uri = Path(image_path).resolve(strict=True).as_uri()
    source = Gio.SettingsSchemaSource.get_default()
    schema = source.lookup("org.gnome.desktop.background", True) if source else None
    if not schema or finished(0):
        return

    # Only one game can own the desktop settings at a time.
    lock_path = Path(GLib.get_user_runtime_dir()) / "marios-madness-wallpaper.lock"
    with lock_path.open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return

        settings = Gio.Settings.new_full(schema, None, None)
        targets = {
            key: GLib.Variant("s", image_uri) for key in ("picture-uri", "picture-uri-dark")
            if schema.has_key(key) and settings.is_writable(key)
        }
        if not targets:
            return
        if schema.has_key("picture-options") and settings.get_string("picture-options") == "none":
            targets["picture-options"] = GLib.Variant("s", "zoom")
        if schema.has_key("picture-opacity") and settings.get_int("picture-opacity") == 0:
            targets["picture-opacity"] = GLib.Variant("i", 100)

        original = {}
        settings.delay()
        try:
            for key, value in targets.items():
                if settings.is_writable(key) and settings.get_value(key) != value:
                    previous = settings.get_user_value(key)
                    if settings.set_value(key, value):
                        original[key] = previous
            settings.apply()
            Gio.Settings.sync()
            while not finished(1):
                pass
        finally:
            # Dispatch queued notifications before comparing against the player's settings.
            context = GLib.MainContext.default()
            while context.iteration(False):
                pass
            settings.revert()
            for key, previous in original.items():
                if settings.get_user_value(key) != targets[key]:
                    continue  # The player chose a different wallpaper during the song.
                if previous is None:
                    settings.reset(key)
                else:
                    settings.set_value(key, previous)
            settings.apply()
            Gio.Settings.sync()


if __name__ == "__main__":
    # A session or process-group shutdown should also run the restoration block.
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    signal.signal(signal.SIGHUP, lambda *_: sys.exit(0))
    run(sys.argv[1])
