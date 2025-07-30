import subprocess

def launch_keyboard():
    try:
        subprocess.Popen(["matchbox-keyboard"])
    except Exception as e:
        print("Failed to launch keyboard:", e)


def close_keyboard():
    try:
        subprocess.call(["pkill", "matchbox-keyboard"])
    except Exception as e:
        print("Failed to close keyboard:", e)
