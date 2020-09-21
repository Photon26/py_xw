from moviepy.editor import *

def get_gif(viddir, firetime, outputname, dir = ""):
    # cap = cv2.VideoCapture(viddir)
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # cap.release()

    firetime = firetime/1000
    duration = 1.5
    # centertime = frameid/fps
    centertime = firetime
    st = centertime-duration
    et = centertime+duration
    wholeclip = (VideoFileClip(viddir)
                 .subclip(st, et)
                 .resize((560, 400)))
    aclip = (wholeclip
         .subclip(0, duration))

    bclip = (wholeclip
            .to_ImageClip(duration)
            .set_duration(1))

    cclip = (wholeclip
             .subclip(duration, 2*duration))
    L = []
    L.append(aclip)
    L.append(bclip)
    L.append(cclip)

    final_clip = concatenate_videoclips(L)
    final_clip.write_gif(dir + "/" + outputname+".gif", fps=15)
    wholeclip.close()




if __name__ == "__main__":
    import time
    import shutil

    st = time.time()
    get_gif("E:/vid/done/a_d_grand_134.MP4", 60000, "tst_grand", "backup")
    print(time.time()-st)
    shutil.move("E:/vid/done/a_d_grand_134.MP4", "E:/vid/a_d_grand_134.MP4")