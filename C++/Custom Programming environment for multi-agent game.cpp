#include <iostream>
#include <cstdlib>
#include <vector>
#include <cmath>
#include <algorithm>

#include "teenyat.h"
#include "tigr.h"

using namespace std;


const tny_uword Test_Func =     0x9000;
const tny_uword Bot_Health =    0x9001;    // Read/Write
const tny_uword Bot_Mode =      0x9002;    // Read/Write
const tny_uword Bot_Team =      0x9003;    // Read/Write
const tny_uword Bot_Pos_X =     0x9004;    // Read/Write
const tny_uword Bot_Pos_Y =     0x9005;    // Read/Write
const tny_uword Bot_Letter =    0x9006;    // Read/Write
const tny_uword Bot_Damage =    0x9007;    // Read/Write
const tny_uword Bot_Hurt =      0x9008;    // Read/Write
const tny_uword Team_Cnt =      0x9009;    // Read
const tny_uword Enemy_Cnt =     0x9010;    // Read
const tny_uword Movement =      0x9011;    // write
const tny_uword Death =         0x9012;    // Read
const tny_uword Stuck =         0x9013;    // Read

// Custom variables for tracking each bots
class Bots {
    public:
        teenyat* ID;
        int Health;
        int Mode;
        int Letter;
        int Team;
        int Pos_X;
        int Pos_Y;
        int Damage;
        int  Hurt;
        int Death;
        int Stuck;

    Bots(teenyat *t, int HP, int M, int L, int T, int X, int Y, int Dmg, int H, int D, int St)
    {
        ID = t;
        Health = HP;
        Mode = M;
        Letter = L;
        Team = T;
        Pos_X = X;
        Pos_Y = Y;
        Damage = Dmg;
        Hurt = H;
        Death = D;
        Stuck = St;
    }
};

vector<Bots> Bot_List;

//Window size for graphic setting
int Window_Max_X = 1000;
int Window_Max_Y = 1000;

void bus_write(teenyat *t, tny_uword addr, tny_word data, uint16_t *delay);
void bus_read(teenyat *t, tny_uword addr, tny_word *data, uint16_t *delay);
int Team_Count(int Caller);
int Enemy_Count(int Caller);
void Bot_Movement(int Caller);
float Calc_Distance(int x1, int x2, int y1, int y2);
void Bot_Moving(int Caller, int Target);
void Draw(Tigr *Screen);
void Test_Damage();
void Hit_Detected(int First, int Second);
void Check_Death();
void Check_Stuck(int Caller);

int main(int argc, char *argv[]) {

    // Tigr set up
    Tigr *Screen;

    Screen = tigrWindow(Window_Max_X,Window_Max_Y,"Process",0);
    tigrClear(Screen, tigrRGB(0,0,0));
    tigrUpdate(Screen);

    //ASM load and bot setup
    FILE *bin_file = fopen(argv[1], "rb");
    FILE *bin_file_1 = fopen(argv[1], "rb");
    FILE *bin_file_2 = fopen(argv[2], "rb");
    FILE *bin_file_3 = fopen(argv[2], "rb");
    FILE *bin_file_4 = fopen(argv[3], "rb");
    FILE *bin_file_5 = fopen(argv[3], "rb");
    teenyat t;
    teenyat t1;
    teenyat t2;
    teenyat t3;
    teenyat t4;
    teenyat t5;
    tny_init_from_file(&t, bin_file, bus_read, bus_write);
    tny_init_from_file(&t1, bin_file_1, bus_read, bus_write);
    tny_init_from_file(&t2, bin_file_2, bus_read, bus_write);
    tny_init_from_file(&t3, bin_file_3, bus_read, bus_write);
    tny_init_from_file(&t4, bin_file_4, bus_read, bus_write);
    tny_init_from_file(&t5, bin_file_5, bus_read, bus_write);
    Bots B1(&t,0,0,0,0,0,0,0,0,0,0);
    Bots B2(&t1,0,0,0,0,0,0,0,0,0,0);
    Bots B3(&t2,0,0,0,0,0,0,0,0,0,0);
    Bots B4(&t3,0,0,0,0,0,0,0,0,0,0);
    Bots B5(&t4,0,0,0,0,0,0,0,0,0,0);
    Bots B6(&t5,0,0,0,0,0,0,0,0,0,0);
    Bot_List.insert(Bot_List.end(),{B1,B2,B3,B4,B5,B6});

    // Running the main program, ctrl c to stop or close the window
    while(!tigrClosed(Screen))
    {
        tny_clock(&t);
        tny_clock(&t1);
        tny_clock(&t2);
        tny_clock(&t3);
        tny_clock(&t4);
        tny_clock(&t5);
        Draw(Screen);
        Test_Damage();
        Check_Death();
    }

    tigrFree(Screen);

    return 0;
}

