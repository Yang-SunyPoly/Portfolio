import math as m
import numpy as np
import cv2
import os
import General_A03 as Test

Path_File_Image_Dir = "./JPEGImages"

def find_WBC(image):
    
    Post_Clean = np.copy(image)
    
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            color = 0            
            for c in image[y,x]:
                color += c
            if color >= 550:
                Post_Clean[y,x] = 0
            elif image[y,x,2] > 150:
                Post_Clean[y,x] = 0
            else:
                Post_Clean[y,x] = 255
                
    ReturnList = []
    
    Post_Clean = cv2.cvtColor(Post_Clean, cv2.COLOR_BGR2GRAY) 
    
    Blob_Index, Blobs = cv2.connectedComponents(Post_Clean)

    for i in range(1,Blob_Index + 1):
        if len(np.where(Blobs == i)[0]) > 250:
            Coords = np.where(Blobs == i)
            Min_X = np.min(Coords[1])
            Max_X = np.max(Coords[1])
            Min_Y = np.min(Coords[0])
            Max_Y = np.max(Coords[0])
            
            ReturnList.append([Min_Y, Min_X, Max_Y, Max_X])

    return ReturnList

    """
        Option 1:
        -Clean (nuke out anything that is not white pixel, convert to gray scale)
        -Start from first white detected
        -extend box from all sides until hit black pixel
        
        extend one side until one of the three conditions apply 
            1. No white pixel detected
            2. The rate of black pixel detected went up compare from before
            3. the rate of white pixel is insignificant
            4. no black pixel detected at all
        
        Does not Work, Detecting boxes from pixel to pixel turn out to be too much work and would take too long
    """

    """
        option 2:
        -Clean (nuke out anything that is not white pixel, convert to gray scale)
        -Pick out all of the detected blobs
        -Assuming the shape of each red cells are symmetrical in one of it's direction
        -find starting point
        -detect how many pixel from starting point to the heigh point and the bouding box is that distance times two
        -stop until all of sub image went though
    """

def find_RBC(image):
    
    Post_Clean = np.copy(image)
    
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            color = 0            
            for c in image[y,x]:
                color += c
            if color >= 550:
                Post_Clean[y,x] = 0
            elif image[y,x,2] > 150:
                Post_Clean[y,x] = 0
            else:
                Post_Clean[y,x] = 255
    
    Sub_Bound = []
    
    Post_Clean = cv2.cvtColor(Post_Clean, cv2.COLOR_BGR2GRAY) 
    
    Blob_Index, Blobs = cv2.connectedComponents(Post_Clean)

    for i in range(1,Blob_Index + 1):
        if len(np.where(Blobs == i)[0]) > 250:
            Coords = np.where(Blobs == i)
            Min_X = np.min(Coords[1])
            Max_X = np.max(Coords[1])
            Min_Y = np.min(Coords[0])
            Max_Y = np.max(Coords[0])
            
            Sub_Bound.append([Min_Y, Min_X, Max_Y, Max_X])
            
            Sub_Image = Post_Clean[Min_Y:Max_Y,Min_X:Max_X]
            
            RedCell_Min_Y, RedCell_Min_X,RedCell_Max_Y,RedCell_Max_X = 0, 0, 0, 0
            
            while RedCell_Max_Y < Max_Y:
                pass
            while RedCell_Max_X < Max_X:
                pass
            
            #While loop would take to long when looking pixel to pixel, would run into same problem with option 1 
            
"""
    #Code for option 1(did not finish)
    Post_Clean = np.copy(image)
    
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            color = 0            
            for c in image[y,x]:
                color += c
            if color >= 550:
                Post_Clean[y,x] = 0
            else:
                Post_Clean[y,x] = 255
    
    Checked = np.empty([])
    ReturnList = np.empty([])
    
    Post_Clean = cv2.cvtColor(Post_Clean, cv2.COLOR_BGR2GRAY) 
    
    for y in range(Post_Clean.shape[0]):
        for x in range(Post_Clean.shape[1]):
            if Post_Clean[y,x] == 0 and Check_existed(y,x,Checked):
                Top, Bot, Left, Right = y, y, x, x
                while (np.sum(Post_Clean[Top:Bot,Left:Right])) / ((Bot - Top) * (Right - Left)) == 255:
                    Bot += 1
                    Left -= 1
                    Right += 1
                while Red_Detection(0,Top, Bot, Left, Right, Post_Clean):
                    pass
  
                    
def Red_Detection(Side ,Top, Bot, Left, Right, image): #0 = left, 1 = Bot , 2 = Right
    Extend = True
    if Side == 0:
        Test = np.array(image[Top:Bot, Left - 10: Right])
        if np.sum(Test) == 0:   #No white pixel detected
            Extend = False
        elif np.sum(Test) / ((Bot - Top) * (Right - Left)) == 255: # no black pixel detected at all
            Extend = False
        elif np.sum(Test) / ((Bot - Top) * (Right - Left)) < 25: # the rate of white pixel is insignificant
            Extend = False
        
    return Extend

       
 
def Check_existed(y,x,list):
    if y in list or x in list:
        True_False = False
    else:
        True_False = True
    return True_False
"""

