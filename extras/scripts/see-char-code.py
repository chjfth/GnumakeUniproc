#-------------------------------------------------------------------------------
# Name:        En-Decode1
# Purpose:
#
# Author:      yigenluwei
#
# Created:     09-05-2011
# Copyright:   (c) yigenluwei 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#V1.1

import  wx
from wx.lib.expando import ExpandoTextCtrl, EVT_ETC_LAYOUT_NEEDED
from wx.lib.wordwrap import wordwrap

class MainDialog(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE,
            useMetal=False,
            ):

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.

        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)

        # This extra style can be set after the UI object has been created.
        #if 'wxMac' in wx.PlatformInfo and useMetal:
            #self.SetExtraStyle(wx.DIALOG_EX_METAL)


        # Now continue with the normal construction of the dialog
        # contents
        sizer = wx.BoxSizer(wx.VERTICAL)
        Tip = u"《输入一些字符，查看它们的编码》"
        label = wx.StaticText(self, -1, Tip,pos = wx.DefaultPosition, size = wx.DefaultSize,style =wx.ALIGN_LEFT)
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 10)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "TypeInto Any Check Strings:   ")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.LEFT, 15)

        self.TextInStrings = ExpandoTextCtrl(self, size=(250,-1))
        self.Bind(EVT_ETC_LAYOUT_NEEDED, self.OnRefit, self.TextInStrings)
        box.Add(self.TextInStrings, 1, wx.ALIGN_CENTRE|wx.RIGHT, 17)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        b = wx.Button(self, -1, u'转换')
        #b.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)
        box.Add(b, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT, 15)

        self.label = wx.StaticText(self, -1,'UNICODE:')
        box.Add(self.label, 0, wx.EXPAND|wx.ALIGN_CENTRE|wx.ALL, 8)

        self.TextOutUnicode = ExpandoTextCtrl(self, size=(250,-1))
        box.Add(self.TextOutUnicode, 0, wx.EXPAND|wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 10)

        StaticBox = wx.StaticBox(self, -1, "Encoded Output")
        bsizer = wx.StaticBoxSizer(StaticBox, wx.VERTICAL)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cb0 = wx.CheckBox(self, -1, "GB2312", (50, 40), (70, 20), wx.NO_BORDER)
        self.cb0.SetValue(True)
        self.cb0.flg = 1
        hsizer.Add(self.cb0, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.TextOutGB2312 = ExpandoTextCtrl(self, size=(250,-1))
        self.Bind(EVT_ETC_LAYOUT_NEEDED, self.OnRefit, self.TextOutGB2312)
        hsizer.Add(self.TextOutGB2312, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        bsizer.Add(hsizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 1)


        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cb1 = wx.CheckBox(self, -1, "GBK", (50, 40), (70, 20), wx.NO_BORDER)
        self.cb1.SetValue(True)
        self.cb1.flg = 1
        hsizer.Add(self.cb1, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.TextOutGBK = ExpandoTextCtrl(self, size=(250,-1))
        self.Bind(EVT_ETC_LAYOUT_NEEDED, self.OnRefit, self.TextOutGBK)
        hsizer.Add(self.TextOutGBK, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        bsizer.Add(hsizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 1)
        #bsizer.Add(hsizer, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        #bsizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)


        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cb2 = wx.CheckBox(self, -1, "BIG5", (50, 40), (70, 20), wx.NO_BORDER)
        self.cb2.SetValue(True)
        self.cb2.flg = 1
        hsizer.Add(self.cb2, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT, 5)
        self.TextOutBIG5 = ExpandoTextCtrl(self, size=(250,-1))
        self.Bind(EVT_ETC_LAYOUT_NEEDED, self.OnRefit, self.TextOutBIG5)
        hsizer.Add(self.TextOutBIG5, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        bsizer.Add(hsizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 1)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cb3 = wx.CheckBox(self, -1, "UTF-8", (50, 40), (70, 20), wx.NO_BORDER)
        self.cb3.SetValue(True)
        self.cb3.flg = 1
        hsizer.Add(self.cb3, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT, 5)
        self.TextOutUTF8 = ExpandoTextCtrl(self, size=(250,-1))
        self.Bind(EVT_ETC_LAYOUT_NEEDED, self.OnRefit, self.TextOutUTF8)
        hsizer.Add(self.TextOutUTF8, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        bsizer.Add(hsizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 1)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cb4 = wx.CheckBox(self, -1, "UTF-16LE", (50, 40), (70, 20), wx.NO_BORDER)
        self.cb4.SetValue(True)
        self.cb4.flg = 1
        hsizer.Add(self.cb4, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.TextOutUTF16 = ExpandoTextCtrl(self, size=(250,-1))
        self.Bind(EVT_ETC_LAYOUT_NEEDED, self.OnRefit, self.TextOutUTF16)
        hsizer.Add(self.TextOutUTF16, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        bsizer.Add(hsizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 1)
        #bsizer.Add(hsizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox0, self.cb0)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox1, self.cb1)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox2, self.cb2)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox3, self.cb3)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox4, self.cb4)

        sizer.Add(bsizer, 1, wx.EXPAND|wx.ALL, 10)
        #box = wx.BoxSizer(wx.HORIZONTAL)

        #label = wx.StaticText(self, -1, "Output:")
        #box.Add(label, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT, 5)
        #sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5)

        self.cp = cp = wx.CollapsiblePane(self, label=u'高级',
                                          style=wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)
        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged, cp)
        self.pane = cp.GetPane()
        self.MakePaneContent(self.pane)

        #sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        sizer.Add(cp, 0, wx.RIGHT|wx.LEFT|wx.EXPAND, 10)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM, 10)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add((270,10))
        b = wx.Button(self, -1, u'清空')
        self.Bind(wx.EVT_BUTTON, self.OnClearMe, b)
        box.Add(b, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5)
        b = wx.Button(self, -1, u'退出')
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, b)
        box.Add(b, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 8)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def EvtCheckBox0(self, event):
        if event.IsChecked():
            self.cb0.flg = 1
        else:
            self.cb0.flg = 0
    def EvtCheckBox1(self, event):
        if event.IsChecked():
            self.cb1.flg = 1
        else:
            self.cb1.flg = 0
    def EvtCheckBox2(self, event):
        if event.IsChecked():
            self.cb2.flg = 1
        else:
            self.cb2.flg = 0
    def EvtCheckBox3(self, event):
        if event.IsChecked():
            self.cb3.flg = 1
        else:
            self.cb3.flg = 0
    def EvtCheckBox4(self, event):
        if event.IsChecked():
            self.cb4.flg = 1
        else:
            self.cb4.flg = 0

    def OnPaneChanged(self, evt=None):
        # redo the layout
        self.Layout()
        self.Fit()

    def MakePaneContent(self, pane):
        '''Just make a few controls to put on the collapsible pane'''
        sizer = wx.FlexGridSizer()
        sizer.AddGrowableCol(1)
        label = wx.StaticText(pane, -1, "Unicode:")
        sizer.Add(label, 0, wx.LEFT | wx.RIGHT,10)
        self.TextInU = ExpandoTextCtrl(pane, size=(50,-1))
        self.Bind(EVT_ETC_LAYOUT_NEEDED, self.OnRefit, self.TextInU)
        sizer.Add(self.TextInU, 0, wx.RIGHT,20)

        b = wx.Button(pane, -1, '>>>')
        self.Bind(wx.EVT_BUTTON, self.OnU2C, b)
        sizer.Add(b, 0, wx.LEFT|wx.RIGHT, 20)

        label = wx.StaticText(pane, -1, "Character:")
        sizer.Add(label, 0, wx.LEFT | wx.RIGHT,10)
        self.TextOutC = ExpandoTextCtrl(pane, size=(50,-1))
        self.Bind(EVT_ETC_LAYOUT_NEEDED, self.OnRefit, self.TextOutC)
        sizer.Add(self.TextOutC, 0, wx.RIGHT,20)

        border = wx.BoxSizer()
        border.Add(sizer, 1, wx.EXPAND|wx.ALL, 10)
        pane.SetSizer(border)

    def OnClearMe(self, event):
        self.TextInStrings.SetValue('')
        self.TextOutUnicode.SetValue('')
        self.TextOutGB2312.SetValue('')
        self.TextOutGBK.SetValue('')
        self.TextOutBIG5.SetValue('')
        self.TextOutUTF8.SetValue('')
        self.TextOutUTF16.SetValue('')
        self.TextInU.SetValue('')
        self.TextOutC.SetValue('')

    def OnCloseMe(self, event):
        self.Close(True)

    def OnRefit(self, evt):
        # The Expando control will redo the layout of the
        # sizer it belongs to, but sometimes this may not be
        # enough, so it will send us this event so we can do any
        # other layout adjustments needed.  In this case we'll
        # just resize the frame to fit the new needs of the sizer.
        self.Fit()

        # Then we call wx.AboutBox giving it that info object
        #wx.AboutBox(info)

    def OnU2C(self, event):
        u=self.TextInU.GetValue()
        if len(u) == 4:
            print type(u)
            self.TextInU.SetBackgroundColour((204, 232, 207, 255))#self.TextInU.GetBackgroundColour()
            try:
                v=int(u,16)
            except:
                print u'error：不是整形'
                self.TextInU.SetBackgroundColour("red")
                self.TextOutC.SetValue('')
                return

            u = unichr(v)
            #u="u\'\\u" + u + "'"
            self.TextOutC.SetValue(u)
        else:
            self.TextInU.SetBackgroundColour("red")
            self.TextOutC.SetValue('')
            print 'error!'

    def OnButton(self, event):
        #print u'测试 is pressed'


        #a = u'哈严'
        a=self.TextInStrings.GetValue()
        self.TextOutUnicode.SetValue(ToUnicode(a))

        #print len(a)
        Str_GB2312=''
        Str_GBK=''
        Str_BIG5=''
        Str_UTF8=''
        Str_UTF16=''#FFFE

        for i in range(len(a)):
            print (i,a[i]),
            a_gb2312 = UnicodeEncoding(a[i],'gb2312')
            a_gbk = UnicodeEncoding(a[i],'gbk')
            a_big5 = UnicodeEncoding(a[i],'big5')
            a_utf_8 = UnicodeEncoding(a[i],'utf-8')
            a_utf_16 =UnicodeEncoding(a[i],'utf-16')

            #Str_GB2312+=ToShow(a_gb2312)
            if a_gb2312 == 0:
                Str_GB2312+='?'
            else:
                Str_GB2312+=ToShow(a_gb2312)
            if a_gbk == 0:
                Str_GBK+='?'
            else:
                Str_GBK+=ToShow(a_gbk)
            if a_big5 == 0:
                Str_BIG5+='?'
            else:
                Str_BIG5+=ToShow(a_big5)
            Str_UTF8+=ToShow(a_utf_8)
            Str_UTF16 += ToShow(a_utf_16)[4:]

            Str_GB2312+=' '
            Str_GBK+=' '
            Str_BIG5+=' '
            Str_UTF8+=' '
            Str_UTF16+=' '
        #s = "哈哈abc"
        #print repr(a)
        #print repr(unichr(54))

        #print ToUnicode(a)

        #print ToUnicode(s)

        '''a_gb2312 = a.encode('gb2312')
        a_big5 = a.encode('big5')
        a_utf_8 = a.encode('utf-8')
        a_utf_16 = a.encode('utf-16')
        print (a_gb2312,a_utf_8,a_utf_16)'''


        #a_iso =UnicodeEncoding(a,'ISO-8859-1')

        print (Str_GB2312,Str_GBK,Str_BIG5,Str_UTF8,Str_UTF16)
        if self.cb0.flg == 1:
            self.TextOutGB2312.SetValue(Str_GB2312)
        if self.cb1.flg == 1:
            self.TextOutGBK.SetValue(Str_GBK)
        if self.cb2.flg == 1:
            self.TextOutBIG5.SetValue(Str_BIG5)
        if self.cb3.flg == 1:
            self.TextOutUTF8.SetValue(Str_UTF8)
        if self.cb4.flg == 1:
            self.TextOutUTF16.SetValue(Str_UTF16)


        '''a_gb2312 = Chs2Unicode(a).encode('gb2312')
        a_big5 = Chs2Unicode(a).encode('big5')
        a_utf_8 = Chs2Unicode(a).encode('utf-8')
        a_utf_16 = Chs2Unicode(a).encode('utf-16')
        print (a_gb2312,a_big5,a_utf_8,a_utf_16)'''

        #s必须为unicode
        '''s_gb2312 = s.encode('gb2312')
        s_big5 = s.encode('big5')
        s_utf_8 = s.encode('utf-8')
        s_utf_16 = s.encode('utf-16')
        print (s_gb2312,s_big5,s_utf_8,s_utf_16)'''



def UnicodeEncoding(UniChr,encoding):
    UniChr = IsEncoded(UniChr, 'utf-8')
    try:
        ret = UniChr.encode(encoding)
    except:
        #ret = '?'
        print " '%s' codec can\'t encode characters" % encoding
        return 0

    return ret

def ToUnicode(Chs):
    Chs = IsEncoded(Chs, 'utf-8')
    #return [ord(c) for c in Chs]
    #print repr(Chs)
    ret = ""
    for c in Chs:
      c = "%04X " % ord(c);
      ret += c
    return ret

def ToShow(Chs):
    #print repr(Chs)
    ret = ""
    for c in Chs:
      c = "%02X" % ord(c);
      ret += c
    return ret


def IsEncoded(s, encoding):
    if isinstance(s, unicode):
        return s
    else:
        return unicode(s, encoding)

def main():
    app = wx.PySimpleApp()
    app.MainLoop()
    dlg = MainDialog(None, -1, "See Char Code v1.0", size=(550, 200),
                         #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME | wx.CLOSE_BOX,
                         style=wx.DEFAULT_DIALOG_STYLE # & ~wx.CLOSE_BOX,
                         )
    dlg.CenterOnScreen()

        # this does not return until the dialog is closed.
    dlg.ShowModal()

    dlg.Destroy()
    #frame = MainFrame()
    #frame.Show(True)#ShowFullScreen


if __name__ == '__main__':
    main()
