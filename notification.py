"""
For all your notification needs.  
Top level functions that will be called, implementations can exist in other modules.
"""
import gi
gi.require_version("Notify", "0.7")
from gi.repository import Notify
Notify.init("Stock Watche")

notification = Notify.Notification.new(
"Summary here!",
"Some \n<i>HTML</i>\n<b>HERE</b>",
"/home/brian/github/StockWatcher/notificationLogo.png")

# Level 2 is important -it stays up until acknowledge
notification.set_urgency(2)
notification.show()

# In case you want to close it progamtically this is how
# notification.close()
# If you want to update the notification
# notification.update("Some new title", "some new body")
import time
print("Sleeping")
time.sleep(5)
print("I'm wide awakeeee")
notification.update("new title!", "new body!")