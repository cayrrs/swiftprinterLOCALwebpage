# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
import sys
import math
import random
from codepoints import *

COLOR_BITS = 8
COLOR_MAXVALUE = (2**COLOR_BITS)-1
UTILITY_BITS = 5
SINGLE_DOT_LINE=4
ONLY_DOTS = False
NUM_MARKERS = 212
NUM_REUSED_COLORS=1
OFFSET=10
TOOL_COUNT = 25

img_name = "reduced.png"
if len(sys.argv)==1:
    print("Swift Printer image to data convertor:\n convert <image_name> <tool_count> <offset> <number_of_reused_colors> <number_of_markers>\n\n image_name\t\t\timage file, has to have reduced colors with pngquant\n tool_count\t\t\tmaximum number of markers used at unce. Default 25.\n offset\t\t\t\tminimal pixel distance between two markers. Defaul 10.\n number_of_reused_colors\tWhen using image with less colors than available markers,\n\t\t\t\tthe rest of available markers will have color(s) of the most prominent color in the picture.\n \t\t\t\tThis option sets how many colors will repeat. Default 1.\n number_of_markers\t\tnumber of available markers\n\n")
    quit()

if len(sys.argv)>1:
    img_name = sys.argv[1]

if len(sys.argv)>2:
    TOOL_COUNT = int(sys.argv[2])
    
if len(sys.argv)>3:
    OFFSET = int(sys.argv[3])

if len(sys.argv)>4:
    NUM_REUSED_COLORS = int(sys.argv[4])

if len(sys.argv)>5:
    NUM_MARKERS = int(sys.argv[5])

X=NUM_REUSED_COLORS
def png_to_matrix(image_path):
    # Open the PNG image
    img = Image.open(image_path)
    
    # Get the RGB values of each pixel
    img_rgb = img.convert('RGB')
    pixel_values = list(img_rgb.getdata())
    
    # Deduplicate the list of RGB values to get unique colors
    unique_colors = list(set(pixel_values))
    
    # Create a mapping from RGB colors to integers
    color_to_integer = {color: i for i, color in enumerate(unique_colors)}
    
    # Convert the image to a 2D NumPy matrix using the mapping
    width, height = img.size
    img_matrix = np.zeros((height, width), dtype=int)
    histogram = [0]*NUM_MARKERS
    for y in range(height):
        for x in range(width):
            pixel_color = pixel_values[y * width + x]
            c=color_to_integer[pixel_color]
            img_matrix[y, x] = c
            histogram[c] = histogram[c]+1
    
    return color_to_integer, img_matrix,histogram

# Example usage:
# Replace 'image.png' with the path to your PNG image file
image_path = img_name
color_to_integer, image_matrix,histogram = png_to_matrix(image_path)

X = X if X <= len(color_to_integer) else len(color_to_integer)
#print(X)
#print(histogram)
index_max = max(range(len(histogram)), key=histogram.__getitem__)

indexed_histogram = list(enumerate(histogram))
sorted_indices = sorted(indexed_histogram, key=lambda x: x[1], reverse=True)

# Extract the first X elements from the sorted list
top_X_indices = [index for index, value in sorted_indices[:X]]

#print(top_X_indices)


#print(histogram[index_max])
mostFrequentColor = index_max
pool=[]
#for i in range(len(histogram)):
#    if histogram[i]>0:
#        pool.append(i)
#    else:
#        pool.append(mostFrequentColor)

for i in range(len(histogram)):
    if histogram[i]>0:
        pool.append(i)
    else:
        pool.append(top_X_indices[i%X])

#for i in range(len(histogram)):
#    pool.append(i%len(color_to_integer))

#print(pool)

#print(color_to_integer)
#print(image_matrix)
#print(image_matrix[0,1023])

IMG_WIDTH= len(image_matrix[0,:])
IMG_HEIGHT=len(image_matrix[:,0])

actual_line = 0;
line_progress = [0]*TOOL_COUNT
line_go = [False] * TOOL_COUNT
line_color = [0] *  TOOL_COUNT
line_scl = [0] * TOOL_COUNT #scl same color length
MAX_NULLS = (2**UTILITY_BITS)-2
SCL_MAX=(2**UTILITY_BITS)-1 #Single Color Line Max

s = ""
def rgbToHex(rgb): #Converts RBG to hex
    return('#%02x%02x%02x' % rgb) #Converts the RGB values to hex
hxclr = []
hexcolors = "" #Create blank list to accumulate hex colors
for RGB in color_to_integer:
    rgb = RGB[0],RGB[1],RGB[2]
    hxclr.append(str(rgbToHex(rgb)))
hxclr_ = []
for i in range(len(pool)):
    hxclr_.append(hxclr[pool[i]])


hexcolors="\n".join(hxclr_)

#print("hexcolors: " + str(len(color_to_integer)))    
with open("image_hex.txt", "w",encoding="UTF-8") as text_file:
    text_file.write(hexcolors)

output_lines = []
PoC=[0]*NUM_MARKERS
for i in range(len(PoC)):
    clist=[]
    for p in range(len(pool)):
        if pool[p] == i:
            clist.append(p)
    PoC[i]=clist

