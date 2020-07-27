def TableF1(event):
    mainTable=Toplevel()
    mainTable.title('Справка')
    mainTable.resizable(0,0)
    Text=Label(mainTable,justify=LEFT,width=82,height=8,text='1) В первой строке таблицы должны находиться названия колонок (она не считывается в базу данных)\n2) Все параметры у животных должны быть указаны\n3) Нельзя вводить новые параметры или изменять последовательность имеющихся\n4) Все слова записываются с маленькой буквы\n5) После запятой ставится пробел\n6) Таблица должна быть в формате xslx (подходит любой excel не старше 2003 года)\n7) Лист с животными в книге, которую вы выбрали должен называться "Лист1"',bg='white')
    Text.pack()

    

def SelectTable(event): #Выбор интересующей таблицы для загрузки в БД
    global SelectFile
    global panelFrameData
    SelectFile.destroy()
    SelectFile=Button(panelFrameData, height=3,text='Выбрать файл', width=28, bg='#0A2E48',fg='white')
    SelectFile.bind("<Button-1>",SelectTable)
    SelectFile.place(x=2,y=36)
    
    op = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("xlsx files","*.xlsx"),("all files","*.*")))
    if op=='':
        return
    book = xlrd.open_workbook(op)
    sheet = book.sheet_by_name("Лист1")
    database=sqlite3.connect('my.sqlite')
    cursor = database.cursor()
    conn=sqlite3.connect('my.sqlite')
    m=conn.cursor()
    k='SELECT COUNT(1) FROM animals'
    m.execute(k)
    number=''
    for i in m:
        for j in range(0,len(i)):
            if i[j]!=',':
                number+=str(i[j])
            else:
                break
        break
    number=int(number)
    for r in range(1, sheet.nrows):
                    name = sheet.cell(r,0).value
                    size= int(sheet.cell(r,1).value)
                    weight= int(sheet.cell(r,2).value)
                    children= int(sheet.cell(r,3).value)
                    frequency= int(sheet.cell(r,4).value)
                    amount= int(sheet.cell(r,5).value)
                    single= sheet.cell(r,6).value
                    swim= sheet.cell(r,7).value
                    roar= sheet.cell(r,8).value
                    food= sheet.cell(r,9).value
                    hunter= sheet.cell(r,10).value
                    whenn= sheet.cell(r,11).value
                    wher= sheet.cell(r,12).value
                    num= number+1
                    query = "INSERT INTO animals (name, size, weight, children, frequency, amount, single, swim, roar, food, hunter, whenn, wher, num) VALUES ("+"'"+name+"'"+","+str(size)+","+str(weight)+","+str(children)+","+str(frequency)+","+str(amount)+","+"'"+single+"'"+","+"'"+swim+"'"+","+"'"+roar+"'"+","+"'"+food+"'"+","+"'"+hunter+"'"+","+"'"+whenn+"'"+","+"'"+wher+"'"+","+str(num)+")"
                    cursor.execute(query)
                    number+=1
    cursor.close()
    database.commit()
    database.close()
    m.close()
    conn.close()
    return


def AddData(event):  #Добавление таблицы
    global panelFrameData
    global SelectFile
    panel.destroy()
    panelFrameData= Frame(root, height = 100, width =210, bg = '#5daeae')
    panelFrameData.pack(side = 'left', fill = 'x')

    back=Button(panelFrameData, height=1,text='Назад', width=12, bg='#0A2E48',fg='white')
    back.bind("<Button-1>",start)
    back.place(x = 2, y = 2)

    SelectFile=Button(panelFrameData, height=3,text='Выбрать файл', width=28, bg='#0A2E48',fg='white')
    SelectFile.bind("<Button-1>",SelectTable)
    SelectFile.place(x=2,y=36)

    Help=Button(panelFrameData, height=1,text='Формат таблицы', width=14, bg='#0A2E48',fg='white')
    Help.bind("<Button-1>",TableF1)
    Help.place(x=100,y=2)


def ChangeRequest(tt): #Оставляет только и зону обитания из всех в вопросе для игры
    ppap=tt.split()
    f=''
    for i in range(len(ppap)):
        if ppap[i][-1]!=',':
            f+=ppap[i]+' '
        else:
            f+=ppap[i][:len(ppap[i])-1]
            break
    return f


