# You need to have your chromedriver setup before starting the BOT. See selenium configuration page
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

from js_listener import JsListener

bot_test_name = "TEST_BOT" # For testing purpose only

# Connection options
opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_argument("--mute-audio")

# Authorize mic
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, # Allow mic
    "profile.default_content_setting_values.media_stream_camera": 2, # Don't allow camera
    "profile.default_content_setting_values.geolocation": 0, 
    "profile.default_content_setting_values.notifications": 0 
})

class SeleniumManager:

    def __init__(self, url, bot_name, bot):
        self.bot_name = bot_name
        self.url = url
        self.js_listener = None
        self.bot = bot

    def start_browser(self):
        self.driver = webdriver.Chrome(options=opt, executable_path='./chromedriver')
        self.wait = WebDriverWait(self.driver, 60)

    def get_url(self):
        self.driver.get(self.url)
    
    def pass_test_page(self): # For testing purpose only
        self.driver.refresh()

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="field0"]')))

        inputs = [
            self.driver.find_element_by_xpath('//*[@id="field0"]'),
            self.driver.find_element_by_xpath('//*[@id="field1"]'),
            self.driver.find_element_by_xpath('//*[@id="field2"]')
        ]

        names = [
            self.bot_name,
            self.bot_name,
            'jojo@jojo.fr'
        ]

        join_button = self.driver.find_element_by_xpath('//*[@id="SessionStartButton"]')

        for i in range(len(inputs)):
            inputs[i].send_keys(names[i])
        
        join_button.click()
        print('test page passed')

        return
    
    def setup_mic(self): # Select the audio output for your BOT
        select_device_id = 'techcheck-audio-mic-select'
        self.wait.until(EC.element_to_be_clickable((By.ID, select_device_id)))
        select_device = self.driver.find_element_by_id(select_device_id)

        for option in select_device.find_elements_by_tag_name('option'):
            if option.text == 'BlackHole 16ch (Virtual)':
                option.click()
                break

        close_setup_xpath = '//*[@id="techcheck-modal"]/button'
        self.click_element(close_setup_xpath)
        return
    
    def click_element(self, xpath): # Waiting for the element to appear and then, click it
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element = self.driver.find_element_by_xpath(xpath)
        element.click()
        return
    
    def pass_mic_setup(self): # For testing purpose only
        # XPATH of the different elements
        close_setup_xpath = '/html/body/div[5]/div/button'
        close_tutorial_xpath = '//*[@id="announcement-modal-page-wrap"]/button'
        side_panel_xpath = '//*[@id="side-panel-open"]'
        main_channel_xpath = '/html/body/div[1]/div[1]/main/div[3]/section/div/div/ul/li/ul/li/bb-channel-list-item/button'

        self.click_element(close_setup_xpath)
        self.click_element(close_tutorial_xpath)
        self.click_element(side_panel_xpath)
        self.click_element(main_channel_xpath)
        return

    def start_listening(self):

        # Script listening for any new items in the '#chat-channel-history' (= main chat)
        script = """
        var targetNode = document.querySelector("#chat-channel-history");
        var config = { childList: true };
        var callback = arguments[0];
        var obsCallback = function(mutationsList, observer) {
            for(let mutation of mutationsList) {
                if (mutation.type === 'childList') {
                    console.log('A child node has been added or removed.');
                    console.log(mutation.addedNodes[0].querySelector("div > div > div > p.activity-body.chat-message__body.ng-binding").textContent);
                    var messageNode = mutation.addedNodes[0].querySelector("div > div > div > p.activity-body.chat-message__body.ng-binding");
                    var username = '';

                    if (messageNode.parentElement.getElementsByTagName('h4').length == 0) {
                        for (let children of targetNode.children) {
                            
                            if (children.getElementsByTagName('h4').length > 0) {
                                username = children.getElementsByTagName('h4')[0].textContent;
                            }
                        }
                    } else {
                        username = messageNode.parentElement.getElementsByTagName('h4')[0].textContent
                    }
                    callback([messageNode.textContent, username]);
                }
            }
        };
        var observer = new MutationObserver(obsCallback);
        observer.observe(targetNode, config);
        """

        self.js_listener = JsListener(self.new_message_sent, self.driver, script)
        self.js_listener.start()
    
    def stop_listening(self):
        self.js_listener.stop_thread = True

    def new_message_sent(self, message):
        content = message[0]
        username = message[1].strip()

        if username != self.bot_name and content.startswith('!'):
            self.bot.choose_bot(content[1:], username)

    def connect_test(self): # Used for testing purpose only
        self.start_browser()
        self.get_url()
        self.pass_test_page()
        self.click_element('//*[@id="dialog-description-audio"]/div[3]/button')
        self.click_element('//*[@id="techcheck-video-ok-button"]')
        self.click_element('//*[@id="announcement-modal-page-wrap"]/button')
        self.click_element('//*[@id="side-panel-open"]')
        self.click_element('/html/body/div[1]/div[1]/main/div[3]/section/div/div/ul/li/ul/li/bb-channel-list-item/button')
        self.click_element('//*[@id="guidance-chat-input-focus"]/div/button')
    
    def send_text_message(self, message): # Send message in the chat. The main chat must be open.
        text_area = self.driver.find_element_by_id('message-input')
        text_area.send_keys(message, Keys.ENTER)
 