from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window
import openai
import my_key
import threading


openai.api_key = my_key.my_api_key
Window.softinput_mode = 'below_target'


class MainScreen(Screen):
    search_box = ObjectProperty()
    chat_list = ObjectProperty()
    event = threading.Event()  # Event to synchronize threads
    
    def search(self):
        self.spinner.active = True
        self.start_background_task()
        
    def update_chat_list(self):    
        
        self.event.wait() #Wait until the answer is ready        
        self.search_box.text = ""
        user_list_item = MDTextField(text=query, readonly=True, focus=False, mode="rectangle", icon_left="account-circle", multiline=True )
        self.ids.chat_list.add_widget(user_list_item)
        ai_list_item = MDTextField(text= ai_message, readonly=True, focus=False, mode="rectangle", icon_right="robot-happy" , multiline=True )
        self.ids.chat_list.add_widget(ai_list_item)
    
        
    def start_background_task(self):
        threading.Thread(target = self.answer).start()
        
    def answer(self, *args):
        global query
        global ai_message
        query = self.search_box.text
        ai_message = Model.result(query)
        self.event.set() #Signal that the answer is ready
       

class ChatApp(MDApp):
    def build(self):
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette="Red"
        return MainScreen()
        
class Model():
    def result(question):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=question,
            temperature=0.6,
            max_tokens=150,
         )
        return (response.choices[0].text.strip())
        


ChatApp().run()
