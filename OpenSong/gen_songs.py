import os
import pathlib

PATH_SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
PATH_OPENSONG_DIR = PATH_SCRIPT_DIR
PATH_SONGBOOK_DIR = PATH_OPENSONG_DIR.parent


def generate_opensong(path_pro):
    with open(path_pro, "r", encoding="utf-8") as file_pro:
        lines_pro = file_pro.readlines()

    for line_lyrics in lines_pro:
        if "{" in line_lyrics:
            continue

        line_chords = "."
        while "[" in line_lyrics:
            index_open = line_lyrics.index("[")
            index_close = line_lyrics.index("]")
            chord = line_lyrics[index_open + 1 : index_close]
            line_chords[index_open + 1] = chord
            line_lyrics = line_lyrics[:index_open] + line_lyrics[index_close:]


def main():
    generate_opensong(
        PATH_SONGBOOK_DIR
        / "songs"
        / "a legnagyobb ajandek - vartam egy ajandekot mi boldogga tehet.pro"
    )


####################################################################################################

if __name__ == "__main__":
    main()
    print("The script was executed")
