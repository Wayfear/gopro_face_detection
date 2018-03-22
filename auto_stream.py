import schedule
import time

def job(t):
    import live_stream
    return

schedule.every().day.at("11:59").do(job, 't')

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute