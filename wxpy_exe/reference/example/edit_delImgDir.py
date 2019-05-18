import time
import wx
from threading import Thread
# from wx.lib.pubsub import pub
from pubsub import pub

#找不到Publisher():出现这个错误是正常的
#现在版本已经将这个类私有化，
#将Publisher的subscribe与sendMessage复制给了subscribe与sendMessage变量。
# 所以我们这样引入头：from wx.lib.pubsub import pub，同时将所有的Publisher()改为pub。

#wxpython是通过wx.CallAfter给主程序推入事件，通过PubSub与主程序传递数据。

########################################################################
class TestThread(Thread):
    """Test Worker Thread Class."""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.start()  # start the thread

    # ----------------------------------------------------------------------
    def run(self):  #run是硬核Thread的函数。。
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        for i in range(6):
            time.sleep(10)
            wx.CallAfter(self.postTime, i) #CallAfter给主程序推入事件
        time.sleep(5)
        # wx.CallAfter(pub.sendMessage, "update", "Thread finished!")
        wx.CallAfter(pub.sendMessage, "update", msg="Thread finished!")

        # ----------------------------------------------------------------------

    def postTime(self, amt):
        """
        Send time to GUI
        """
        amtOfTime = (amt + 1) * 10
        # pub.sendMessage("update", amtOfTime)
        pub.sendMessage("update", msg=amtOfTime)

    ########################################################################


class MyForm(wx.Frame):

    # ----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Tutorial")

        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        self.displayLbl = wx.StaticText(panel, label="Amount of time since thread started goes here")
        self.btn = btn = wx.Button(panel, label="Start Thread")

        btn.Bind(wx.EVT_BUTTON, self.onButton)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.displayLbl, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(sizer)

        # create a pubsub receiver
        pub.subscribe(self.updateDisplay, "update")
        #pub是和主程序传递数据的，执行函数，猜测这个"update"是个key

        # ----------------------------------------------------------------------

    def onButton(self, event):
        """
        Runs the thread
        """
        TestThread()    #这里开了一个线程
        self.displayLbl.SetLabel("Thread started!")
        btn = event.GetEventObject()
        btn.Disable()   #然后让按钮变得不可以点

        # ----------------------------------------------------------------------

    def updateDisplay(self, msg):
        #然后主线程的数据就放在msg里。
        """
        Receives data from thread and updates the display
        """
        # t = msg.data
        t = msg
        if isinstance(t, int):
            self.displayLbl.SetLabel("Time since thread started: %s seconds" % t)
        else:
            self.displayLbl.SetLabel("%s" % t)
            self.btn.Enable()

        # ----------------------------------------------------------------------


# Run the program
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyForm().Show()
    app.MainLoop()