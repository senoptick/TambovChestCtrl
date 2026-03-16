import vlc
import os
import random
import keyboard
import time
import sys

VIDEO_FOLDER = "videos"
BLACK_FILE = "black.mp4"  #

videos = [os.path.join(VIDEO_FOLDER, f) for f in os.listdir(VIDEO_FOLDER) if f.endswith(".mp4")]

instance = vlc.Instance("--fullscreen", "--no-video-deco", "--video-on-top", "--input-repeat=99999")
player = instance.media_player_new()

playlist = []
current_index = 0
last_video_previous_playlist = None
lid_open = False

def generate_playlist():
    global playlist, last_video_previous_playlist
    if len(videos) <= 1:
        playlist[:] = videos
    else:
        while True:
            new_playlist = videos.copy()
            random.shuffle(new_playlist)
            if last_video_previous_playlist is None or new_playlist[0] != last_video_previous_playlist:
                break
        playlist[:] = new_playlist

def play_video(path):
    media = instance.media_new(path)
    player.set_media(media)
    player.play()
    time.sleep(0.3)
    player.set_fullscreen(True)

generate_playlist()

play_video(BLACK_FILE)

while True:
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN:
        
        if event.name == "2":  
            if not lid_open:
                lid_open = True
                if current_index >= len(playlist):
                    last_video_previous_playlist = playlist[-1]
                    generate_playlist()
                    current_index = 0
                play_video(playlist[current_index])
            time.sleep(0.2)
    
        if event.name == "1": 
            if lid_open:
                lid_open = False
                play_video(BLACK_FILE)
                current_index += 1
            time.sleep(0.2)
    
        if event.name == "3": 
            player.stop()
            sys.exit(0)
    
        if lid_open and playlist:
            state = player.get_state()
            if state in [vlc.State.Ended, vlc.State.Stopped, vlc.State.Error]:
                play_video(playlist[current_index % len(playlist)])
    
        time.sleep(0.05)
