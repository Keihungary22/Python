from tkinter import*
import sqlite3 #to use sqlite
import tkinter.ttk as ttk #tkinter is for GUI
import tkinter.messagebox as tkMessageBox

#簡単に言えば、ウィジェットは実際のユーザーインターフェースの部品であり、
#パレットはそれらの部品を取り扱うためのデザインツールやツールキット内のセクションを指します。

root = Tk() #instance of tkinter
root.title("Contact List")
width = 700
height = 400
screen_width = root.winfo_screenwidth() #to get the center of the screen
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2) # to get the center of the screen
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y)) #set the position of the screen
root.resizable(0, 0) #user can not resize the window
root.config(bg="silver") #background, color code

FIRSTNAME = StringVar() #variable class in tkinter to keep string  
LASTNAME = StringVar()
GENDER = StringVar()
AGE = StringVar()
ADDRESS = StringVar()
CONTACT = StringVar()


def Database():
    conn = sqlite3.connect("pythontut.db")
    cursor = conn.cursor() #make cursor to control conn
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT, gender TEXT, age TEXT, address TEXT, contact TEXT)")
    #if there is no table 'member' in the database create with assigned data(variable name, variable type) 
    cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
    #get all data from 'member' and sort by lastname ascendant order
    fetch = cursor.fetchall() #fetch means that you get data from the database
    for data in fetch:
        tree.insert('', 'end', values=(data)) #insert the info to tree
    cursor.close() #cursor close
    conn.close() #connection close

