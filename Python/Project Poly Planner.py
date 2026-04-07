"""
Code made by: Yuxuan Yang
SUNY Polytechnic Institute
Fall 2024 Semester
CS 512 Dr.Zaman
"""
import tkinter as TK
import time
import numpy as np
import datetime as DATE
import calendar as CL
import os
from pathlib import Path

# variables 
Entry = [[],
         [],
         [],
         [],
         [],
         [],
         []]

file_path = Path("Saves")

Spending = np.array([0,0,0,0,0,0,0])
Exchange_Spend = np.array([0,0,0,0,0,0,0])
Points_Spend = np.array([0,0,0,0,0,0,0])

Total_Points = Goal_Points = Total_Exchange = Goal_Exchange = Total_Money = Goal_Money = 0
Window = TK.Tk()

directory_name = "Saves"

Current_Date = DATE.datetime.now()
Current_Calendar = CL.Calendar()

#Acquire dates
def Whats_date(a):
    if a == 0:
        a = 7
    calendar = CL.Calendar()
    Date_List_Re = []
    Date_list = calendar.monthdatescalendar(int(Current_Date.strftime("%Y")),int(Current_Date.strftime("%m")))
    
    for x in range(len(Date_list)):
        for y in range(len(Date_list[x])):
            Date_List_Re += [str(Date_list[x][y])]

    Today = int(Current_Date.strftime("%w"))
    Today_day = int(Current_Date.strftime("%d"))
    
    if Today_day + a > len(Date_List_Re):
        Date_list_Next = calendar.monthdatescalendar(int(Current_Date.strftime("%Y")),int(Current_Date.strftime("%m")) + 1)
        Date_List_Re_Next = []
        
        for x in range(len(Date_list_Next)):
            for y in range(len(Date_list_Next[x])):
                Date_List_Re_Next += [str(Date_list_Next[x][y])]
                
        return(Date_List_Re_Next[a - 1])

    if a == Today:
        return(Date_List_Re[int(Today_day)])
    
    if a < Today_day:
        Index = Today_day - (Today - a)
        return(Date_List_Re[int(Index)])

    return(Date_List_Re[int(a)])

#creating buttons
But_Day = [TK.Button(Window,text = str(Spending[0]), bg = "snow", activebackground="gray25", command = lambda: Input_Daily(0), font = ("Minion Pro",18)),
            TK.Button(Window,text = str(Spending[1]), bg = "snow", activebackground="gray25", command = lambda: Input_Daily(1), font = ("Minion Pro",18)),
            TK.Button(Window,text = str(Spending[2]), bg = "snow", activebackground="gray25", command = lambda: Input_Daily(2), font = ("Minion Pro",18)),
            TK.Button(Window,text = str(Spending[3]), bg = "snow", activebackground="gray25", command = lambda: Input_Daily(3), font = ("Minion Pro",18)),
            TK.Button(Window,text = str(Spending[4]), bg = "snow", activebackground="gray25", command = lambda: Input_Daily(4), font = ("Minion Pro",18)),
            TK.Button(Window,text = str(Spending[5]), bg = "snow", activebackground="gray25", command = lambda: Input_Daily(5), font = ("Minion Pro",18)),
            TK.Button(Window,text = str(Spending[6]), bg = "snow", activebackground="gray25", command = lambda: Input_Daily(6), font = ("Minion Pro",18))]

#creating labels
Label_Day = [TK.Label(Window,text = str(Whats_date(1)),bg = "gold",font = ("Minion Pro",18)),
             TK.Label(Window,text = str(Whats_date(2)),bg = "gold",font = ("Minion Pro",18)),
             TK.Label(Window,text = str(Whats_date(3)),bg = "gold",font = ("Minion Pro",18)),
             TK.Label(Window,text = str(Whats_date(4)),bg = "gold",font = ("Minion Pro",18)),
             TK.Label(Window,text = str(Whats_date(5)),bg = "gold",font = ("Minion Pro",18)),
             TK.Label(Window,text = str(Whats_date(6)),bg = "gold",font = ("Minion Pro",18)),
             TK.Label(Window,text = str(Whats_date(0)),bg = "gold",font = ("Minion Pro",18))]