def AppendQuests(amountofquests,a,b,c): #Функция составления вопросов в игре
    global question
    if len(question)<=amountofquests:
        question.append(str(a)+str(b)+str(c))
    else:
        question[amountofquests]=str(a)+str(b)+str(c)

    
def Changer(a): # Замена сокращений из БД на полные предложения
    if a=='м':
        a='Самцы'
    if a=='ж':
        a='Самки'
    if a=='вм':
        a='Самки и самцы'
    if a=='д':
        a='Только днем'
    if a=='н':
        a='Только ночью'
    if a=='в':
        a='Всегда'
    return a


def CapitalLetters(a,LenOfStr): # Расставление заглавных букв и переносов в строках с информвцией
        ttmp=0
        tk=a
        mas2=[]
        cn=0
        cn2=0
        for p in range(len(tk)):
            if tk[p]!=' ':
                cn+=1
            if p==len(tk)-1:
                mas2.append(cn)
                cn=0
            if tk[p]==' ':
                mas2.append(cn)
                cn=0

        aa=''
        aa+=tk[0].upper()

        for z in range(1,len(tk)):
            if tk[z]==' ' and tk[z+1:z+3]!='и ':
                aa+=tk[z]
                aa+=tk[z+1].upper()
            elif tk[z]==' ' and tk[z+1]=='и' and tk[z+2]==' ':
                aa+=tk[z:z+2]
            elif tk[z-1]!=' ':
                aa+=tk[z]
        tt=''
        g=0
        g2=0
        ff=0
        while g < len(aa):
            if g2+mas2[cn2]>LenOfStr:
                tt+='\n '
                g2=0
                ff+=1
            else:
                tt+=aa[g:g+mas2[cn2]+1]
                g+=mas2[cn2]+1
                g2+=mas2[cn2]+1
                cn2+=1
        return str(tt) , ff    


def hellp(event): #Спаравка
    main=Tk()
    main.title('Справка')
    main.geometry('250x95')
    main.resizable(0,0)
    hell = Label(main,text="Д - охотятся только днем\nН - охотятся только ночью\nВ - охотятся всегда\nМ - охотятся только самцы\nЖ - охотятся только самки\nВм - охотятся вместе",width=35, bg="white",font='arial 9')
    hell.place(x=0, y=0)
    isiton=1

    
def FullSizePic(event):
    main2=Toplevel()
    main2.title('Изображение')
    main2.resizable(0,0)
    global NameOfAnimal
    im = PIL.Image.open(NameOfAnimal)
    sizer=im.size
    a=sizer[0]/sizer[1]
    small=(750,int(750/a))
    imnew=im.resize(small)
    photo = PIL.ImageTk.PhotoImage(imnew)
    Picture2=Label(main2, image=photo)
    Picture2.image=photo
    Picture2.pack()



def printer(event): #Функция вывода информации о животном
    a=0
    global mass
    global panelFrame2
    global MassOfBeginings
    panelFrame2.destroy()
    panelFrame2 = Frame(root, height = 560, width = 252, bg = 'white')
    panelFrame2.pack(side = 'right', fill = 'x')
    tmp=event.widget.curselection()
    MassOfPrints=[]
    TinyMass=[''," см"," кг"," шт"," раз в год"," шт"]    
    if (tmp!=()):
        op=tmp[0]
        arr=[]
        
        txt=''
        for i in range(13):
            if i!=10 and i!=11:
                arr.append(mass[op][i])
            if i==10 or i==11:
                arr.append(Changer(mass[op][i]))

            if type(mass[op][i]) is str:
                er=CapitalLetters(arr[i],30)
                txt+= MassOfBeginings[i]+er[0]
            else:
                txt+= MassOfBeginings[i]+str(arr[i])+TinyMass[i]
            txt+='\n'*2
        listbox =Label(panelFrame2, text=txt,justify=LEFT,anchor=N, height=37,width=36, bg="white")
        listbox.pack()
        a=445
        try:
            
            im = PIL.Image.open(mass[op][0]+".jpg")
            sizer=im.size
            z=sizer[0]/sizer[1]
            if z>1:
                size=(int(100*z),100)
            else:
                size=(int(100*z),100)
            imnew=im.resize(size)
            photo = PIL.ImageTk.PhotoImage(imnew)
            Picture=Button(panelFrame2, image=photo)
            Picture.image=photo
            Picture.place(x=10,y=a)
            global NameOfAnimal
            NameOfAnimal=mass[op][0]+".jpg"
            Picture.bind("<Button-1>",FullSizePic)
        except FileNotFoundError:
            return
            
