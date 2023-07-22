import argparse
from pythonosc import udp_client
import time

parser = argparse.ArgumentParser()
parser.add_argument("-md", metavar="MARKDOWN", help="The markdown file to pull data from")
parser.add_argument("-ip", metavar="IP_ADDRESS", help="The IP Address of the console")
parser.add_argument("-port", metavar="PORT", help="The Port of the console to send OSC to")
parser.add_argument("-q", metavar="CUE_HEADER", help="The header of the cue number column")
parser.add_argument("--i", metavar="TIME_HEADER", help="The header of the time column")
parser.add_argument("--l", metavar="LABEL_HEADER", help="The header of the label column")
parser.add_argument("--n", metavar="NOTES_HEADER", help="The header of the notes column")
parser.add_argument("--s", metavar="SCENE_HEADER", help="The header of the Scene Name Column")

args = vars(parser.parse_args())

client = udp_client.SimpleUDPClient(args["ip"], int(args["port"]))

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
                clean_line[j] = clean_line[j].replace("#", "No. ")
            # Append clean row data to rows
            rows.append(clean_line)
        # Get rid of header split line
    rows = rows[:1] + rows[2:]

# Pick headers to use based on user input
found_cue_header = False
found_time_header = False
found_label_header = False
found_notes_header = False
found_scene_header = False

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
            "Please ensure the header of the time column is spelled correctly, cased properly, and is wrapped in quotes")
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
            "Please ensure the header of the label column is spelled correctly, cased properly, and is wrapped in quotes")
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
            "Please ensure the header of the notes column is spelled correctly, cased properly, and is wrapped in quotes")
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
            "Please ensure the header of the scene column is spelled correctly, cased properly, and is wrapped in quotes")
        quit()

rows = rows[1:]

for i in range(len(rows)):
    # Loop through table, sending whatever OSC messages we can
    client.send_message("/eos/newcmd", "Record Cue %s Enter" % rows[i][cue_header_index])
    if found_time_header:
        client.send_message("/eos/newcmd", "Cue %s Time %s Enter" % (rows[i][cue_header_index], rows[i][time_header_index]))
    if found_label_header:
        client.send_message("/eos/newcmd", "Cue %s Label %s Enter" % (rows[i][cue_header_index], rows[i][label_header_index]))
    if found_notes_header:
        client.send_message("/eos/newcmd", "Cue %s Notes %s Enter" % (rows[i][cue_header_index], rows[i][notes_header_index]))
    if found_scene_header:
        if len(rows[i][scene_header_index]) > 0:
            client.send_message("/eos/newcmd", "Cue %s Scene %s Enter" % (rows[i][cue_header_index], rows[i][scene_header_index]))

    time.sleep(.2)
