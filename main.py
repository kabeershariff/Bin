from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window
from kivy.clock import Clock
import openai
import my_key
import threading


openai.api_key = my_key.my_api_key
Window.softinput_mode = 'below_target'


class MainScreen(Screen):
    search_box = ObjectProperty()
    chat_list = ObjectProperty()
    
    def start_input(self):
        self.spinner.active = True
        global query
        query = self.search_box.text
        self.search_box.text = ""
        user_list_item = MDTextField(text=query, readonly=True, focus=False, mode="rectangle", icon_left="account-circle", multiline=True )
        self.ids.chat_list.add_widget(user_list_item)
    
    def search(self):
        
        self.start_background_task()
        result_thread.join()
        ai_list_item = MDTextField(text= ai_message, readonly=True, focus=False, mode="rectangle", icon_right="robot-happy" , multiline=True )
        self.ids.chat_list.add_widget(ai_list_item)
        
    
    def start_background_task(self):
        global result_thread
        result_thread = threading.Thread(target = self.answer)
        result_thread.start()
        
    def answer(self, *args):
        global ai_message
        ai_message = Model.result(query)
        self.spinner.active = False
        
        
      
    

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