def go1(event): #Функция полученя информации из окошек в поисковике и вывода списка животных

    global MassOfEntryes
    global panelFrame1
    global panelFrame2
    global panelFrame3
    
    global mass
    global mylist
    global scrollbar
    global fll
    global MassOfArguments
    MassOfArguments=[]
    
    chk=0
    for i in range(18):
        MassOfEntryes[i]['bg']='white'
        MassOfArguments.append('')
        MassOfArguments[i]=MassOfEntryes[i].get()
        if i>=1 and i<=10:
            if i%2!=0:
                if MassOfArguments[i]=='':
                    MassOfArguments[i]='0'
            else:
                if MassOfArguments[i]=='':
                    MassOfArguments[i]='10000'
            if MassOfArguments[i].isdigit()==0:
                chk=1
                MassOfEntryes[i]["bg"]="red"
        else:
            MassOfArguments[i]=MassOfArguments[i].lower()
            if MassOfArguments[i].isalpha()==0 and MassOfArguments[i]!="":
                chk=1
                MassOfEntryes[i]["bg"]="red"
    
    if chk==0:
        if fll!=0:
            mylist.destroy()
            scrollbar.destroy()
        qq=0       
        conn = sqlite3.connect('my.sqlite')
        n = conn.cursor()
        MassOfPartsOfRequest=["SELECT * FROM animals where name like '%","%' and size between "," and "," and weight between "," and "," and children between "," and "," and frequency between "," and "," and amount between "," and "," and single like '%","%' and swim like '%","%' and roar like '%","%' and food like '%","%' and hunter like '","' and whenn like '%","%' and wher like '%","%'"]
        s=''
        for i in range(len(MassOfArguments)):
            if i==15:
                if MassOfArguments[i]=='м' or MassOfArguments[i]=='ж':
                    s+=MassOfPartsOfRequest[i]+MassOfArguments[i]
                else:
                    s+=MassOfPartsOfRequest[i]+"%"+MassOfArguments[i]+"%"
            else:
                s+=MassOfPartsOfRequest[i]+MassOfArguments[i]
        s+=MassOfPartsOfRequest[len(MassOfPartsOfRequest)-1]
        p=270
        q=40
        n.execute(s)
        scrollbar = Scrollbar(panelFrame3)
        scrollbar.pack( side = RIGHT, fill = Y )
        mylist = Listbox(panelFrame3, yscrollcommand = scrollbar.set,height=29,width=25, selectmode="SINGLE")
        mylist.pack( side = LEFT)
        cnt=0
        for j in n:
            mylist.insert(END, j[0][0].upper()+j[0][1:])
            mass.append(0)
            mass[cnt]=j
            cnt+=1
        scrollbar.config( command = mylist.yview)
        mylist.bind("<<ListboxSelect>>", printer)
        p=270
        q=40
        fll=1
        n.close()
        conn.close()


