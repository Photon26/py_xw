from moviepy.editor import *

# cv2 cap.set(), CV_CAP_PROP_POS_MSEC n m s l

def save_Img(viddir, t, savedir):
    clip = (VideoFileClip(viddir).resize((560, 400)))
    clip.save_frame(savedir, t=t)
    clip.close()

if __name__ == "__main__":
    save_Img("H:/vid/s10/bug/g_d_make_126.mp4", 82, "tst.jpg")