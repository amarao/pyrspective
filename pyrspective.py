#!/usr/bin/python
import math
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
    

def get_parallel_line(horizon, distance, helper, step_size, step, max_x, max_y):
    '''
        return paralllel to horizon line

        line counted from helper line toward horizon with step_size
        positive step - to horizon, negative - away from

        line is clipped to max_x, max_y

        return (x1;y1), (x2;y2) set for clipped line or four None if line is invisible

    '''
    #see proofs/proof2.png
    B = float(distance)
    H = float((horizon - helper))
    x = float(step_size)
    n = float(step)
    zN = H * n * x / (n * x + B)
    new_y = helper + zN
    print n, x, H, zN, new_y
    if new_y < 0 or new_y > max_y:
        return (None, None), (None, None)
    else:
        return (0, new_y), (max_x, new_y)

class Canvas:
    def __init__(self):
        self.x = 800
        self.y = 600
        self.dotsize = 3
        self.horizon = 0
        self.vanish = 400
        self.distance = 20 
        self.horizon_color = svgwrite.rgb(50, 50, 50, '%')
        self.helper_color = svgwrite.rgb(50, 50, 75, '%')
        self.helper_opacity = 0.5
        self.filename='perspective.svg'
        self.helper = 600
        self.step_size = 80 
        self.steps = 10

c = Canvas()

class Pyrspective:
    def __ini__(self):
        pass

    def canvas(self, x, y):
        '''
            Set canvas size
        '''
        self.max_x = x
        self.max_y = y

    def add_horizon(self, horizon, angle, id=None):
        '''
            Add horizon to horizons list
            or replace existing (is id is not None)
            horizon is defined by distance
            from canvas start (0, 0)
            Can add vanish point is vanish is not None
            return horizon ID

        '''
        pass

    def add_horizon_by_points(self, begin, end, id=None):
        '''
            Add horizon to horizon list
            or replace existing (if id is not None)
            horizon is defined by two points
            each point has two coords (x,y)
            They can be outside canvas
            Can add vanish point is vanish is not None
            return horizon ID
        '''
        pass
        

    def add_vanish_point(self, point, horizon_id=1):
        '''
            Add vanish point to the horizon
            If point lies outside horizon, vertical projection
            is taken, if this not possible (horizon is vertical),
            horizontal projection happens.
        '''
        pass
            

if __name__ == '__main__':
    import svgwrite
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
    
    for step in range(1,c.steps+1):
        begin, end = get_parallel_line(c.horizon, c.distance, c.helper, c.step_size, step, c.x, c.y)
        if None not in begin:
            print begin, end
            dwg.add(dwg.line(begin, end, stroke=c.horizon_color, stroke_opacity = c.helper_opacity))
            

    dwg.save()
call(['xdg-open', c.filename])

