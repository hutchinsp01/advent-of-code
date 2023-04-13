import string
import sys
import time
from pathlib import Path

import numpy as np
from day23 import part2vis

LINE_UP = "\033[1A"
LINE_CLEAR = "\x1b[2K"

FONT_FILL = "#"
FONT_BLANK = "."

FILL_CHAR = "\u2588"
BLANK_CHAR = " "

DISPLAY_SIZE_X = 40
DISPLAY_SIZE_Y = 6


def load_font():
    font = (Path(__file__).parent / "font.txt").read_text()
    font_array = np.array([list(line) for line in font.splitlines()])
    chars = f" {string.digits}!{string.ascii_lowercase}{string.ascii_uppercase}"
    return {char: font_array[:, i * 5 : (i + 1) * 5] for i, char in enumerate(chars)}


LETTER_TO_ARRAY = load_font()


def register_range(x_register):
    return range(x_register - 1, x_register + 2)


class Text_Generator:
    def __init__(
        self,
        text,
        size_x=DISPLAY_SIZE_X,
        size_y=DISPLAY_SIZE_Y,
        fill_char=FILL_CHAR,
        blank_char=BLANK_CHAR,
    ):
        self.size_x = size_x
        self.size_y = size_y
        self.blank_char = blank_char
        self.fill_char = fill_char
        self.text_string = text

    def create_text(self):
        text_banner = np.array(
            [[self.blank_char] * 5 * len(self.text_string)] * self.size_y
        )
        for i, letter in enumerate(self.text_string):
            before, after = (self.size_y - 6) // 2, (self.size_y - 6) // 2 + 6
            text_banner[before:after, i * 5 : (i + 1) * 5] = LETTER_TO_ARRAY.get(
                letter, "."
            )
        text_banner[text_banner == FONT_BLANK] = self.blank_char
        text_banner[text_banner == FONT_FILL] = self.fill_char
        return text_banner

    def create_frames(self):
        text_banner = self.create_text()
        frames = []
        for i in range(len(self.text_string) * 5 - self.size_x + 1):
            frame = np.array([[BLANK_CHAR] * self.size_x] * self.size_y)
            frame = text_banner[:, i : self.size_x + i]
            frames.append(frame)
        return frames


class Day23Visualiser:
    def __init__(self, file_name="day23-test.txt"):
        self.file_name = file_name

    def get_output(self):
        self.output = part2vis(self.file_name)

    def get_size(self):
        all_points = set()
        for frame in self.output:
            for point in frame:
                all_points.add(point)
        min_x = min([x.real for x in all_points])
        min_y = min([x.real for x in all_points])
        max_x = max([x.imag for x in all_points])
        max_y = max([x.imag for x in all_points])
        self.size_x = int(max_x - min_x + 1)
        self.size_y = int(max_y - min_y + 1)
        return self.size_x, self.size_y

    def transpose_to_positive(self):
        all_points = set()
        for frame in self.output:
            for point in frame:
                all_points.add(point)
        min_x = min([x.real for x in all_points])
        min_y = min([x.real for x in all_points])
        self.output = [
            [point - min_x - min_y * 1j for point in frame] for frame in self.output
        ]

    def generate_frames(self, frame_size_x, frame_size_y):
        self.transpose_to_positive()
        x_offset = (frame_size_x - self.size_x) // 2
        y_offset = (frame_size_y - self.size_y) // 2

        self.frames = []
        for frame in self.output:
            frame_array = np.array([[BLANK_CHAR] * frame_size_x] * frame_size_y)
            for point in frame:
                x, y = int(point.real), int(point.imag)
                frame_array[y + y_offset, x + x_offset] = FILL_CHAR
            [self.frames.append(frame_array) for _ in range(5)]

        return self.frames


class Video:
    def __init__(
        self,
        size_x=DISPLAY_SIZE_X,
        size_y=DISPLAY_SIZE_Y,
        fill_char=FILL_CHAR,
        blank_char=BLANK_CHAR,
    ):
        self.size_x = size_x
        self.size_y = size_y
        self.blank_char = blank_char
        self.fill_char = fill_char
        self.frames = []
        self.instructions = []

    def add_frame(self, frame):
        self.frames.append(frame)

    def add_frames(self, frames):
        self.frames.extend(frames)

    def add_blank_frames(self, n):
        self.frames.extend(
            [
                np.array([[self.blank_char] * self.size_x] * self.size_y)
                for _ in range(n)
            ]
        )

    def add_fill_frames(self, n):
        self.frames.extend(
            [np.array([[self.fill_char] * self.size_x] * self.size_y) for _ in range(n)]
        )

    def add_text(self, text):
        text_generator = Text_Generator(text, self.size_x, self.size_y)
        self.frames.extend(text_generator.create_frames())

    def create_pixel_list(self):
        return [
            pixel
            for frame in [list(frame.flatten()) for frame in self.frames]
            for pixel in frame
        ]

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
                if self._check_register(
                    x_register, self.get_pixel(pixel_list, i + 2), i + 2
                ):
                    self.instructions.append("noop")
                else:
                    self.instructions.append(
                        f"addx {self._get_next_addx(pixel_list, i, x_register)}"
                    )
                    x_register = x_register + self._get_next_addx(
                        pixel_list, i, x_register
                    )
                    skip = True
            except IndexError:
                pass

    def _screen_size_mod(self, n):
        return n % self.size_x

    def _get_next_addx(self, pixel_list, i, x_register):
        next_x_register = 0
        two_ahead = self.get_pixel(pixel_list, i + 2)
        three_ahead = self.get_pixel(pixel_list, i + 3)
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
    def __init__(
        self,
        size_x=DISPLAY_SIZE_X,
        size_y=DISPLAY_SIZE_Y,
        fill_char=FILL_CHAR,
        blank_char=BLANK_CHAR,
        frame_time=0.1,
    ):
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
        d = "".join(
            [
                f"{''.join(self.display[i:i+self.size_x])}\n"
                for i in range(0, len(self.display), self.size_x)
            ]
        )
        if not initial:
            sys.stdout.write(LINE_UP * self.size_y)
        sys.stdout.write(d)
        sys.stdout.flush()


def videoSubmission():
    day23 = Day23Visualiser()
    day23.get_output()
    x, y = day23.get_size()
    x += 2
    y += 2
    if x < DISPLAY_SIZE_X:
        x = DISPLAY_SIZE_X
    if y < DISPLAY_SIZE_Y:
        y = DISPLAY_SIZE_Y

    day23.generate_frames(frame_size_x=x, frame_size_y=y)
    display = Display(frame_time=0.01, size_x=x, size_y=y)
    video = Video(size_x=x, size_y=y)

    video.add_text("     THIS IS DAY 23 VISUALISED IN DAY 10      ")
    video.add_blank_frames(10)
    video.add_frames(day23.frames)
    video.add_blank_frames(10)
    video.add_text("THANKS FOR WATCHING")

    video.generate_instructions()
    display.run(video.instructions)


videoSubmission()
