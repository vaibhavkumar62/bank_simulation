from tkinter import Tk,Label,Frame,Button,Entry,messagebox,simpledialog,filedialog
import time
import Generator
import sqlite3
from datetime import datetime
import TableCreator
import Emailhandler
TableCreator.create()
import re
from PIL import Image,ImageTk
import os           #for update image


def update_time():
    curdate=time.strftime("%d-%b-%Y ⏱️%r")
    date.configure(text=curdate)
    date.after(1000,update_time)

def forgot_screen():
    def back():
        frm.destroy()
        existuser_screen()

    def reset_click():
        e_acn.delete(0,"end")
        e_adhar.delete(0,"end")
        e_acn.focus()

    def send_otp():
        gen_otp=Generator.generate_otp()
        acn=e_acn.get()
        adhar=e_adhar.get()

        conobj=sqlite3.connect(database="mybank.sqlite")
        curobj=conobj.cursor()
        query='''select name,email,pass from accounts where acn=? and adhar=?'''
        curobj.execute(query,(acn,adhar))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
            messagebox.showerror('Forgot Password','Record Not Found')
        else:
            Emailhandler.send_otp(tup[1],tup[0],gen_otp)
            user_otp=simpledialog.askinteger("Password Recovery","Enter OTP")
            if gen_otp==user_otp:
                messagebox.showinfo("Password Recovery",f"Your Password = {tup[2]}")
            else:
                messagebox.showerror("Password recovery","Invalid otp")

    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='purple')
    frm.place(relx=0,rely=.17,relwidth=1,relheight=.73)

    back_btn=Button(frm,text='Back',bg='red',font=('arial',20,'bold'),bd=5,command=back)
    back_btn.place(relx=0,rely=0)

    lbl_acn=Label(frm,text='🧑‍💼Acn',width=7,font=('arial',20,'bold'),bg='black',fg='white')
    lbl_acn.place(relx=.3,rely=.2)

    e_acn=Entry(frm,font=('arial',18,'bold'),bd=5)
    e_acn.place(relx=.41,rely=.2)
    e_acn.focus()      #for cursor blink on first column

    lbl_adhar=Label(frm,text='Adhar',width=7,font=('arial',20,'bold'),bg='black',fg='white')
    lbl_adhar.place(relx=.3,rely=.3)

    e_adhar=Entry(frm,font=('arial',18,'bold'),bd=5)
    e_adhar.place(relx=.41,rely=.3)

    otp_btn=Button(frm,text='Send Otp',width=8,bg='red',font=('arial',20,'bold'),bd=5,command=send_otp)
    otp_btn.place(relx=.35,rely=.55)

    reset_btn=Button(frm,text='Reset',width=8,bg='red',font=('arial',20,'bold'),bd=5,command=reset_click)
    reset_btn.place(relx=.48,rely=.55)

