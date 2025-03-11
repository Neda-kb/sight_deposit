from datetime import datetime

def log_current_time(message):
    current_time = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
    print(f'{current_time}: {message}')