import pytube
import ssl
import subprocess

bcolors = {
    'HEADER': '\033[95m',
    'OKBLUE': '\033[94m',
    'OKGREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m'
}


def run():
    ssl._create_default_https_context = ssl._create_unverified_context
    print(bcolors['HEADER'] + 'URL:' + bcolors['WARNING'])
    video = input()
    yt = pytube.YouTube(video, on_progress_callback=progress_function)

    print(bcolors['HEADER'] + "Name:       " + yt.title)

    url = yt.streams.get_by_itag('137').url  # 1080p

    if not url:
        url = yt.streams.get_by_itag('136').url  # 720p

    if not url:
        url = yt.streams.get_by_itag('22').url  # 720p

    aurl = yt.streams.get_by_itag('18').url

    for asd in url:
        print(asd)

    process_call_str = 'ffmpeg -i "{0}" -i "{1}"' \
                       ' -acodec aac -b:a 192k -avoid_negative_ts ' \
                       'make_zero -map 0:v:0 -map 1:a:0 "{2}"' \
        .format(str(url), str(aurl), yt.title + '.mp4')
    status = subprocess.check_call(process_call_str, shell=True)

    return

    downlodRes = '720p'
    streamFile = yt.streams.filter(res='720p', file_extension='mp4').first()

    if not streamFile:
        downlodRes = '480p'
        streamFile = yt.streams.filter(res='480p', file_extension='mp4').first()

    if not streamFile:
        downlodRes = '360p'
        streamFile = yt.streams.filter(res='360p', file_extension='mp4').first()

    if not streamFile:
        print(bcolors['FAIL'] + 'ERROR')
    print('Resolution: ' + downlodRes)
    streamFile.download()
    print(bcolors['OKBLUE'] + '\nDone')


run()