void bus_write(teenyat *t, tny_uword addr, tny_word data, uint16_t *delay) 
{
    // Checking who is calling write
    int Bot = 0;
    for(int i = 0; i < Bot_List.size(); i++)
    {
        if (t == Bot_List[i].ID)
        {
            Bot = i;
            break;
        }
    }
    switch (addr)
    {
    case Bot_Health:
        Bot_List[Bot].Health = data.u;
        break;
    case Bot_Mode:
        Bot_List[Bot].Mode = data.u;
        break;
    case Bot_Team:
        Bot_List[Bot].Team = data.u;
        break;
    case Bot_Pos_X:
        Bot_List[Bot].Pos_X = data.u;
        break;
    case Bot_Pos_Y:
        Bot_List[Bot].Pos_Y = data.u;
        break;
    case Bot_Letter:
        Bot_List[Bot].Letter = data.u;
        break;
    case Bot_Damage:
        Bot_List[Bot].Damage = data.u;
        break;
    /*
    case Test_Func:
        cout << Bot_List[Bot].Health << endl;
        break;
    */ 
    case Movement:
        Bot_Movement(Bot);
        break;
    default:
        break;
    }
}

void bus_read(teenyat *t, tny_uword addr, tny_word *data, uint16_t *delay)
{
    // Answer variable used to return to agents
    int Bot = 0;
    int Answer = 0;
    for(int i = 0; i < Bot_List.size(); i++)
    {
        if (t == Bot_List[i].ID)
        {
            Bot = i;
            break;
        }
    }
    switch (addr)
    {
        case Bot_Health:
            data->s = Bot_List[Bot].Health;
            break;
        case Bot_Mode:
            data->s = Bot_List[Bot].Mode;
            break;
        case Bot_Team:
            data->s = Bot_List[Bot].Team;
            break;
        case Bot_Pos_X:
            data->s = Bot_List[Bot].Pos_X;
            break;
        case Bot_Pos_Y:
            data->s = Bot_List[Bot].Pos_Y;
            break;
        case Bot_Letter:
            data->s = Bot_List[Bot].Letter;
            break;
        case Bot_Damage:
            data->s = Bot_List[Bot].Damage;
            break;
        case Team_Cnt:
            Answer = Team_Count(Bot);
            data->s = Answer;
            break;
        case Enemy_Cnt:
            Answer = Team_Count(Bot);
            data->s = Answer;
            break;
        case Death:
            data->s = Bot_List[Bot].Death;
            break;
        case Stuck:
            Check_Stuck(Bot);
            data->s = Bot_List[Bot].Stuck;
        default:
            break;
    }
}

// Used to check how many teammates alive on map
int Team_Count(int Caller)
{
    int Answer = 0;
    for(int i = 0; i < Bot_List.size(); i++)
    {
        if (Bot_List[i].Team == Bot_List[Caller].Team && i != Caller)
        {
            Answer++;
        }
    }
    return Answer;
}

// Used to check how many enemy alive on map
int Enemy_Count(int Caller)
{
     int Answer = 0;
    for(int i = 0; i < Bot_List.size(); i++)
    {
        if (Bot_List[i].Team != Bot_List[Caller].Team && i != Caller)
        {
            Answer++;
        }
    }
    return Answer;
}

