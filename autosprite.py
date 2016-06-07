import os
import sys
from PIL import Image
from random import choice
import re

images = []
imagelocations = []
imagesizes = []
imagenames = []
currentimage = 0
spritesheetname = "".join(choice("abcdefghijklmnopqrstuvwxyz") for i in range(10))

def analyseImage(path):
    '''
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode
    before processing all frames.
    '''
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results


def processImage(path):
    '''
    Iterate the GIF, extracting each frame.
    '''
    mode = analyseImage(path)['mode']

    im = Image.open(path)

    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGBA')

    try:
        while True:
            print("saving %s (%s) frame %d, %s %s" % (path, mode, i, im.size, im.tile))

            '''
            If the GIF uses local colour tables, each frame will have its own palette.
            If not, we need to apply the global palette to the new frame.
            '''
            if not im.getpalette():
                im.putpalette(p)

            new_frame = Image.new('RGBA', im.size)

            '''
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
            If so, we need to construct the new frame by pasting it on top of the preceding frames.
            '''
            if mode == 'partial':
                new_frame.paste(last_frame)

            new_frame.paste(im, (0,0), im.convert('RGBA'))
            new_frame.save('temp/%s-%d.png' % (''.join(os.path.basename(path).split('.')[:-1]), i), 'PNG')

            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass

def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)

print("")
print("==================================")
print("Checking for things!")
print("==================================")
print("")

if(os.path.exists("images") == True):
    if(os.path.isdir("images") == True):
        print("Found images folder!")
    else:
        print("Found a file with the name 'images', but it doesn't seem to be a folder.")
        sys.exit(-1)
else:
    print("No images folder found. We will create it for you!")
    os.makedirs("images")
    sys.exit(-2)

imagescount = 0
for filename in os.listdir(os.getcwd() + "/images"):
    if(filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".gif")):
        imagescount += 1
if(imagescount == 0):
    print("No images found in the images folder that could be made into emotes...")
    sys.exit(-3)

if(os.path.exists("temp") == True):
    if(os.path.isdir("temp") == True):
        print("Found temp folder!")
    else:
        print("Found a file with the name 'temp', but it doesn't seem to be a folder.")
        sys.exit(-1)
else:
    print("No temp folder found. Making it now.")
    os.makedirs("temp")
    #sys.exit(-2)

imagescount = 0
for filename in os.listdir(os.getcwd() + "/temp"):
    if(filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".gif")):
        imagescount += 1
if(imagescount != 0):
    print("Temp folder is not empty.")
    sys.exit(-4)

print("")
print("==================================")
print("Detecting animated images!")
print("==================================")
print("")

animemotefilename = ""

for filename in os.listdir(os.getcwd() + "/images"):
    if(filename.endswith(".gif")):
        print("Found emote file " + filename)

        im = Image.open("images/" + filename)

        try:
            while 1:
                im.seek(im.tell()+1)
        except EOFError:
            if(im.tell() > 100):
                print("Animated emote is over 100 frames long.")
                sys.exit(-6)
            else:
                if(im.tell() == 0):
                    print("Animated emote only has 1 frame. This should not be an animated emote.")
                    sys.exit(-7)
                else:
                    print("Animated emote is " + str(im.tell()) + " frames long")
            pass

        im.close()

        processImage('images/' + filename)
        animemotefilename = filename

        new_im = Image.new('RGBA', (1000,1000), (255, 0, 0, 0))

        currentimage = 0
        totalimages = 0
        animimage = []
        for filename in os.listdir(os.getcwd() + "/temp"):
            if(filename.endswith(".png") or filename.endswith(".jpg")):
                totalimages += 1
                animimage.append(filename)
        if(totalimages == 0):
            print("No images found in the images folder that could be made into emotes...")
            sys.exit(-9)

        sort_nicely(animimage)

        for i in range(0,1000,100):
            for j in range(0,1000,100):
                if(currentimage < totalimages):
                    im = Image.open(os.getcwd() + "/temp/" + animimage[currentimage])
                    print("Opened image " + os.getcwd() + "/temp/" + animimage[currentimage])
                    im.thumbnail((100,100))
                    imagelocations.append([i, j])
                    emotename = animimage[currentimage].replace(' ', '')[:-4]
                    print("Placing emote " + emotename + " at location " + str(i) + ", " + str(j))
                    imagenames.append(emotename)
                    (width, height) = im.size
                    print("Emote is " + str(width) + " pixels wide and " + str(height) + " pixels high.")
                    imagesizes.append([width, height])
                    new_im.paste(im, (i,j))
                    currentimage += 1

        currentimage = 0
        totalimages = 0

        print("Saved spritesheet as " + animemotefilename[:-4] + ".png")

        new_im.save(animemotefilename[:-4] + '.png')

        new_im.close()

        for filename in os.listdir(os.getcwd() + "/temp"):
            if(filename.endswith(".png") or filename.endswith(".jpg")):
                os.remove(os.getcwd() + "/temp/" + filename)

