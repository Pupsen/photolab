import cv2
import moviepy.editor as mp


def reflect_video(path_to_open, path_to_save):
    cap = cv2.VideoCapture(path_to_open)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(path_to_save, fourcc, fps, (width, height))

    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.flip(frame, 1)
            out.write(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def get_audio(path_to_open, path_to_save):
    clip = mp.VideoFileClip(path_to_open)
    clip.audio.write_audiofile(path_to_save)
    clip.close()


def set_audio_to_video(video_path, audio_path):
    videoclip = mp.VideoFileClip(video_path)
    audioclip = mp.AudioFileClip(audio_path)
    videoclip.audio = audioclip
    return videoclip


def crop_video(default_video, write_path, time_left, time_right):
    videoclip = default_video.subclip(time_left, time_right)
    videoclip.write_videofile(write_path)


def run(file_dir, times):
    cropped_video_path = 'crop.mp4'
    reflected_video_path = 'output.mp4'
    audio_path = 'output.wav'

    default_video = mp.VideoFileClip(file_dir)
    fragments = []

    for i, time in enumerate(times):
        crop_video(default_video, cropped_video_path, time['start'], time['end'])
        reflect_video(cropped_video_path, reflected_video_path)
        get_audio(cropped_video_path, audio_path)
        fragment = set_audio_to_video(reflected_video_path, audio_path)
        fragment.write_videofile('fragment-reflection-' + str(i) + '.mp4')
        # fragment.close()
        fragments.append('fragment-reflection-' + str(i) + '.mp4')

    default_video.close()
    return fragments
