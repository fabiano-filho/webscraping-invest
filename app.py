from flask import Flask, request, jsonify
from pydub import AudioSegment
import speech_recognition as sr
import os

from webscraping import WebscrapingInvest

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Receber o arquivo de áudio enviado no corpo da requisição
    audio_file = request.files['audio_file']
    audio_file.save("audio.ogg")
    
    # Convertendo o arquivo para .wav
    sound = AudioSegment.from_file("audio.ogg", format="ogg")
    sound.export("audio.wav", format="wav")
    
    # Inicializar o reconhecedor de fala
    r = sr.Recognizer()
    
    # Abrir o arquivo de áudio convertido
    audio = sr.AudioFile("audio.wav")
    
    # Reconhecer o texto no arquivo de áudio
    with audio as source:
        audio = r.record(source)
    text = r.recognize_google(audio, language='pt-BR')
    
    # Removendo arquivos gerados
    os.remove("audio.ogg")
    os.remove("audio.wav")
    
    # Retornar o texto reconhecido
    return jsonify(text=text)


@app.route('/invest/<code>', methods=['GET'])
def invest(code):
    webscraping = WebscrapingInvest(code)
    response = webscraping.get_info()
    webscraping.close()
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT", default=5000))
