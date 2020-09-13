#!/bin/python3
import tkinter, random, time

stlpce=30
riadky=20
scorebar=1
bunka=35
body=0

width = stlpce*bunka
height = riadky*bunka
scorebar_haight = scorebar*bunka
root=tkinter.Tk()
root.title("Snake")
canvas = tkinter.Canvas(width=width-2, height=height+scorebar_haight, background='green')
canvas.pack()
canvas.create_rectangle(0,height,width,width+scorebar_haight, fill='white', width=0)

level=0
colors=['purple', 'orange', 'red']
bonus_length=1

def nacitaj_mapu(map_number):
    global had, pohybX, pohybY, mapa, mapGoal, colors, bonus_length
    canvas.delete('obejkty_mapy', 'had')
    mapa=[]
    jeden_stlpec=[]
    for y in range(riadky):
        jeden_stlpec.append('0')
    for x in range(stlpce):
        mapa.append(list(jeden_stlpec))

    subor = open('maps/map'+str(map_number)+'.txt', 'r')
    retazec=subor.read().replace('\r','').replace('\n', '').split('#')
    subor.close
    znak=0
    for y in range(riadky):
        for x in range(stlpce):
            mapa[x][y]=retazec[0][znak]
            znak+=1
            if mapa[x][y]=='1':
                canvas.create_rectangle(x*bunka, y*bunka, (x+1)*bunka, (y+1)*bunka, fill='orange', width=0, tags='obejkty_mapy')

    pohybX=int(retazec[3])
    pohybY=int(retazec[4])
    mapGoal=int(retazec[5])
    had=[[int(retazec[1]),int(retazec[2]),bonus_length,len(colors)-1]] #[StartX, StartY, Length, color_code]

def update_text():
    global mapGoal
    canvas.delete('texty')
    canvas.create_text(width//8,height+scorebar_haight//2,text='Length: '+str(len(had)), font='Arial 16 bold',tags='texty', fill='purple')
    canvas.create_text(width//8*7,height+scorebar_haight//2,text='Next level: '+str(mapGoal), font='Arial 16 bold',tags='texty', fill='purple')
    canvas.create_text(width//2,height+scorebar_haight//2,text='Level: '+str(level), font='Arial 16 bold',tags='texty', fill='purple')
    
def pohyb_hada():
    global had,pohybX,pohybY, stlpce, riadky, color_value, colors, level, bonus_length
    x=(had[-1][0]+pohybX)%stlpce
    y=(had[-1][1]+pohybY)%riadky
    
    if mapa[x][y]=='9':
        level+=1
        if level==6:
            canvas.update()
            time.sleep(2)
            root.destroy()
        bonus_length=len(had)
        nacitaj_mapu(level)
        novy_bod()
        return
    
    if mapa[x][y]=='1':
        bonus_length=1
        level=0
        nacitaj_mapu(level)
        novy_bod()
        return
    
    nasiel=0
    if mapa[x][y]=='7':
        mapa[x][y]='0'
        nasiel=1
        novy_bod()

    if len(had)==1:
        color_value=0
    else:
        color_value=(color_value+1)%len(colors)
        
    nova_cast=[x, y, nasiel, color_value]

    delete=False
    for i in range(len(had)-1,-1,-1):
        if had[i][0]==x and had[i][1]==y:
            delete=True
        if delete:
            del had[i]
    
    had.append(nova_cast)
    if had[0][2]==0:
        del had[0]
    else:
        had[0][2]-=1

    canvas.delete('had')
    for cast in had:
        canvas.create_rectangle(cast[0]*bunka,cast[1]*bunka,cast[0]*bunka+bunka,cast[1]*bunka+bunka, fill=colors[cast[3]], tags='had', width=1)

def novy_bod():
    global stlpce, riadky, had
    canvas.delete('bod')
    hladaj=True
    while hladaj:
        x=random.randrange(stlpce)
        y=random.randrange(riadky)
        if mapa[x][y]=='0':
            if len(had)<mapGoal:
                mapa[x][y]='7'
                canvas.create_rectangle(x*bunka,y*bunka,x*bunka+bunka,y*bunka+bunka, fill='white', tags='bod', width=0)
            else:
                mapa[x][y]='9'
                canvas.create_rectangle(x*bunka,y*bunka,x*bunka+bunka,y*bunka+bunka, fill='black', tags='bod', width=0)
                
            hladaj=False

def tuk(event):
    global pohybX, pohybY
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    direction = ['Left', 'Right', 'Up', 'Down']
    for i in range(4):
        if event.keysym == direction[i]:
            pohybX=dx[i]
            pohybY=dy[i]

def casovac():
    pohyb_hada()
    update_text()
    canvas.after(150,casovac)

canvas.bind_all('<Key>', tuk)
nacitaj_mapu(level)
novy_bod()
casovac()
tkinter.mainloop()
