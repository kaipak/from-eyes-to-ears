import sounddevice
from sound_maker import SoundMaker

sq = SoundMaker(True)
# Play sequentially car (Volume 3) then door (Volume 5)
print(
    sq.playsounds({
        'truck': 3,
        'door': 5
    }, 1, False)
)

# Play overlay 4 Cats at Volume 8
print(
    sq.playsounds({
        'cat': 8
    }, 4, True)
)

sq = SoundMaker(False)
# Play overlay 4 Cats at Volume 8
print(
    sq.playsounds({
        'cat': 8
    }, 4, True)
)
