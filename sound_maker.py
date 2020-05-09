from lxml import html
import requests
import urllib.request
from pydub import AudioSegment
import time
import numpy as np
import os
import sys
from pprint import pprint

if 'sounddevice' in sys.modules:
    import sounddevice

class SoundMaker:
    URL = "http://soundbible.com/suggest.php"
    DIR = "./sound_files"
    autoplay=False

    def __init__(self, autoplay=False):
        self.autoplay=autoplay

    def playsounds(self, dics):
        combined = AudioSegment.empty()
        allsounds = list()
        for d in dics:
            sounds, c = self.buildsounds(d, 1, True)
            combined += c
            allsounds.append(sounds)

        render = self.DIR + "/buffer.wav"
        combined.export(render, format="wav")
        render = render if os.path.exists(render) and len(allsounds) > 0 else None
        return (render, allsounds)

    def buildsounds(self, tags, take=1, overlay=False):
        gcount = 1
        if not os.path.exists(self.DIR):
            os.mkdir(self.DIR)
        allsounds = list()
        combined = AudioSegment.empty()
        for k, v in tags.items():
            sounds = self.getsounds(k, take)
            volume = v
            for z in sounds:
                ext = os.path.splitext(z)[1]
                basefile = self.DIR + "/sb_" + str(gcount)
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

        return allsounds, combined
    
    def getsounds(self, tag, take=1):
        tag = tag.lower()
        page = requests.get(self.URL + "?q=" + tag)
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
