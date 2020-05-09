import sounddevice
import soundfile as sf
from sound_maker import SoundMaker

sq = SoundMaker()
# Play sequentially car (Volume 3) then door (Volume 5)
file, sounds = sq.playsounds([
    {
        'truck': 3
    },
    {
        'cat': 2,
        'person': 1
    }

])

if file is not None:
    data, fs = sf.read(file, dtype='float32')
    sounddevice.play(data, fs)
    status = sounddevice.wait()
