import moviepy.editor as mp
from moviepy.editor import concatenate_videoclips
import os


def crop_video(default_video, time_left, time_right):
    videoclip = default_video.subclip(time_left, time_right)
    return videoclip


def insert_fragments(default_video, fragments, times):
    elements = []
    start = 0
    end = times[0]['start']

    for i, time in enumerate(times):
        elements.append(default_video.subclip(start, end))

        fragment = mp.VideoFileClip(fragments[i])

        for j in range(time['count']):
            elements.append(fragment)

        start = time['end']
        end = None if i == len(times) - 1 else times[i+1]['start']

    elements.append(default_video.subclip(times[-1]['end']))

    res = concatenate_videoclips(elements)

    return res


def run(file_dir, final_path, times):
    default_video = mp.VideoFileClip(file_dir)
    fragments = []

    for i, time in enumerate(times):
        fragment = crop_video(default_video, time['start'], time['end'])
        fragment.write_videofile('fragment' + str(i) + '.mp4')
        fragments.append('fragment' + str(i) + '.mp4')

    default_video = insert_fragments(default_video, fragments, times)
    default_video.write_videofile(final_path)
    default_video.close()

    for fragment in fragments:
        os.remove(fragment)


test_file_dir = 'C:\\Users\\stepan.samsonov\\PycharmProjects\\photoHack\Video\\test\\help_lady.mp4'
final_path = 'final.mp4'
times = [
    {'start': 4, 'end': 5, 'count': 1},
    {'start': 5, 'end': 8, 'count': 1},
    {'start': 13, 'end': 14, 'count': 1},
]

run(test_file_dir, final_path, times)
