# Author: namespace-std 
# Split accompany in piano midi.  

# pip install mido
import mido

def splitfile(input, output):
    FILE = mido.MidiFile(input)

    for i,track in enumerate(FILE.tracks):
        print('Track {}: {}'.format(i, track.name))
        # for msg in track:
            # print(msg.type,end=" ")
            # print(msg)

    FILE2 = mido.MidiFile()
    FILE2.type = FILE.type
    FILE2.ticks_per_beat = FILE.ticks_per_beat

    # track = MidiTrack()
    # mid.tracks.append(track)

    FILE2.tracks.append(FILE.tracks[0])
    FILE2.tracks.append(FILE.tracks[1])

    # FILE2.tracks.append(FILE.tracks[2])

    FILE2.save(output)
