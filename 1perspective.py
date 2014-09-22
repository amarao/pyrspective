#!/usr/bin/python

import svgwrite
from subprocess import call

def get_step(lower, upper, varnish, max_x, step_size,step):
    '''
        calculate heler line for step 'Step'
        if line does not fit in [0;x] range
        it recalculated to be clipped
        return lower position for line

        see proofs/proof1.png for math
    '''
    projected_X = varnish + step * step_size
    if projected_X < 0:
        a = - projected_X 
        L = lower - upper
        M = varnish
        c = float (L * a) / (M + a)
        y = lower - c 
        return 0, y 
    elif projected_X > max_x:
        a = projected_X - max_x
        L = lower - upper
        M = max_x - varnish  # triangle in other direction
        c = float (L * a) / (M + a)
        y = lower - c
        return max_x,y
    else:
        return projected_X, lower

class Canvas:
    def __init__(self):
        self.x = 1920
        self.y = 1080
        self.dotsize = 3
        self.horizon = 100
        self.varnish = self.x/3
        self.horizon_color = svgwrite.rgb(50, 50, 50, '%')
        self.helper_color = svgwrite.rgb(50, 50, 75, '%')
        self.helper_opacity = 0.2
        self.filename='1perspective.svg'
        self.bottom = int( self.y * 0.9)
        self.step_size = 64
        

c = Canvas()

dwg = svgwrite.Drawing(c.filename, size=(c.x,c.y), profile='tiny')
dwg.add(dwg.line((0, c.horizon), (c.x, c.horizon), stroke = c.horizon_color))
dwg.add(dwg.circle(center = (c.varnish, c.horizon), r = c.dotsize , stroke = c.horizon_color, stroke_opacity = c.helper_opacity))
dwg.add(dwg.line((0, c.bottom), (c.x, c.bottom), stroke = c.helper_color))
for step in range(-64,129):  # TODO calculate for symmetry
    x, y = get_step(c.bottom, c.horizon, c.varnish, c.x, c.step_size, step)
    if x == c.varnish:  # vertical line, double opacity if possible
        opacity = min (1, c.helper_opacity * 2)
    else:
        opacity = c.helper_opacity
    dwg.add(dwg.line((x, y), (c.varnish, c.horizon), stroke = c.helper_color, stroke_opacity=opacity))
    if y == c.bottom:
        dwg.add(dwg.circle(center = (x, c.bottom), r = c.dotsize, stroke = c.helper_color, stroke_opacity = c.helper_opacity))


dwg.save()
call(['xdg-open', c.filename])