//Use to determent how the bot is moving, who is its target
void Bot_Movement(int Caller)
{
    float Target_Distance = 0;
    int Target = 0;
    if (Bot_List[Caller].Mode == 0 || Bot_List[Caller].Mode == 1)
    {
        for(int i = 0; i < Bot_List.size(); i++)
        {
            if (Bot_List[i].Team != Bot_List[Caller].Team && i != Caller)
            {
                float Calc = Calc_Distance(Bot_List[Caller].Pos_X, Bot_List[i].Pos_X,Bot_List[Caller].Pos_Y, Bot_List[i].Pos_Y);
                if (Target_Distance == 0 || Calc < Target_Distance)
                {
                    Target_Distance = Calc;
                    Target = i;
                }
            }
        }
    }
    else
    {
        for(int i = 0; i < Bot_List.size(); i++)
        {
            if (Bot_List[i].Team == Bot_List[Caller].Team && i != Caller)
            {
                float Calc = Calc_Distance(Bot_List[Caller].Pos_X, Bot_List[i].Pos_X,Bot_List[Caller].Pos_Y, Bot_List[i].Pos_Y);
                if (Target_Distance == 0 || Calc < Target_Distance)
                {
                    Target_Distance == Calc;
                    Target = i;
                }
            }
        }
    }
    Bot_Moving(Caller, Target);
}

//Used to calcuate the distance between two agents
float Calc_Distance(int x1, int x2, int y1, int y2)
{
    float Result = pow((x2 - x1),2);
    Result = Result + pow((y2 - y1),2);
    Result = sqrt(Result);
    return Result;
}

//Actual Moving code for bots
void Bot_Moving(int Caller, int Target)
{
    if (Bot_List[Caller].Mode == 0 || Bot_List[Caller].Mode == 2)
    {
        if (Bot_List[Caller].Pos_X < Bot_List[Target].Pos_X)
        {
            if(Bot_List[Caller].Pos_X < Window_Max_X - 3)
            {
                Bot_List[Caller].Pos_X++;
            }
        }
        else if (Bot_List[Caller].Pos_X > Bot_List[Target].Pos_X)
        {
            if(Bot_List[Caller].Pos_X > 0)
            {
                Bot_List[Caller].Pos_X--;
            }
        }
        if (Bot_List[Caller].Pos_Y < Bot_List[Target].Pos_Y)
        {
            if(Bot_List[Caller].Pos_Y < Window_Max_Y - 3)
            {
                Bot_List[Caller].Pos_Y++;
            }
        }
        else if (Bot_List[Caller].Pos_Y > Bot_List[Target].Pos_Y)
        {
            if(Bot_List[Caller].Pos_Y > 3)
            {
                Bot_List[Caller].Pos_Y--;
            }
        }
    }

    if (Bot_List[Caller].Mode == 1 || Bot_List[Caller].Mode == 3)
    {
        if (Bot_List[Caller].Pos_X <= Bot_List[Target].Pos_X)
        {
            if(Bot_List[Caller].Pos_X > 0)
            {
                Bot_List[Caller].Pos_X--;
            }
        }
        else if (Bot_List[Caller].Pos_X >= Bot_List[Target].Pos_X)
        {
            if(Bot_List[Caller].Pos_X < Window_Max_X - 3)
            {
                Bot_List[Caller].Pos_X++;
        
            }
        }
        if (Bot_List[Caller].Pos_Y <= Bot_List[Target].Pos_Y)
        {
            if(Bot_List[Caller].Pos_Y > 3)
            {
                Bot_List[Caller].Pos_Y--;
            }
        }
        else if (Bot_List[Caller].Pos_Y >= Bot_List[Target].Pos_Y)
        {
            if(Bot_List[Caller].Pos_Y < Window_Max_Y - 3)
            {
               Bot_List[Caller].Pos_Y++;
            }
        }
    }
    return;
}

// Drawing code for screen
void Draw(Tigr *Screen)
{
    tigrClear(Screen, tigrRGB(0,0,0));
    for(int i = 0; i < Bot_List.size(); i++)
    {
        if(Bot_List[i].Team == 0)
        {
            tigrFill(Screen, Bot_List[i].Pos_X, Bot_List[i].Pos_Y, 3 , 3 , tigrRGB(255,0,0));
        }
        else if(Bot_List[i].Team == 1)
        {
            tigrFill(Screen, Bot_List[i].Pos_X, Bot_List[i].Pos_Y, 3 , 3 , tigrRGB(0,255,0));
        }
        else
        {
            tigrFill(Screen, Bot_List[i].Pos_X, Bot_List[i].Pos_Y, 3 , 3 , tigrRGB(0,0,255));
        }
    }
    tigrUpdate(Screen);
    return;
}

