##Vertices 0-7  (x,y,z)
vertices= ( 
    (3, -.2, -1),
    (3, .2, -1),
    (-3, .2, -1),
    (-3, -.2, -1),
    (3, -.2, 1),
    (3, .2, 1),
    (-3, .2, 1),
    (-3, -.2, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,6),
    (5,1),
    (5,4),
    (5,6),
    (7,3),
    (7,4),
    (7,6)
)

surfaces = (   
    (0,1,2,3),
    (4,5,6,7),
    (1,5,4,0),
    (3,2,6,7),
    (1,2,6,5),
    (0,3,7,4)
)

#1, 1, 1 = white
#0, 0, 0 = black
colors = (
    #Back
    (0, 0, 0),
    #Front
    (0, 0, 0),
    #Sides (Not Shown)
    ((1.0/255*242),(1.0/255*66),(1.0/255*128)),
    ((1.0/255*242),(1.0/255*66),(1.0/255*128)),
    #Top
    (0, 0, 0),
    #Bottom
    (1, 1, 1),  
)