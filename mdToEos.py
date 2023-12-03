import argparse
from pythonosc import udp_client
import time
import re

parser = argparse.ArgumentParser()
parser.add_argument("--md", metavar="MARKDOWN", help="The markdown file to pull data from")
parser.add_argument("--csv", metavar="CSV", help="The CSV file to pull data from")
parser.add_argument("-ip", metavar="IP_ADDRESS", help="The IP Address of the console")
parser.add_argument("-port", metavar="PORT", help="The Port of the console to send OSC to")
parser.add_argument("-q", metavar="CUE_HEADER", help="The header of the Cue Number column")
parser.add_argument("--i", metavar="TIME_HEADER", help="The header of the Time column")
parser.add_argument("--l", metavar="LABEL_HEADER", help="The header of the Label column")
parser.add_argument("--n", metavar="NOTES_HEADER", help="The header of the Notes column")
parser.add_argument("--s", metavar="SCENE_HEADER", help="The header of the Scene Name Column")
parser.add_argument("--m", metavar="MARK_HEADER", help="The header of the Mark column")
parser.add_argument("--b", metavar="BLOCK_HEADER", help="The header of the Block column")
parser.add_argument("--f", metavar="BLOCK_HEADER", help="The header of the Follow column")
parser.add_argument("--x", metavar="BLOCK_HEADER", help="The header of the Execute column")

args = vars(parser.parse_args())

client = udp_client.SimpleUDPClient(args["ip"], int(args["port"]))

# Check whether the user specified a markdown or CSV file to pull cues from
if args["md"] is not None:
    # Convert markdown to an array
    with open(args["md"]) as f:
        rows = []
        for row in f.readlines():
            # Ignore everything outside the table
            if row[0] == "|":
                # Strip pipes
                temp_row = row[1:-2]
                # Split line and ignore column whitespace
                clean_line = [col.strip() for col in temp_row.split('|')]

                for j in range(len(clean_line)):
                    # Eos doesn't like pounds, so replace them if they appear in user text
                    clean_line[j] = clean_line[j].replace("#", "No. ")
                if len(clean_line[0]) > 0:
                    # Append clean row data to rows
                    rows.append(clean_line)
        # Get rid of header split line
        rows = rows[:1] + rows[2:]

elif args["csv"] is not None:
    # Convert CSV to an array
    with open(args["csv"]) as f:
        rows = []
        for row in f.readlines():
            # Split line and ignore column whitespace
            clean_line = [col.strip() for col in row.split(',')]

            for j in range(len(clean_line)):
                # Eos doesn't like pounds, so replace them if they appear in user text
                clean_line[j] = clean_line[j].replace("#", "No. ")

            # If the first cell on a given row is one or more "-," this is from an unlinted markdown file. Don't add it.
            if not re.search("^-+$", clean_line[0]) and len(clean_line[0]) > 0:
                # Append clean row data to rows
                rows.append(clean_line)

else:
    # User did not specify either filetype, quit.
    print("Please specify either a markdown (.md) file with --md or a CSV file (.csv) file with --csv.")
    quit()

# Pick headers to use based on user input
found_cue_header = False
found_time_header = False
found_label_header = False
found_notes_header = False
found_scene_header = False
found_block_header = False
found_mark_header = False
found_follow_header = False
found_execute_header = False

for i in range(len(rows[0])):
    if rows[0][i] == args["q"]:
        cue_header_index = i
        found_cue_header = True
        break

if not found_cue_header:
    print("Please ensure the header of the cuelist is spelled correctly, cased properly, and is wrapped in quotes")
    quit()

if args["i"]:
    # User specified a time column, find the index
    for i in range(len(rows[0])):
        if rows[0][i] == args["i"]:
            time_header_index = i
            found_time_header = True
            break

    if not found_time_header:
        print(
            "Please ensure the header of the time column is spelled correctly, "
            "cased properly, and is wrapped in quotes")
        quit()

if args["l"]:
    # User specified a label column, find the index
    for i in range(len(rows[0])):
        if rows[0][i] == args["l"]:
            label_header_index = i
            found_label_header = True
            break

    if not found_label_header:
        print(
            "Please ensure the header of the label column is spelled correctly, "
            "cased properly, and is wrapped in quotes")
        quit()