def SubmitData():
    if FIRSTNAME.get() == "" or LASTNAME.get() == "" or GENDER.get() == "" or AGE.get() == "" or ADDRESS.get() == "" or CONTACT.get() == "":
        result = tkMessageBox.showwarning('', 'Please Complete the form.', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("pythontut.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO `member` (firstname, lastname, gender, age, address, contact) VALUES(?, ?, ?, ?, ?, ?)", (str(FIRSTNAME.get()), str(LASTNAME.get()), str(GENDER.get()), int(AGE.get()), str(ADDRESS.get()), str(CONTACT.get())))
        conn.commit() #before commit, the edition isn't done on database, it's just on transaction. To reflect on the database, commit is needed.
        cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        AGE.set("")
        ADDRESS.set("")
        CONTACT.set("")

def UpdateData():
    if GENDER.get() == "":
        result = tkMessageBox.showwarning('', 'Please complete filling', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("pythontut.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE `member` SET `firstname` = ?, `lastname` = ?, `gender` = ?, `age` = ?, `address` = ?, `contact` = ? WHERE `mem_id` = ?", (str(FIRSTNAME.get()), str(LASTNAME.get()), str(GENDER.get()), str(AGE.get()), str(ADDRESS.get()), str(CONTACT.get()), int(mem_id)))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        AGE.set("")
        ADDRESS.set("")
        CONTACT.set("")


def OnSelected(event):
    global mem_id, UpdateWindow
    curItem = tree.focus()
    #tree.focus() は、ユーザーがクリックして選択したアイテムを返します。
    #このメソッドは、選択がない場合には ''（空文字列）を返します。
    #一方で、アイテムが選択されている場合は、そのアイテムのIDを返します。
    contents = (tree.item(curItem))
    selecteditem = contents['values']
    mem_id = selecteditem[0]
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    AGE.set("")
    ADDRESS.set("")
    CONTACT.set("")
    FIRSTNAME.set(selecteditem[1])
    LASTNAME.set(selecteditem[2])
    AGE.set(selecteditem[4])
    ADDRESS.set(selecteditem[5])
    CONTACT.set(selecteditem[6])
    UpdateWindow = Toplevel()
    #to make Toplevel window, it's separeted to mainwindow
    UpdateWindow.title("Contact List")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) + 450) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    UpdateWindow.resizable(0, 0)
    UpdateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'NewWindow' in globals():
        NewWindow.destroy()

    #form
    FormTitle = Frame(UpdateWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(UpdateWindow)
    ContactForm.pack(side=TOP, pady=10)
    RadioGroup = Frame(ContactForm)
    Male = Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male", font=('arial', 14)).pack(side=LEFT)
    Female = Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female", font=('arial', 14)).pack(side=LEFT)

    #labels
    lbl_title = Label(FormTitle, text="Updating Contracts", font=('arial', 16), bg="orange", width=300)
    lbl_title.pack(fill=X)
    lbl_firstname = Label(ContactForm, text="Firstname", font=('arial', 14), bd=5)
    lbl_firstname.grid(row=0, sticky=W) 
    #sticky オプションは、ウィジェットがセル内のどの方向に対して配置されるかを指定します。
    # W は "west"（西）の略で、セルの左側に配置されることを示します。この場合、lbl_firstname はセルの左端に配置されます。
    #sticky オプションは次のような値を取ります：
    #N（北）: 上
    #S（南）: 下
    #E（東）: 右
    #W（西）: 左
    #NE（北東）: 右上
    #NW（北西）: 左上
    #SE（南東）: 右下
    #SW（南西）: 左下
    lbl_lastname = Label(ContactForm, text="Lastname", font=('arial', 14), bd=5)
    lbl_lastname.grid(row=1, sticky=W)
    lbl_gender = Label(ContactForm, text="Gender", font=('arial', 14), bd=5)
    lbl_gender.grid(row=2, sticky=W)
    lbl_age = Label(ContactForm, text="Age", font=('arial', 14), bd=5)
    lbl_age.grid(row=3, sticky=W)
    lbl_address = Label(ContactForm, text="Address", font=('arial', 14), bd=5)
    lbl_address.grid(row=4, sticky=W)
    lbl_contact = Label(ContactForm, text="Contact", font=('arial', 14), bd=5)
    lbl_contact.grid(row=5, sticky=W)

    #entry
    firstname = Entry(ContactForm, textvariable=FIRSTNAME, font=('arial', 14))
    firstname.grid(row=0, column=1)
    lastname = Entry(ContactForm, textvariable=LASTNAME, font=('arial', 14))
    lastname.grid(row=1, column=1)
    RadioGroup.grid(row=2, column=1)
    age = Entry(ContactForm, textvariable=AGE,  font=('arial', 14))
    age.grid(row=3, column=1)
    address = Entry(ContactForm, textvariable=ADDRESS,  font=('arial', 14))
    address.grid(row=4, column=1)
    contact = Entry(ContactForm, textvariable=CONTACT,  font=('arial', 14))
    contact.grid(row=5, column=1)

    #button
    btn_updatecon = Button(ContactForm, text="Update", width=50, command=UpdateData)
    btn_updatecon.grid(row=6, columnspan=2, pady=10)

def DeleteData():
    if not tree.selection():
        result = tkMessageBox.showwarning('', 'Please select one of them.', icon="warning")
    else:
        result = tkMessageBox.askquestion('', 'Are you sure to delete this contact?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            conn = sqlite3.connect("pythontut.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM `member` WHERE `mem_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()


def AddNewWindow():
    global NewWindow
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    AGE.set("")
    ADDRESS.set("")
    CONTACT.set("")
    NewWindow = Toplevel()
    NewWindow.title("Contact List")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) - 455) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    NewWindow.resizable(0, 0)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()

    #Form
    FormTitle = Frame(NewWindow)
    FormTitle.pack(side = TOP)
    ContactForm = Frame(NewWindow)
    ContactForm.pack(side=TOP, pady = 10)
    RadioGroup = Frame(ContactForm)
    Male = Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male", font=('arial', 14)).pack(side=LEFT)
    Female = Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female", font=('arial', 14)).pack(side=LEFT)

    #Label
    lbl_title = Label(FormTitle, text = "Adding New Contact", font=('arial', 16), bg="#66ff66", width = 300)
    lbl_title.pack(fill=X)
    #垂直方向や両方向に対しても同様の伸縮が可能です。
    #たとえば、fill=Y は垂直方向に伸縮し、fill=BOTH は両方向に伸縮します。
    #簡潔に言えば、fill=X は水平方向に広がるようにウィジェットを配置するオプションです。
    lbl_firstname = Label(ContactForm, text = "Firstname", font = ('arial', 14), bd = 5)
    lbl_firstname.grid(row = 0, sticky = W)
    lbl_lastname = Label(ContactForm, text = "Lastname", font = ('arial', 14), bd = 5)
    lbl_lastname.grid(row = 1, sticky = W)
    lbl_gender = Label(ContactForm, text = "Gender", font = ('arial', 14), bd = 5)
    lbl_gender.grid(row = 2, sticky = W)
    lbl_age = Label(ContactForm, text = "Age", font = ('arial', 14), bd = 5)
    lbl_age.grid(row = 3, sticky = W)
    lbl_address = Label(ContactForm, text = "Address", font = ('arial', 14), bd = 5)
    lbl_address.grid(row = 4, sticky = W)
    lbl_contact = Label(ContactForm, text = "Contact", font = ('arial', 14), bd = 5)
    lbl_contact.grid(row = 5, sticky = W)
    
    firstname = Entry(ContactForm, textvariable = FIRSTNAME, font = ('arial', 14))
    firstname.grid(row = 0, column = 1)
    lastname = Entry(ContactForm, textvariable = LASTNAME, font = ('arial', 14))
    lastname.grid(row = 1, column = 1)
    RadioGroup.grid(row = 2, column = 1)
    age = Entry(ContactForm, textvariable = AGE, font = ('arial', 14))
    age.grid(row = 3, column = 1)
    address = Entry(ContactForm, textvariable = ADDRESS, font = ('arial', 14))
    address.grid(row = 4, column = 1)
    contact = Entry(ContactForm, textvariable = CONTACT, font = ('arial', 14))
    contact.grid(row = 5, column = 1)

    #button
    btn_addcon = Button(ContactForm, text = "Save", width = 50, command = SubmitData)
    btn_addcon.grid(row = 6, columnspan = 2, pady = 10)


