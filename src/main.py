import asyncio
import os
import webbrowser
from time import time as tick
from pypresence import Presence
from mainui import DiscordMediaPresenceUI
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager

async def get_media_info():
    sessions = await MediaManager.request_async()
    if sessions:
        if current_session := sessions.get_current_session():
            if info := await current_session.try_get_media_properties_async():
                info_dict = {attr: getattr(info, attr) for attr in dir(info) if not attr.startswith('_')}
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
        self.mainwindow.resizable(True, False)
    def github(self):
        webbrowser.open("https://github.com/osage-chan/discord-media-presence")

    def set_text(self, id, text):
        return self.builder.get_object(id).config(text=text)

presence = Presence("1266609108455260221")

closing = False
last_tick = 0
update_time = 3
app = DiscordMediaPresence()

def update_or_connect_and_then_update(**kwargs):
    try:
        presence.update(**kwargs)
    except Exception:
        presence.connect()
        presence.update(**kwargs)

def update():
    global last_tick
    if closing:
        os._exit(1)

    if tick() - last_tick <= update_time:
        return
    last_tick = tick()
    if result := asyncio.run(get_media_info()):
        a, b, c = result
        update_presence(a, b, c)

def update_presence(media, timeline, paused):
    song_artist = f"by {media['artist']}"
    tracks = [media["track_number"] + 1, media["album_track_count"] + 1]
    if paused != 5:
        end = ((timeline.last_updated_time + timeline.end_time) - timeline.position).timestamp()
        start = timeline.last_updated_time.timestamp()
        update_or_connect_and_then_update(
            details=media["title"] or "No Song",
            state=song_artist or "Nobody",
            party_size=tracks or [1,1],
            start=start or 0,
            end=end or 0,
            buttons=[{
                "label": "Want this status?",
                "url": "https://github.com/osage-chan/discord-media-presence/releases/latest"
            }]
        )
    else:
        update_or_connect_and_then_update(
            details="Not listening to anything"
        )
    app.set_text("title", media["title"])
    app.set_text("author", song_artist)
    app.set_text("party", f"{tracks[0]} of {tracks[1]}\n")

app.run(update)