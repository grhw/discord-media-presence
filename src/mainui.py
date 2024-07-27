#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "main.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class DiscordMediaPresenceUI:
    def __init__(self, master=None):
        self.builder = pygubu.Builder()
        self.builder.add_resource_paths(RESOURCE_PATHS)
        self.builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Tk = self.builder.get_object("tk1", master)
        self.builder.connect_callbacks(self)

    def run(self,callback):
        while True:
            callback()
            self.mainwindow.update()


    def github(self):
        pass


if __name__ == "__main__":
    app = DiscordMediaPresenceUI()
    app.run()
