import speech_recognition as sr
import moviepy.editor as mp
from pydub import AudioSegment
import math
import os

class Video2Text:



    def __init__(self):

        pass



    def video2audiowav(self, videoFileName, audioFileName):
        ##### LECTURA DEL VIDEO
        clip = mp.VideoFileClip(videoFileName) # LECTURA DE VIDEO
        clip.audio.write_audiofile(audioFileName) ## Extraer audio
    


    def splitwav(self, audioFileName, seconds):
        ### DIVIDIR EL AUDIO EN PARTES
        seg = seconds

        speech = AudioSegment.from_wav(audioFileName)

        batch_size = seg * 1000
        duracion = speech.duration_seconds
        batches = math.ceil(duracion / seg)
        self.batches = batches

        inicio = 0
        for i in range(batches):
            pedazo = speech[inicio: inicio + batch_size]
            pedazo.export(f'pedazo_{i}.wav', format='wav') #guardamos el audio de 10s
            inicio+= batch_size



    def splitwav2text(self, textFileName):

        # LECTURA DE ARCHIVO DE AUDIO
        ## Se valida si el fichero existe o no, en caso de no existir se crea
        if(~os.path.exists(textFileName)):
            with open(textFileName, 'w') as file:
                file.write("")
        
        r = sr.Recognizer() ## INICIAR SPEECH RECOGNITION
            
        for i in range(self.batches):
            print(f"Processing Pedazo{i}ToText")

            try:
                audio = sr.AudioFile(f"pedazo_{i}.wav") # LECTURA DE AUDIO

                with audio as source:
                    r.adjust_for_ambient_noise(source)
                    audio_file = r.record(source) 

                result = r.recognize_google(audio_file, language='es-ES') # RECONOCIMIENTO DE VOZ EN AUDIO

                with open(textFileName, 'a+') as file:
                    file.write(result) # ESCRITURA DEL TEXTO
            except:
                print(f"\tProblems to get transcript :( pedazo_{i}")
    


    def cleanProcessing(self, audioFileName):

        if(os.path.exists(audioFileName)):
            os.remove(audioFileName)
        
        for i in range(1000):
            if(os.path.exists(f"pedazo_{i}.wav")):
                os.remove(f"pedazo_{i}.wav")
            else:
                break
                        



if __name__ == "__main__":

    ##### INITIALIZATIONS
    vt = Video2Text()
    videoFileName = "" ## Filename to extract transcript (MP4)
    audioFileName = f"{videoFileName.replace('.mp4','')}_extracted_audio.wav"
    textFileName = f"{videoFileName.replace('.mp4','')}_text.txt"

    vt.video2audiowav(videoFileName, audioFileName) ## Genera el audio
    vt.splitwav(audioFileName, 120) ## Divide el audio en partes
    vt.splitwav2text(textFileName) ## Genera el transcrito de las partes
    vt.cleanProcessing(audioFileName) ## Limpia el proceso
