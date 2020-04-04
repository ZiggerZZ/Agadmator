from pytube import Playlist, YouTube
from pathlib import Path
from absl import flags, app

FLAGS = flags.FLAGS
flags.DEFINE_string('url', None, 'URL of a playlist.')


def download_playlist(url):
    """
    :param url: URL of channel
    :return: None
    """
    if not url:
        print('Please specify an url: python download.py --url=...')
        return
    playlist = Playlist(url)
    playlist_video_dir = Path('videos', playlist.title())
    playlist_video_dir.mkdir()
    playlist_subtitles_dir = Path('subtitles', playlist.title())
    playlist_subtitles_dir.mkdir()
    for video in playlist:
        try:
            yt = YouTube(video)
            video_highest_resolution = yt.streams.get_highest_resolution()
            title = video_highest_resolution.default_filename
            print('Downloading subtitles of', title, '. Url:', video)
            srt = yt.captions['en'].generate_srt_captions()
            with open(Path(playlist_subtitles_dir, title).with_suffix('.srt'), 'w') as f:
                f.write(srt)
            print('Downloading video', title)
            yt.streams.get_highest_resolution().download(output_path=playlist_video_dir)
        except:
            print("Couldn't save ", video)


def main(_):
    download_playlist(FLAGS.url)


if __name__ == '__main__':
    app.run(main)