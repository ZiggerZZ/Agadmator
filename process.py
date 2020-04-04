import pysrt
from moviepy.editor import *
from pathlib import Path
from absl import flags, app

FLAGS = flags.FLAGS
flags.DEFINE_string('phrase', 'hello everyone', 'Phrase to search.')

HELLO_EVERYONE = 'hello everyone'
SORRY_ABOUT_THAT = 'sorry about that'
COMPLETELY_NEW_GAME = 'completely new game'
CAPTURES_CAPTURES_AND_CAPTURES = 'captures captures and captures'
GIVE_YOU_A_COUPLE_OF_SECONDS = "give you a couple of seconds"
ENJOY_THE_SHOW = 'enjoy the show'
# may be need to take the sub before to get the whole phrase
# may be also need to watch 2-grams of subs to get the phrase if it's not found

def get_time(sub_time):
    return sub_time.hours, sub_time.minutes, sub_time.seconds + 0.0001 * sub_time.milliseconds


def extract_subtitles_time(file, phrase):
    """
    file - srt file
    """
    subs = pysrt.open(file)
    times = []

    for sub in subs:
        if phrase in sub.text:
            times.append((sub.start, sub.end))
            # break

    return times

#TODO: add handling of same videos in different directories
def concatenate_clips(phrase):
    """
    Concatenates extracts from videos from videos/ directory
    """
    subtitles = Path('subtitles/')
    compilations = Path('compilations/')
    clips = []
    names = set()
    for videos in Path('videos/').iterdir():
        print(videos)
        for video in videos.glob('*.mp4'):
            clip = VideoFileClip(str(video))
            name = video.stem
            if name not in names:
                times = extract_subtitles_time((subtitles/videos.stem/name).with_suffix('.srt'), phrase)
                for time in times:
                    start, end = time
                    new_clip = clip.subclip(get_time(start), get_time(end))
                    clips.append(new_clip)
                names.add(name)
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(str((compilations / phrase).with_suffix('.mp4')))


def main(_):
    concatenate_clips(FLAGS.phrase)


if __name__ == '__main__':
    app.run(main)