if args["n"]:
    # User specified a notes column, find the index
    for i in range(len(rows[0])):
        if rows[0][i] == args["n"]:
            notes_header_index = i
            found_notes_header = True
            break

    if not found_notes_header:
        print(
            "Please ensure the header of the notes column is spelled correctly, "
            "cased properly, and is wrapped in quotes")
        quit()

if args["s"]:
    # User specified a scene column, find the index
    for i in range(len(rows[0])):
        if rows[0][i] == args["s"]:
            scene_header_index = i
            found_scene_header = True
            break

    if not found_scene_header:
        print(
            "Please ensure the header of the scene column is spelled correctly, "
            "cased properly, and is wrapped in quotes")
        quit()

if args["b"]:
    # User specified a block column, find the index
    for i in range(len(rows[0])):
        if rows[0][i] == args["b"]:
            block_header_index = i
            found_block_header = True
            break

    if not found_block_header:
        print(
            "Please ensure the header of the block column is spelled correctly, "
            "cased properly, and is wrapped in quotes")
        quit()

if args["m"]:
    # User specified a block column, find the index
    for i in range(len(rows[0])):
        if rows[0][i] == args["m"]:
            mark_header_index = i
            found_mark_header = True
            break

    if not found_mark_header:
        print(
            "Please ensure the header of the mark column is spelled correctly, "
            "cased properly, and is wrapped in quotes")
        quit()

if args["f"]:
    # User specified a Follow column, find the index
    for i in range(len(rows[0])):
        if rows[0][i] == args["f"]:
            follow_header_index = i
            found_follow_header = True
            break

    if not found_follow_header:
        print(
            "Please ensure the header of the follow column is spelled correctly, "
            "cased properly, and is wrapped in quotes")
        quit()

if args["x"]:
    # User specified an Execute column, find the index
    for i in range(len(rows[0])):
        if rows[0][i] == args["x"]:
            execute_header_index = i
            found_execute_header = True
            break

    if not found_execute_header:
        print(
            "Please ensure the header of the Execute column is spelled correctly, "
            "cased properly, and is wrapped in quotes")
        quit()

# Trim the table headers off
rows = rows[1:]

# Go to Live so cues can be recorded
client.send_message("/eos/key/live", "")

# Record cues
for i in range(len(rows)):
    # Loop through table, sending whatever OSC messages we can
    client.send_message("/eos/newcmd", "Record Cue %s Enter" % rows[i][cue_header_index])
    if found_time_header:
        time_separator = " / "
        split_time = rows[i][time_header_index].split("/")
        time_string = time_separator.join(split_time)
        client.send_message("/eos/newcmd", "Cue %s Time %s Enter" % (rows[i][cue_header_index], time_string))
    if found_label_header:
        client.send_message("/eos/newcmd", "Cue %s Label %s Enter" %
                            (rows[i][cue_header_index], rows[i][label_header_index]))
    if found_notes_header:
        client.send_message("/eos/newcmd", "Cue %s Notes %s Enter" %
                            (rows[i][cue_header_index], rows[i][notes_header_index]))
    if found_scene_header:
        # If the user put anything in the scene cell, treat it as a scene header
        if len(rows[i][scene_header_index]) > 0:
            client.send_message("/eos/newcmd", "Cue %s Scene %s Enter" %
                                (rows[i][cue_header_index], rows[i][scene_header_index]))
    if found_block_header:
        # If the user put anything in the block cell, block the cue
        if len(rows[i][block_header_index]) > 0:
            client.send_message("/eos/newcmd", "Cue %s Block Enter" % rows[i][cue_header_index])
    if found_mark_header:
        # If the user put anything in the mark cell, block the cue
        if len(rows[i][mark_header_index]) > 0:
            client.send_message("/eos/newcmd", "Cue %s Mark Enter" % rows[i][cue_header_index])
    if found_follow_header:
        # If the user put anything in the follow cell, treat it as a follow time
        client.send_message("/eos/newcmd", "Cue %s Follow %s Enter" %
                            (rows[i][cue_header_index], rows[i][follow_header_index]))
    if found_execute_header:
        # If the user put anything in the execute cell, hope they formatted it correctly, because we can't check.
        client.send_message("/eos/newcmd", "Cue %s Execute %s Enter" %
                            (rows[i][cue_header_index], rows[i][execute_header_index]))
        client.send_message("/eos/newcmd", "Enter")

    time.sleep(.2)