def welcome_screen(acn=None):
    def logout():
        frm.destroy()
        main_screen()

    def check_screen():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='pink')
        ifrm.place(relx=.21,rely=.15,relwidth=.66,relheight=.72)

        title_lbl=Label(ifrm,text="This is Check Details Screen",
                        font=('arial',20,'bold'),bg='white',fg='purple')
        title_lbl.pack()

        conobj=sqlite3.connect(database="mybank.sqlite")
        curobj=conobj.cursor()
        query='''select acn,bal,adhar,email,opendate from accounts where acn=?'''
        curobj.execute(query,(acn,))
        tup=curobj.fetchone()
        conobj.close()

        details=f'''
Account No = {tup[0]}\n
Account Bal = {tup[1]}\n
Account Adhar = {tup[2]}\n
Account Email = {tup[3]}\n
Account Opendate = {tup[4]}\n
'''
        lbl_details=Label(ifrm,text=details,bg='white',fg='purple',font=('arial',15,))
        lbl_details.place(relx=.2,rely=.2)


    def update_screen():
        def update_db():
            name=e_name.get()
            email=e_email.get()
            mob=e_mob.get()
            pwd=e_pass.get()

            conobj=sqlite3.connect(database='mybank.sqlite')
            curobj=conobj.cursor()
            query='''update accounts set name=?,email=?,mob=?,pass=? where acn=?'''
            curobj.execute(query,(name,email,mob,pwd,acn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update screen","Details updated successfully")
            welcome_screen(acn)

        conobj=sqlite3.connect(database="mybank.sqlite")
        curobj=conobj.cursor()
        query='''select name,email,mob,pass from accounts where acn=?'''
        curobj.execute(query,(acn,))
        tup=curobj.fetchone()
        conobj.close()

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='pink')
        ifrm.place(relx=.21,rely=.15,relwidth=.66,relheight=.72)

        title_lbl=Label(ifrm,text="This is Update Details Screen",
                        font=('arial',20,'bold'),bg='white',fg='purple')
        title_lbl.pack()

        lbl_name=Label(ifrm,text='🧑‍💼Name',width=7,font=('arial',20,'bold'),bg='black',fg='white')
        lbl_name.place(relx=.05,rely=.2)

        e_name=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_name.place(relx=.21,rely=.2)
        e_name.focus()      #for cursor blink on first column

        lbl_pass=Label(ifrm,text='Pass',width=7,font=('arial',20,'bold'),bg='black',fg='white')
        lbl_pass.place(relx=.05,rely=.35)

        e_pass=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_pass.place(relx=.21,rely=.35)

        lbl_mob=Label(ifrm,text='📲Mob',width=7,font=('arial',20,'bold'),bg='black',fg='white')
        lbl_mob.place(relx=.51,rely=.2)

        e_mob=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_mob.place(relx=.67,rely=.2)

        lbl_email=Label(ifrm,text='Email',width=7,font=('arial',20,'bold'),bg='black',fg='white')
        lbl_email.place(relx=.51,rely=.35)

        e_email=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_email.place(relx=.67,rely=.35)

        e_name.insert(0,tup[0])
        e_email.insert(0,tup[1])
        e_mob.insert(0,tup[2])
        e_pass.insert(0,tup[3])

        submit_btn=Button(ifrm,text='Submit',width=7,bg='red',font=('arial',20,'bold'),bd=5,command=update_db)
        submit_btn.place(relx=.40,rely=.6)


    def deposit_screen():
        def deposit_db():
            amt=float(e_amt.get())
            conobj=sqlite3.connect(database="mybank.sqlite")
            curobj=conobj.cursor()
            query='''update accounts set bal=bal+? where acn=?'''
            curobj.execute(query,(amt,acn))
            tup=curobj.fetchone()
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Deposit Screen",f'{amt} deposited successfully')
            e_amt.delete(0,"end")
            e_amt.focus()

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='pink')
        ifrm.place(relx=.21,rely=.15,relwidth=.66,relheight=.72)

        title_lbl=Label(ifrm,text="This is Deposit Details Screen",
                        font=('arial',20,'bold'),bg='white',fg='purple')
        title_lbl.pack()

        lbl_amt=Label(ifrm,text='Amount',width=7,font=('arial',20,'bold'),bg='black',fg='white')
        lbl_amt.place(relx=.05,rely=.2)

        e_amt=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_amt.place(relx=.21,rely=.2)
        e_amt.focus()

        submit_btn=Button(ifrm,text='Submit',width=7,bg='red',font=('arial',20,'bold'),bd=5,command=deposit_db)
        submit_btn.place(relx=.40,rely=.6)

    def withdraw_screen():
        def withdraw_db():
            amt=float(e_amt.get())
            conobj=sqlite3.connect(database="mybank.sqlite")
            curobj=conobj.cursor()
            query='''select bal,email,name from accounts where acn=?'''
            curobj.execute(query,(acn,))
            tup=curobj.fetchone()
            conobj.close()

            if tup[0]>=amt:
                gen_otp=Generator.generate_otp()
                Emailhandler.send_otp_withdraw(tup[1],tup[2],gen_otp,amt)
                user_otp=simpledialog.askinteger("Withdraw OTP","OTP")
                if gen_otp==user_otp:
                    conobj=sqlite3.connect(database="mybank.sqlite")
                    curobj=conobj.cursor()
                    query='''update accounts set bal=bal-? where acn=?'''
                    curobj.execute(query,(amt,acn))
                    tup=curobj.fetchone()
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo("Withdraw  Screen",f'{amt} withdrawn successfully')
                    e_amt.delete(0,"end")
                    e_amt.focus()
                else:
                    messagebox.showerror("Withdraw Screen","Invalid Otp")
                    submit_btn.configure(text="Resend Otp")
            else:
                messagebox.showwarning("Withdraw  Screen",f"Insufficient Bal: {tup[0]}")
            
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='pink')
        ifrm.place(relx=.21,rely=.15,relwidth=.66,relheight=.72)

        title_lbl=Label(ifrm,text="This is Withdraw Details Screen",
                        font=('arial',20,'bold'),bg='white',fg='purple')
        title_lbl.pack()

        lbl_amt=Label(ifrm,text='Amount',width=7,font=('arial',20,'bold'),bg='black',fg='white')
        lbl_amt.place(relx=.05,rely=.2)

        e_amt=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_amt.place(relx=.21,rely=.2)
        e_amt.focus()

        submit_btn=Button(ifrm,text='Send Otp',width=9,bg='red',font=('arial',20,'bold'),bd=5,command=withdraw_db)
        submit_btn.place(relx=.40,rely=.6)

    def transfer_screen():
        def transfer_db():
            to_acn=int(e_to.get())
            amt=float(e_amt.get())

            conobj=sqlite3.connect(database="mybank.sqlite")
            curobj=conobj.cursor()
            query='''select * from accounts where acn=?'''
            curobj.execute(query,(to_acn,))
            tup=curobj.fetchone()
            conobj.close()

            if tup==None:
                messagebox.showerror("Transfer Screen","Invalid To ACN")
                return

            conobj=sqlite3.connect(database="mybank.sqlite")
            curobj=conobj.cursor()
            query='''select bal,email,name from accounts where acn=?'''
            curobj.execute(query,(acn,))
            tup=curobj.fetchone()
            conobj.close()

            if tup[0]>=amt:
                gen_otp=Generator.generate_otp()
                Emailhandler.send_otp_transfer(tup[1],tup[2],gen_otp,amt,to_acn)
                user_otp=simpledialog.askinteger("Transfer OTP","OTP")
                if gen_otp==user_otp:
                    conobj=sqlite3.connect(database="mybank.sqlite")
                    curobj=conobj.cursor()
                    query1='''update accounts set bal=bal-? where acn=?'''
                    query2='''update accounts set bal=bal+? where acn=?'''

                    curobj.execute(query1,(amt,acn))
                    curobj.execute(query2,(amt,to_acn))

                    tup=curobj.fetchone()
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo("Transfer Screen",f'{amt} transfered successfully')
                    e_amt.delete(0,"end")
                    e_amt.focus()
                else:
                    messagebox.showerror("Transfer Screen","Invalid Otp")
                    transfer_btn.configure(text="Resend Otp")
            else:
                messagebox.showwarning("Transfer Screen",f"Insufficient Bal: {tup[0]}")
            

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='pink')
        ifrm.place(relx=.21,rely=.15,relwidth=.66,relheight=.72)

        title_lbl=Label(ifrm,text="This is Transfer Details Screen",
                        font=('arial',20,'bold'),bg='white',fg='purple')
        title_lbl.pack()

        lbl_to=Label(ifrm,text='To ACN',width=7,font=('arial',20,'bold'),bg='black',fg='white')
        lbl_to.place(relx=.05,rely=.2)

        e_to=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_to.place(relx=.21,rely=.2)
        e_to.focus()

        lbl_amt=Label(ifrm,text='Amount',width=7,font=('arial',20,'bold'),bg='black',fg='white')
        lbl_amt.place(relx=.05,rely=.35)

        e_amt=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_amt.place(relx=.21,rely=.35)
       
        transfer_btn=Button(ifrm,text='Transfer',width=9,bg='red',font=('arial',20,'bold'),bd=5,command=transfer_db)
        transfer_btn.place(relx=.40,rely=.7)

    conobj=sqlite3.connect(database="mybank.sqlite")
    curobj=conobj.cursor()
    query='''select name from accounts where acn=?'''
    curobj.execute(query,(acn,))
    tup=curobj.fetchone()
    conobj.close()

    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='purple')
    frm.place(relx=0,rely=.17,relwidth=1,relheight=.73)

    logout_btn=Button(frm,text='LogOut',bg='red',font=('arial',20,'bold'),bd=5,command=logout)
    logout_btn.place(relx=0.88,rely=0)

    lbl_wel=Label(frm,text=f'Welcome,{tup[0]}',font=('arial',20,'bold'),bg='black',fg='white')
    lbl_wel.place(relx=.001,rely=0)

    def update_pic():
        name=filedialog.askopenfilename()
        os.rename(name,f"{acn}.jpg")
        img_profile=Image.open(f'{acn}.jpg').resize((170,90))
        imgtk_profile=ImageTk.PhotoImage(img_profile,master=root)
        lbl_img_profile=Label(frm,image=imgtk_profile)
        lbl_img_profile.place(relx=0.005,rely=0.09)
        lbl_img_profile.image=imgtk_profile

    if os.path.exists(f'{acn}.jpg'):                #for update image
        img_profile=Image.open(f'{acn}.jpg').resize((170,90))
    else:
        img_profile=Image.open('shubham.jpg').resize((170,90))
    
    imgtk_profile=ImageTk.PhotoImage(img_profile,master=root)

    lbl_img_profile=Label(frm,image=imgtk_profile)
    lbl_img_profile.place(relx=0.005,rely=0.09)
    lbl_img_profile.image=imgtk_profile


    pic_btn=Button(frm,text='Update Profile',width=14,bg='red',font=('arial',15,'bold'),bd=5,command=update_pic)
    pic_btn.place(relx=0.001,rely=0.29)

    check_btn=Button(frm,text='Check Details',width=14,bg='red',font=('arial',15,'bold'),bd=5,command=check_screen)
    check_btn.place(relx=0.001,rely=0.41)

    update_btn=Button(frm,text='Update Details',width=14,bg='red',font=('arial',15,'bold'),bd=5,command=update_screen)
    update_btn.place(relx=0.001,rely=0.53)

    deposit_btn=Button(frm,text='Deposit Amount',width=14,bg='green',fg='white',font=('arial',15,'bold'),bd=5,command=deposit_screen)
    deposit_btn.place(relx=0.001,rely=.65)

    withdraw_btn=Button(frm,text='Withdraw Amount',width=14,bg='green',fg='white',font=('arial',15,'bold'),bd=5,command=withdraw_screen)
    withdraw_btn.place(relx=0.001,rely=.77)

    transfer_btn=Button(frm,text='Transfer Amount',width=14,bg='green',fg='white',font=('arial',15,'bold'),bd=5,command=transfer_screen)
    transfer_btn.place(relx=0.001,rely=.89)

