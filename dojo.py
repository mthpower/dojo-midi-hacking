from midifile import MIDIFile
import re
import pygame
import time


parser = re.compile('([a-g])(#|b)?(\d)?:?(\d)?')


def addTrack(midi, track_number, track_name, tempo):
    midi.addTrackName(track_number, 0, track_name)
    # tempo in beats per minute
    midi.addTempo(track_number, 0, tempo)

def writeFile(midi, filename):
    binfile = open(filename, 'wb')
    midi.writeFile(binfile)
    binfile.close()

notes_map = {
    'c': 12,
    'd': 14,
    'e': 16,
    'f': 17,
    'g': 19,
    'a': 21,
    'b': 23,
}

def convert(note, current_octave=4):
    parts = parser.findall(note.lower())[0]
    note, fs, octave, duration = parts
    tone = notes_map[note]

    if fs == '#':
        tone += 1
    elif fs == 'b':
        tone -= 1

    tone += 12 * int(octave or current_octave)

    return tone, int(octave or current_octave), int(duration) if duration else None
def main():
    myMidi = MIDIFile(2)

    addTrack(myMidi, 0, 'track-1', 120)

    notes = [
        'c4:1', 'e', 'g', 'c5', 'e5', 'g4', 'c5', 'e5', 'c4', 'e', 'g', 'c5', 'e5', 'g4', 'c5', 'e5',
        'c4', 'd', 'g', 'd5', 'f5', 'g4', 'd5', 'f5', 'c4', 'd', 'g', 'd5', 'f5', 'g4', 'd5', 'f5',
        'b3', 'd4', 'g', 'd5', 'f5', 'g4', 'd5', 'f5', 'b3', 'd4', 'g', 'd5', 'f5', 'g4', 'd5', 'f5',
        'c4', 'e', 'g', 'c5', 'e5', 'g4', 'c5', 'e5', 'c4', 'e', 'g', 'c5', 'e5', 'g4', 'c5', 'e5',
        'c4', 'e', 'a', 'e5', 'a5', 'a4', 'e5', 'a5', 'c4', 'e', 'a', 'e5', 'a5', 'a4', 'e5', 'a5',
        'c4', 'd', 'f#', 'a', 'd5', 'f#4', 'a', 'd5', 'c4', 'd', 'f#', 'a', 'd5', 'f#4', 'a', 'd5',
        'b3', 'd4', 'g', 'd5', 'g5', 'g4', 'd5', 'g5', 'b3', 'd4', 'g', 'd5', 'g5', 'g4', 'd5', 'g5',
        'b3', 'c4', 'e', 'g', 'c5', 'e4', 'g', 'c5', 'b3', 'c4', 'e', 'g', 'c5', 'e4', 'g', 'c5',
        'b3', 'c4', 'e', 'g', 'c5', 'e4', 'g', 'c5', 'b3', 'c4', 'e', 'g', 'c5', 'e4', 'g', 'c5',
        'a3', 'c4', 'e', 'g', 'c5', 'e4', 'g', 'c5', 'a3', 'c4', 'e', 'g', 'c5', 'e4', 'g', 'c5',
        'd3', 'a', 'd4', 'f#', 'c5', 'd4', 'f#', 'c5', 'd3', 'a', 'd4', 'f#', 'c5', 'd4', 'f#', 'c5',
        'g3', 'b', 'd4', 'g', 'b', 'd', 'g', 'b', 'g3', 'b3', 'd4', 'g', 'b', 'd', 'g', 'b'
    ]
    # notes = ["C4:4", "D", "E", "C", "C", "D", "E", "C", "E", "F", "G:8",
    #     "E:4", "F", "G:8"]
    current_octave = 4
    current_duration = 4
    current_time = 0

    for x in notes:
        tone, octave, duration = convert(x, current_octave)

        if octave:
            current_octave = octave
        if duration:
            current_duration = duration

        myMidi.addNote(0, 0, tone, current_time, current_duration / 4.0, 100)
        current_time += current_duration / 4.0

    writeFile(myMidi, 'output.mid')
    pygame.init()
    pygame.mixer.music.load("output.mid")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(2)


if __name__ == '__main__':
    main()

