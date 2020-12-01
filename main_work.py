import sys, time, datetime
import subprocess
import shlex
import base64

global PROCESS
PROCESS=None

def take_snapshot():
    global PROCESS
    now = datetime.datetime.now()
    print(now, 'Here i\'m about to take a snapshot..... it may take 1+ hour ')
    time.sleep(30)
    print('snapshot done!!!!!!!')

def restart_node():
    global PROCESS
    CMD = '/usr/local/bin/cennznet --chain=/cennznet/genesis/azalea.raw.json --base-path=/mnt/cennznet'
    PROCESS = subprocess.Popen(['/usr/local/bin/cennznet', '--chain=/cennznet/genesis/azalea.raw.json', '--base-path=/mnt/cennznet', '--name=Snapshot', '--telemetry-url=ws://cennznet-telemetry.centrality.me:8000/submit 0'])

def take_snapshot_and_restart_node():
    global PROCESS
    if PROCESS is not None:
        try:
            PROCESS.kill()
            PROCESS.terminate()
        except:
            pass
    
    take_snapshot()
    restart_node()

# every Monday 09:00 am
def is_time_for_snapshot(now_datetime):
    time_tuple  = now_datetime.timetuple()
    weekday = now_datetime.weekday()
    if weekday == 2 and time_tuple.tm_hour == 9 and time_tuple.tm_min == 0 and time_tuple.tm_sec >=0 and time_tuple.tm_sec <=10:
        return True
    else:
        return False

# every 5 minutes
def is_time_for_snapshot_5min(now_datetime):
    time_tuple  = now_datetime.timetuple()
    weekday = now_datetime.weekday()
    if time_tuple.tm_min%5 == 0 and time_tuple.tm_sec >=0 and time_tuple.tm_sec <=6:
        return True
    else:
        return False

def main():
    while True:
        now = datetime.datetime.now()
        if is_time_for_snapshot_5min(now):
            take_snapshot_and_restart_node()
        else:
            time.sleep(5)

if __name__ == '__main__':
    main()