def existuser_screen():
    def back():
        frm.destroy()
        main_screen()

    def fp_click():
        frm.destroy()
        forgot_screen()

    def reset_click():
        e_acn.delete(0,"end")
        e_pass.delete(0,"end")
        e_acn.focus()

    def submit_click():
        acn=e_acn.get()
        pwd=e_pass.get()

        conobj=sqlite3.connect(database="mybank.sqlite")
        curobj=conobj.cursor()
        query='''select * from accounts where acn=? and pass=?'''
        curobj.execute(query,(acn,pwd))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
            messagebox.showerror("Login","Invalid Credentials")
        else:
            acn=tup[0]
            frm.destroy()
            welcome_screen(acn)

    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='purple')
    frm.place(relx=0,rely=.17,relwidth=1,relheight=.73)

    back_btn=Button(frm,text='Back',bg='red',font=('arial',20,'bold'),bd=5,command=back)
    back_btn.place(relx=0,rely=0)

    lbl_acn=Label(frm,text='🧑‍💼Acn',width=7,font=('arial',20,'bold'),bg='black',fg='white')
    lbl_acn.place(relx=.3,rely=.2)

    e_acn=Entry(frm,font=('arial',18,'bold'),bd=5)
    e_acn.place(relx=.41,rely=.2)
    e_acn.focus()      #for cursor blink on first column

    lbl_pass=Label(frm,text='🔐Pass',width=7,font=('arial',20,'bold'),bg='black',fg='white')
    lbl_pass.place(relx=.3,rely=.3)

    e_pass=Entry(frm,font=('arial',18,'bold'),bd=5,show='*')
    e_pass.place(relx=.41,rely=.3)

    submit_btn=Button(frm,text='Submit',width=7,bg='red',font=('arial',20,'bold'),bd=5,command=submit_click)
    submit_btn.place(relx=.35,rely=.55)

    reset_btn=Button(frm,text='Reset',width=7,bg='red',font=('arial',20,'bold'),bd=5,command=reset_click)
    reset_btn.place(relx=.48,rely=.55)

    fp_btn=Button(frm,text='Forget Password',width=14,bg='red',font=('arial',20,'bold'),bd=5,command=fp_click)
    fp_btn.place(relx=.37,rely=.7)


