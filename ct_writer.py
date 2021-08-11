# length = 133
# head = 4
# barlength = length - 5
# logger = open("C:/Users/GAO/Desktop/fanmade_ct.txt", "w")
#
# for i in range(head+1, length-2):
#     logger.write("      <Note Bar=\""+str(i)+"\" length=\"1\" level=\"1\" />\n")
#
# logger.write("\n\n\n")
#
# for i in range(head+1, length-3):
#     logger.write("      <ActionList start_bar=\""+str(i)+"\" dance_len=\"1\" seq_len=\"1\" level=\"2\" type=\"\" />\n")
#
# logger.write("      <ActionList start_bar=\""+str(length-3)+"\" dance_len=\"4\" seq_len=\"4\" level=\"2\" type=\"\" />\n")
# logger.write("\n\n\n")
#
# for i in range(head+6, barlength+1):
#     logger.write("    <Bar>"+str(i)+"</Bar>\n")

length = 200
head = 4
stbar = 100
barlength = length - 5
logger = open("C:/Users/GAO/Desktop/fanmade_ct.txt", "w")
#   把这段覆盖sectionseq段落的note行
logger.write("    <Section type=\"note\" startbar=\"" + str(head+1) + "\" endbar=\"" + str(stbar-1) +"\" mark=\"\" param1=\"\" />\n")
logger.write("    <Section type=\"showtime\" startbar=\"" + str(stbar) + "\" endbar=\"" + str(stbar+3) + "\" mark=\"dance\" param1=\"\" />\n")
logger.write("    <Section type=\"note\" startbar=\"" + str(stbar+6) + "\" endbar=\"" + str(length-4) + "\" mark=\"\" param1=\"\" />\n\n\n")


for i in range(head+1, length-2):
    if i == stbar:
        logger.write("      <Note Bar=\"" + str(i) + "\" length=\"4\" level=\"1\" />\n")
    elif stbar < i < stbar + 6:
        pass
    else:
        logger.write("      <Note Bar=\""+str(i)+"\" length=\"1\" level=\"1\" />\n")

logger.write("\n\n\n")

for i in range(head+1, length-3):
    if i == stbar:
        logger.write("      <ActionList start_bar=\""+str(i)+"\" dance_len=\"4\" seq_len=\"4\" level=\"2\" type=\"\" />\n")
    elif stbar < i < stbar + 4:
        pass
    else:
        logger.write("      <ActionList start_bar=\""+str(i)+"\" dance_len=\"1\" seq_len=\"1\" level=\"2\" type=\"\" />\n")

logger.write("      <ActionList start_bar=\""+str(length-3)+"\" dance_len=\"4\" seq_len=\"4\" level=\"2\" type=\"\" />\n")
logger.write("\n\n\n")

for i in range(head+6, barlength+1):
    if stbar-1 < i < stbar + 8:
        pass
    else:
        logger.write("    <Bar>"+str(i)+"</Bar>\n")

logger.write("\n\n\n    <effect name=\"wutai_scene_note_biaozhun_01\" bar=\"" + str(head+1) + "\" length=\"" + str(stbar-head-1) + "\" />\n")
logger.write("    <effect name=\"wutai_scene_note_biaozhun_01\" bar=\"" + str(stbar+4) + "\" length=\"" + str(length-stbar-9) + "\" />")