from sdxf import *

#the left swoop
left=Block('swoop_left')
left.append(Arc(center=(0,0),radius=1,startAngle=0,endAngle=90))
left.append(Line(points=[(1,0),(1,-3)]))
left.append(Arc(center=(2,-3),radius=1,startAngle=180,endAngle=270))
left.append(Line(points=[(2,-4),(2.5,-4)]))


pokey=Block('pokeybit')
pokey.append(Line(points=[(0,0),(0.5,-1)]))
pokey.append(Line(points=[(0.5,-1),(1,0)]))


right=Block('swoop_right')
right.append(Line(points=[(0,-4),(.5,-4)]))
right.append(Arc(center=(.5,-3),radius=1,startAngle=270,endAngle=360))
right.append(Line(points=[(1.5,-3),(1.5,0)]))
right.append(Arc(center=(2.5,0),radius=1,startAngle=90,endAngle=180))




comb = Drawing()
comb.blocks.append(left)
comb.blocks.append(right)
comb.blocks.append(pokey)



def draw_tine(drawing, p, ga, width):
    drawing.append(Insert('swoop_left', point=(0+p[0],0+p[1])))
    for n in range(width):
        drawing.append(Insert('pokeybit', point=(2.5+ga*n+p[0],-4+p[1])))
        if n+1 == width:
            drawing.append(Insert('swoop_right', point=(3.5+ga*n+p[0],0+p[1])))
        else:
            drawing.append(Line(points=[(3.5+ga*n+p[0],-4+p[1]),(3.5+(n+1)*ga-1+p[0],-4+p[1])]))

#creates a needle comb bottom
#takes a pattern (list of tine and spacing widths), gauge in mm, number of needles to span, y position
#and whether the starting "tine" should be down (1) or up (0)
def draw_comb(drawing, pattern, gauge=5, width=30, y=0, tine=True):
    start_tine = tine
    #this is just so everything lines up nicely
    if start_tine:
        current_x = 0
    else:
        current_x = 1
    while current_x < width * gauge:
        if tine:
            current_x += 1
        if start_tine:
            current_x -= 6 - gauge
        else:
            drawing.append(Line(points=[(current_x -1,y+1),(current_x,y+1)]))
        tine = start_tine
        #iterate over the pattern
        for needles in pattern:
            #if we're drawing a tine
            if tine == 1:
                draw_tine(drawing, (current_x,y), gauge, needles)
                current_x += (needles-1)*gauge+6
                print current_x
                tine = not tine
            #oftherwise it's a space
            else:
                space_width = needles*gauge - 1
                drawing.append(Line(points=[(current_x, y+1), (current_x + space_width , y+1)]))
                current_x += space_width
                print current_x
                tine = not tine
    if tine:
        drawing.append(Line(points=[(current_x,y+1),(current_x + 1,y+1)]))


repeat = [
        ([24], True),
        ([1,1], True),
        ([2,1], True),
        ([2,2], True)
            
    ]
current_y = 0

gauge = 5
width = 24


for line in repeat:
    draw_comb(comb, line[0], gauge, width, y = current_y, tine=line[1] )
    current_y += 10


comb.saveas('combs/standard_' + str(gauge) +'mm.dxf')