#Frame
Top = Frame(root, width = 500, bd = 1, relief = SOLID)
#bd = the width of the border
#ウィジェットの境界の描画スタイルを指定するオプションです。
#このオプションを使用すると、ウィジェットの外観を異なるスタイルで表示できます。
#relief オプションにはいくつかの値があります。主な値は以下の通りです：
#FLAT: ボーダーや影がないフラットな外観。
#SUNKEN: ウィジェットが沈んでいるような立体感を持たせる。
#RAISED: ウィジェットが浮き上がっているような立体感を持たせる。
#GROOVE: ウィジェットを囲む溝のような外観。
#RIDGE: ウィジェットを囲む隆起のような外観

Top.pack(side = TOP)
Mid = Frame(root, width = 500, bg = "silver")
Mid.pack(side = TOP)
MidLeft = Frame(Mid, width = 100)
MidLeft.pack(side = LEFT, pady = 10)
MidLeftPadding = Frame(Mid, width = 370, bg = "silver")
MidLeftPadding.pack(side = LEFT)
MidRight = Frame(Mid, width = 100)
MidRight.pack(side = RIGHT, pady = 10)
TableMargin = Frame(root, width = 500)
TableMargin.pack(side = TOP)

#lable
lbl_title = Label(Top, text = "Contact Management System", font = ('arial', 16), width = 500)
lbl_title.pack(fill = X)

#button
btn_add = Button(MidLeft, text = "+ ADD NEW", bg = "#66ff66", command = AddNewWindow)
btn_add.pack()
btn_delete = Button(MidRight, text = "DELETE", bg = "red", command = DeleteData)
btn_delete.pack(side = RIGHT)

#table
scrollbarx = Scrollbar(TableMargin, orient = HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient = VERTICAL)
tree = ttk.Treeview(TableMargin, columns = ("MemberID", "Firstname", "Lastname", "Gender", "Age", "Address", "Contact"), height = 400, selectmode = "extended", yscrollcommand = scrollbary.set, xscrollcommand = scrollbary.set)
#Tkinterの拡張ウィジェットであり、ツリー形式のデータを表示するために使用されます。
#主にデータの階層的な表示や選択、展開などの機能を提供します。
#TableMargin フレーム内にツリービューを作成し、7つのカラム
#（"MemberID", "Firstname", "Lastname", "Gender", "Age", "Address", "Contact"）を持っています。
scrollbary.config(command = tree.yview)
#config は "configuration" の略で、設定や構成を変更するためのメソッドや機能を指します。
#PythonのtkinterなどのGUIライブラリや、他の多くのプログラムで使われます。
#configメソッドを使用することで、ウィジェットのプロパティや挙動を変更することができます。
#tree.yview メソッドが呼び出され、tree ウィジェットの垂直方向の表示がスクロールバーに同期して変更されるようになります。
scrollbary.pack(side = RIGHT, fill = Y)
scrollbarx.config(command = tree.xview)
scrollbarx.pack(side = BOTTOM, fill = X)
tree.heading('MemberID', text = "MemberID", anchor = W)
#heading メソッドは、ttk.Treeview ウィジェットのカラムのヘッダーを設定します。
#このメソッドは、特定のカラムに対してヘッダーのテキストやアンカー（配置）などを指定するのに使います
#anchor パラメータは、ヘッダーのテキストの配置を指定します。W は "west" を表し、左寄せを意味します。
tree.heading('Firstname', text = "Firstname", anchor = W)
tree.heading('Lastname', text = "Lastname", anchor = W)
tree.heading('Gender', text = "Gender", anchor = W)
tree.heading('Age', text = "Age", anchor = W)
tree.heading('Address', text = "Address", anchor = W)
tree.heading('Contact', text = "Contact", anchor = W)
tree.column('#0', stretch = NO, minwidth = 0, width = 0)
tree.column('#1', stretch = NO, minwidth = 0, width = 0)
tree.column('#2', stretch = NO, minwidth = 0, width = 80)
tree.column('#3', stretch = NO, minwidth = 0, width = 120)
tree.column('#4', stretch = NO, minwidth = 0, width = 90)
tree.column('#5', stretch = NO, minwidth = 0, width = 80)
tree.column('#6', stretch = NO, minwidth = 0, width = 120)
tree.column('#7', stretch = NO, minwidth = 0, width = 120)
tree.pack()
tree.bind('<Double-Button-1>', OnSelected)
#この行は、ttk.Treeview ウィジェットに対してダブルクリックのイベント
#（'<Double-Button-1>'）が発生したときに、OnSelected という関数を呼び出すようにバインドしています。
# ダブルクリックされたときに特定のアクションを実行するためのものです。

#bind メソッドは、イベントとそれに対するハンドラ（処理を行う関数やコード）を関連付けるために使用されます。
#具体的には、特定のウィジェットやウィンドウで発生するイベントに対して、指定されたハンドラを呼び出すように設定します。

#initialization
if __name__ == '__main__':
    Database()
    root.mainloop()