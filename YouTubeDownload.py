import pytube
import ssl
import subprocess
from sys import platform

bcolors = {
    'HEADER':       '\033[95m',
    'OKBLUE':       '\033[94m',
    'OKGREEN':      '\033[92m',
    'WARNING':      '\033[93m',
    'FAIL':         '\033[91m',
    'ENDC':         '\033[0m',
    'BOLD':         '\033[1m',
    'UNDERLINE':    '\033[4m'
}

tag_youtube_content = {
    '1080P_VIDEO':      '137',
    '720P_VIDEO':       '136',
    '720P_VIDEO_AUDIO': '22',
    '360P_VIDEO_AUDIO': '18'
}


def notify_mac_os(title, text):
    process_call_str = 'terminal-notifier -title "{0}" -message "{1}" -sound default'\
        .format(str(title), str(text))

    subprocess.check_call(process_call_str, shell=True)


def ffmpeg_download(title, url, aurl=None):

    process_call_str = 'ffmpeg -i "{0}" -i "{1}"' \
                       ' -acodec aac -b:a 192k -avoid_negative_ts ' \
                       'make_zero -map 0:v:0 -map 1:a:0 "{2}"' \
        .format(str(url), str(aurl), title + '.mp4')

    return process_call_str


def run():
    ssl._create_default_https_context = ssl._create_unverified_context
    print(bcolors['HEADER'] + 'URL:' + bcolors['WARNING'])
    video = input()
    yt = pytube.YouTube(video)

    title = yt.title

    print(bcolors['HEADER'] + "Name:       " + title)

    url = yt.streams.get_by_itag('137').url  # 1080p

    aurl = yt.streams.get_by_itag('18').url

    process_call_str = ffmpeg_download(title, url, aurl)

    status = subprocess.check_call(process_call_str, shell=True)

    title_app = 'Yotube Download'
    message_status = 'Video loading success: ' + title

    if status:
        message_status = 'Video loading error: ' + title + '\n' + status

    from sys import platform
    if platform == "darwin":
        notify_mac_os(title_app, message_status)


run()

