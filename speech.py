# -*- coding: utf-8 -*-
import pyaudio
import speech_recognition as sr

p = pyaudio.PyAudio()
devinfo = p.get_device_info_by_index(1)

FORMAT = pyaudio.paInt32
CHANNELS = 1
RATE = devinfo['defaultSampleRate']
CHUNK = 1024
RATE = 44100  
INPUT_BLOCK_TIME = .05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)

next_skip_words = ['skip', 'next', 'following', 'upcoming']
pause_play_words = ['pause', 'play', 'stop', 'start', 'go', 'hold on', 'halt', 'freeze', 'break', 'cease', 'terminate']
swap_connections = ['swap', 'switch', 'exchange', 'swivel', 'pivot']


'''info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print ("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
        if p.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels') > 0:
            print ("Output Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name'))

print (devinfo)
'''


def open_mic_in_stream():
        device_index = 0

        stream = p.open(   format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 input_device_index = device_index,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)
        

        return stream
    
def open_mic_out_stream():
        device_index = 1

        stream = p.open(   format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 output = True,
                                 output_device_index = device_index,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)
        

        return stream
    
def listen( stream ):
        print ("Listening")
        try:
            block = stream.read(INPUT_FRAMES_PER_BLOCK)
            print ("Listened to block")
            return block
        except Exception as e:
            print( "Error recording: %s"%(e) )
            return
        
def play( stream, block ):
    try:
        stream.write(block)
        print ("done playing")
    except IOError as e:
        print( "Erorr playing blocvk: %s"%(e) )

def main():
    r = sr.Recognizer()
    with sr.Microphone() as source:                
        audio = r.listen(source)                   
    try: 
        found = False
        command = r.recognize_google(audio)
        words = command.split(' ')
        for i in range(0, len(command)):
            if words[i] in next_skip_words:
                found = True
                print ("You selected next song or video")
                break
            elif command in pause_play_words:
                found = True
                print("You selected pause or play")
                break
            elif command in swap_connections:
                found = True
                print("You selected to swap connections")
                break
        if not found:
            print("Sorry, I could not understand what you said")
            
            
        print("You said " + command)
    except Exception as e:
        print (e)

    #in_stream = open_mic_in_stream()
    #out_stream = open_mic_out_stream()
    
    '''for i in range(0, 10):
        block = bluetoothAudioData
        play( out_stream, block )
    out_stream.close() # plays music in headphones from bluetooth data transmission'''
    p.terminate()

main()