#Window setting for main window
Window_Size = "1600x600"
Window.title("Planner")
Window.geometry(Window_Size)
Window.configure(bg = "gold")

#Setting up addtional buttons, label and buttons positions
But_Total_Money = TK.Button(Window,text = "Totals", bg = "skyblue1", activebackground="gray25", command = lambda: Input("Total"), font = ("Minion Pro",18))
But_Goal_Money = TK.Button(Window,text = "Weekly Goals", bg = "skyblue1", activebackground="gray25", command = lambda: Input("Goal"), font = ("Minion Pro",18))
But_Save = TK.Button(Window, text = "Save",  bg = "skyblue1", activebackground="gray25", command = lambda: Save(), font = ("Minion Pro",18))
But_View = TK.Button(Window, text = "View History",  bg = "skyblue1", activebackground="gray25", command = lambda: View(), font = ("Minion Pro",18))

But_Total_Money.grid(row=0,column=0,sticky="ew")
But_Goal_Money.grid(row=1,column=0,sticky="ew")
But_Save.grid(row=2,column=0,sticky="ew")
But_View.grid(row=3,column=0,sticky="ew")

Label_Day[0].grid(row=9,column=5,sticky="ew",pady=(150,0),padx=10)
Label_Day[1].grid(row=9,column=6,sticky="ew",pady=(150,0),padx=10)
Label_Day[2].grid(row=9,column=7,sticky="ew",pady=(150,0),padx=10)
Label_Day[3].grid(row=9,column=8,sticky="ew",pady=(150,0),padx=10)
Label_Day[4].grid(row=9,column=9,sticky="ew",pady=(150,0),padx=10)
Label_Day[5].grid(row=9,column=10,sticky="ew",pady=(150,0),padx=10)
Label_Day[6].grid(row=9,column=11,sticky="ew",pady=(150,0),padx=10)

But_Day[0].grid(row=10,column=5,sticky="ew", padx=10)
But_Day[1].grid(row=10,column=6,sticky="ew",padx=10)
But_Day[2].grid(row=10,column=7,sticky="ew",padx=10)
But_Day[3].grid(row=10,column=8,sticky="ew",padx=10)
But_Day[4].grid(row=10,column=9,sticky="ew",padx=10)
But_Day[5].grid(row=10,column=10,sticky="ew",padx=10)
But_Day[6].grid(row=10,column=11,sticky="ew",padx=10)

Current_Date_Check = 0

#Main function
def main():
    #Getting current Date's save file and load it up if exist
    global Total_Points, Goal_Points, Total_Exchange, Goal_Exchange, Total_Money, Goal_Money
    if not os.path.exists(file_path):
        os.mkdir(directory_name)
    
    Year = int(Current_Date.strftime("%Y"))
    Month = int(Current_Date.strftime("%m"))
    Today = int(Current_Date.strftime("%d"))
    List = Current_Calendar.monthdayscalendar(Year, Month)

    exit = False
    for Weeks in range(len(List)):
        for Days in List[Weeks]:
            if Today == Days:
                Save_Week = Weeks
                exit = True
                break
        if exit:
            break

    Check_Save_File = Path("Saves/" + str(Year) + "/" + str(Month) + "/" + str(Save_Week) + ".txt")
    Load(Check_Save_File)
    Window.mainloop()

#Rest function when loading, so don't adding up
def Rest():
    global Entry, Spending, Exchange_Spend, Points_Spend, Total_Points, Goal_Points, Total_Exchange, Goal_Exchange, Total_Money, Goal_Money
    Entry = [[],
         [],
         [],
         [],
         [],
         [],
         []]

    Spending = np.array([0,0,0,0,0,0,0])
    Exchange_Spend = np.array([0,0,0,0,0,0,0])
    Points_Spend = np.array([0,0,0,0,0,0,0])

    Total_Points = Goal_Points = Total_Exchange = Goal_Exchange = Total_Money = Goal_Money = 0

