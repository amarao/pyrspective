#!/usr/bin/python
import math
import svgwrite
from subprocess import call
from lineClipping import cohensutherland

def get_vanish_ray(horizon, vanish, helper, step_size, step, max_x, max_y):
    '''
        Calculate clipped ray (line) for vanish point
        at (horizon; vanish) for horizontal horizon
        and 1-point perpective 
        Clipping occure on canvas with size (0;0)-(max_x;max_y)
    
        Step is calculated aganist visually vertial
        line, which is 0. Negative and positive values are
        symmetric against vertial line.
        
        Helper line is line somewhere in space, parallel 
        to horizon.

        Horizon and helper line may be outside of canvas.

        Return two touples (x1,y1), (x2,y2) to draw the line.

        Raise exception if horizon and helper same

        horizon - Y-coordinate
        vanish - X-coordinate
        helper - Y-coordinate
        max_x - X-coordinate
        max_y - Y-coordinate
        step_size - length
        step - amount of step_size

    '''
    start_x = vanish + step * step_size  # point of crossing of ray with helper line
    start_y = helper
    end_x = vanish
    end_y = horizon

    x1, y1, x2, y2 = cohensutherland(0, max_y, max_x, 0, start_x, start_y, end_x, end_y, 0)
    return (x1,y1), (x2, y2)
    

def get_parallel_line(horizon, helper, step_size, step, max_x, max_y):
    '''
        return paralllel to horizon line

        line counted from helper line toward horizon with step_size
        positive step - to horizon, negative - away from

        line is clipped to max_x, max_y

        return (x1;y1), (x2;y2) set for clipped line or four None if line is invisible

    '''
    #see proofs/proof2.png
    H = float(abs(horizon - helper))
    z1 = float(step_size)
    n = float(step)
    zN = math.copysign(H * n / (n + H/z1 -1), horizon-helper)
    new_y = helper + zN
    print H, zN, new_y
    if new_y < 0 or new_y > max_y:
        return (None, None), (None, None)
    else:
        return (0, new_y), (max_x, new_y)

class Canvas:
    def __init__(self):
        self.x = 800
        self.y = 600
        self.dotsize = 3
        self.horizon = -100
        self.vanish = 200
        self.horizon_color = svgwrite.rgb(50, 50, 50, '%')
        self.helper_color = svgwrite.rgb(50, 50, 75, '%')
        self.helper_opacity = 0.5
        self.filename='1perspective.svg'
        self.helper = 600
        self.step_size = 20 
        self.steps = 200

c = Canvas()

dwg = svgwrite.Drawing(c.filename, size=(c.x,c.y), profile='tiny')
dwg.add(dwg.line((0, c.horizon), (c.x, c.horizon), stroke = c.horizon_color))
dwg.add(dwg.circle(center = (c.vanish, c.horizon), r = c.dotsize , stroke = c.horizon_color, stroke_opacity = c.helper_opacity))
dwg.add(dwg.line((0, c.helper), (c.x, c.helper), stroke = c.helper_color))
for step in range(0,c.steps):
    begin, end = get_vanish_ray(c.horizon, c.vanish, c.helper, c.step_size, -step, c.x, c.y)
    if None not in begin:
        dwg.add(dwg.line(begin, end, stroke = c.horizon_color, stroke_opacity = c.helper_opacity))
    begin, end = get_vanish_ray(c.horizon, c.vanish, c.helper, c.step_size, step, c.x, c.y)
    if None not in begin:
        dwg.add(dwg.line(begin, end, stroke = c.horizon_color, stroke_opacity = c.helper_opacity))

for step in range(0,c.steps):
    begin, end = get_parallel_line(c.horizon, c.helper, c.step_size, step, c.x, c.y)
    if None not in begin:
        dwg.add(dwg.line(begin, end, stroke=c.horizon_color, stroke_opacity = c.helper_opacity))
        

dwg.save()
call(['xdg-open', c.filename])