def searcher(event): #Функция отрисовки окошек для поисковика
    global panel
    global fll
    global panelFrame1
    global panelFrame2
    global panelFrame3
    global mass

    panel.destroy()
    
    mass=[]
    qq=0
    fll=0

    panelFrame1 = Frame(root, height = 560, width = 460, bg = '#5daeae')
    panelFrame1.pack(side = 'left', fill = 'x')

    panelFrame2 = Frame(root, height = 560, width = 252, bg = 'white')
    panelFrame2.pack(side = 'right', fill = 'x')

    panelFrame3 = Frame(root, height = 100, width = 170, bg = '#5daeae')
    panelFrame3.place(x=280,y=80)

    back=Button(panelFrame1, height=1,text='Назад', width=14, bg='#0A2E48',fg='white')
    back.bind("<Button-1>",start)
    back.place(x = 8, y = 5)
    global MassOfLabels
    global MassOfEntryes
    MassOfLabels=[]
    MassOfEntryes=[]
    MassOfVariables=[]
    MassOfSentences=['Название','Размер (см)','Вес (кг)','Особей в \n потомстве (шт)','Частота рождения \n потомсва (в год)','Число особей в \n семье (шт)','Охотятся одни \n (Да/Нет)','Плавают \n (Да/Нет)','Рычат \n (Да/Нет)','Кого едят \n (во мн.ч)','Кто охотится \n (М/Ж/Вм)','Когда охотится \n (Д/Н/В)','Где живут']
    a=37
    for i in range(13):
        MassOfLabels.append('')
        MassOfLabels[i]=Label(panelFrame1,text=MassOfSentences[i],width=14,height=2)
        MassOfLabels[i].place(x = 10, y = a)
        a+=40
    a=39
    MassOfEntryes.append('')
    MassOfVariables.append('')
    MassOfEntryes[0] = Entry(panelFrame1, textvariable = MassOfVariables[0], width=40,bd=8, bg="white")
    MassOfEntryes[0].place(x = 116, y = 39)
    a+=40
    for i in range(1,18):
        flag=0
        MassOfEntryes.append('')
        if i<=10:
            x=IntVar()
            x=''
            MassOfVariables.append(x)
        if i>10:
            x=StringVar()
            MassOfVariables.append(x)
            
        MassOfEntryes[i]=Entry(panelFrame1,textvariable=MassOfVariables[i],width=10,bd=8,bg="white")
        if type(MassOfVariables[i]) is str and i%2==0:
            MassOfEntryes[i].place(x = 194, y = a)
            flag=1
        else:
            MassOfEntryes[i].place(x = 116, y = a)
        if flag==1 or i>10:
            a+=40

    butsearch = Button(panelFrame1, text="Поиск", width = 10, height=1, bg="#0A2E48",fg="white", activebackground="#0A2E48")
    butsearch.bind("<Button-1>",go1)

    root.bind("<Return>",go1)
    butsearch.place(x = 377, y = 41)

    f1 = Button(panelFrame1, text="?", width = 10, height=2, bg="#0A2E48",fg="white", activebackground="#0A2E48")
    f1.bind("<Button-1>",hellp)
    f1.place(x = 198, y = 515)


def guesed(): #Функция, которая пишет что животное в игре отгадано
    global nameinthegame
    global panelFrameGame
    global panelofrightanimal
    global question
    question=[]
    panelFrameGame.destroy()
    panelofrightanimal=Frame(root, height =300, width =450, bg = 'white')
    panelofrightanimal.pack(side = 'left', fill = 'x')

    rightnameofaimal=Label(panelofrightanimal, height=3,text=nameinthegame[0][0].upper()+nameinthegame[0][1:], width=57, bg='#5daeae',fg='black',bd=4)
    rightnameofaimal.place(x = 20, y = 180)

    global requestforgame
    global use
    global amountofquests
    global lenofappend
    lenofappend=[]
    amountofquests=0
    use=[]
    requestforgame="SELECT * FROM animals where name like '%%'"

    playagain=Button(panelofrightanimal, height=3,text='Еще раз', width=57, bg='lightgrey',fg='black')
    playagain.bind("<Button-1>",gme)
    playagain.place(x = 20, y = 240)

    try:
        im = PIL.Image.open(nameinthegame[0]+'.jpg')
        sizer=im.size
        a=sizer[0]/sizer[1]
        small=(int(160*a),160)
        imnew=im.resize(small)
        photo = PIL.ImageTk.PhotoImage(imnew)
        Picture2=Label(panelofrightanimal, image=photo)
        Picture2.image=photo
        Picture2.place(x = int((450-160*a)/2), y = 10)
    except FileNotFoundError:
        return

    
def reseter(event): #Функция перезапуска игры
    global requestforgame # Это всё должны быть параметры функции
    global use
    global cheker
    global lenofappend
    global amountofquests
    global question
    question=[]
    amountofquests=0
    lenofappend=[]
    requestforgame="SELECT * FROM animals where name like '%%'"
    use=[]
    cheker=1
    gme(1)

    
