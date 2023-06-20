"""
Script for processing .pro files in current folder
"""

import os
import pathlib
import shutil

PATH_SCRIPT_DIR = pathlib.Path(__file__).resolve().parent

LOG = []


def loginfo(message):
    """
    Printing and storing log info
    """

    global LOG
    LOG.append(f"{message}\n")
    print(message)


def get_tag(tag, text_full, filename):
    """
    Getting the text of a specific tag
    """

    tag_opener = "{" + f"{tag}:"
    if tag_opener in text_full:
        index_tag_start = text_full.index(tag_opener)
        index_tag_end = text_full.index("}", index_tag_start) + 1
        text_tag = text_full[index_tag_start:index_tag_end]
        value_tag = text_full[index_tag_start + len(tag_opener) : index_tag_end - 1]
    else:
        text_tag = "{" + f"{tag}:" + "}"
        value_tag = ""

    if "" == value_tag:
        loginfo(f"INFO_4 The {tag} is missing in {filename}")

    return text_tag


def preprocess_pro(path_dir, filename):
    """
    Function for preprocessing .pro files
    """

    with open(path_dir / filename, "r", encoding="utf-8") as file_pro:
        text_pro_in = file_pro.read()

    text_pro_out = text_pro_in

    while " \n" in text_pro_out:
        text_pro_out = text_pro_out.replace(" \n", "\n")

    while "{ " in text_pro_out:
        text_pro_out = text_pro_out.replace("{ ", "{")

    while " {" in text_pro_out:
        text_pro_out = text_pro_out.replace(" {", "{")

    while " }" in text_pro_out:
        text_pro_out = text_pro_out.replace(" }", "}")

    while "} " in text_pro_out:
        text_pro_out = text_pro_out.replace("} ", "}")

    text_title = get_tag("title", text_pro_out, filename)
    text_pro_out = text_pro_out.replace(text_title, "")
    text_subtitle = get_tag("subtitle", text_pro_out, filename)
    text_pro_out = text_pro_out.replace(text_subtitle, "")
    text_key = get_tag("key", text_pro_out, filename)
    text_pro_out = text_pro_out.replace(text_key, "")
    text_pro_out = f"{text_title}\n{text_subtitle}\n{text_key}\n\n{text_pro_out}"

    text_artist = get_tag("artist", text_pro_out, filename)
    if "{artist:}" == text_artist:
        text_pro_out = f"{text_pro_out}\n/{text_artist}"

    # while "}\n\n" in text_pro_out:
    #    text_pro_out = text_pro_out.replace("}\n\n", "}\n")
    # text_pro_out = text_pro_out.replace("{end_of_chorus}", "{end_of_chorus}\n")
    # text_pro_out = text_pro_out.replace("{end_of_tab}", "{end_of_tab}\n")
    # text_pro_out = text_pro_out.replace("{comment:", "\n{comment:", 1)

    while " :" in text_pro_out:
        text_pro_out = text_pro_out.replace(" :", ":")

    while "title: " in text_pro_out:
        text_pro_out = text_pro_out.replace("title: ", "title:")
    while "subtitle: " in text_pro_out:
        text_pro_out = text_pro_out.replace("subtitle: ", "subtitle:")
    while "key: " in text_pro_out:
        text_pro_out = text_pro_out.replace("key: ", "key:")
    while "comment: " in text_pro_out:
        text_pro_out = text_pro_out.replace("comment: ", "comment:")
    text_pro_out = text_pro_out.replace("Capo:", "Capo: ")
    text_pro_out = text_pro_out.replace("artist:", "artist: ")

    if "/{artist:" in text_pro_out:
        index_artist_closer = text_pro_out.index("}", text_pro_out.index("{artist:"))
        text_pro_out = (
            text_pro_out[:index_artist_closer]
            + " "
            + text_pro_out[index_artist_closer:]
        )
    else:
        loginfo(f"INFO_6 The artist is missing in {filename}")
    if 1 < text_pro_out.count("/{artist:"):
        loginfo(f"INFO_7 The artist is multiplified in {filename}")

    while "  " in text_pro_out:
        text_pro_out = text_pro_out.replace("  ", " ")

    while "\n\n\n" in text_pro_out:
        text_pro_out = text_pro_out.replace("\n\n\n", "\n\n")

    if text_pro_in != text_pro_out:
        with open(path_dir / filename, "w", encoding="utf-8") as file_pro:
            file_pro.write(text_pro_out)


def process_pro(path_dir, filename):
    """
    Function for processing .pro files
    """

    preprocess_pro(path_dir, filename)

    with open(path_dir / filename, "r", encoding="utf-8") as file_pro:
        lines_pro = file_pro.readlines()

    number_line = 0
    for line in lines_pro:
        number_line += 1

        if 1 == number_line:
            if "{title:" not in line:
                loginfo(f"INFO_1 The title is missing in {filename}")
            else:
                index_start = line.index(":") + 1
                title = line[index_start:-2]

        if 2 == number_line:
            if "{subtitle:" not in line:
                loginfo(f"INFO_2 The subtitle is missing in {filename}")
            else:
                index_start = line.index(":") + 1
                subtitle = line[index_start:-2]

        # if 3 == number_line:
        #    if "{key:" not in line:
        #        loginfo(f"INFO_3 The key is wrong in {filename}")
        #    else:
        #        index_start = line.index(":") + 1
        #        key = line[index_start:-2]

        if 5 == number_line:
            if "{comment:" not in line:
                loginfo(f"INFO_5 The 1st comment is missing in {filename}")
            else:
                index_start = line.index(":") + 1
                key = line[index_start:-2]

    filename_new = f"{title} - {subtitle}.pro".lower()
    if filename != filename_new:
        shutil.copy(path_dir / filename, path_dir / filename_new)
        os.remove(path_dir / filename)


def process_folder(path_dir):
    """
    Processing given folder
    """

    files_dir = os.listdir(path_dir)
    for file in files_dir:
        if ".pro" == file[-4:]:
            process_pro(path_dir, file)


####################################################################################################

process_folder(PATH_SCRIPT_DIR / "songs")

path_log = PATH_SCRIPT_DIR / "_processor.log"
with open(path_log, "w", encoding="utf-8") as file_log:
    file_log.writelines(LOG)

print("The script was executed")