#print(PoC)
ticks = 0
while True:
    end = False
    line_go = [False] * TOOL_COUNT
    line_scl = [0] * TOOL_COUNT
    line_marker = [0] * TOOL_COUNT
    aval_colors = []
    for a in PoC:
        aval_colors.append(a.copy())
    #print(aval_colors)

            
    
#    print(line_progress)
    for i in range(0,len(line_go)):
        if (actual_line+i>IMG_WIDTH-1):
            break
        line_color[i] = image_matrix[line_progress[i],actual_line+i]
        mymarker = aval_colors[line_color[i]][0]
        line_marker[i] = mymarker
        mycolor = line_color[i] 
#        print(line_color[i],mycolor)
#        print(aval_colors)
        if len(aval_colors[line_color[i]])>1:
            aval_colors[line_color[i]].pop(0)

        for y in range (line_progress[i],(line_progress[i]+SINGLE_DOT_LINE) if ONLY_DOTS else (line_progress[i]+SCL_MAX)):
            if y>=IMG_HEIGHT:
                break
            if image_matrix[y,actual_line+i] == mycolor:
                line_scl[i] = line_scl[i]+1
            else:
                break
        if (i == 0):
            line_go[i] = True
        else:
            if line_progress[i]+OFFSET<(line_progress[i-1]):
                if line_progress[i]+line_scl[i]+OFFSET>=(line_progress[i-1]):
                    line_scl[i] = line_progress[i-1] - (line_progress[i] + OFFSET)
                colorBlocked = False
                blocked_by = 0
                for q in range(0,i):
                    if mymarker == line_marker[q] and line_go[q]:
                        blocked_by = q
                        colorBlocked = True
                    if colorBlocked:
                        if line_scl[i]>line_scl[blocked_by]:
                            line_go[i] = True
                            line_go[blocked_by] = False
                if not colorBlocked:
                    line_go[i] = True


    #break
    subs = ""
    subs_ = []
    moveToNextLine = False
    isLine = False
    colorcheck=[]
    for i in range(0,len(line_go)):
        progressor = 0
        if line_go[i]:
            progressor = line_scl[i]-1 if line_scl[i]-1 <= SCL_MAX else SCL_MAX
            
            if line_marker[i] in colorcheck:
                print("ERROR")
                print(line_marker)
                print(line_go)
                print(line_scl)
                raise Exception("ses asi posral,ne???")
                break
            colorcheck.append(line_marker[i])

            X = progressor << COLOR_BITS | line_marker[i] # combine number of same color and color value into one integer

            #print(line_progress[i],line_scl[i],progressor)
            #print(X,CODEPOINTS[X])
            subs_.append(CODEPOINTS[X])
# TODO: Decoding this seems to really slow down the machine in RR, commenting out for the time being
#            if progressor==SCL_MAX:
#                subs_.append(CODEPOINTS[line_scl[i]])
            
            if line_scl[i] >= SINGLE_DOT_LINE:
                isLine=True
            line_progress[i] = line_progress[i]+line_scl[i]
            if line_progress[i] > IMG_HEIGHT:
                line_progress[i] = IMG_HEIGHT

            if line_progress[i] == IMG_HEIGHT:
                if i!=0:
                    print("ERROR:Other then line[0] achieved end of line")
                    end = True
                    break
                moveToNextLine=True
        else:
            subs_.append(",")

    # calculate the number of game ticks
    # dots takes 2, line takes 3
    if isLine:
        ticks = ticks + 3 
    else:
        ticks = ticks + 2

    if moveToNextLine:
        line_progress.pop(0)
        line_progress.append(0)
        actual_line = actual_line + 1
        p=actual_line/IMG_WIDTH*100
        print(f"{p:.2f}% ",end = "\r")
        if actual_line==IMG_WIDTH:
            end = True
            break
                
                

    for i in range(len(subs_)-1,0,-1):
        if subs_[i] == ",":
            subs_.pop(i)
        else:
            break

    nullNum = 0
    for i in range(len(subs_)-1,-1,-1):
        if subs_[i] == "," and nullNum<MAX_NULLS:
            nullNum = nullNum + 1
            subs_.pop(i)

        elif subs_[i] == "," and nullNum==MAX_NULLS:
            subs_.pop(i)
            nullNum = nullNum + 1
            subs_.insert(i,CODEPOINTS[nullNum<<COLOR_BITS|COLOR_MAXVALUE])
            nullNum = 0
        else:
            if nullNum>0:
                subs_.insert(i+1,CODEPOINTS[nullNum<<COLOR_BITS|COLOR_MAXVALUE])
                nullNum = 0
    
    if nullNum>0:
        subs_.insert(0,CODEPOINTS[nullNum<<COLOR_BITS|COLOR_MAXVALUE])
        nullNum = 0
        

    subs="".join(subs_)
    output_lines.append(subs)


    if end:
        break

output_lines.insert(0,"0;"+str(IMG_WIDTH)+";"+str(IMG_HEIGHT)+";"+str(NUM_MARKERS)+";"+str(random.randint(0, 100000)))
print(output_lines[0],output_lines[1])
s = "\n".join(output_lines)
slen = len(s)
print("Lenght: " + str(slen) + "\nTable count:" + str(slen/(400.0*515.0)) + "\nPrint time: " + str(ticks/30/3600))
with open("image_data.txt", "w",encoding="UTF-8") as text_file:
    text_file.write(s)