def prewquest(event): #Функция, чтобы вернуть к предыдущему вопросу
    global use
    global lenofappend
    global requestforgame
    global cheker
    global amountofquests
    global bac
    global chack
    chack=1
    if amountofquests>0:
        bac=1
        amountofquests-=1
        use=use[0:len(use)-2]
        requestforgame=requestforgame[0:len(requestforgame)-lenofappend[amountofquests]]
        cheker=1
        amountofquests=0
        gme(1)


def yes(event): #Вспомогательная функция к def answer
    answer(0)


def no(event): # Тоже самое
    answer(1)


def answer(event): #Функция, которая обрабатывает ответ из игры
    global mid
    global randnum
    global requestforgame
    global flaggame
    global massofpatterns
    global use
    global lenofappend
    global amountofquests
    global chack
    chack=0
    amountofquests+=1
    tinymass=['',' not']
    if event==0:
        if randnum<=4:
            x=" and "+massofpatterns[randnum+1]+" between "+str(mid+1)+" and '1000'"
            requestforgame+=x
            if len(lenofappend)<amountofquests:
                lenofappend.append(len(x))
            else:
                lenofappend[amountofquests-1]=len(x)

    else:
        if randnum<=4:
            x=" and "+massofpatterns[randnum+1]+" between 0 and "+str(mid)
            requestforgame+=x
            if len(lenofappend)<amountofquests:
                lenofappend.append(len(x))
            else:
                lenofappend[amountofquests-1]=len(x)
    if randnum>=5:
        conn = sqlite3.connect('my.sqlite') #подключаемся к базе
        n = conn.cursor()
        n.execute(requestforgame)
        if randnum>=5 and randnum<=6:
            for i in n:
                x=" and "+massofpatterns[randnum+2]+tinymass[event]+" like '%да%'"
                requestforgame+=x
                if len(lenofappend)<amountofquests:
                    lenofappend.append(len(x))
                else:
                    lenofappend[amountofquests-1]=len(x)
                break
        if randnum>6:
            for i in n:
                x=" and "+massofpatterns[randnum+2]+tinymass[event]+" like '%"+i[randnum+2]+"%'"
                if randnum==7 or randnum==10:
                    f=ChangeRequest(i[randnum+2])
                    x=" and "+massofpatterns[randnum+2]+tinymass[event]+" like '%"+f+"%'"
                requestforgame+=x
                if len(lenofappend)<amountofquests:
                    lenofappend.append(len(x))
                else:
                    lenofappend[amountofquests-1]=len(x)
                break
    flaggame=1
    conn = sqlite3.connect('my.sqlite') #подключаемся к базе
    n = conn.cursor()
    n.execute(requestforgame)
    global nameinthegame
    global panelFrameGame
    cheese=0
    for i in n:
        cheese+=1
        nameinthegame=i
    if cheese==1:
        guesed()
    if cheese==0:

        global panelofmistake

        panelFrameGame.destroy()
        panelofmistake=Frame(root, height =300, width =450, bg = 'white')
        panelofmistake.pack(side = 'left', fill = 'x')

        rightnameofaimal=Label(panelofmistake, height=3,text='Такое животное я не знаю', width=57, bg='#5daeae',fg='black',bd=4)
        rightnameofaimal.place(x = 20, y = 50)

        playagain=Button(panelofmistake, height=3,text='Еще раз', width=57, bg='lightgrey',fg='black')
        playagain.bind("<Button-1>",gme)
        playagain.place(x = 20, y = 110)

        amountofquests=0
        requestforgame="SELECT * FROM animals where name like '%%'"
        use=[]
    if cheese>1:
        gme(1)
        
