"""Run with python3 tests/test_gnome_wallpaper.py on a system with GNOME schemas and PyGObject."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import time


def check_wallpaper(directory):
    # Select a private settings database before importing GIO or launching the helper.
    os.environ.update(GSETTINGS_BACKEND="keyfile", XDG_CONFIG_HOME=str(directory),
                      XDG_RUNTIME_DIR=str(directory), XDG_CACHE_HOME=str(directory),
                      DBUS_SESSION_BUS_ADDRESS=f"unix:path={directory}/no-session-bus")
    from gi.repository import Gio, GLib

    repo = Path(__file__).resolve().parents[1]
    image = directory / "game's wallpaper #1.png"
    shutil.copyfile(repo / "assets/preload/images/toolate.png", image)
    command = [sys.executable, "-I", str(repo / "linux/gnome-wallpaper.py"), str(image)]
    settings = Gio.Settings.new("org.gnome.desktop.background")
    light, dark = "picture-uri", "picture-uri-dark"
    original = "file:///original.jpg"
    settings.set_string(light, original)
    settings.set_string("picture-options", "none")
    settings.set_int("picture-opacity", 0)
    Gio.Settings.sync()

    def expect(light_uri, dark_uri):
        deadline = time.monotonic() + 5
        while True:
            while GLib.MainContext.default().iteration(False):
                pass
            # A missing user value means this key still follows its schema default.
            values = [settings.get_user_value(key) for key in (light, dark)]
            actual = [value.unpack() if value is not None else None for value in values]
            if actual == [light_uri, dark_uri]:
                return
            if time.monotonic() >= deadline:
                raise AssertionError(f"Expected {[light_uri, dark_uri]}, found {actual}")
            time.sleep(0.02)

    with subprocess.Popen(command, stdin=subprocess.PIPE) as helper:
        expect(image.as_uri(), image.as_uri())
        assert settings.get_string("picture-options") == "zoom"
        assert settings.get_int("picture-opacity") == 100
        with subprocess.Popen(command, stdin=subprocess.PIPE) as second:
            assert second.wait(timeout=5) == 0
        expect(image.as_uri(), image.as_uri())
        helper.stdin.close()
        assert helper.wait(timeout=5) == 0
    expect(original, None)
    assert settings.get_string("picture-options") == "none"
    assert settings.get_int("picture-opacity") == 0

    # Killing this client closes its pipe to the helper, just as a game crash does.
    client = """import subprocess, sys
helper = subprocess.Popen(sys.argv[1:], stdin=subprocess.PIPE)
sys.stdin.read()
"""
    with subprocess.Popen([sys.executable, "-c", client, *command], stdin=subprocess.PIPE) as game:
        expect(image.as_uri(), image.as_uri())
        settings.set_string(light, "file:///players-new-choice.jpg")
        Gio.Settings.sync()
        game.kill()
        game.wait(timeout=5)
    expect("file:///players-new-choice.jpg", None)


def test_gnome_wallpaper():
    # An external test runner may have already initialized its own GSettings backend.
    subprocess.run([sys.executable, "-I", __file__], check=True)


if __name__ == "__main__":
    with TemporaryDirectory() as tmp:
        check_wallpaper(Path(tmp))
    print("GNOME wallpaper tests passed")
