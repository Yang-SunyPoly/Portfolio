import numpy as np
import gradio as gr
import math as m
import cv2

def getOneLBPLabel(subimage, label_type):
    
    Lable = 0
    Array = np.copy(subimage)
    Array = Array.flatten()     #make Array into 1 Dim
    Center = Array[4]           #copy Center for comparison 
    Check_Empty = True

    CA = np.copy(Array)
    Array = np.array([CA[0],CA[1],CA[2],CA[5],CA[8],CA[7],CA[6],CA[3]], dtype="int")
    
    for Index in range(Array.shape[0]):
        if Array[Index] > Center:
            Array[Index] = 1
            Check_Empty = False     #is not Label 0
        else:
            Array[Index] = 0
    if Check_Empty:
        return 0
    
    match label_type.value:
        case 'Uniform':
            Swap_Zero_To_One = False
            Swap_One_To_Zero = False
            for Index in range(Array.shape[0]):
                if Index != 7:  #If is not last element, compare with next
                    Check = Array[Index] - Array[(Index + 1)]
                else:   #If is last element, compare with first element
                    Check = Array[Index] - Array[0]
                if Check < 0:   #if is a zero to one swap
                    if Swap_Zero_To_One == False:
                        Swap_Zero_To_One = True
                    else:   #if there are more than one, zero to one swap
                        Lable = 8
                        break
                if Check > 0:   #if is a one to zero swap
                    if Swap_One_To_Zero == False:
                        Swap_One_To_Zero = True
                    else:   #if there are more than one, one to zero swap
                        Lable = 8
                        break
                if Array[Index] == 1 and Check == 0:    #if is ones in sequence
                    Lable += 1
            if Swap_One_To_Zero:   #if is not 8th lable, needed because of detection of label
                Lable += 1
                        
        case 'Full':
            Bin =""     #for binary number
            for Index in range(Array.shape[0]):
                if Array[Index] == 1:
                    Bin = "1" + Bin      #string concatenation
                else:
                    Bin = "0" + Bin
            Lable = int(Bin,2)    #convert binary to decimal 
            
        case _:
            Swap_Zero_To_One = False
            Swawp_One_To_Zero = False
            Pos_Of_Beg = 0
            for Index in range(Array.shape[0]):
                if Index != 7:
                    Check = Array[Index] - Array[(Index + 1)]
                else:
                    Check = Array[Index] - Array[0]
                if Check < 0:
                    if Swap_Zero_To_One == False:
                        Pos_Of_Beg = Index  #save where Zero to One swap Happens
                        Swap_Zero_To_One = True
                    else:
                        Lable = 8
                        break
                if Check > 0:
                    if Swawp_One_To_Zero == False:
                        Swawp_One_To_Zero = True
                    else:
                        Lable = 8
                        break
                if Array[Index] == 1 and Check == 0:
                    Lable += 1
            if Swawp_One_To_Zero:
                Lable += 1
            if Lable == 9:  #if is garbage label
                Lable = 58
            else:
                if Pos_Of_Beg == 0:
                    Lable = Pos_Of_Beg * 7 + Lable
                else:
                    Lable = Pos_Of_Beg * 7 + 1 + Lable
            
    return Lable

def getLBPImage(image, label_type):
    
    Padded = cv2.copyMakeBorder(image, 1, 1, 1, 1, cv2.BORDER_CONSTANT, None, value = 0)
    LBP_Image = np.copy(image)
    
    for Index_Y in range(image.shape[0]):
        for Index_X in range(image.shape[1]):
            LBP_Image[Index_Y, Index_X] = getOneLBPLabel(Padded[Index_Y:Index_Y + 3, Index_X:Index_X + 3], label_type)
            
    return LBP_Image
    
def getOneRegionLBPFeatures(subImage, label_type):
    Histogram = 0
    #subImage = np.expand_dims(subImage, axis=-1)
    match label_type.value:
        case 'Uniform':
            Histogram = cv2.calcHist([subImage],[0],None,[10],[0,10])[:,0]            
        case 'Full': 
            Histogram = cv2.calcHist([subImage],[0],None,[256],[0,256])[:,0]
        case _: 
            Histogram = cv2.calcHist([subImage],[0],None,[59],[0,59])[:,0]
            
    Total_Pixels = subImage.shape[0] * subImage.shape[1]
    Histogram /= Total_Pixels   
    return Histogram

def getLBPFeatures(featureImage, regionSideCnt, label_type):
    Sub_Width = m.floor(featureImage.shape[1] / regionSideCnt)
    Sub_Height = m.floor(featureImage.shape[0] / regionSideCnt)
    
    Hist = []
    for Index_Y in range(regionSideCnt):
        for Index_X in range(regionSideCnt):
            Sub_Image = featureImage[Index_Y * Sub_Height:(Index_Y + 1) * Sub_Height, Index_X * Sub_Width:(Index_X + 1) * Sub_Width]
            Hist.append(getOneRegionLBPFeatures(Sub_Image, label_type))
    All_Hist = np.copy(Hist)
    All_Hist = np.reshape(All_Hist,(All_Hist.shape[0]*All_Hist.shape[1],))
    return All_Hist