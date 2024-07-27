import asyncio
import os
import webbrowser
from time import time as tick
from pypresence import Presence
from mainui import DiscordMediaPresenceUI
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager

async def get_media_info():
    sessions = await MediaManager.request_async()
    if current_session := sessions.get_current_session():
        info = await current_session.try_get_media_properties_async()
        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}
        info_dict['genres'] = list(info_dict['genres'])
        return info_dict, current_session.get_timeline_properties(), current_session.get_playback_info().playback_status

def close():
    global closing
    closing = True

class DiscordMediaPresence(DiscordMediaPresenceUI):
    def __init__(self, master=None):
        super().__init__(master)
        self.mainwindow.protocol("WM_DELETE_WINDOW", close)
        self.mainwindow.iconbitmap("./_internal/icon32.ico")
        self.mainwindow.resizable(False, True)
    def github(self):
        webbrowser.open("https://github.com/osage-chan/discord-media-presence")
        
    def set_text(self,id,text):
        return self.builder.get_object(id).config(text=text)


presence = Presence("1266609108455260221")
presence.connect()

closing = False
last_tick = 0
app = DiscordMediaPresence()

def update():
    if tick() - last_tick <= 7.5:
        return
    last_tick == tick()
    if result := asyncio.run(get_media_info()):
        update_presence(result)


def update_presence(result):
    media, timeline, paused = result

    if closing:
        os._exit(1)
        
    song_artist = f"by {media["artist"]}"
    tracks = [media["track_number"]+1,media["album_track_count"]+1]
    if paused != 5:
        end = (timeline.last_updated_time + timeline.end_time).timestamp()
        start = (timeline.last_updated_time).timestamp()
        presence.update(
            details=media["title"],
            state=song_artist,
            party_size=tracks,
            start=start,
            end=end,
            )
    else:
        presence.update(
            details="Not listening to anything"
        )
    app.set_text("title", media["title"])
    app.set_text("author", song_artist)
    app.set_text("party", f"{tracks[0]} of {tracks[1]}\n")

app.run(update)