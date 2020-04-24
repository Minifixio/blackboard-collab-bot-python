from selenium_manager import SeleniumManager
from window_manager import Window
from music_bot import MusicBot
from subprocess import call
import api_manager as api
import time 

presentation_txt = open('./utils/presentation_speech.txt', 'r') # Setup your presentation text here
commands_txt = open('./utils/commands.txt', 'r') # Setup your commands documentation here
bot_speech_txt = open('./utils/bot_speech.txt', 'r') # Setup your presentation speech here
commands_lines = commands_txt.readlines()

bot_name = 'BOTS3'

class Bot:

    def __init__(self):
        self.sm = SeleniumManager('https://eu.bbcollab.com/collab/ui/session/guest/07731b875d3f4c27933ca970d57d0d84', bot_name, self)
        self.music_bot = MusicBot(self.sm)

        self.commands = { 
            'musique': self.music_bot.command,
            'aide': self.help,
            'parle': self.speak,
            'covid': self.covid,
            'meme': self.meme,
            'chat': self.cat_img,
            'traduire': self.translate
            }

        self.window = Window(self.sm, self)

    def choose_bot(self, param, username):
        print('choose bot ', param)
        command = param.split(' ')[0]

        if len(param.split(' ')) > 1:
            content = param.split(' ', 1)[1]
        else:
            content = ''

        if command in self.commands:
            self.commands[command](content, username)
        else:
            self.sm.send_text_message('Désolé ' + username + ' cette commande n\'existe pas !')
    
    def help(self, content, username):
        for line in commands_lines:
            time.sleep(0.5) 
            self.sm.send_text_message(line.strip())
    
    def speak(self, content, username):
        call(["python3", "voice.py", content]) # Workaround to avoid Threads issues (working on Mac)
    
    def covid(self, content, username):
        confirmed, recovered, deaths = api.get_corona_stats('france')
        self.sm.send_text_message('Covid : en France, il y a :')
        time.sleep(1) 
        self.sm.send_text_message(str(confirmed) + ' cas confirmés')
        time.sleep(1) 
        self.sm.send_text_message(str(recovered) + ' soignés')
        time.sleep(1) 
        self.sm.send_text_message(str(deaths) + ' personnes décédées')

    def meme(self, content, username):
        meme_img = api.get_meme()
        self.sm.send_text_message(username + ', voici un meme ' + meme_img)

    def translate(self, content, username):
        trad = api.translate(content)
        self.sm.send_text_message(username + ' voici ta traduction : ')
        time.sleep(0.5) 
        self.sm.send_text_message(trad)

    def cat_img(self, content, username):
        if username != bot_name:
            cat_img = api.get_random_cat()
            self.sm.send_text_message(username + ', voici une image de chat : ' + cat_img)
    
    def introduce(self):
        call(["python3", "voice.py", bot_speech_txt.read()]) # Say the presentation speech
        presentation_lines = presentation_txt.readlines()

        for line in presentation_lines: # Read presentation text
            self.sm.send_text_message(line.strip())

        self.help('', '')
        return

bot = Bot() # Init BOT