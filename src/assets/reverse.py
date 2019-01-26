import cv2
import moviepy.editor as mp
from moviepy.editor import concatenate_videoclips
import time as tm
import wave
import os


def reverse_video(path_to_open, path_to_save):
    cap = cv2.VideoCapture(path_to_open)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(path_to_save, fourcc, fps, (width, height))
    frame_list = []

    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            # out.write(frame)
            frame_list.append(frame)

            # cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    for frame in reversed(frame_list):
        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def get_audio(path_to_open, path_to_save):
    clip = mp.VideoFileClip(path_to_open)
    clip.audio.write_audiofile(path_to_save)
    clip.close()


def reverse_audio(path_to_open, path_to_write):
    wavefile_name = path_to_open
    wf = wave.open(wavefile_name, 'rb')

    CHANNELS = wf.getnchannels()
    RATE = wf.getframerate()
    SAMPWIDTH = wf.getsampwidth()

    FRAMES = 1

    full_data = []
    data = wf.readframes(FRAMES)

    while data:
        full_data.append(data)
        data = wf.readframes(FRAMES)

    data = b''.join(full_data[::-1])

    wf = wave.open(path_to_write, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(SAMPWIDTH)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()


def set_audio_to_video(video_path, audio_path, path_to_write):
    videoclip = mp.VideoFileClip(video_path)
    audioclip = mp.AudioFileClip(audio_path)

    videoclip.audio = audioclip
    videoclip.write_videofile(path_to_write)

    return videoclip


def crop_video(default_video, write_path, time_left, time_right):
    videoclip = default_video.subclip(time_left, time_right)
    videoclip.write_videofile(write_path)

    return videoclip


def insert_fragments(default_video, fragments, times):
    elements = []
    start = 0
    end = times[0]['end']

    for i, time in enumerate(times):
        elements.append(default_video.subclip(start, end))
        elements.append(mp.VideoFileClip(fragments[i]))

        start = time['start']
        end = None if i == len(times) - 1 else times[i+1]['end']

    elements.append(default_video.subclip(times[-1]['start']))

    res = concatenate_videoclips(elements)

    return res


def run(file_dir, final_path, times):
    cropped_video_path = 'crop.mp4'
    reversed_video_path = 'output.mp4'
    audio_path = 'output.wav'
    reversed_audio_path = 'reversed_output.wav'
    fragment_path = 'fragment.mp4'

    default_video = mp.VideoFileClip(file_dir)
    fragments = []

    for i, time in enumerate(times):
        print('REVERSE NUMBER:', i)
        crop_video(default_video, cropped_video_path, time['start'], time['end'])
        reverse_video(cropped_video_path, reversed_video_path)
        get_audio(cropped_video_path, audio_path)
        reverse_audio(audio_path, reversed_audio_path)
        fragment = set_audio_to_video(reversed_video_path, reversed_audio_path, fragment_path)

        fragment.write_videofile('fragment' + str(i) + '.mp4')
        fragment.close()

        fragments.append('fragment' + str(i) + '.mp4')

    default_video = insert_fragments(default_video, fragments, times)
    default_video.write_videofile(final_path)
    default_video.close()

    os.remove(reversed_video_path)
    os.remove(audio_path)
    os.remove(reversed_audio_path)
    os.remove(cropped_video_path)

    for fragment in fragments:
        os.remove(fragment)