#Load function for loading variables
def Load(Check_Save_File):
    global Entry, Spending, Exchange_Spend, Points_Spend, Total_Points, Goal_Points, Total_Exchange, Goal_Exchange, Total_Money, Goal_Money
    Rest()
    Check_Save_File = Path(Check_Save_File)
    if Check_Save_File.exists():
        File = open(Check_Save_File, "r")
        Text = File.read().split()

        for Index,Items in enumerate(Text):
            if Items == 'Total_Points':
                Total_Points = int(Text[Index + 1])
                break
        
        for Index,Items in enumerate(Text):
            if Items == 'Goal_Points':
                Goal_Points = int(Text[Index + 1])
                break
        
        for Index,Items in enumerate(Text):
            if Items == 'Total_Exchange':
                Total_Exchange = int(Text[Index + 1])
                break
            
        for Index,Items in enumerate(Text):
            if Items == 'Goal_Exchange':
                Goal_Exchange = int(Text[Index + 1])
                break

        for Index,Items in enumerate(Text):
            if Items == 'Total_Money':
                Total_Money = int(Text[Index + 1])
                break
        
        for Index,Items in enumerate(Text):
            if Items == 'Goal_Money':
                Goal_Money = int(Text[Index + 1])
                break
        
        for Index,Items in enumerate(Text):
            if Items == 'Day':
                Change_Daily(int(Text[Index + 1]),str(Text[Index + 2]),str(Text[Index + 3]))

#Save function, writing details to a text file      
def Save():

    #Setting folder structure
    Year = int(Current_Date.strftime("%Y"))
    Month = int(Current_Date.strftime("%m"))
    Today = int(Current_Date.strftime("%d"))
    List = Current_Calendar.monthdayscalendar(Year, Month)
    
    file_path = Path("Saves/" + str(Year))
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    file_path = Path("Saves/" + str(Year) + "/"+ str(Month))
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    for Weeks in range(len(List)):
        for Days in List[Weeks]:
            if Today == Days:
                Save_Week = Weeks
                break
                break

    Check_Save_File = Path("Saves/" + str(Year) + "/" + str(Month) + "/" + str(Save_Week) + ".txt")
    if not Check_Save_File.exists():
        with open(Check_Save_File, 'w') as file:
            file.close()
    
    #Saving details
    file = open(Check_Save_File,"w")
    Save_Text = "Year " + str(Year) +"\n"
    Save_Text += "Month " + str(Month) + "\n"
    Save_Text += "Week " + str(Save_Week) + "\n"

    Save_Text += "Total_Points " + str(Total_Points) + "\n"
    Save_Text += "Goal_Points " + str(Goal_Points) + "\n"
    Save_Text += "Total_Exchange " + str(Total_Exchange) + "\n"
    Save_Text += "Goal_Exchange " + str(Goal_Exchange) + "\n"
    Save_Text += "Total_Money " + str(Total_Money) + "\n"
    Save_Text += "Goal_Money " + str(Goal_Money) + "\n"

    for Day in range(len(Entry)):
        if len(Entry[Day]) > 0:
            for Items in range(len(Entry[Day])):
                Save_Text += "Day " + str(Day) + " "
                Save_Text += str(Entry[Day][Items][0]) + " " + str(Entry[Day][Items][1]) + "\n"

    file.write(str(Save_Text))
    file.close()

#Change Dates info for main UI
def View():

    #Grabbing all files dir
    global Current_Date_Check
    List_Date = []
    for Year in os.listdir(file_path):
        Path_Month = (str(file_path) + "/" + Year)
        for Month in os.listdir(Path_Month):
            Path_Week = (str(file_path) + "/" + Year + "/" + Month)
            for Week in os.listdir(Path_Week):
                Apending = str(str(Path_Week) + "/" + Week)
                List_Date.append(Apending)
        
    Current_Date_Check = 0
    if  len(List_Date) >= 0:
        date = List_Date[Current_Date_Check]
    else:
        return()

    W = TK.Tk()
    W.configure(bg = "gold")
    W.title("View")
    W.geometry("300x100")
    Label = TK.Label(W,text = date,bg="gold",font = ("Minion Pro",15))
    Label.pack(padx = 1, pady = 1)
    Change = TK.Button(W,text = "Ok", bg = "skyblue1", activebackground="gray25", command = lambda: [destory_window(W),Load(date)], font = ("Minion Pro",10))
    Change.pack(padx = 2, pady = 1,fill="both")
    Change_date = TK.Button(W,text = "Next", bg = "skyblue1", activebackground="gray25", command = lambda: [Change_date_Next()], font = ("Minion Pro",10))
    Change_date.pack(padx = 2, pady = 2,fill="both")

    #Changing dates
    def Change_date_Next():
        global Current_Date_Check
        if Current_Date_Check >= (len(List_Date) - 1):
            Current_Date_Check = 0
        else:
            Current_Date_Check += 1
        date = List_Date[Current_Date_Check]
        Label.config(text = date)
        Load(date)

