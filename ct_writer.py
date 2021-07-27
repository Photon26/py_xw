length = 120
head = 4
barlength = length - 5
logger = open("C:/Users/GAO/Desktop/fanmade_ct.txt", "w")

for i in range(head+1, length-2):
    logger.write("      <Note Bar=\""+str(i)+"\" length=\"1\" level=\"1\" />\n")

logger.write("\n\n\n")

for i in range(head+1, length-3):
    logger.write("      <ActionList start_bar=\""+str(i)+"\" dance_len=\"1\" seq_len=\"1\" level=\"2\" type=\"\" />\n")

logger.write("      <ActionList start_bar=\""+str(length-3)+"\" dance_len=\"4\" seq_len=\"4\" level=\"2\" type=\"\" />\n")
logger.write("\n\n\n")

for i in range(head+6, barlength+1):
    logger.write("    <Bar>"+str(i)+"</Bar>\n")

