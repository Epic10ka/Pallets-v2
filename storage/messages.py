from time import sleep
from rich import print
from rich.panel import Panel



def timer(x = 3, sleep_time = 1, center_value = 0, msg = '', show_msg = False):

    if show_msg:
        print(f'[bright_white]{msg}\n[/]'.center(center_value))

    for c in range(0, x):

        print(f'[bright_white]*[/]'.center(center_value-2))

        sleep(sleep_time)


def error_message(msg):

    print(Panel.fit(msg, title = f'<[red]ERROR[/]>'))