#Applying inputs
def Change_Value(x,w,wi):
    global Total_Money, Goal_Money, Total_Points, Total_Exchange, Goal_Exchange, Goal_Points
    if x == "Total" and str(w.get()).isdigit():
        Total_Money = int(w.get())
        destory_window(wi)
    elif x == "Add_Money" and str(w.get()).isdigit():
        Total_Money += int(w.get())
        But_Total_Money.config(text = "Total")
        destory_window(wi)
    elif x == "Subtract_Money" and str(w.get()).isdigit():
        if Total_Money - int(w.get()) >= 0:
            Total_Money -= int(w.get())
            But_Total_Money.config(text = "Total")
            destory_window(wi)
        else:
            Warning("Not Enough Money")
    elif x == "Swipe" and str(w.get()).isdigit():
        Total_Exchange = int(w.get())
        destory_window(wi)
    elif x == "Points" and str(w.get()).isdigit():
        Total_Points = int(w.get())
        destory_window(wi)
    elif x == "Goal" and str(w.get()).isdigit():
        Goal_Money = int(w.get())
        for I in range(len(But_Day)):
            But_Day[I].config(bg = whatColor(I))
        destory_window(wi)
    elif x == "Goal_Swipe" and str(w.get()).isdigit():
        Goal_Exchange = int(w.get())
        for I in range(len(But_Day)):
            But_Day[I].config(bg = whatColor(I))
        destory_window(wi)
    elif x == "Goal_Points" and str(w.get()).isdigit():
        Goal_Points = int(w.get())
        for I in range(len(But_Day)):
            But_Day[I].config(bg = whatColor(I))
        destory_window(wi)
    else:
        Warning("Did not input a number")
        
#Giving warning
def Warning(text):
    W = TK.Tk()
    W.configure(bg = "gold")
    W.title("Warning")
    W.geometry("300x100")
    Label = TK.Label(W,text = text,bg="gold",font = ("Minion Pro",15))
    Label.pack(padx = 1, pady = 1)
    Quit = TK.Button(W,text = "Ok", bg = "skyblue1", activebackground="gray25", command = lambda: destory_window(W), font = ("Minion Pro",10))
    Quit.pack(padx = 2, pady = 1,fill="both")
    
