import os
import Image
from random import choice
from string import lowercase

images = []
imagelocations = []
imagesizes = []
imagenames = []
currentimage = 0
spritesheetname = "".join(choice(lowercase) for i in range(10))

print ""
print "=================================="
print "Detecting images!"
print "=================================="
print ""

for filename in os.listdir(os.getcwd() + "/images"):
    if(filename.endswith(".png")) or (filename.endswith(".jpg")):
        images.append(filename)
        print "Found emote file " + filename
    else:
        print "Ignored file " + filename

totalimages = len(images)

print ""
print "=================================="
print "Generating spritesheet!"
print "=================================="
print ""

new_im = Image.new('RGBA', (1000,1000), (255, 0, 0, 0))

for i in xrange(0,1000,100):
    for j in xrange(0,1000,100):
        if(currentimage < totalimages):
            im = Image.open(os.getcwd() + "/images/" + images[currentimage])
            print "Opened image " + os.getcwd() + "/images/" + images[currentimage]
            im.thumbnail((100,100))
            imagelocations.append([i, j])
            emotename = images[currentimage].replace(' ', '')[:-4]
            print "Placing emote " + emotename + " at location " + str(i) + ", " + str(j)
            imagenames.append(emotename)
            (width, height) = im.size
            print "Emote is " + str(width) + " pixels wide and " + str(height) + " pixels high."
            imagesizes.append([width, height])
            new_im.paste(im, (i,j))
            currentimage += 1

print "Saved spritesheet as " + spritesheetname + ".png"

new_im.save(spritesheetname + '.png')

print ""
print "=================================="
print "Generating CSS!"
print "=================================="
print ""

print "Preparing to generate main css chunk"

maincsschunk = ""
emotecount = 0

for image in imagenames:
    if(emotecount < len(imagenames)-1):
        maincsschunk += "a[href=" + '"' + image + '"' + "],\r\n"
        emotecount += 1
        print "Added emote " + image + " to main css chunk."
    else:
        maincsschunk += "a[href=" + '"' + image + '"' + "]{\r\n"
        print "Added emote " + image + " to main css chunk."

print "Adding generic css to main css chunk"
maincsschunk += "display:block;\r\nclear:none;\r\nfloat:left;\r\nbackground-image(%%" + spritesheetname + "%%);\r\n}\r\n"

print "Generating emote css chunks"

emotecsschunks = []
tempemotecsschunk = ""
emotecount = 0

for image in imagenames:
    print "Making emote CSS chunk for emote " + image
    tempemotecsschunk = "a[href|=" + '"/' + image + '"' + "]{\r\n"
    emoteposition = imagelocations[emotecount]
    emotepositionx = emoteposition[0]
    emotepositiony = emoteposition[1]
    tempemotecsschunk += "background-position:" + str(emotepositionx) + "px " + str(emotepositiony) + " px;\r\n"
    print "Setting emote position to " + str(emotepositionx) + "px, " + str(emotepositiony) + "px"
    emotesize = imagesizes[emotecount]
    emotesizewidth = emotesize[0]
    emotesizeheight = emotesize[1]
    tempemotecsschunk += "width:" + str(emotesizewidth) + "px;\r\n"
    print "Setting emote width to " + str(emotesizewidth)
    tempemotecsschunk += "height:" + str(emotesizeheight) + "px;\r\n"
    print "Setting emote height to " + str(emotesizeheight)
    tempemotecsschunk += "}\r\n"
    emotecsschunks.append(tempemotecsschunk)
    print "Finished generation of emote CSS chunk for emote " + image
    emotecount += 1

print "Combining CSS chunks"

generatedcss = maincsschunk
for csschunk in emotecsschunks:
    generatedcss += csschunk

print "Writing CSS to file"
with open("css.txt", "w") as text_file:
    text_file.write(generatedcss)

print "Finshed job! Have a good day/night! c:"
