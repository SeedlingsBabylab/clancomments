import pyclan as pc
import os
import argparse
import csv


def parse_dirs(dirs):
    comms = []
    for dir in dirs:
        for root, dir_dirs, files in os.walk(dir):
            for file in files:
                if file.endswith(".cha"):
                    cf = pc.ClanFile(os.path.join(root, file))
                    comments = cf.get_user_comments()
                    print "{} -- {} comments".format(file, len(comments))
                    if not any("silence" in x.content for x in comments):
                        print "\tno silences here"
                    comms.append((file, comments))

    return comms


def parse_files(files):
    comms = []
    for file in files:
        if file.endswith(".cha"):
            cf = pc.ClanFile(file)
            comments = cf.get_user_comments()
            comms.append((file, comments))


def output_csv(comments):
    with open("clancomments.csv", "wb") as out:
        writer = csv.writer(out)
        writer.writerow(["file", 'onset', 'comment'])
        for group in comments:
            for comm in group[1]:
                writer.writerow([group[0], comm.onset, comm.content])

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Pull out all the comments in CLAN files")
    parser.add_argument("--dirs", nargs="+", type=str, help="Directories with CLAN files")
    parser.add_argument("--files", nargs="+", type=str, help="CLAN files")
    args = parser.parse_args()
    if args.dirs:
        comments = parse_dirs(args.dirs)
    if args.files:
        comments = parse_files()

    output_csv(comments)