#Setting Functions when Goals or Total is pressed
def Input(x):
    #Window setting
    WI = TK.Tk()
    
    WI.configure(bg = "gold")
    WI.title("Enter the amount")
    WI.geometry("400x200")
    
    Frame = TK.Frame(WI)
    Frame.columnconfigure(0,weight=1)
    Frame.columnconfigure(1,weight=1)

    #Which Button is pressed
    if x == "Goal":
        Label_Money = TK.Label(Frame, text = "Money",justify="center",bg = "skyblue1")
        Label_Money_Amount = TK.Label(Frame, text = str(Goal_Money),justify="center",bg = "skyblue1")
        Label_Swipe = TK.Label(Frame, text = "Swipes",justify="center",bg = "skyblue1")
        Label_Swipe_Amount = TK.Label(Frame, text = str(Goal_Exchange),justify="center",bg = "skyblue1")
        Label_Points = TK.Label(Frame, text = "Points",justify="center",bg = "skyblue1")
        Label_Points_Amount = TK.Label(Frame, text = str(Goal_Points),justify="center",bg = "skyblue1")

        Label_Money.grid(column = 0, row = 0,sticky="we")
        Label_Money_Amount.grid(column = 1, row = 0,sticky="we")
        Input_Line = TK.Entry(Frame)
        Enter = TK.Button(Frame, text="Set", command = lambda: Change_Value(x, Input_Line,WI), font = ("Minion Pro",10))
        Cancel = TK.Button(Frame, text="Cancel", command = lambda: destory_window(WI), font = ("Minion Pro",10))
        Input_Line.grid(column = 0, row = 1, columnspan = 2, rowspan = 1,sticky="we")
        Enter.grid(column = 0, row = 2,sticky="we")
        Cancel.grid(column = 1, row = 2,sticky="we")
        
        Label_Swipe.grid(column = 0, row = 4,sticky="we")
        Label_Swipe_Amount.grid(column = 1, row = 4,sticky="we")
        Input_Line_Swipe = TK.Entry(Frame)
        Input_Line_Swipe.grid(column = 0, row = 5, columnspan = 2, rowspan = 1,sticky="we")
        Enter_Swipe = TK.Button(Frame, text="Set", command = lambda: Change_Value("Goal_Swipe", Input_Line_Swipe,WI), font = ("Minion Pro",10))
        Cancel_Swipe = TK.Button(Frame, text="Cancel", command = lambda: destory_window(WI), font = ("Minion Pro",10))
        Enter_Swipe.grid(column = 0, row = 6,sticky="we")
        Cancel_Swipe.grid(column = 1, row = 6,sticky="we")
        
        Label_Points.grid(column = 0, row = 7,sticky="we")
        Label_Points_Amount.grid(column = 1, row = 7,sticky="we")
        Input_Line_Points = TK.Entry(Frame)
        Input_Line_Points.grid(column = 0, row = 8, columnspan = 2, rowspan = 1,sticky="we")
        Enter_Points = TK.Button(Frame, text="Set", command = lambda: Change_Value("Goal_Points", Input_Line_Points,WI), font = ("Minion Pro",10))
        Cancel_Points = TK.Button(Frame, text="Cancel", command = lambda: destory_window(WI), font = ("Minion Pro",10))
        Enter_Points.grid(column = 0, row = 9,sticky="we")
        Cancel_Points.grid(column = 1, row = 9,sticky="we")
    
    elif x == "Total":

        Label_Money = TK.Label(Frame, text = "Money",justify="center",bg = "skyblue1")
        Label_Money_Amount = TK.Label(Frame, text = str(Total_Money),justify="center",bg = "skyblue1")
        Label_Swipe = TK.Label(Frame, text = "Swipes",justify="center",bg = "skyblue1")
        Label_Swipe_Amount = TK.Label(Frame, text = str(Total_Exchange),justify="center",bg = "skyblue1")
        Label_Points = TK.Label(Frame, text = "Points",justify="center",bg = "skyblue1")
        Label_Points_Amount = TK.Label(Frame, text = str(Total_Points),justify="center",bg = "skyblue1")

        Input_Line = TK.Entry(Frame)
        Enter = TK.Button(Frame, text="Set", command = lambda: Change_Value(x, Input_Line,WI), font = ("Minion Pro",10))
        Cancel = TK.Button(Frame, text="Cancel", command = lambda: destory_window(WI), font = ("Minion Pro",10))
        Input_Line.grid(column = 0, row = 1, columnspan = 2, rowspan = 1,sticky="we")
        Enter.grid(column = 0, row = 2,sticky="we")
        Cancel.grid(column = 1, row = 2,sticky="we")

        Add = TK.Button(Frame, text="Add", command = lambda: Change_Value("Add_Money", Input_Line,WI), font = ("Minion Pro",10))
        Sub = TK.Button(Frame, text="Subtract", command = lambda: Change_Value("Subtract_Money", Input_Line,WI), font = ("Minion Pro",10))
        Label_Money.grid(column = 0, row = 0,sticky="we")
        Label_Money_Amount.grid(column = 1, row = 0,sticky="we")
        Add.grid(column = 0, row = 3,sticky="we")
        Sub.grid(column = 1, row = 3,sticky="we") 
        
        Label_Swipe.grid(column = 0, row = 4,sticky="we")
        Label_Swipe_Amount.grid(column = 1, row = 4,sticky="we")
        Input_Line_Swipe = TK.Entry(Frame)
        Input_Line_Swipe.grid(column = 0, row = 5, columnspan = 2, rowspan = 1,sticky="we")
        Enter_Swipe = TK.Button(Frame, text="Set", command = lambda: Change_Value("Swipe", Input_Line_Swipe,WI), font = ("Minion Pro",10))
        Cancel_Swipe = TK.Button(Frame, text="Cancel", command = lambda: destory_window(WI), font = ("Minion Pro",10))
        Enter_Swipe.grid(column = 0, row = 6,sticky="we")
        Cancel_Swipe.grid(column = 1, row = 6,sticky="we")
        
        Label_Points.grid(column = 0, row = 7,sticky="we")
        Label_Points_Amount.grid(column = 1, row = 7,sticky="we")
        Input_Line_Points = TK.Entry(Frame)
        Input_Line_Points.grid(column = 0, row = 8, columnspan = 2, rowspan = 1,sticky="we")
        Enter_Points = TK.Button(Frame, text="Set", command = lambda: Change_Value("Points", Input_Line_Points,WI), font = ("Minion Pro",10))
        Cancel_Points = TK.Button(Frame, text="Cancel", command = lambda: destory_window(WI), font = ("Minion Pro",10))
        Enter_Points.grid(column = 0, row = 9,sticky="we")
        Cancel_Points.grid(column = 1, row = 9,sticky="we")

    Frame.pack(fill='both')
    