def Show_Image_Path(Image_Path):
    
    Path_File_Image = os.path.join(Path_File_Image_Dir , Image_Path)
    
    image = cv2.imread(Path_File_Image)

    cv2.imshow("Pre_Image",image)

    cv2.waitKey(0)

    cv2.destroyAllWindows()
    
def Show_Image_Array(Image):
    
    cv2.imshow("Image",Image)

    cv2.waitKey(0)

    cv2.destroyAllWindows()
    
def Show_Image_Compare(Pre,Clean,Post):
    
    cv2.imshow("Pre",Pre)
    cv2.imshow("Clean",Clean)
    cv2.imshow("Post",Post)
    
    cv2.waitKey(0)

    cv2.destroyAllWindows()

def Clean_Image(Image_Path):
    
    Path_File_Image = os.path.join(Path_File_Image_Dir , Image_Path)
    
    Image = cv2.imread(Path_File_Image)
    
    Post_Clean = np.copy(Image)
    
    Post_Process = np.copy(Image)
    
    Post_Clean = cv2.cvtColor(Post_Clean, cv2.COLOR_BGR2GRAY) 
    
    Bounding_List = [] #np.empty([])

    for y in range(Image.shape[0]):
        for x in range(Image.shape[1]):
            color = 0            
            for c in Image[y,x]:
                color += c
            if color >= 550:
                Post_Clean[y,x] = 0
            #else:
            #    Post_Clean[y,x] = 255
            if Image[y,x,2] > 150:
                Post_Clean[y,x] = 0
            else:
                Post_Clean[y,x] = 255

    Blob_Index, Blobs = cv2.connectedComponents(Post_Clean)

    for i in range(1,Blob_Index + 1):
        if len(np.where(Blobs == i)[0]) > 100:
            Coords = np.where(Blobs == i)
            Min_X = np.min(Coords[1])
            Max_X = np.max(Coords[1])
            Min_Y = np.min(Coords[0])
            Max_Y = np.max(Coords[0])

            print(Min_Y, Min_X, Max_Y, Max_X)
            Bounding_List.append([Min_Y, Min_X, Max_Y, Max_X])
            print(Bounding_List)

    #Bounding_List = np.delete(Bounding_List,0)
    print(Bounding_List)

    Test.draw_bounding_boxes(Post_Process, Bounding_List, (0,255,0))
    
    #Post_Clean = cv2.cvtColor(Post_Clean, cv2.COLOR_BGR2GRAY) 
    
    #print("Size Y ", len(range(Post_Clean.shape[0])))
    #print("Size X ", len(range(Post_Clean.shape[1])))
    """
    for y in range(Post_Clean.shape[0]):
        for x in range(Post_Clean.shape[1]):
            if Post_Clean[y,x] == 0:
                Top, Bot, Left, Right = y, y, x, x
                while Post_Clean[Top, Left] != 255 and Left > 0:
                    Left -= 1
                while Post_Clean[Top, Right] != 255 and Right < len(range(Post_Clean.shape[1])) - 1:
                    Right += 1
                while Post_Clean[Bot, x] != 255 and Bot < len(range(Post_Clean.shape[0])) - 1:
                    Bot += 1
                
                Size = (Right - Left) * (Bot - Top)
                
                if Size < 100:
                    Post_Clean[Top:Bot, Left:Right] = 255
            
                #print(Clean_Dark)
    """
             
    Show_Image_Compare(Image, Post_Clean, Post_Process)
    
    
    


def main():
    
    Path_File_Image_List = os.listdir(Path_File_Image_Dir)
    
    
    Clean_Image(Path_File_Image_List[43])
    
        
if __name__ == "__main__":
    main()