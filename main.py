#-*-coding:utf8;-*-  
#qpy:2  
#qpy:kivy 

import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

import kivy
kivy.require('1.11.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.core.audio import SoundLoader
from kivy.clock import Clock, mainthread
from kivy.utils import get_color_from_hex

from module import db # db
from module import user
from module import paraphrase
from gtts import gTTS
from time import sleep
import os
import pyglet
import speech_recognition as sr

class TranslateParaphraseApp(App):

    def build(self):
        Window.clearcolor = (1, 1, .98, 0)
        fontName='static/NanumSquareRoundR.ttf'
        self.text = TextInput(multiline=False)
        self.text.font_name = fontName
        self.text.bind(on_text_validate=self.on_enter)
        self.text.text_language = "kor"
        self.text.font_size= 20
        self.text.hint_text = "Input what you want to paraphrase."
        self.text.size_hint_y = None
        self.text.height = 40
        self.text.width = 30
        
        self.result = StackLayout()
        self.result.orientation = 'lr-tb'
        self.result.height=400

        self.say = Button(text='Touch and speak something.')
        self.say.bind(on_release=self.speech)
        self.say.background_color = get_color_from_hex('ff7473')
        
        self.boxLayout = BoxLayout(size_hint_y=None)
        self.boxLayout.padding = 25
        self.boxLayout.spzcing = 10
        self.boxLayout.orientation = 'vertical'

        self.result.add_widget(self.text)
        self.result.spacing = 10
        self.result.add_widget(self.say)
        self.boxLayout.add_widget(self.result)

        self.anchor2 = AnchorLayout()
        
        self.root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        self.root.add_widget(self.boxLayout)

        return self.root

    def on_enter(self, instance):
        print('User pressed enter in', self.text.text)

        self.boxLayout.remove_widget(self.anchor2)
        self.boxLayout.remove_widget(self.result)

        return self.trans(self.text.text)


    def on_enter2(self, instance):
        print('User pressed enter in', self.text.text)
        self.result.remove_widget(self.text)
        self.result.remove_widget(self.say)
        self.boxLayout.remove_widget(self.result)
        self.boxLayout.remove_widget(self.anchor2)

        return self.trans(self.text.text)
    
    def speech(self, instance):
        self.text.text = "Say something!"
        Clock.schedule_once(lambda d: self.GetAudio(), 0)

        return
 
    def GetAudio(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        self.audio = audio
        try:
            self.text.text =r.recognize_google(audio, language = 'en')
            self.boxLayout.remove_widget(self.anchor2)
            self.trans(self.text.text)
        except sr.UnknownValueError:
            self.text.text = "I can't understand your audio."
        except sr.RequestError as e:
            self.text.text = "Could not request results"

        return
 
    def speech2(self, instance):
        self.text.text = "Say something!"
        Clock.schedule_once(lambda d: self.GetAudio2(), 0)

        return
 
    def GetAudio2(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        self.audio = audio
        try:
            self.text.text =r.recognize_google(audio, language = 'en')
            self.result.remove_widget(self.text)
            self.result.remove_widget(self.say)
            self.boxLayout.remove_widget(self.result)
            self.boxLayout.remove_widget(self.anchor2)
            self.trans(self.text.text)
        except sr.UnknownValueError:
            self.text.text = "I can't undersatnd your audio."
        except sr.RequestError as e:
            self.text.text = "Could not request results"

        return


    def trans(self, message):
        tr = paraphrase.paraphrase()
        trans = tr.manyResult(message) # paraphrase

        if len(trans) > 18:
            transL = 18
        else:
            transL = len(trans)

        if transL > 10:
            transL = 10

        self.result.remove_widget(self.text)
        self.result.remove_widget(self.say)
        
        self.result = StackLayout()
        self.result.orientation = 'lr-tb'
        self.result.height=400
        
        self.text.text = ''
        self.text.bind(on_text_validate=self.on_enter2)
        self.result.add_widget(self.text)
        self.result.spacing = 10
        self.say.bind(on_release=self.speech2)
        self.result.add_widget(self.say)

        for i in range(0, transL):
            button = Button(text=trans[i], font_size=20, width=Window.width-50, size_hint=(None, 1.2))
            button.background_color = get_color_from_hex('47b8e0') #[1, .30, .30, 1] #[1, .45, .45, 1]
            button.bind(on_release=self.speak)
            self.result.add_widget(button)
        
        self.anchor2 = AnchorLayout()
        self.anchor2.anchor_x = 'left'
        self.anchor2.anchor_y = 'bottom'
        self.anchor2.add_widget(self.result)
        
        self.boxLayout.add_widget(self.anchor2)

        return self.root

    def speak(self, instance):
        message = instance.text
        print(message)

        tts = gTTS(text=message, lang='en')
        filename = 'tmp/speak.mp3'
        tts.save(filename)

        sound = SoundLoader.load(filename)
        if sound:
            print("Sound found at %s" % sound.source)
            print("Sound is %.3f seconds" % sound.length)
            sound.play()

            os.system('start ' + filename)

        return 'speak'
    

if __name__ in ('__main__', '__android__'):
    TranslateParaphraseApp().run()