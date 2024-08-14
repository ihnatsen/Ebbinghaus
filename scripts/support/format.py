__COLOURS_DICT = {
    "red": (204, 50, 50),
    "green": (0, 102, 0),
    "blue": (0, 65, 204),
    "yellow": (255, 255, 0),
    "orange": (204, 102, 0),
    "purple": (128, 0, 128),
    "cyan": (0, 255, 255),
    "pink": (255, 0, 153)}
__NONE_ANSI = "\u001b[0m"


def paint(string, rgb: list | str) -> str:
    string = str(string)
    colour = None
    match rgb:
        case str() as name:
            if __COLOURS_DICT.get(name):
                colour = '\033[38;2;{};{};{}m'.format(*__COLOURS_DICT[name])
            else:
                return string
        case list():
            colour = '\033[38;2;{};{};{}m'.format(*rgb)

    return f'{colour}{string}{__NONE_ANSI}'


__all__ = ['paint']