//Test if two agents are close enough to count as hitting each other, igrone teammates
void Test_Damage()
{
    for(int i = 0; i < Bot_List.size(); i++)
    {
        Bot_List[i].Hurt = 0;
    }
    for(int i = 0; i < Bot_List.size(); i++)
    {
        for(int a = 0; a < Bot_List.size(); a++)
        {
            if (i == a || Bot_List[a].Team == Bot_List[i].Team)
            {
                continue;
            }
            float Calc = Calc_Distance(Bot_List[i].Pos_X, Bot_List[a].Pos_X,Bot_List[i].Pos_Y, Bot_List[a].Pos_Y);
            if (Calc < 3)
            {
                Hit_Detected(i,a);
            }
        }
    }
}

// Code to determine what happen after hit detected, and turn on hurt flag
void Hit_Detected(int First, int Second)
{
    if (Bot_List[First].Letter == 0)
    {
        if(Bot_List[Second].Letter == 1)
        {
            Bot_List[Second].Health -= Bot_List[First].Damage;
            Bot_List[Second].Hurt = 1;
        }
        else if(Bot_List[Second].Letter == 2)
        {
            Bot_List[First].Health -= Bot_List[Second].Damage;
            Bot_List[First].Hurt = 1;
        }
        else
        {
            Bot_List[First].Health -= Bot_List[Second].Damage;
            Bot_List[Second].Health -= Bot_List[First].Damage;
            Bot_List[First].Hurt = 1;
            Bot_List[Second].Hurt = 1;
        }
    }
    if (Bot_List[First].Letter == 1)
    {
        if(Bot_List[Second].Letter == 2)
        {
            Bot_List[Second].Health -= Bot_List[First].Damage;
            Bot_List[Second].Hurt = 1;
        }
        else if(Bot_List[Second].Letter == 0)
        {
            Bot_List[First].Health -= Bot_List[Second].Damage;
            Bot_List[First].Hurt = 1;
        }
        else
        {
            Bot_List[First].Health -= Bot_List[Second].Damage;
            Bot_List[Second].Health -= Bot_List[First].Damage;
            Bot_List[First].Hurt = 1;
            Bot_List[Second].Hurt = 1;
        }

    }
    if (Bot_List[First].Letter == 2)
    {
        if(Bot_List[Second].Letter == 0)
        {
            Bot_List[Second].Health -= Bot_List[First].Damage;
            Bot_List[Second].Hurt = 1;
        }
        else if(Bot_List[Second].Letter == 1)
        {
            Bot_List[First].Health -= Bot_List[Second].Damage;
            Bot_List[First].Hurt = 1;
        }
        else
        {
            Bot_List[First].Health -= Bot_List[Second].Damage;
            Bot_List[Second].Health -= Bot_List[First].Damage;
            Bot_List[First].Hurt = 1;
            Bot_List[Second].Hurt = 1;
        }

    }
}

//Detect if any agents health have drop below 0
void Check_Death()
{
    for(int i = 0; i < Bot_List.size(); i++)
    {
        if(Bot_List[i].Health <= 0)
        {
            Bot_List[i].Death = 1;
        }
        else
        {
            Bot_List[i].Death = 0;
        }
    }
}

// Check if the agent is stuck on one of the corner of the screen
void Check_Stuck(int Caller)
{
    if ((Bot_List[Caller].Pos_X == 0 && Bot_List[Caller].Pos_Y <= 4) || 
        (Bot_List[Caller].Pos_X >= Window_Max_X - 3 && Bot_List[Caller].Pos_Y >= Window_Max_Y - 4) ||
        (Bot_List[Caller].Pos_X == 0 && Bot_List[Caller].Pos_Y >= Window_Max_Y - 4) ||
        (Bot_List[Caller].Pos_X >= Window_Max_X - 3&& Bot_List[Caller].Pos_Y <= 4))
    {
        Bot_List[Caller].Stuck = 1;
    }
    else
    {
        Bot_List[Caller].Stuck = 0;
    }
    return;
}