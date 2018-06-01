import pyclan as pc
import os
import argparse
import csv
from shutil import copy

processed_dir = "processed2"


def parse_dirs(dirs):
    comms = []
    for dir in dirs:
        for root, dir_dirs, files in os.walk(dir):
            for file in files:
                if file.endswith(".cha"):
                    print file
                    cf = pc.ClanFile(os.path.join(root, file))
                    comments = cf.get_user_comments()
                    # print "{} -- {} comments".format(file, len(comments))
                    os.rename(os.path.join(root, file),
                         os.path.join(processed_dir, file))
                    # if not any("silence" in x.content for x in comments):
                    #     print "\tno silences here"
                    output_csv([(file, comments)])
                    # comms.append((file, comments))

    return comms


def parse_files(files):
    comms = []
    for file in files:
        if file.endswith(".cha"):
            cf = pc.ClanFile(file)
            comments = cf.get_user_comments()
            comms.append((file, comments))
    return comms


def output_csv(comments):
    if os.path.exists("clancomments.csv"):
        exists = True
    else:
        exists = False

    with open("clancomments.csv", "a") as out:
        writer = csv.writer(out)
        if not exists:
            writer.writerow(["file", 'onset', 'comment'])
        for group in comments:
            for comm in group[1]:
                writer.writerow([group[0], comm.onset, comm.content])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Pull out all the comments in CLAN files")
    parser.add_argument("--dirs", nargs="+", type=str,
                        help="Directories with CLAN files")
    parser.add_argument("--files", nargs="+", type=str, help="CLAN files")
    args = parser.parse_args()
    if args.dirs:
        output_csv([])
        comments = parse_dirs(args.dirs)
    if args.files:
        output_csv([])
        comments = parse_files(args.files)

    # output_csv(comments)