def gme(event): #Основная функция игры
    global requestforgame
    global massofpatterns
    global flaggame
    global use
    global mid
    global randnum
    global cheker
    global lenofappend
    global question
    global amountofquests
    global bac
    global panelofmistake
    global lastrandnum
    global chack
    if 'panelofmistake' in globals():
        panelofmistake.destroy()

    if 'panelofrightanimal' in globals():
        panelofrightanimal.destroy()
    
    panel.destroy()
    test.destroy()
    global panelFrameGame
    if flaggame==1 or cheker==1:
        panelFrameGame.destroy()
        flaggame=0
        cheker=0
    panelFrameGame = Frame(root, height =300, width =450, bg = '#5daeae')
    panelFrameGame.pack(side = 'left', fill = 'x')

    toMenu=Button(panelFrameGame, height=1,text='Назад', width=10, bg='#0A2E48',fg='white')
    toMenu.bind("<Button-1>",start)
    toMenu.place(x = 2, y = 2)
    dd=0
    massofquest=['больше ','весит больше ','приносит больше ','приносит потомство чаще ','имеет более ','умеет плавать ?','рычит ?','Питается ли ваше животное этим : ','охотится ','охотится ','Живет ли ваше животное на этой территорие : ']
    massofquest2=[' см в длину',' кг',' особей в потомстве',' раз в год',' особей в семье']

    if len(use)>10:
        use=[]

    while dd!=1:
        firsttime=1
        if chack==0:
            lastrandnum=randnum
            randnum=random.randint(0,10)
        else:
            randnum=lastrandnum
        if not randnum in use:
            dd=1
            use.append(randnum)
            if randnum<=4:
                conn = sqlite3.connect('my.sqlite')
                n = conn.cursor()
                n.execute(requestforgame)
                counter=0
                mid=0
                for i in n:
                    counter+=1
                    mid+=int(i[randnum+1])
                mid=mid//counter
                d=str(mid)+massofquest2[randnum]+' ?'
                AppendQuests(amountofquests,'Ваше животное ',massofquest[randnum],d)
            if randnum==5 or randnum==6:
                AppendQuests(amountofquests,'Ваше животное ',massofquest[randnum],'')
            if randnum>=7:
                conn = sqlite3.connect('my.sqlite')
                n = conn.cursor()
                n.execute(requestforgame)
                for i in n:
                    ttmp=0
                    tk=str(i[randnum+2])
                    if randnum==10:
                        tk='\n '+tk
                        tt=CapitalLetters(tk,45)
                        f=ChangeRequest(tt[0])
                        AppendQuests(amountofquests,massofquest[randnum],f,' ?')
                        break
                    if randnum==7:
                        tk='\n '+tk
                        tt=CapitalLetters(tk,45)
                        f=ChangeRequest(tt[0])
                        AppendQuests(amountofquests,massofquest[randnum],f,' ?')
                        break
                    else:
                        m='У загаданного вами вида охотятся только '
                        p='У загаданного вами вида охотятся '
                        n=' ?'
                        l='Ваше животное охотится только '
                        k='Ваше животное охотится '
                        tt=Changer(tk)
                        tt=tt.lower()
                        if tk=='м' or tk=='ж':
                            AppendQuests(amountofquests,m,tt,n)
                            break
                        if tk=='вм':
                            AppendQuests(amountofquests,p,tt,n)
                            break
                        if tk=='д' or tk=='н':
                            AppendQuests(amountofquests,l,tt,n)
                            break
                        if tk=='в':
                            AppendQuests(amountofquests,k,tt,n)
                            break
                            
                        tt=CapitalLetters(tk,40)
                        if len(question)<=amountofquests:
                            question.append('Ваше животное '+massofquest[randnum]+tt[0]+n)
                        else:
                            question[amountofquests]='Ваше животное '+massofquest[randnum]+tt[0]+n
                        break

    bac=0
    questionlbl=Label(panelFrameGame, height=3,text=question[amountofquests], width=57, bg='white',fg='black',bd=4)
    questionlbl.place(x = 20, y = 40)

    yesButton=Button(panelFrameGame, height=6,text='Да', width=26, bg='#ebe7dd',fg='black')
    yesButton.bind("<Button-1>",yes)
    yesButton.place(x = 20, y = 105)

    noButton=Button(panelFrameGame, height=6,text='Нет', width=26, bg='#ebe7dd',fg='black')
    noButton.bind("<Button-1>",no)
    noButton.place(x = 236, y = 105)

    reset=Button(panelFrameGame, height=3,text='Заново', width=26, bg='lightgrey',fg='black')
    reset.bind("<Button-1>",reseter)
    reset.place(x = 20, y = 230)

    prev=Button(panelFrameGame, height=3,text='Предыдущий вопрос', width=26, bg='lightgrey',fg='black')
    prev.bind("<Button-1>",prewquest)
    prev.place(x = 236, y = 230)



