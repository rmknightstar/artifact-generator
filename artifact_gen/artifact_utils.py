from PIL import Image, ImageSequence,ImageDraw, ImageFont
import os
import os.path
import sys
import json
import requests
from io import BytesIO
from datetime import datetime, timedelta

font_cache=dict()
yyyymm=None
def get_font(font_face,font_size):
  global font_cache
  font_path = f"{VPPR}/Fonts/{font_face}.ttf"
  font_id = f"{font_face}:{font_size}"
  if not font_id in font_cache:
    font_cache[font_id] = ImageFont.truetype(font_path, int(font_size))
  return font_cache[font_id]
def get_pos(xoff,xref,width,yoff,yref,height):
  xref_ = "C" if xref[0].upper() == "M" else xref[0].upper()
  yref_ = "M" if yref[0].upper() == "C" else yref[0].upper()
  x=0
  y=0
  if xref_ == "C":
    x= int(xoff) - width // 2
  elif xref_ == "R":
    x= int(xoff) - width
  else:
    x= int(xoff)
  if yref_ == "M":
    y= int(yoff) - height // 2
  elif yref_ == "B":
    y= int(yoff) - height
  else:
    y= int(yoff)
  return (x,y)

def process_text(im,obj):
  draw = ImageDraw.Draw(im)
  font=get_font(obj["font_face"],obj["font_size"])
  left, top, right, bottom = font.getbbox(obj["text"])
  width = right - left
  height = bottom - top
  pos=get_pos(obj["xoff"],obj["xref"],width,obj["yoff"],obj["yref"],height)
  draw.text(pos, obj["text"], font=font, fill=obj["color"])

def process_image(im,obj):
  global yyyymm
  global VPPR
  # Import thumnbmailed image
  venue_path = f"{VPPR}/{yyyymm}/{obj['img_src']}"  # Replace with your overlay image path
  venue_image = Image.open(venue_path)
  max_width = int(obj["max_width"])
  max_height = int(obj["max_height"])

  venue_image.thumbnail((max_width, max_height))

  # Get the new dimensions of the overlay image
  width, height = venue_image.size

  pos=get_pos(obj["xoff"],obj["xref"],width,obj["yoff"],obj["yref"],height)
  # Paste the overlay image onto the base image at the calculated position
  im.paste(venue_image, pos)

def process_artifact(artifact):
  im = Image.open(f'{VPPR}/{artifact["base"]}')
  image_width, image_height = im.size
  for elem in artifact["elements"]:
    if "text" in elem:
      process_text(im,elem)
    else:
      process_image(im,elem)
  return im

def second_wed_formated(year, month):
  # Start with the first day of the month
  first_day = datetime(year, month, 1)
  # Find the first Wednesday
  first_wednesday = first_day + timedelta(days=(2 - first_day.weekday() + 7) % 7)
  # Add 7 days to get the second Wednesday
  second_wednesday = first_wednesday + timedelta(days=7)
  formatted_date = second_wednesday.strftime("%B %-d, %Y")  # For Unix-based systems (Linux, macOS)

  return formatted_date