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