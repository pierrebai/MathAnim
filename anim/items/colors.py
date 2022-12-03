from .color import color

#################################################################
#
# Colors

no_color = color(0, 0, 0, 0)

orange    = color(235, 180,  40)
yellow    = color(223, 223,  40)
blue      = color( 68, 125, 255)
green     = color( 83, 223,  56)
black     = color(  0,   0,   0)
white     = color(255, 255, 255)
cyan      = color( 30, 190, 220)
gray      = color(220, 220, 220)
red       = color(255,  84,  46)
purple    = color(190, 30, 220)
sable     = color(210, 190, 160)

dark_orange   = orange.darker(130)
dark_blue     = blue.darker(130)
dark_green    = green.darker(130)
dark_cyan     = cyan.darker(130)
dark_gray     = gray.darker(130)
dark_red      = red.darker(130)
dark_purple   = purple.darker(130)

pale_blue     = blue.lighter(130); pale_blue.setAlpha(120)
pale_red      = red.lighter(130); pale_red.setAlpha(120)
pale_green    = green.lighter(130); pale_green.setAlpha(120)
pale_gray     = gray.lighter(240); pale_gray.setAlpha(120)
