"""
    A Meter widget that presents data and progress in a radial style gauge.

    Author: Israel Dryer, israel.dryer@gmail.com
    Modified: 2021-05-22
    source: https://github.com/israel-dryer/ttkbootstrap/issues/34

    Inspired by: https://www.jqueryscript.net/chart-graph/Customizable-Animated-jQuery-HTML5-Gauge-Meter-Plugin.html
"""
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from tkinter import StringVar, IntVar
from tkinter import ttk
from tkinter.ttk import Frame
from ttkbootstrap import Style, Colors


class Meter(Frame):
    """A radial meter that can be used to show progress of long running operations or the amount of work completed

    This widget is very flexible and can be customized to show a wide variety of styles.  There are two primary meter
    types which can be set with the ``metertype`` parameter: 'full', and 'semi', which show the arc of the meter in
    a full or semi circle. You can also customize the arc of the circe with the ``arcrange`` and ``arcoffset``
    parameters.

    The progressbar indicator can be displayed as a solid color or with stripes with the ``stripethickness`` parameter.
    By default, the ``stripethickness`` is 0, which results in a solid progressbar. A higher ``stripethickness`` results
    in larger widgets around the meter.

    Various text and label options exist. You can prepend or append text to the centeral text displayed on the widget
    with the ``textappend`` and ``textprepend`` parameters.  You can also change the style and font size of those
    elements.

    Variable are generated by default for this widget and they can be linked to other widgets by referencing them via
    the widget: ``Meter.amountusedvariable``, ``Meter.amounttotalvariable``, etc...

    Properties are also available for these variables so that they can be modified and access without calling the
    getter and setter directly.  For example: ``Meter.amountused`` or ``Meter.amountused = 55`` will get or set the
    amount used on the widget without having to call the ``get`` or ``set`` methods of the tkinter variable.

    """

    def __init__(self,
                 master=None,
                 arcrange=None,
                 arcoffset=None,
                 amounttotal=100,
                 amountused=0,
                 labelfont='Helvetica 10 bold',
                 labelstyle='secondary.TLabel',
                 labeltext=None,
                 metersize=200,
                 meterstyle='primary.TLabel',
                 metertype='full',
                 meterthickness=10,
                 showvalue=True,
                 stripethickness=0,
                 textappend=None,
                 textfont='Helvetica 25 bold',
                 textprepend=None,
                 wedgesize=0,
                 **kw):
        """
        Args:
              master (Widget): parent widget

        Keyword Args:
            arcoffset (int): the amount to offset the arc's starting position in degrees; 0 is at 3 o'clock.
            arcrange (int): the range of the arc in degrees from starting to ending position.
            amounttotal (int): the maximum value of the meter.
            amountused (int): the current value of the meter; display on the meter if ``showvalue`` is ``True``.
            labelfont(int): the font size of the supplemental label.
            labelstyle (str): the ttk style used to render the supplemental label.
            labeltext (str): supplemental text that appears `below` the central text of the meter.
            metersize (int): the size of the meter; represented by one side length of a square.
            meterstyle (str): the ttk style used to render the meter and central text.
            metertype (str): `full`, or `semi`; displays a full-circle or semi-circle.
            meterthickness (int): the thickness of the meter's progress bar.
            showvalue (bool): shows the meter value in the central text of the meter; default = True.
            stripethickness (int): shows the meter's progressbar in solid or striped form. If the value is greater than
                0, the meter's progressbar changes from a solid to a stripe, where the value is the thickness of the
                stripes.
            textappend (str): a short string appended to the central meter text.
            textfont (int): the font size of the central text shown on the meter.
            textprepend (str): a short string prepended to the central meter text.
            wedgesize (int): if greater than zero, the width of the wedge on either side of the current meter value.
        """
        super().__init__(master=master, **kw)
        self.box = ttk.Frame(self, width=metersize, height=metersize)

        # default arcoffset and arcrange for 'semi' and 'full' meter modes.
        if metertype == 'semi':
            self.arcoffset = -225 if not arcoffset else arcoffset
            self.arcrange = 270 if not arcrange else arcrange
        else:  # aka 'full'
            self.arcoffset = -90 if not arcoffset else arcoffset
            self.arcrange = 360 if not arcrange else arcrange

        # widget variables
        self.amountusedvariable = IntVar(value=amountused)
        self.amounttotalvariable = IntVar(value=amounttotal)
        self.labelvariable = StringVar(value=labeltext)
        self.amountusedvariable.trace_add('write', self.draw_meter)

        # misc widget settings
        self.towardsmaximum = True
        self.metersize = metersize
        self.meterthickness = meterthickness
        self.meterforeground = self.lookup(meterstyle, 'foreground')
        self.meterbackground = Colors.update_hsv(self.lookup(meterstyle, 'background'), vd=-0.1)
        self.stripethickness = stripethickness
        self.showvalue = showvalue
        self.wedgesize = wedgesize

        # meter image
        self.meter = ttk.Label(self.box)
        self.draw_base_image()
        self.draw_meter()

        # text & Label widgets
        self.textcontainer = ttk.Frame(self.box)
        self.textprepend = ttk.Label(self.textcontainer, text=textprepend, font=labelfont, style=labelstyle)
        self.textprepend.configure(anchor='s', padding=(0, 5))
        self.text = ttk.Label(self.textcontainer, textvariable=self.amountusedvariable, style=meterstyle, font=textfont)
        self.textappend = ttk.Label(self.textcontainer, text=textappend, font=labelfont, style=labelstyle)
        self.textappend.configure(anchor='s', padding=(0, 5))
        self.label = ttk.Label(self.box, text=labeltext, style=labelstyle, font=labelfont)

        # geometry manager
        self.meter.place(x=0, y=0)
        self.box.pack()
        if labeltext:
            self.textcontainer.place(relx=0.5, rely=0.45, anchor='center')
        else:
            self.textcontainer.place(relx=0.5, rely=0.5, anchor='center')
        if textprepend:
            self.textprepend.pack(side='left', fill='y')
        if showvalue:
            self.text.pack(side='left', fill='y')
        if textappend:
            self.textappend.pack(side='left', fill='y')
        self.label.place(relx=0.5, rely=0.6, anchor='center')

    @property
    def amountused(self):
        return self.amountusedvariable.get()

    @amountused.setter
    def amountused(self, value):
        self.amountusedvariable.set(value)

    @property
    def amounttotal(self):
        return self.amounttotalvariable.get()

    @amounttotal.setter
    def amounttotal(self, value):
        self.amounttotalvariable.set(value)

    def draw_base_image(self):
        """Draw the base image to be used for subsequent updates"""
        self.base_image = Image.new('RGBA', (self.metersize * 5, self.metersize * 5))
        draw = ImageDraw.Draw(self.base_image)

        # striped meter
        if self.stripethickness > 0:
            for x in range(self.arcoffset, self.arcrange + self.arcoffset,
                           2 if self.stripethickness == 1 else self.stripethickness):
                draw.arc((0, 0, self.metersize * 5 - 20, self.metersize * 5 - 20),
                         x, x + self.stripethickness - 1, self.meterbackground, self.meterthickness * 5)
        # solid meter
        else:
            draw.arc((0, 0, self.metersize * 5 - 20, self.metersize * 5 - 20),
                     self.arcoffset, self.arcrange + self.arcoffset, self.meterbackground, self.meterthickness * 5)

    def draw_meter(self, *args):
        """Draw a meter

        Args:
            *args: if triggered by a trace, will be `variable`, `index`, `mode`.
        """
        im = self.base_image.copy()
        draw = ImageDraw.Draw(im)
        if self.stripethickness > 0:
            self.draw_striped_meter(draw)
        else:
            self.draw_solid_meter(draw)
        self.meterimage = ImageTk.PhotoImage(im.resize((self.metersize, self.metersize), Image.CUBIC))
        self.meter.configure(image=self.meterimage)

    def draw_solid_meter(self, draw):
        """Draw a solid meter

        Args:
            draw (ImageDraw): an object used to draw an arc on the meter
        """
        if self.wedgesize > 0:
            meter_value = self.meter_value()
            draw.arc((0, 0, self.metersize * 5 - 20, self.metersize * 5 - 20),
                     meter_value - self.wedgesize, meter_value + self.wedgesize,
                     self.meterforeground, self.meterthickness * 5)
        else:
            draw.arc((0, 0, self.metersize * 5 - 20, self.metersize * 5 - 20),
                     self.arcoffset, self.meter_value(), self.meterforeground, self.meterthickness * 5)

    def draw_striped_meter(self, draw):
        """Draw a striped meter

        Args:
            draw (ImageDraw): an object used to draw an arc on the meter
        """
        if self.wedgesize > 0:
            meter_value = self.meter_value()
            draw.arc((0, 0, self.metersize * 5 - 20, self.metersize * 5 - 20),
                     meter_value - self.wedgesize, meter_value + self.wedgesize,
                     self.meterforeground, self.meterthickness * 5)
        else:
            for x in range(self.arcoffset, self.meter_value() - 1, self.stripethickness):
                draw.arc((0, 0, self.metersize * 5 - 20, self.metersize * 5 - 20),
                         x, x + self.stripethickness - 1, self.meterforeground, self.meterthickness * 5)

    def lookup(self, style, option):
        """Wrapper around the tcl style lookup command

        Args:
            style (str): the name of the style used for rendering the widget.
            option (str): the option to lookup from the style option database.

        Returns:
            any: the value of the option looked up.
        """
        return self.tk.call("ttk::style", "lookup", style, '-%s' % option, None, None)

    def meter_value(self):
        """Calculate the meter value

        Returns:
            int: the value to be used to draw the arc length of the progress meter
        """
        return int((self.amountused / self.amounttotal) * self.arcrange + self.arcoffset)

    def step(self, delta=1):
        """Increase the indicator value by ``delta``.

        The default increment is 1. The indicator will reverse direction and count down once it reaches the maximum
        value.

        Keyword Args:
            delta (int): the amount to change the indicator.
        """
        if self.amountused >= self.amounttotal:
            self.towardsmaximum = True
            self.amountused = self.amountused - delta
        elif self.amountused <= 0:
            self.towardsmaximum = False
            self.amountused = self.amountused + delta
        elif self.towardsmaximum:
            self.amountused = self.amountused - delta
        else:
            self.amountused = self.amountused + delta


#if __name__ == '__main__':
    #def test(meter):
    #    meter.step()
        #meter.after(10, test, meter)

    