import sys
import selenium
from threading import Thread

# Using a Thread for any async tasks as executing JS scripts
class JsListener(Thread):

    def __init__(self, callback, webdriver, script):
        Thread.__init__(self)
        self.callback = callback
        self.script = script
        self.webdriver = webdriver
        self.stop_thread = False

    def run(self):
        print('started thread')
        while(True):
            self.callback(self.listen())
            if self.stop_thread: 
                print('stopped thread')
                break


    def listen(self):
        self.webdriver.set_script_timeout(10000000000)

        try:
            # Execute JS script with a callback function as return
            result = self.webdriver.execute_async_script(self.script)
            return result
        except selenium.common.exceptions.InvalidArgumentException:
            self.webdriver.set_script_timeout(10000000000)
        