#When a input from daily input is called
def Input_Daily(Day):
    #Windows setting
    WI = TK.Tk()
    
    WI.configure(bg = "gold")
    WI.title("Enter Your Input")
    WI.geometry("400x200")
    
    Frame = TK.Frame(WI)
    Frame.columnconfigure(0,weight=1)
    Frame.columnconfigure(1,weight=1)
    Frame.pack(fill='both')
    
    #Moeny
    Input_Line = TK.Entry(Frame)
    Label_Money = TK.Label(Frame, text = "Money",justify="center",bg = "skyblue1")
    Label_Money_Amount = TK.Label(Frame, text = str(0),justify="center",bg = "skyblue1")
    
    Spent = TK.Button(Frame,text = "Money Spent", command = lambda: [Change_Daily(Day,"Spend",Input_Line.get()),destory_window(WI)], font = ("Minion Pro",10))
    Gain = TK.Button(Frame,text = "Money Gain", command = lambda: [Change_Daily(Day,"Gain",Input_Line.get()),destory_window(WI)], font = ("Minion Pro",10))

    Input_Line.grid(column = 0, row = 1, columnspan = 2, rowspan = 1,sticky="we")
    Spent.grid(column = 0, row = 2,sticky="we")
    Gain.grid(column = 1, row = 2,sticky="we")
    Label_Money.grid(column = 0, row = 0,sticky="we")
    Label_Money_Amount.grid(column = 1, row = 0,sticky="we")

    #Exchange
    Input_Line_Exchange = TK.Entry(Frame)
    Label_Exchange = TK.Label(Frame, text = "Meal Exchange",justify="center", bg = "skyblue1")
    Label_Exchange_Amount = TK.Label(Frame, text = str(0), justify="center", bg = "skyblue1")
    Spent_Exchange = TK.Button(Frame,text = "Used Meal Exchange", command = lambda: [Change_Daily(Day,"Exchange_Spend",Input_Line_Exchange.get()),destory_window(WI)], font = ("Minion Pro",10))

    Label_Exchange.grid(column = 0, row = 3,sticky="we")
    Label_Exchange_Amount.grid(column = 1, row = 3,sticky="we")
    Input_Line_Exchange.grid(column = 0, row = 4, columnspan = 2, rowspan = 1,sticky="we")
    Spent_Exchange.grid(column = 0, row = 5,sticky="we", columnspan = 2, rowspan = 1)
    
    #Points
    Input_Line_Points = TK.Entry(Frame)
    Label_Points = TK.Label(Frame, text = "Points",justify="center", bg = "skyblue1")
    Label_Points_Amount = TK.Label(Frame, text = str(0), justify="center", bg = "skyblue1")
    Spent_Points = TK.Button(Frame,text = "Points Spent", command = lambda: [Change_Daily(Day,"Points_Spend",Input_Line_Points.get()),destory_window(WI)], font = ("Minion Pro",10))
    Gain_Points = TK.Button(Frame,text = "Points Refiled", command = lambda: [Change_Daily(Day,"Points_Gain",Input_Line_Points.get()),destory_window(WI)], font = ("Minion Pro",10))

    Label_Points.grid(column = 0, row = 6,sticky="we")
    Label_Points_Amount.grid(column = 1, row = 6,sticky="we")
    Input_Line_Points.grid(column = 0, row = 7, columnspan = 2, rowspan = 1,sticky="we")
    Spent_Points.grid(column = 0, row = 8,sticky="we", columnspan = 1, rowspan = 1)
    Gain_Points.grid(column = 1, row = 8,sticky="we", columnspan = 1, rowspan = 1)

    Spending_Points = Spending_Exchange = Spending_Money = 0

    #Adding input to List
    for Index,Item in enumerate(Entry[Day]):
        if Entry[Day][Index][0] == "Spend":
            Make_Label = TK.Label(WI,text = "Money Spent: " + " " + str(Entry[Day][Index][1]))
            Make_Label.pack(fill = "x")
            Make_Label.config(bg = "hot pink")
            Spending_Money -= int(Entry[Day][Index][1])
        elif Entry[Day][Index][0] == "Gain":
            Make_Label = TK.Label(WI,text = "Money Gain: " + " " + str(Entry[Day][Index][1]))
            Make_Label.pack(fill = "x")
            Make_Label.config(bg = "cyan")
            Spending_Money += int(Entry[Day][Index][1])
        elif Entry[Day][Index][0] == "Exchange_Spend":
            Make_Label = TK.Label(WI,text = "Exchange Spent: " + " " + str(Entry[Day][Index][1]))
            Make_Label.pack(fill = "x")
            Make_Label.config(bg = "hot pink")
            Spending_Exchange -= int(Entry[Day][Index][1])
        elif Entry[Day][Index][0] == "Points_Spend":
            Make_Label = TK.Label(WI,text = "Points Spent: " + " " + str(Entry[Day][Index][1]))
            Make_Label.pack(fill = "x")
            Make_Label.config(bg = "hot pink")
            Spending_Points -= int(Entry[Day][Index][1])
        elif Entry[Day][Index][0] == "Points_Gain":
            Make_Label = TK.Label(WI,text = "Points Gain: " + " " + str(Entry[Day][Index][1]))
            Make_Label.pack(fill = "x")
            Make_Label.config(bg = "cyan")
            Spending_Points += int(Entry[Day][Index][1])
    
    Label_Money_Amount.config(text = str(Spending_Money))
    Label_Exchange_Amount.config(text = str(Spending_Exchange))
    Label_Points_Amount.config(text = str(Spending_Points))

