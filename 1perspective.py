#!/usr/bin/python

import svgwrite
from subprocess import call
from lineClipping import cohensutherland

def get_ray(horizon, vanish, helper, step_size, step, max_x, max_y):
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
    print x1, y1, x2, y2
    return (x1,y1), (x2, y2)
    
#    answer = [start_x, start_y, end_x, end_y]
   
    #  check for left X-clipping for start_x
#    if start_x < 0:
#        new_x = 0
#        new_y = helper - float((helper - horizon) * abs(start_x)) / (vanish + abs(start_x))  # crossing point of left side
#        answer[0] = new_x
#        answer[1] = new_y

    # check for right X-clipping for start_x
#    if start_x > max_x:
#        new_x = max_x
#        new_y = helper - float((helper-horizon) * (start_x - max_x)) / (max_x - vanish + start_x - max_x ) # crossing point on right side
#        answer[0] = new_x
#        answer[1] = new_y


#    return (answer[0], answer[1]), (answer[2], answer[3])
    

def get_step(lower, upper, vanish, max_x, step_size,step):
    '''
        calculate heler line for step 'Step'
        if line does not fit in [0;x] range
        it recalculated to be clipped
        return lower position for line

        see proofs/proof1.png for math
    '''
    projected_X = vanish + step * step_size
    if projected_X < 0:
        a = - projected_X 
        L = lower - upper
        M = vanish
        c = float (L * a) / (M + a)
        y = lower - c 
        return 0, y 
    elif projected_X > max_x:
        a = projected_X - max_x
        L = lower - upper
        M = max_x - vanish  # triangle in other direction
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
        self.horizon = -200 
        self.vanish = 1880
        self.horizon_color = svgwrite.rgb(50, 50, 50, '%')
        self.helper_color = svgwrite.rgb(50, 50, 75, '%')
        self.helper_opacity = 0.5
        self.filename='1perspective.svg'
        self.helper = 2000
        self.step_size = 64
        self.steps = 1000

c = Canvas()

dwg = svgwrite.Drawing(c.filename, size=(c.x,c.y), profile='tiny')
dwg.add(dwg.line((0, c.horizon), (c.x, c.horizon), stroke = c.horizon_color))
dwg.add(dwg.circle(center = (c.vanish, c.horizon), r = c.dotsize , stroke = c.horizon_color, stroke_opacity = c.helper_opacity))
dwg.add(dwg.line((0, c.helper), (c.x, c.helper), stroke = c.helper_color))
for step in range(0,c.steps):
    begin, end = get_ray(c.horizon, c.vanish, c.helper, c.step_size, -step, c.x, c.y)
    if None not in begin:
        dwg.add(dwg.line(begin, end, stroke = c.horizon_color, stroke_opacity = c.helper_opacity))
    begin, end = get_ray(c.horizon, c.vanish, c.helper, c.step_size, step, c.x, c.y)
    if None not in begin:
        dwg.add(dwg.line(begin, end, stroke = c.horizon_color, stroke_opacity = c.helper_opacity))

dwg.save()
call(['xdg-open', c.filename])

