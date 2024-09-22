import cv2
import numpy as np
import pygame
from moviepy.editor import VideoFileClip

ascii_chars = "@%#*+=-:. "

def frame_to_ascii(frame, cols, rows):
    frame = cv2.resize(frame, (cols, rows))
    colored_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ascii_frame = np.zeros((rows, cols), dtype=str)
    colors = np.zeros((rows, cols, 3), dtype=int)

    for i in range(rows):
        for j in range(cols):
            pixel_value = gray_frame[i, j]
            ascii_index = pixel_value * (len(ascii_chars) - 1) // 255
            ascii_frame[i, j] = ascii_chars[ascii_index]
            colors[i, j] = colored_frame[i, j]
    
    return ascii_frame, colors

def main(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    pygame.init()
    pygame.mixer.init()

    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile("temp_audio.mp3")
    pygame.mixer.music.load("temp_audio.mp3")

    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h

    original_width = int(clip.size[0])
    original_height = int(clip.size[1])

    aspect_ratio = original_width / original_height
    if screen_width / screen_height < aspect_ratio:
        new_width = screen_width
        new_height = int(screen_width / aspect_ratio)
    else:
        new_height = screen_height
        new_width = int(screen_height * aspect_ratio)

    cols = new_width // 10
    rows = new_height // 20

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Courier", 12)

    pygame.mixer.music.play()  

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        ascii_frame, colors = frame_to_ascii(frame, cols, rows)
        screen.fill((0, 0, 0))  

        for i in range(rows):
            for j in range(cols):
                char = ascii_frame[i, j]
                r, g, b = colors[i, j]
                text_surface = font.render(char, True, (r, g, b))
                screen.blit(text_surface, (j * 10, i * 20))

        pygame.display.flip()
        clock.tick(60)  

    cap.release()
    pygame.quit()

if __name__ == "__main__":
    video_path = input("Drop MP4 File here and press ENTER: ")
    main(video_path)
