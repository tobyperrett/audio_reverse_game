import os
import glob

from pydub import AudioSegment, effects
from pydub.playback import play

in_folder = "movies"
out_folder = "out"



def load_audio():
    forwards = []
    wc = os.path.join(in_folder, "*.mp3")
    for song in glob.glob(wc):
        audio = AudioSegment.from_mp3(song)
        forwards.append(effects.normalize(audio))
    return forwards

def reverse_all(forwards):
    backwards = [f.reverse() for f in forwards]
    return backwards

def generate_tracks(forwards, backwards, silence=2000, repetitions=1):
    silence = AudioSegment.silent(silence)
    questions = AudioSegment.empty()
    answers = AudioSegment.empty()
    for f, b in zip(forwards, backwards):
        questions = questions + silence + b
        answers = answers + silence + b + silence + f
    
    

    for count in range (0, repetitions -1):
        questions =  questions + AudioSegment.silent(10000) + questions
    
    return questions, answers

def write_tracks(questions, answers):
    q_fn = os.path.join(out_folder, in_folder+"_questions.mp3")
    a_fn = os.path.join(out_folder, in_folder+"_answers.mp3")
    questions.export(q_fn, format="mp3")
    answers.export(a_fn, format="mp3")

forwards = load_audio()
backwards = reverse_all(forwards)

q, a = generate_tracks(forwards, backwards)
write_tracks(q, a)
