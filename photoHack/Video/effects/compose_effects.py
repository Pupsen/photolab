import moviepy.editor as mp
from moviepy.editor import concatenate_videoclips

from Video.effects.reverse import run as reverse_run
from Video.effects.loop import run as loop_run
from Video.effects.reflection import run as reflection_run


def run(file_dir, target_dir, data):
    data.sort(key=lambda x: x['start'])

    reversed_times, reversed_fragments = [], []
    looped_times, looped_fragments = [], []
    reflected_times, reflected_fragments = [], []
    
    for elem in data:
        if elem['type'] == 'reverse':
            reversed_times.append(elem)
        elif elem['type'] == 'loop':
            looped_times.append(elem)
        elif elem['type'] == 'reflect':
            reflected_times.append(elem)
            
    reversed_fragments = reverse_run(file_dir, reversed_times)
    looped_fragments = loop_run(file_dir, looped_times)
    reflected_fragments = reflection_run(file_dir, reflected_times)

    default_video = mp.VideoFileClip(file_dir)
    start = 0
    end = data[0]['start']
    elements = []

    current_reverse = 0
    current_loop = 0
    current_reflect = 0

    for i, elem in enumerate(data):
        elements.append(default_video.subclip(start, end))
        if elem['type'] == 'reverse':
            elements.append(mp.VideoFileClip(reversed_fragments[current_reverse]))
            current_reverse += 1

            start = elem['start']
            end = None if i == len(data) - 1 else data[i + 1]['start']

        elif elem['type'] == 'loop':
            fragment = mp.VideoFileClip(looped_fragments[current_loop])
            current_loop += 1

            for j in range(elem['count']):
                elements.append(fragment)

            start = elem['end']
            end = None if i == len(data) - 1 else data[i + 1]['start']

        elif elem['type'] == 'reflect':
            elements.append(mp.VideoFileClip(reflected_fragments[current_reflect]))
            current_reflect += 1
            start = elem['end']
            end = None if i == len(data) - 1 else data[i + 1]['start']

    elements.append(default_video.subclip(data[-1]['start']))

    res = concatenate_videoclips(elements)
    res.write_videofile(target_dir)


# times = [
#     {'start': 4, 'end': 5, 'type': 'reverse'},
#     {'start': 5, 'end': 8, 'type': 'reverse'},
#     {'start': 13, 'end': 14, 'type': 'reverse'},
#
#     {'start': 2, 'end': 3, 'type': 'loop', 'count': 3},
#     {'start': 6, 'end': 8, 'type': 'loop', 'count': 3},
#     {'start': 13, 'end': 14, 'type': 'loop', 'count': 3},
#
#     {'start': 2, 'end': 4, 'type': 'reflect'},
#     {'start': 7, 'end': 11, 'type': 'reflect'},
#     {'start': 12, 'end': 14, 'type': 'reflect'},
# ]

# run(test_file_dir, final_path)