def chec(event): #Функция проверки теста
    flag=1
    global animal
    global numofrightanswer
    global l
    global MassOfRbuttons
    global AmountOfAskedQuests
    global AmountOfAnsweredRight
    l=whichischosen.get()
    if l!=0:
        if l==numofrightanswer+1:
            MassOfRbuttons[l-1]["bg"]="green"
            AmountOfAnsweredRight+=1
        else:
            MassOfRbuttons[l-1]["bg"]="red"
            MassOfRbuttons[numofrightanswer]["bg"]="green"

        nextquestion=Button(panelFrame, height=5,text='Следующий\nвопрос', width=10, bg='lightgrey',fg='black')
        nextquestion.bind("<Button-1>",tst)
        nextquestion.place(x = 415, y = 220)

        
def tst(event): #Основная функция для теста
    global animal
    global panelFrame
    global flag
    global l
    global numofrightanswer
    global whichischosen
    global usedname
    global AmountOfAnsweredRight
    global AmountOfAskedQuests
    AmountOfAskedQuests+=1
    panel.destroy()
    test.destroy()
    if flag==1:
        panelFrame.destroy()
        flag=0

    animal=[]
    k=0
    chek=0
    usednow=[]
    
    conn = sqlite3.connect('my.sqlite') #подключаемся к базе
    n = conn.cursor()
    a="SELECT * FROM animals where name like '%%'"
    n.execute(a)
    counter=0
    for i in n:
        counter+=1

    if len(usedname)>10:
        usedname=[]
    while k!=4:
        m=random.randint(1,counter)
        if m not in usedname and m not in usednow:
            s='SELECT * FROM animals where num='+str(m)
            if chek==0:
                usedname.append(m)
            chek=1
            n.execute(s) # диапазон строк
            k+=1
            for j in n:
                animal.append(j)
            usednow.append(m)
        
    panelFrame = Frame(root, height =320, width =505, bg = '#5daeae')
    panelFrame.pack(side = 'left', fill = 'x')

    back=Button(panelFrame, height=1,text='Назад', width=10, bg='#0A2E48',fg='white')
    back.bind("<Button-1>",start)
    back.place(x = 2, y = 2)

    answer=Button(panelFrame, height=5,text='Проверить', width=10, bg='lightgrey',fg='black')
    answer.bind("<Button-1>",chec)
    answer.place(x = 415, y = 220)
    
    mass2=[]
    used2=[]
    n=0
    while n!=4:
        s=random.randint(0,3)
        if s not in used2:
            if s==0:
                numofrightanswer=len(mass2)
            mass2.append(s)
            used2.append(s)
            n+=1
    a=220
    whichischosen=IntVar()
    global MassOfRbuttons
    MassOfRbuttons=[]
    for i in range(4):
        MassOfRbuttons.append('')
        MassOfRbuttons[i]=Radiobutton(panelFrame,text=animal[mass2[i]][0][0].upper()+animal[mass2[i]][0][1:len(animal[mass2[i]][0])],height=2,width=24,variable=whichischosen,value=i+1,bg='#ebe7dd')
        if i%2==0:
            MassOfRbuttons[i].place(x=7,y=a)
        else:
            MassOfRbuttons[i].place(x=210,y=a)
            a+=45
    i=0
    quest=[]
    used=[12,9]
    massofnames=[]
    SmalMass=[''," см"," кг"," шт"," раз в год"," шт",'','','','','','','']
    Ends=[]
    global MassOfBeginings
    LokalMassOfBeginings=MassOfBeginings
    LokalMassOfBeginings[1]='Средний размер взрослой особи: '
    LokalMassOfBeginings[2]='Средний вес взрослой особи: '

    massofnames.append(LokalMassOfBeginings[12])
    Ends.append(SmalMass[12])
    x=Changer(animal[0][12])
    y=CapitalLetters(x,28)
    quest.append(y[0])

    massofnames.append(LokalMassOfBeginings[9])
    Ends.append(SmalMass[9])
    x=Changer(animal[0][9])
    y=CapitalLetters(x,28)
    quest.append(y[0])    
    while i!=4:
        a=random.randint(1,12)
        fla=0
        if not a in used:
            i+=1
            massofnames.append(LokalMassOfBeginings[a])
            Ends.append(SmalMass[a])
            if a<9:
                quest.append(animal[0][a])
            else:
                x=Changer(animal[0][a])
                y=CapitalLetters(x,28)
                quest.append(y[0])
            used.append(a)

    MassOfParametres=[]
    a=44
    for i in range(6):
        MassOfParametres.append('')
        MassOfParametres[i]=Label(panelFrame, height=3,text=massofnames[i]+str(quest[i])+Ends[i], width=34, bg='white',fg='black')
        if i%2==0:
            MassOfParametres[i].place(x = 5, y = a)
        else:
            MassOfParametres[i].place(x = 255, y = a)
            a+=58
    flag=1

    TotalNumberOfQuests=Label(panelFrame, height=2,text='Всего отвечено: '+str(AmountOfAskedQuests)+' вопросов', width=22, bg='#ebe7dd',fg='black')
    TotalNumberOfQuests.place(x=89,y=4)

    AnsweredRight=Label(panelFrame, height=2,text='Отвечено правильно: '+str(AmountOfAnsweredRight)+' вопросов', width=34, bg='#ebe7dd',fg='black')
    AnsweredRight.place(x=255,y=4)
    