# adding input for Entry List, Using Entry for loading and saving purpose 
def Change_Daily(Day,Mode,Amount):
    global Total_Money, Total_Exchange, Total_Points
    if Amount.isdigit():
        if Mode == "Spend":
            Entry[Day] += [["Spend", Amount]]
            Spending[Day] -= int(Amount)
            Total_Money -= int(Amount)
        elif Mode == "Gain":
            Entry[Day] += [["Gain", Amount]]
            Spending[Day] += int(Amount)
            Total_Money += int(Amount)
        elif Mode == "Exchange_Spend":
            Entry[Day] += [["Exchange_Spend", Amount]]
            Exchange_Spend[Day] += int(Amount)
            Total_Exchange -= int(Amount)
        elif Mode == "Points_Spend":
            Entry[Day] += [["Points_Spend", Amount]]
            Points_Spend[Day] += int(Amount)
            Total_Points -= int(Amount)
        elif Mode == "Points_Gain":
            Entry[Day] += [["Points_Gain", Amount]]
            Points_Spend[Day] += int(Amount)
            Total_Points += int(Amount)

        But_Day[Day].config(text = Spending[Day],bg = whatColor(Day))
        But_Total_Money.config(text = "Total")
    else:
        Warning("Did not input a number")
    
#Setting color for button
def whatColor(Day):
    if Goal_Money == 0 or Spending[Day] == 0:
        return("snow")
    Remain = np.sum(Spending)
    Check = Spending[Day] *-1
    Check /= Goal_Money
    if Check >= 0.75:
        Warning("Your spending is getting close to your goal")
        return("red2")
    elif Check >= 0.5:
        return("orange2")
    elif Check >= 0.25:
        return("gold")
    else:
        return("green1")
    
#Killing Window
def destory_window(x):
    if len(x.children) != 0:
        x.destroy()

if __name__=="__main__":
    main()