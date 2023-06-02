import subprocess

file = 'GTV/4-yt-play-videos/4-yt-play-videos.py'

for i in range(10):
    print(f"run #{i+1}")
    try:
        subprocess.run(['python3', file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Process {i} failed with error: {e}")