def start(event): #Создает начальное окно
    global panel
    global test
    global use
    global requestforgame
    global usedname
    global lenofappend
    global amountofquests
    global question
    global isiton
    global chack
    global AmountOfAnsweredRight
    global AmountOfAskedQuests
    AmountOfAskedQuests=-1
    AmountOfAnsweredRight=0
    root.unbind("<Return>")
    chack=0
    isiton=0
    question=[]
    amountofquests=0
    lenofappend=[]
    usedname=[]
    requestforgame="SELECT * FROM animals where name like '%%'"
    use=[]
    if 'panelFrameData' in globals():
        panelFrameData.destroy()
    if 'panelFrame1' in globals():
        panelFrame1.destroy()
    if 'panelFrame2' in globals():
        panelFrame2.destroy()
    if 'panelFrame3' in globals():
        panelFrame3.destroy()
    if 'panelFrame' in globals():
        panelFrame.destroy()
    if 'panelFrameGame' in globals():
        panelFrameGame.destroy()

    
    panel = Frame(root, height =235, width =200, bg = '#5daeae')
    panel.pack(side = 'left', fill = 'x')
    
    test = Button(panel, text="Тест", width = 20, height=2, bg="#0A2748",fg="white")
    test.bind("<Button-1>",tst)
    test.place(x = 25, y = 75)

    game = Button(panel, text="Игра", width = 20, height=2, bg="#0A2748",fg="white")
    game.bind("<Button-1>",gme)
    game.place(x = 25, y = 120)

    finder = Button(panel, text="Поисковик", width = 20, height=2, bg="#0A2748",fg="white")
    finder.bind("<Button-1>",searcher)
    finder.place(x = 25, y = 30)

    correct = Button(panel, text="Добавить таблицу", width = 20, height=2, bg="#0A2748",fg="white")
    correct.bind("<Button-1>",AddData)
    correct.place(x = 25, y = 165)
    


# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import filedialog
import fileinput
from PIL import ImageTk, Image
import PIL.Image
import PIL.ImageTk
import os
import random 
import sqlite3
import xlrd

root = Tk()
root.title('БД')
#root.size = 900, 500
root.resizable(0,0)
##root.place()
requestforgame="SELECT * FROM animals where name like '%%'"
massofpatterns=['name','size','weight','children','frequency','amount','single','swim','roar','food','hunter','whenn','wher']
MassOfBeginings=["Название: ","Размер: ","Вес: ","Особей в потомстве: ","Частота рождение потомства: ","Число особей в семье: ","Охотятся в одиночку: ","Умеют плавать: ","Рычат: ","Еда: ","Кто охотится: ","Когда охотятся: ","Где живут: "]
MassOfEndings=[''," см"," кг",'',''," раз в год"]
flag=0
l=0
flaggame=0
usedname=[]
question=[]
cheker=0
lenofappend=0
bac=0
randnum=0
x = (root.winfo_screenwidth() - root.winfo_reqwidth())/2 -200
y = (root.winfo_screenheight() - root.winfo_reqheight())/2 - 100
root.geometry("+%d+%d" % (x, y))
root.deiconify()
start(1)
root.mainloop()
