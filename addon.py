from xbmcgui import Dialog, WindowDialog,DialogProgress
import xbmcaddon
from threading import Timer
import xbmcaddon
import xbmcgui


class KeyListener(WindowDialog):
    TIMEOUT = 5

    #def __new__(cls):
     # gui_api = tuple(map(int, xbmcaddon.Addon('xbmc.gui').getAddonInfo('version').split('.')))
       # file_name = "DialogNotification.xml" if gui_api >= (5, 11, 0) else "DialogKaiToast.xml"
      # return super(KeyListener, cls).__new__(cls, "", "")

    def __init__(self):
        self.key = None

    def onInit(self):
        napis = ControlTextBox (150, 150, 300, 160, "Press button to turn hyperion off","font13", 0xFFFFFFFF)
        self.addControl(napis)
        napis.setVisible(True)
        try:
            self.getControl(401).addLabel("label1")
            self.getControl(402).addLabel("label2")
        except AttributeError:
            self.getControl(401).setLabel("label3")
            self.getControl(402).setLabel("label4")

    def onAction(self, action):
        code = action.getButtonCode()
        self.key = None if code == 0 else str(code)
        self.close()

    @staticmethod
    def record_key():
        notify = xbmcgui.Dialog()
        notify.notification("Lightberry","Press key within 5 sec...",xbmcgui.NOTIFICATION_INFO,5000,False)
        dialog = KeyListener()
        timeout = Timer(KeyListener.TIMEOUT, dialog.close)
        timeout.start()
        dialog.doModal()
        timeout.cancel()
        
        key = dialog.key
        del dialog
        return key

xbmcgui.Dialog().ok("Hyperion keytab editor", "After clicking ok you will have 5 seconds to push the button on the remote, which you want to use to turn hyperion OFF")
offCode = KeyListener().record_key();
if offCode=="":
    xbmcgui.Dialog().ok("Hyperion keytab editor", "Sorry, but it looks like we cannot use this button.\nPLease start the plugin again and pick different button")
    exit(1);
    
xbmcgui.Dialog().ok("Hyperion keytab editor", "Great!\nNow, after clicking ok you will have 5 seconds to push the button on the remote, which you want to use to turn hypeion ON")
onCode = KeyListener().record_key();
if onCode=="":
    xbmcgui.Dialog().ok("Hyperion keytab editor", "Sorry, but it looks like we cannot use this button.\nPLease start the plugin again and pick different button")
    exit(1);
keymapxml = open("/storage/.kodi/userdata/keymaps/hyperion.xml","w")
keymapxml.write("<keymap><global><keyboard>")
keymapxml.write("<key id=\""+offCode+"\">RunScript(\"/storage/turn_off.py\")</key>")
keymapxml.write("<key id=\""+onCode+"\">RunScript(\"/storage/turn_on.py\")</key>")
keymapxml.write("</keyboard></global></keymap>")

keymapxml.close()
xbmcgui.Dialog().ok("Hyperion keytab editor", "Awesome! we got " +offCode+" and "+onCode,"Please restart KODI for the changes to take effect and remember that these buttons may work only in Kodi Menu")




