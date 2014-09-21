#!/usr/bin/python

import svgwrite
from subprocess import call

def get_step(x, y, center, step_size,step):
    '''
        return X coordinate for step 'step', it can be negative
    '''
    return center + step * step_size

class Canvas:
    def __init__(self):
        self.x = 1920
        self.y = 1080
        self.dotsize = 3
        self.horizon = 100
        self.varnish = self.x/2 
        self.horizon_color = svgwrite.rgb(50, 50, 50, '%')
        self.helper_color = svgwrite.rgb(50, 50, 75, '%')
        self.filename='1perspective.svg'
        self.bottom = self.y - self.horizon
        self.steps = 100
        self.step_size = self.x/float(self.steps)
        self.step0 = -int(self.varnish/self.step_size)
        self.step_end = int(self.x/self.step_size) + self.step0
        

c = Canvas()

dwg = svgwrite.Drawing(c.filename, size=(c.x,c.y), profile='tiny')
dwg.add(dwg.line((0, c.horizon), (c.x, c.horizon), stroke = c.horizon_color))
dwg.add(dwg.circle(center = (c.varnish, c.horizon), r = c.dotsize , stroke = c.horizon_color))
dwg.add(dwg.line((0, c.bottom), (c.x, c.bottom), stroke = c.helper_color))
for step in range(c.step0,c.step_end):
    x = get_step(c.x, c.y, c.varnish, c.step_size, step)
    dwg.add(dwg.line((x, c.bottom), (c.varnish, c.horizon), stroke = c.helper_color))
    dwg.add(dwg.circle(center = (x, c.bottom), r = c.dotsize, stroke = c.helper_color))

dwg.save()
call(['xdg-open', c.filename])

