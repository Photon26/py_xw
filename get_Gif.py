from moviepy.editor import *

def get_gif(viddir, firetime, outputname, dir = ""):
    # cap = cv2.VideoCapture(viddir)
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # cap.release()

    firetime = firetime/1000
    duration1 = 1.5
    duration2 = 0.5
    # centertime = frameid/fps
    centertime = firetime
    st = centertime-duration1
    et = centertime+duration2
    wholeclip = (VideoFileClip(viddir)
                 .subclip(st, et)
                 .resize((560, 400)))
    aclip = (wholeclip
             .subclip(0, duration1)
             .speedx(0.5))

    bclip = (wholeclip
             .to_ImageClip(duration1)
             .set_duration(0.8))

    cclip = (wholeclip
             .subclip(duration1, duration1+duration2))
    L = []
    L.append(aclip)
    L.append(bclip)
    L.append(cclip)

    final_clip = concatenate_videoclips(L)
    final_clip.write_gif(dir + "/" + outputname+".gif", fps=10)
    wholeclip.close()




if __name__ == "__main__":
    import time
    import shutil

    st = time.time()
    get_gif("E:/vid/done/a_d_grand_134.MP4", 60000, "tst_grand", "backup")
    print(time.time()-st)
    shutil.move("E:/vid/done/a_d_grand_134.MP4", "E:/vid/a_d_grand_134.MP4")