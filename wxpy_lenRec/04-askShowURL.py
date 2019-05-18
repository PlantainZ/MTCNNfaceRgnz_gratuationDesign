#codeing=utf-8


import wx
import wx.html2

class MyBrowser(wx.Dialog):
  def __init__(self, *args, **kwds):
    wx.Dialog.__init__(self, *args, **kwds)
    sizer = wx.BoxSizer(wx.VERTICAL)
    self.browser = wx.html2.WebView.New(self)
    sizer.Add(self.browser, 1, wx.EXPAND, 10)
    self.SetSizer(sizer)
    self.SetSize((700, 700))

  def askURL(self):
    dlg = wx.TextEntryDialog(self, 'Enter a URL', 'HTMLWindow')
    if dlg.ShowModal() == wx.ID_OK:
      return self.browser.LoadURL(dlg.GetValue())

if __name__ == '__main__':
  app = wx.App()
  dialog = MyBrowser(None, -1)
  dialog.askURL()
  # dialog.browser.LoadURL("https://www.baidu.com/?tn=91960356_hao_pg") #加载页面。如果是加载html字符串应该使用  dialog.browser.SetPage(html_string,"")
  dialog.Show()
  app.MainLoop()