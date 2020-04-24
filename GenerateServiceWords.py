import PIL

ttf = r'C:\Windows\Fonts\BOOKOS.TTF'
ttfb = r'C:\Windows\Fonts\BOOKOSB.TTF'
FOLDER = 'C:\\Users\\o.beckett\\Desktop\\'

'''
$ = Title
£ = Bold
# = Split here.
'''

oos = """
$Opening Chant

O Christus resurrexit, Christus resurrexit.
O Alleluia, Alleluia!
O Christ is risen, Christ is risen.
O Alleluia, Alleluia!
Alleluia Christ is risen.
£He is risen indeed. Alleluia!
#
$Gloria

Glory to God, glory to God,
glory in the highest!
£Glory to God, glory to God,
£glory in the highest!
#
To God be glory for ever!
£To God be glory for ever!
#
Alleluia! Amen! Alleluia! Amen!
Alleluia! Amen! Alleluia! Amen!
£Alleluia! Amen! Alleluia! Amen!
£Alleluia! Amen! Alleluia! Amen!
"""

emphcolour = (45,78,34)
W = 600
H = 800
BORDER = 50

"""
|--A--|--B--|--C--|
"""
A = 300
B = 800
C = 800
D = 100
KARAOKESIZE = int((D-40)/2)

from PIL import ImageFont, ImageDraw, Image

def getfontsize(splittext, blank):
   
    fontsize = 1  # starting font size
    font = ImageFont.truetype(ttf, fontsize)
    maxwidth = 0
    maxheight = 0 

    while (maxwidth < blank.size[0] - BORDER) and (maxheight < blank.size[1] - BORDER):

        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype(ttf, fontsize)
        #print(blank.size)
        maxwidth = max([font.getsize(x)[0] for x in splittext])
        maxheight = 0
        maxheight = max([font.getsize(x)[1] for x in splittext])*len(splittext)
        #print(maxwidth, maxheight)

    # optionally de-increment to be sure it is less than criteria
    fontsize -= 1
    return fontsize

def drawimage(splittext, fontsize, blank, draw, txt, index, karaoke=False):
    font = ImageFont.truetype(ttf, fontsize)
    fontbold = ImageFont.truetype(ttfb, fontsize)
    fontemph = ImageFont.truetype(ttfb, fontsize+2)

    normaltext = []
    boldtext = []
    emphtext = []
    for l in splittext:
        if "£" in l:
            boldtext.append(l.replace("£",""))
            if not karaoke:
                normaltext.append("")
                emphtext.append("")
        elif "$" in l:
            emphtext.append(l.replace("$",""))
            if not karaoke:
                normaltext.append("")
                boldtext.append("")
        else:
            if karaoke and l is "":
                pass
            else:
                normaltext.append(l)
            if not karaoke:
                boldtext.append("")
                emphtext.append("")

    w, h = draw.textsize(txt, font=font)
    print(normaltext, boldtext)

    print('final font size',fontsize)
    if karaoke:
        draw.text((A+10,10), "\n".join(normaltext[:2]), font=font, fill="black") # put the text on the image
        draw.text((A+B+10,10), "\n".join(boldtext), font=fontbold, fill="black") # put the text on the image
        draw.text((10,10), "\n".join(emphtext), font=fontemph, fill=emphcolour) # put the text on the image
    else:
        draw.text(((W-w)/2,(H-h)/2), "\n".join(normaltext), font=font, fill="black") # put the text on the image
        draw.text(((W-w)/2,(H-h)/2), "\n".join(boldtext), font=fontbold, fill="black") # put the text on the image
        draw.text(((W-w)/2,(H-h)/2), "\n".join(emphtext), font=fontemph, fill=emphcolour) # put the text on the image
    blank.save(FOLDER+r'{0}{1}.png'.format(splittext[0],index)) # save it

def process (oos, index):
    #image = Image.open('test.jpg')
    blank  = Image.new('RGB', (W, H), color = (256, 256, 256))

    draw = ImageDraw.Draw(blank)
    txt = "share/fonts/truetype/customfonts/KeepC"

    txt = oos

    splittext = txt.split("\n")
    fontsize = getfontsize(splittext, blank)
    drawimage(splittext, fontsize, blank, draw, txt, "{0}_{1}".format(index,splittext[1]))

def processkaraoke (oos, index):
    #image = Image.open('test.jpg')
    blank  = Image.new('RGB', (A+B+C, D), color = (256, 256, 256))

    draw = ImageDraw.Draw(blank)
    txt = "share/fonts/truetype/customfonts/KeepC"

    txt = oos

    splittext = txt.split("\n")
    fontsize = KARAOKESIZE
    drawimage(splittext, fontsize, blank, draw, txt, "k_{0}_{1}".format(index,splittext[1]), karaoke=True)

split = oos.split("#")

for i, s in enumerate(split):
    process(s, i)

for i, s in enumerate(split):
    processkaraoke(s, i)