from pyboxen import boxen


def log(title:str, text:str):
    print(
    boxen(
        text,
        title=title,
        subtitle=":white_check_mark:",
        subtitle_alignment="center",
        color="yellow",
        padding=1,
    )
)

def log_error(title:str, text:str):
    print(
    boxen(
        text,
        title=title,
        subtitle=":x:",
        subtitle_alignment="center",
        color="red",
        padding=1,
    )
)