def newuser_screen():
    def back():
        frm.destroy()
        main_screen()

    def reset_click():
        e_name.delete(0,"end")
        e_email.delete(0,"end")
        e_mob.delete(0,"end")
        e_adhar.delete(0,"end")
        e_name.focus()

    def createacn_db():
        name=e_name.get()
        email=e_email.get()
        mob=e_mob.get()
        adhar=e_adhar.get()

        if len(name)==0 or len(email)==0 or len(mob)==0 or len(adhar)==0:
            messagebox.showwarning("New User","Empty fields are not allowed")
            return
        match=re.fullmatch(r"[a-zA-Z0-9_.]+@[a-zA-Z]+\.[a-zA-Z]+",email)
        if match==None:
            messagebox.showwarning("New User","Invalid Email")
            return
        match=re.fullmatch("[6-9][0-9]{9}",mob)
        if match==None:
            messagebox.showwarning("New User","Invalid Mob No.")
            return
        match=re.fullmatch("[0-9]{12}",adhar)
        if match==None:
            messagebox.showwarning("New User","Invalid Adhar")
            return
        
        bal=0
        opendate=datetime.now()
        pwd=Generator.generate_pass()
        query='''insert into accounts values(?,?,?,?,?,?,?,?)'''
        conobj=sqlite3.connect(database="mybank.sqlite")
        curobj=conobj.cursor()
        curobj.execute(query,(None,name,pwd,mob,email,adhar,bal,opendate))
        conobj.commit()
        conobj.close()

        conobj=sqlite3.connect(database="mybank.sqlite")
        curobj=conobj.cursor()
        query='''select max(acn) from accounts'''
        curobj.execute(query)
        tup=curobj.fetchone()
        conobj.close()
        Emailhandler.send_credentials(email,name,tup[0],pwd)

        messagebox.showinfo('Account Creation','Your account is opened \nwe have mailed your credentials to given email')

    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='purple')
    frm.place(relx=0,rely=.17,relwidth=1,relheight=.73)

    back_btn=Button(frm,text='Back',bg='red',font=('arial',20,'bold'),bd=5,command=back)
    back_btn.place(relx=0,rely=0)

    lbl_name=Label(frm,text='🧑‍💼Name',width=7,font=('arial',20,'bold'),bg='black',fg='white')
    lbl_name.place(relx=.1,rely=.2)

    e_name=Entry(frm,font=('arial',18,'bold'),bd=5)
    e_name.place(relx=.21,rely=.2)
    e_name.focus()      #for cursor blink on first column

    lbl_email=Label(frm,text='Email',width=7,font=('arial',20,'bold'),bg='black',fg='white')
    lbl_email.place(relx=.1,rely=.3)

    e_email=Entry(frm,font=('arial',18,'bold'),bd=5)
    e_email.place(relx=.21,rely=.3)

    lbl_mob=Label(frm,text='📲Mob',width=7,font=('arial',20,'bold'),bg='black',fg='white')
    lbl_mob.place(relx=.5,rely=.2)

    e_mob=Entry(frm,font=('arial',18,'bold'),bd=5)
    e_mob.place(relx=.61,rely=.2)

    lbl_adhar=Label(frm,text='Adhar',width=7,font=('arial',20,'bold'),bg='black',fg='white')
    lbl_adhar.place(relx=.5,rely=.3)

    e_adhar=Entry(frm,font=('arial',18,'bold'),bd=5)
    e_adhar.place(relx=.61,rely=.3)

    submit_btn=Button(frm,text='Submit',width=7,bg='red',font=('arial',20,'bold'),bd=5,command=createacn_db)
    submit_btn.place(relx=.35,rely=.55)

    reset_btn=Button(frm,text='Reset',width=7,bg='red',font=('arial',20,'bold'),bd=5,command=
                     reset_click)
    reset_btn.place(relx=.48,rely=.55)


