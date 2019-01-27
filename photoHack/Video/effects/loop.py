import moviepy.editor as mp


def run(file_dir, times):
    default_video = mp.VideoFileClip(file_dir)
    fragments = []

    for i, time in enumerate(times):
        fragment_path = 'fragment-loop-' + str(i) + '.mp4'
        fragment = default_video.subclip(time['start'], time['end'])
        fragment.write_videofile(fragment_path)

        fragments.append(fragment_path)

    default_video.close()
    return fragments
