from lxml import html
import sounddevice as sd
import soundfile as sf
import requests
import urllib.request
from pydub import AudioSegment
import time
import numpy as np
import os

URL = "http://soundbible.com/suggest.php"
DIR = "./files"


def playsounds(tags, take=1, overlay=False):
    gcount = 1
    if not os.path.exists(DIR):
        os.mkdir(DIR)
    allsounds = list()
    for k, v in tags.items():
        sounds = getsounds(k, take)
        volume = v
        combined = AudioSegment.empty()
        for z in sounds:
            ext = os.path.splitext(z)[1]
            basefile = DIR + "/sb_" + str(gcount)
            file = basefile + ext
            sbyte = AudioSegment.empty()

            ### Sleep may be needed if ip starts getting blacklisted
            ### for pinging the server too much
            # if gcount > 1:
            #     time.sleep(0.3)

            # simple clean to urlencode spaces... may be others
            # TODO: Real URL encoding per component
            z = z.replace(" ", "%20")

            urllib.request.urlretrieve(z, file)
            if ext == ".mp3":
                sbyte = AudioSegment.from_mp3(file)
            elif ext == ".wav":
                sbyte = AudioSegment.from_wav(file)

            else:
                print("ERROR: Unknown audio type: " + ext)
            sbyte = sbyte - 10 + int(volume / 1)

            if overlay:
                combined = sbyte.overlay(combined)
            else:
                combined += sbyte

            allsounds.append(os.path.basename(z))
            gcount += 1

        render = DIR + "/buffer.wav"
        combined.export(render, format="wav")
        # TODO maybe add other file types later
        if os.path.exists(render) and gcount > 1:
            data, fs = sf.read(render, dtype='float32')
            sd.play(data, fs)
            status = sd.wait()

    return allsounds


def getsounds(tag, take=1):
    tag = tag.lower()
    page = requests.get(URL + "?q=" + tag)
    tree = html.fromstring(page.content)

    root = "//tr[@class='row-b']/"
    names = tree.xpath(root + "td/a/strong/text()")
    mp3s = tree.xpath(root + "td[2]/div/a[@href]/@href")

    results = list()

    if len(mp3s) == len(names):
        for i in range(len(names)):
            name = names[i].lower()
            if tag == name or name.startswith(tag) or name.endswith(tag):
                # Best match use this first
                results.append(mp3s[i])

        # Safeguard that we get... something
        # TODO: could improve simple scoring logic
        for i in range(len(names)):
            name = names[i].lower()
            results.append(mp3s[i])
            if i > 10:
                break
    else:
        print("ERROR: Could not find Sounds")

    if len(results) == 0:
        print("ERROR: No Results")

    return results[0:take]