import wx


class MyTarget(wx.TextDropTarget):
    def __init__(self, object):
        wx.TextDropTarget.__init__(self)
        self.object = object

    def OnDropText(self, x, y, data):
        self.object.InsertStringIem(0, data)

class Mywin(wx.Frame):

    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title, size=(-1, 300))
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.HORIZONTAL)
        languages = ['C', 'C++', 'Java', 'Python', 'Perl', 'JavaScript',
                     'PHP', 'VB.NET', 'C#']

        self.lst1 = wx.ListCtrl(panel, -1, style=wx.LC_LIST)
        self.lst2 = wx.ListCtrl(panel, -1, style=wx.LC_LIST)
        for lang in languages:
            self.lst1.InsertStringItem(0, lang)
        #逐个逐个放到lst1里面去

        dt = MyTarget(self.lst2)
        #将lst2设成一个拖拽放置的目标控件
        self.lst2.SetDropTarget(dt)
        #是window自带的方法~
        wx.EVT_LIST_BEGIN_DRAG(self, self.lst1.GetId(), self.OnDragInit)
        #当开始拖拽的时候。启动拖动事件

        box.Add(self.lst1, 0, wx.EXPAND)
        box.Add(self.lst2, 1, wx.EXPAND)

        panel.SetSizer(box)
        panel.Fit()
        self.Centre()
        self.Show(True)

    def OnDragInit(self, event):
        #在目标上拖拽，并在源处删除
        text = self.lst1.GetItemText(event.GetIndex())
        tobj = wx.PyTextDataObject(text)
        src = wx.DropSource(self.lst1)
        src.SetData(tobj)
        src.DoDragDrop(True)
        #当开始调用DoDragDrop方法拖动一个数据对象时，
        # DoDragDrops在拖放过程中，检测当前光标位置下的控件是不是有效的放置目标
        self.lst1.DeleteItem(event.GetIndex())


ex = wx.App()
Mywin(None, 'Drag&Drop Demo - www.yiibai.com')
ex.MainLoop()
