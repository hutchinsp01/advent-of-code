import sys
import time

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

def print_display(initial=False):
    d = "".join([f"{''.join(display[i:i+40])}\n" for i in range(0, len(display), 40)])
    if not initial:
        sys.stdout.write(LINE_UP * 6)
    sys.stdout.write(d)
    sys.stdout.flush()

def cycle(cycle, display, x_register):
    time.sleep(0.01)
    if (cycle - 1) % 40 in [x_register - 1, x_register, x_register + 1]:
        display[cycle - 1] = "#"
    print_display()
    return (cycle + 1, display)

display = ["." for _ in range(40) for _ in range(6)]
cycle_count = 1
x_register = 1
print_display(initial=True)
for line in open("day10.txt").read().splitlines():
    match line.split(" "):
        case ["noop"]:
            cycle_count, display = cycle(cycle_count, display, x_register)
        case ["addx", s]:
            cycle_count, display = cycle(cycle_count, display, x_register)
            cycle_count, display = cycle(cycle_count, display, x_register)
            x_register += int(s)
