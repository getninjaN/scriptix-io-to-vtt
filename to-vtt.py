import os
import re
import argparse
import asyncio
import codecs
import json


def to_time(ms):
  hours = int((ms / (1000 * 60 * 60)) % 24)
  hours_str = str(hours).zfill(2)
  minutes = int((ms / (1000 * 60)) % 60)
  minutes_str = str(minutes).zfill(2)
  seconds = int((ms / 1000) % 60)
  seconds_str = str(seconds).zfill(2)
  milliseconds = int(ms - (seconds * 1000))
  milliseconds_str = str(milliseconds)[0:3].zfill(3)

  return "{}:{}:{}.{}".format(hours_str, minutes_str, seconds_str, milliseconds_str)

async def reader(args):
  with open(args.file) as file:
    json_data = json.load(file)
    filename = "{}.{}".format(os.path.splitext(os.path.basename(file.name))[0], "vtt")

  style = "A:middle L:90%"

  phrases = []

  # Fix times
  for caption in json_data:
    count = 1
    new_lined = False
    for result in caption["result"]:
      await asyncio.sleep(0)
      if len(result) > 0:
        result_word = result[0]
        result_end = to_time(result[2])

        if count == 1:
          current_row = ""
          result_start = to_time(result[1])

        current_row = current_row + result_word + " "

        count += 1

        if len(current_row) >= 64:
          phrases.append({
            "start_time": result_start,
            "end_time": result_end,
            "text": current_row,
            "length": len(current_row)
          })
          current_row = ""
          count = 1
          new_lined = False
        elif len(current_row) >= 32 and not new_lined:
          current_row = current_row + "\n"
          new_lined = True

    if len(current_row) > 0:
      phrases.append({
        "start_time": result_start,
        "end_time": result_end,
        "text": current_row,
        "length": len(current_row)
      })

  writer(phrases, filename, style)

def writer(phrases, filename, style):
  vtt = codecs.open(filename, "w+", "utf-8")
  index = 1

  vtt.write("WEBVTT\n\n")

  for phrase in phrases:
    print("Writing: " + phrase["start_time"] + " --> " + phrase["end_time"])
    vtt.write(str(index) + "\n")
    
    index += 1

    vtt.write(phrase["start_time"] + " --> " + phrase["end_time"] + " " + style + "\n")
    vtt.write(phrase["text"] + "\n\n")

  vtt.close()
  print("Done. Your captions can be found in ./" + filename)

def main():
  parser = argparse.ArgumentParser("To VTT")
  parser.add_argument("file", help="Path to file")

  args = parser.parse_args()

  asyncio.run(reader(args))

if __name__ == "__main__":
  main()