def main_screen():  #to make main screen frame

    def newuser_click():
        frm.destroy()
        newuser_screen()

    def existuser_click():
        frm.destroy()
        existuser_screen()

    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='blue')
    frm.place(relx=0,rely=.17,relwidth=1,relheight=.73)

    newuser_btn=Button(frm,text='New User \nCreate account',
                       font=('arial',20,'bold'),
                       fg='black',
                       bg='red',
                       bd=5,
                       width=14,
                       activebackground='purple',
                       activeforeground='white',
                       command=newuser_click)
    newuser_btn.place(relx=.27,rely=.3)

    existuser_btn=Button(frm,text='Existing User \nSign In',
                       font=('arial',20,'bold'),
                       fg='black',
                       bg='red',
                       bd=5,
                       width=14,
                       activebackground='purple',
                       activeforeground='white',
                       command=existuser_click)
    existuser_btn.place(relx=.5,rely=.3)

root=Tk()   #ye code top level window banata hai
root.state('zoomed')    #to make fullscreen window
root.resizable(width=False,height=False)    #ye window ko unresizeable banata hai
root.configure(bg='red')

title=Label(root,text="Banking Simulation",
            font=('arial',40,'bold','underline'),bg='red')
title.pack()

curdate=time.strftime("%d-%b-%Y ⏱️%r")
date=Label(root,text=curdate,
           font=('arial',18,'bold'),bg='red',fg='yellow')
date.pack(pady=15)      #pady is for space between upperacse
update_time()

img=Image.open('bank_logo.png').resize((170,130))
imgtk=ImageTk.PhotoImage(img,master=root)

lbl_img=Label(root,image=imgtk)
lbl_img.place(relx=0.001,rely=0)

img1=Image.open('bank_logo1.jpg').resize((170,130))
imgtk1=ImageTk.PhotoImage(img1,master=root)

lbl_img1=Label(root,image=imgtk1)
lbl_img1.place(relx=0.87,rely=0)

footer=Label(root,text="Developed by:Vaibhav Kumar \n📲6207248794",
            font=('arial',20,'bold'),bg='red')
footer.pack(side='bottom')

main_screen()
root.mainloop()     #to make window visible


