import string
import sys
import time
from pathlib import Path

import numpy as np
from constants import *


def load_font():
    font = (Path(__file__).parent / "font.txt").read_text()
    font_array = np.array([list(line) for line in font.splitlines()])
    chars = f" {string.digits}!{string.ascii_lowercase}{string.ascii_uppercase}"
    return {char: font_array[:, i * 5: (i + 1) * 5] for i, char in enumerate(chars)}

LETTER_TO_ARRAY = load_font()

def register_range(x_register):
    return range(x_register - 1, x_register + 2)

class Text_Generator:
    def __init__(self, text, size_x=DISPLAY_SIZE_X, size_y=DISPLAY_SIZE_Y, fill_char=FILL_CHAR, blank_char=BLANK_CHAR):
        self.size_x = size_x
        self.size_y = size_y
        self.blank_char = blank_char
        self.fill_char = fill_char
        self.text_string = text

    def create_text(self):
        text_banner = np.array([[self.fill_char] * 5 * len(self.text_string)] * self.size_y)
        for i, letter in enumerate(self.text_string):
            text_banner[:, i * 5: (i + 1) * 5] = LETTER_TO_ARRAY.get(letter, ".")
        text_banner[text_banner == FONT_BLANK] = self.blank_char
        text_banner[text_banner == FONT_FILL] = self.fill_char
        return text_banner

    def create_frames(self):
        text_banner = self.create_text()
        frames = []
        for i in range(len(self.text_string) * 5 - self.size_x + 1):
            frame = np.array([[BLANK_CHAR] * self.size_x] * self.size_y)
            frame = text_banner[:, i: self.size_x + i]
            frames.append(frame)
        return frames


class Video:
    def __init__(self, size_x=DISPLAY_SIZE_X, size_y=DISPLAY_SIZE_Y, fill_char=FILL_CHAR, blank_char=BLANK_CHAR):
        self.size_x = size_x
        self.size_y = size_y
        self.blank_char = blank_char
        self.fill_char = fill_char
        self.frames = []
        self.instructions = []

    def add_frame(self, frame):
        self.frames.append(frame)

    def add_blank_frames(self, n):
        self.frames.extend([np.array([[self.blank_char] * self.size_x] * self.size_y) for _ in range(n)])

    def add_fill_frames(self, n):
        self.frames.extend([np.array([[self.fill_char] * self.size_x] * self.size_y) for _ in range(n)])

    def add_test_frames(self, n):
        self.frames.extend([np.array([[self.fill_char, self.blank_char] * self.size_x] * self.size_y) for _ in range(n // 2)])
        self.frames.extend([np.array([[self.fill_char, self.blank_char, self.blank_char] * self.size_x] * self.size_y) for _ in range(n // 3)])
        self.frames.extend([np.array([[self.fill_char, self.blank_char, self.blank_char, self.blank_char] * self.size_x] * self.size_y) for _ in range(n // 4)])
        self.frames.extend([np.array([[self.blank_char, self.fill_char, self.fill_char] * self.size_x] * self.size_y) for _ in range(n //3)])
        self.frames.extend([np.array([[self.blank_char, self.fill_char, self.fill_char, self.fill_char] * self.size_x] * self.size_y) for _ in range(n // 4)])

    def add_text(self, text):
        text_generator = Text_Generator(text)
        self.frames.extend(text_generator.create_frames())

    def create_pixel_list(self):
        return [pixel for frame in [list(frame.flatten()) for frame in self.frames] for pixel in frame]

    def get_pixel(self, list, n):
        return list[n - 1]

    def generate_instructions(self):
        pixel_list = self.create_pixel_list()
        x_register = 1
        self.instructions = []
        skip = False
        for i, _ in enumerate(pixel_list, start=1):
            if skip:
                skip = False
                continue
            try:
                if self._check_register(x_register, self.get_pixel(pixel_list, i+2), i+2):
                    self.instructions.append("noop")
                else:
                    self.instructions.append(f"addx {self._get_next_addx(pixel_list, i, x_register)}")
                    x_register = (x_register + self._get_next_addx(pixel_list, i, x_register))
                    skip = True
            except IndexError:
                pass

    def _screen_size_mod(self, n):
        return n % self.size_x

    def _get_next_addx(self, pixel_list, i, x_register):
        next_x_register = 0
        two_ahead = self.get_pixel(pixel_list, i+2)
        three_ahead = self.get_pixel(pixel_list, i+3)
        if two_ahead == self.fill_char and three_ahead == self.blank_char:
            next_x_register = i
        if two_ahead == self.fill_char and three_ahead == self.fill_char:
            next_x_register = i + 1
        if two_ahead == self.blank_char and three_ahead == self.fill_char:
            next_x_register = i + 2
        if two_ahead == self.blank_char and three_ahead == self.blank_char:
            next_x_register = i + 4

        normalised_x_register = self._screen_size_mod(next_x_register)
        return normalised_x_register - x_register

    def _check_register(self, x_register, pixel, tick):
        if self._screen_size_mod(tick) in register_range(x_register):
            return pixel == self.fill_char
        return pixel == self.blank_char


class Display:
    def __init__(self, size_x=DISPLAY_SIZE_X, size_y=DISPLAY_SIZE_Y, fill_char=FILL_CHAR, blank_char=BLANK_CHAR, frame_time=0.1):
        self.display = [blank_char for _ in range(size_x) for _ in range(size_y)]
        self.size_x = size_x
        self.size_y = size_y
        self.blank_char = blank_char
        self.fill_char = fill_char
        self.frame_time = frame_time
        self.cycle_count = 1
        self.x_register = 1

    def _screen_size_mod(self, n):
        return n % self.size_x

    def cycle(self):
        time.sleep(self.frame_time / (self.size_x * self.size_y))
        calc_cycle = self.cycle_count % (self.size_x * self.size_y)
        if self._screen_size_mod(calc_cycle - 1) in register_range(self.x_register):
            self.display[calc_cycle - 1] = FILL_CHAR
        else:
            self.display[calc_cycle - 1] = BLANK_CHAR
        self.print_display()
        self.cycle_count += 1

    def run(self, instructions):
        self.cycle_count = 1
        self.x_register = 1
        self.print_display(initial=True)
        for instruction in instructions:
            match instruction.split(" "):
                case ["noop"]:
                    self.cycle()
                case ["addx", s]:
                    self.cycle()
                    self.cycle()
                    self.x_register += int(s)

    def print_display(self, initial=False):
        d = "".join([f"{''.join(self.display[i:i+self.size_x])}\n" for i in range(0, len(self.display), self.size_x)])
        if not initial:
            sys.stdout.write(LINE_UP * self.size_y)
        sys.stdout.write(d)
        sys.stdout.flush()

display = Display(frame_time=0.01)
video = Video()
video.add_blank_frames(5)
video.add_text("  BARNSEY DONT LIE, THIS IS A GREAT VIDEO ")
video.generate_instructions()
display.run(video.instructions)
# print(video.instructions)
