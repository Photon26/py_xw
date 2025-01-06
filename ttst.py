from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips

# Load the video file
video = VideoFileClip("video.mp4")

# Define Part A: Trim a section from the video (e.g., from 0s to 5s)
part_a = video.subclip(0, 5)

# Define Part B: Load a still image and set duration explicitly
# Ensure fps matches the video to prevent frame mismatches
part_b = ImageClip("image.jpg", duration=2)
part_b = part_b.set_fps(24)  # Explicitly set a standard FPS for stability
part_b = part_b.set_duration(2)  # Ensure 2 seconds duration

# Define Part C: Trim another section from the video (e.g., from 10s to 15s)
part_c = video.subclip(10, 15)

# Match the frame rates of all clips
part_a = part_a.set_fps(24)
part_c = part_c.set_fps(24)

# Concatenate the three parts
final_clip = concatenate_videoclips([part_a, part_b, part_c], method="compose")

# Export as a GIF
final_clip.write_gif("output.gif", fps=10)

# Close resources
video.close()
part_b.close()
part_c.close()