images = []
imagelocations = []
imagesizes = []
imagenames = []
currentimage = 0
totalimages = 0

print("")
print("==================================")
print("Detecting images!")
print("==================================")
print("")

for filename in os.listdir(os.getcwd() + "/images"):
    if(filename.endswith(".png") or filename.endswith(".jpg")):
        images.append(filename)
        print("Found emote file " + filename)
    else:
        print("Ignored file " + filename)

totalimages = len(images)

print("")
print("==================================")
print("Generating spritesheet!")
print("==================================")
print("")

new_im = Image.new('RGBA', (1000,1000), (255, 0, 0, 0))

for i in range(0,1000,100):
    for j in range(0,1000,100):
        if(currentimage < totalimages):
            im = Image.open(os.getcwd() + "/images/" + images[currentimage])
            print("Opened image " + os.getcwd() + "/images/" + images[currentimage])
            im.thumbnail((100,100))
            imagelocations.append([i, j])
            emotename = images[currentimage].replace(' ', '')[:-4]
            print("Placing emote " + emotename + " at location " + str(i) + ", " + str(j))
            imagenames.append(emotename)
            (width, height) = im.size
            print("Emote is " + str(width) + " pixels wide and " + str(height) + " pixels high.")
            imagesizes.append([width, height])
            new_im.paste(im, (i,j))
            currentimage += 1

print("Saved spritesheet as " + spritesheetname + ".png")

new_im.save(spritesheetname + '.png')

print("")
print("==================================")
print("Generating CSS!")
print("==================================")
print("")

print("Preparing to generate main css chunk")

maincsschunk = ""
emotecount = 0

for image in imagenames:
    if(emotecount < len(imagenames)-1):
        maincsschunk += "a[href=" + '"/' + image + '"' + "],\r\n"
        emotecount += 1
        print("Added emote " + image + " to main css chunk.")
    else:
        maincsschunk += "a[href=" + '"/' + image + '"' + "]{\r\n"
        print("Added emote " + image + " to main css chunk.")

print("Adding generic css to main css chunk")
maincsschunk += "  display:block;\r\n  clear:none;\r\n  float:left;\r\n  background-image:url(%%" + spritesheetname + "%%);\r\n}\r\n"

print("Generating emote css chunks")

emotecsschunks = []
tempemotecsschunk = ""
emotecount = 0

for image in imagenames:
    print("Making emote CSS chunk for emote " + image)
    tempemotecsschunk = "a[href|=" + '"/' + image + '"' + "]{\r\n"
    emoteposition = imagelocations[emotecount]
    emotepositionx = emoteposition[0]
    emotepositiony = emoteposition[1]
    tempemotecsschunk += "  background-position:-" + str(emotepositionx) + "px -" + str(emotepositiony) + "px;\r\n"
    print("Setting emote position to -" + str(emotepositionx) + "px, -" + str(emotepositiony) + "px")
    emotesize = imagesizes[emotecount]
    emotesizewidth = emotesize[0]
    emotesizeheight = emotesize[1]
    tempemotecsschunk += "  width:" + str(emotesizewidth) + "px;\r\n"
    print("Setting emote width to " + str(emotesizewidth))
    tempemotecsschunk += "  height:" + str(emotesizeheight) + "px;\r\n"
    print("Setting emote height to " + str(emotesizeheight))
    tempemotecsschunk += "}\r\n"
    emotecsschunks.append(tempemotecsschunk)
    print("Finished generation of emote CSS chunk for emote " + image)
    emotecount += 1

print("Combining CSS chunks")

generatedcss = maincsschunk
for csschunk in emotecsschunks:
    generatedcss += csschunk

print("Writing CSS to file")
with open("css.txt", "w") as text_file:
    text_file.write(generatedcss)

print("Finshed job! Have a good day/night! c:")
