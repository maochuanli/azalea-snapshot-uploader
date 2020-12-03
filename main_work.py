import sys, time, datetime
import subprocess
import shlex
import base64

global PROCESS
PROCESS=None

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def run_cmd(cmd):
    eprint('CMD: ' + cmd)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    result = process.communicate()[0]
    eprint('{}'.format(result.decode()))
    return process.returncode, result.decode()

def create_index_html():
    template = '''
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
    <html>
    <head>
    <title>Index of /</title>
    </head>
    <body>
    <h1>Index of /</h1>
    {}
    </ul>
    </body></html>
    '''
    eprint('Creating the index.html file......')
    file_list_content = ''
    rc, out = run_cmd('aws s3 ls s3://cennznet-snapshots.centralityapp.com/')
    lines = out.split('\n')
    for line in lines:
        if len(line) > 0 and line.endswith('chains.tar.gz'):
            file_name = line.split()[-1]
            file_list_content += '<li><a href="{}"> {}</a></li>'.format(file_name)
    index_file_content = template.format(file_list_content)

    with open('/root/index.html', 'w') as f:
        f.write(index_file_content)

    eprint('AWS s3 copy the index.html file......')
    eprint('AWS s3 copy the index.html file......')
    eprint('AWS s3 copy the index.html file......')
    eprint('AWS s3 copy the index.html file......')
    rc, out = run_cmd('aws s3 cp /root/index.html s3://cennznet-snapshots.centralityapp.com/')

def take_snapshot():
    global PROCESS
    now = datetime.datetime.now()
    format = "%Y-%m-%d-%a-%H-%M-%S"
    new_file_name = '{}.chains.tar.gz'.format(now.strftime(format))
    eprint('About to take a snapshot..... it may take 1+ hour {}'.format(now))
    rc, out = run_cmd('/bin/rm -f /mnt/cennznet/*.tar.gz')

    tar_process = subprocess.Popen(['/bin/tar', '-czvf', new_file_name, 'chains'], cwd="/mnt/cennznet")
    tar_process.wait()
    
    rc, out = run_cmd('aws s3 ls s3://cennznet-snapshots.centralityapp.com/')
    eprint('s3 ls exitcode: ', rc)
    rc, out = run_cmd('aws s3 cp /mnt/cennznet/{} s3://cennznet-snapshots.centralityapp.com/'.format(new_file_name))
    eprint('s3 cp exitcode: ', rc)

    eprint('snapshot done!!!!!!!')
    create_index_html()
    eprint('index.html file done!!!!!!!')

def restart_node():
    global PROCESS
    eprint('About to start cennznet Process...')
    PROCESS = subprocess.Popen(['/usr/local/bin/cennznet', '--chain=/cennznet/genesis/azalea.raw.json', '--base-path=/mnt/cennznet', '--name=Snapshot', '--telemetry-url=ws://cennznet-telemetry.centrality.me:8000/submit 0'])

def take_snapshot_and_restart_node():
    global PROCESS
    rc, out = run_cmd('aws sts get-caller-identity')
    if PROCESS is not None:
        try:
            eprint('To Kill the current cennznet Process...')
            PROCESS.kill()
            PROCESS.terminate()
            PROCESS.wait()
            eprint('Process exit code is: {}'.format(PROCESS.returncode))
            take_snapshot()
        except:
            pass
    else:
        eprint('No cennznet Process running...')

    restart_node()

# every Wednesday 09:00 am
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
    if time_tuple.tm_min%5 == 0 and time_tuple.tm_sec >=0 and time_tuple.tm_sec <=6:
        return True
    else:
        return False

def main():
    restart_node()
    while True:
        now = datetime.datetime.now()
        if is_time_for_snapshot_5min(now):
            take_snapshot_and_restart_node()

        time.sleep(5)

if __name__ == '__main__':
    main()