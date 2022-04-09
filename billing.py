from os import name
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3
import time
from datetime import date, timedelta
import os
import tempfile


class BillClass:
        def __init__(self,root):
                self.root=root
                # self.root.attributes('-fullscreen', True)
                self.root.geometry("1350x700+0+0")
                self.root.title("Classic Dry Cleaners | Developed by Hasan Mehmood")
                self.root.config(bg="white")
                self.cart_list=[]
                self.chk_print=0
                #==============title==============================================
                self.icon_title=PhotoImage(file="images/logo1.png")
                title=Label(self.root,text="Classic Dry Cleaners", image=self.icon_title,compound=LEFT, font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)
#===============Button Loug Out========================================
                btn_logout= Button(self.root,command=self.logout,text="Logout",font=("times new roman", 15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=150)
#===============clock==============================================
                self.var_adv = IntVar()

                self.lbl_clock=Label(self.root,text="Welcome\t\t Date: DD-MM-YY\t\t Time: HH:MM:SS", font=("times new roman",15,),bg="#4d636d",fg="white")
                self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
                
                self.adv=Label(self.root,text="Advance", font=("times new roman",15,"bold"),bg="#4d636d",fg="white").place(x=990,y=70)
                self.adv=Entry(self.root,textvariable=self.var_adv, font=("times new roman",15,"bold"),bg="lightyellow").place(x=1085,y=72)

#=================Product Frame=======================================
                self.var_search=StringVar()

                ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
                ProductFrame1.place(x=6,y=110,width=410,height=550)

                pTitle=Label(ProductFrame1,text="All Products",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)
# ==================Product Search Frame===========================================
                ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
                ProductFrame2.place(x=2,y=42,width=398,height=375)

                lbl_search=Label(ProductFrame2,text="Search Product | By Name ",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)

                lbl_search=Label(ProductFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=5,y=45)
                txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow")
                txt_search.place(x=133,y=47,width=150,height=22)
                txt_search.bind("<Key>", self.search)
                btn_search=Button(ProductFrame2,text="Search",font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=287,y=45,width=100,height=25)
                btn_show_all=Button(ProductFrame2,text="Show All ",font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=287,y=10,width=100,height=25)

# ==================Product Details Frame=============================================

                ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE)
                ProductFrame3.place(x=2,y=140,width=398,height=385)

                scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
                scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)
                self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
                scrollx.pack(side=BOTTOM,fill=X)
                scrolly.pack(side=RIGHT,fill=Y)
                scrollx.config(command=self.product_Table.xview)
                scrolly.config(command=self.product_Table.yview)
                self.product_Table.heading("pid",text="PID")
                self.product_Table.heading("name",text="Name")
                self.product_Table.heading("price",text="Price")
                self.product_Table.heading("qty",text="Quantity")
                self.product_Table.heading("status",text="Status")
                self.product_Table["show"]="headings"

                self.product_Table.column("pid",width=30)
                self.product_Table.column("name",width=100)
                self.product_Table.column("price",width=90)
                self.product_Table.column("qty",width=60)
                self.product_Table.column("status",width=90)
                self.product_Table.pack(fill=BOTH,expand=1)
                self.product_Table.bind("<ButtonRelease-1>",self.get_data)

                lbl_note=Label(ProductFrame1,text="Note:'Enter 0 Quantity to remove product from the Cart.'",font=("goudy old style",12),anchor='w',bg="white",fg="red").pack(side=BOTTOM,fill=X)
        
                # =============================Customer Frame=========================================================
                self.var_cname=StringVar()
                self.var_contact=StringVar()

                CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
                CustomerFrame.place(x=420,y=110,width=530,height=70)

                cTitle=Label(CustomerFrame,text="Customer Details",font=("goudy old style",15),bg="lightgrey").pack(side=TOP,fill=X)
                lbl_name=Label(CustomerFrame,text="Name",font=("times new roman",15),bg="white").place(x=5,y=35)
                txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13),bg="lightyellow").place(x=80,y=35,width=180)
        
                lbl_contact=Label(CustomerFrame,text="Contact No.",font=("times new roman",15),bg="white").place(x=270,y=35)
                txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13),bg="lightyellow").place(x=380,y=35,width=140)
       
     # ===============Cal Cart Frame===========================================

                Cal_Cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
                Cal_Cart_Frame.place(x=420,y=190,width=530,height=360)
                # ==============Calculator Frame===========================================
# ========================All Functions==================================================

        # ===============Cart Frame===========================================

                cart_Frame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
                cart_Frame.place(x=55,y=8,width=400,height=342)
                self.cartTitle=Label(cart_Frame,text="Cart  Total Products: [0]",font=("goudy old style",15),bg="lightgrey")
                self.cartTitle.pack(side=TOP,fill=X)


                scrolly=Scrollbar(cart_Frame,orient=VERTICAL)
                scrollx=Scrollbar(cart_Frame,orient=HORIZONTAL)

                self.CartTable=ttk.Treeview(cart_Frame,columns=("pid","name","price","qty",),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
                scrollx.pack(side=BOTTOM,fill=X)
                scrolly.pack(side=RIGHT,fill=Y)

                scrollx.config(command=self.CartTable.xview)
                scrolly.config(command=self.CartTable.yview)

                self.CartTable.heading("pid",text="PID")
                self.CartTable.heading("name",text="Name")
                self.CartTable.heading("price",text="Price")
                self.CartTable.heading("qty",text="QTY")
                self.CartTable["show"]="headings"

                self.CartTable.column("pid",width=38)
                self.CartTable.column("name",width=90)
                self.CartTable.column("price",width=86)
                self.CartTable.column("qty",width=40)
                self.CartTable.pack(fill=BOTH,expand=1)
                self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)

                # ===========ADD Cart Widgets Frame===========================================
                self.var_pid=StringVar()
                self.var_pname=StringVar()
                self.var_price=StringVar()
                self.var_qty=StringVar()
                self.var_stock=StringVar()


                Add_CartWidgetsFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
                Add_CartWidgetsFrame.place(x=420,y=550,width=530,height=110)

                lbl_p_name=Label(Add_CartWidgetsFrame,text="Product Name",font=("times new roman",15),bg="white").place(x=5,y=5)
                txt_p_name=Entry(Add_CartWidgetsFrame,textvariable=self.var_pname,font=("times new roman",15),bg="lightyellow",state="readonly").place(x=5,y=35,width=190,height=22)

                lbl_p_price=Label(Add_CartWidgetsFrame,text="Price per Quantity",font=("times new roman",15),bg="white").place(x=230,y=5)
                txt_p_price=Entry(Add_CartWidgetsFrame,textvariable=self.var_price,font=("times new roman",15),bg="lightyellow",state="readonly").place(x=230,y=35,width=150,height=22)

                lbl_p_qty=Label(Add_CartWidgetsFrame,text="Quantity",font=("times new roman",15),bg="white").place(x=410,y=5)
                txt_p_qty=Entry(Add_CartWidgetsFrame,textvariable=self.var_qty,font=("times new roman",15),bg="lightyellow").place(x=420,y=35,width=50,height=22)

                self.lbl_inStock=Label(Add_CartWidgetsFrame,text="In Stock",font=("times new roman",15),bg="white")
                self.lbl_inStock.place(x=5,y=70)

                btn_clear_cart=Button(Add_CartWidgetsFrame,text="Clear",command=self.clear_cart,font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=165,y=70,width=150,height=30)
                btn_add_cart=Button(Add_CartWidgetsFrame,text="Add | Update Cart",command=self.add_update_cart,font=("times new roman",15,"bold"),bg="orange",cursor="hand2").place(x=330,y=70,width=180,height=30)

                # =================================Billing Area============================
                billFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
                billFrame.place(x=953,y=110,width=410,height=410)
                BTitle=Label(billFrame,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="#f44336",fg="white").pack(side=TOP,fill=X)
                scrolly=Scrollbar(billFrame,orient=VERTICAL)
                scrolly.pack(side=RIGHT,fill=Y)
                self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
                self.txt_bill_area.pack(fill=BOTH,expand=1)
                scrolly.config(command=self.txt_bill_area.yview)

# ====================Billing Buttons==================================================
                billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
                billMenuFrame.place(x=953,y=520,width=410,height=140)

                self.lbl_amnt=Label(billMenuFrame,text='Bill Amount\n[0]',font=('goudy old style',15,"bold"),bg="#3f51b5",fg="white")
                self.lbl_amnt.place(x=2,y=5,width=120,height=70)

                
                self.lbl_discount=Label(billMenuFrame,text='Advance\n[0]',font=('goudy old style',15,"bold"),bg="#8bc34a",fg="white")
                self.lbl_discount.place(x=124,y=5,width=120,height=70)
                
                self.lbl_net_pay=Label(billMenuFrame,text='Balance\n[0]',font=('goudy old style',15,"bold"),bg="#607d8b",fg="white")
                self.lbl_net_pay.place(x=246,y=5,width=160,height=70)
                
                btn_print=Button(billMenuFrame,text='Print',command=self.print_bill,cursor="hand2",font=('goudy old style',15,"bold"),bg="crimson",fg="white")
                btn_print.place(x=2,y=80,width=120,height=50)

                btn_clear_all=Button(billMenuFrame,text='Clear All',command=self.clear_all,cursor="hand2",font=('goudy old style',15,"bold"),bg="gray",fg="white")
                btn_clear_all.place(x=124,y=80,width=120,height=50)

                btn_generate=Button(billMenuFrame,text='Generate/Save Bill',command=self.generate_bill,cursor="hand2",font=('goudy old style',11,"bold"),bg="#009688",fg="white")
                btn_generate.place(x=246,y=80,width=160,height=50)
# ====================================Footer=========================================================
                footer=Label(self.root,text="Classic Dry Cleaners | Developed by Hasan Mehmood",font=("times new roman",11),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
                self.show()
                # self.bill_top()
                self.update_date_time()
# =====================================All Functions===================================================
        def show(self):
                con=sqlite3.connect(database=r'ims.db')
                cur=con.cursor()
                try:
                        # self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
                        cur.execute("Select pid,name,price,qty,status from product where status='Active'")
                        rows=cur.fetchall()
                        self.product_Table.delete(*self.product_Table.get_children())
                        for row in rows:
                                self.product_Table.insert('',END,values=row)
                except Exception as ex:
                        messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


        def search(self, ev):
                con=sqlite3.connect(database=r'ims.db')
                cur=con.cursor()

                try:
                        # if self.var_search.get()=="":
                        #         messagebox.showerror("Error","Please Enter something.",parent=self.root)
                        # else: 
                        cur.execute("Select pid,name,price,qty,status from product where name LIKE '%"+self.var_search.get()+"%' and status='Active'")
                        rows=cur.fetchall()
                        if len(rows)!=0:

                                self.product_Table.delete(*self.product_Table.get_children())
                                for row in rows:
                                        self.product_Table.insert('',END,values=row)

                        else:
                                # messagebox.showerror("Error","No record found.",parent=self.root)
                                self.product_Table.delete(*self.product_Table.get_children())


                except Exception as ex:
                        messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


# ==================Calculator Functions==============================================

        def get_input(self,num):
                xnum=self.var_cal_input.get()+str(num)
                self.var_cal_input.set(xnum)

        def clear_cal(self):
               self.var_cal_input.set('') 

        def perform_cal(self):
                result=self.var_cal_input.get()
                self.var_cal_input.set(eval(result))



        def get_data(self,ev):
                f=self.product_Table.focus()
                content=(self.product_Table.item(f))
                row=content['values']
                self.var_pid.set(row[0])
                self.var_pname.set(row[1])
                self.var_price.set(row[2])
                self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
                self.var_stock.set(row[3])
                self.var_qty.set('1')
                # self.var_adv.set('0')
        

        def get_data_cart(self,ev):
                f=self.CartTable.focus()
                content=(self.CartTable.item(f))
                row=content['values']
                self.var_pid.set(row[0])
                self.var_pname.set(row[1])
                self.var_price.set(row[2])
                self.var_qty.set(row[3])
                self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
                self.var_stock.set(row[4])
                
        def add_update_cart(self):
                if self.var_pid.get()=='':
                        messagebox.showerror("Error","Please select product from list.",parent=self.root)
                elif self.var_qty.get()=='':
                        messagebox.showerror("Error","Quantity is required.",parent=self.root)
                elif int(self.var_qty.get())>int(self.var_stock.get()):
                        messagebox.showerror("Error","Invalid Quantity. Out of Stock.",parent=self.root)

                else:
                        price_cal=float(int(self.var_qty.get())*float(self.var_price.get()))
                        price_cal=float(price_cal)
                        price_cal=self.var_price.get()
                        # pid,name,price,qty,stock

                        cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get(), self.var_adv.get()]
                        # self.cart_list.append(cart_data)
                        
# =======================Update Cart===========================================
                        present='no'
                        index_=0
                        for row in self.cart_list:
                                if self.var_pid.get()==row[0]:
                                        present='yes'
                                        break
                                index_+=1
                        if present=='yes':
                                op=messagebox.askyesno("Confirmation","Product already present\nDo you want to add again?",parent=self.root)
                                if op==True:
                                        if self.var_qty.get()=="0":
                                                self.cart_list.pop(index_)
                                        else:
                                                self.cart_list[index_][2]=price_cal #price
                                                self.cart_list[index_][3]=self.var_qty.get() #Qty
                        else:
                                self.cart_list.append(cart_data)
                        self.show_cart()
                        self.bill_updates()
                

        def bill_updates(self):
                self.bill_amnt=0
                self.net_pay=0
                self.advance=0
                # self.balance=0
                for row in self.cart_list:
                        self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))
                
                # self.advan = row[5]
                # self.balance= float(self.bill_amnt) - float(self.var_adv.get())
                # self.lbl_discount.config(text=f'Advance\n{str(row[5])}')
                self.lbl_amnt.config(text=f'Total\n{str(self.bill_amnt)}')
                # self.lbl_net_pay.config(text=f'Balance\n{str(self.balance)}')
                self.cartTitle.config(text=f"Cart Total Products: [{str(len(self.cart_list))}]")
                
        def show_cart(self):
                try:
                        self.CartTable.delete(*self.CartTable.get_children())
                        for row in self.cart_list:
                                self.CartTable.insert('',END,values=row)
                except Exception as ex:
                        messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

        def generate_bill(self):
                if self.var_cname.get()=="" or self.var_contact=="":
                        messagebox.showerror("Error","Customer Details are required.",parent=self.root)
                elif len(self.cart_list)==0:
                        messagebox.showerror("Error","Add products to generate bill.",parent=self.root)
                else:
                        # ======Bill Top=========
                        self.bill_top()
                        # ======Bill Mid=========
                        self.bill_middle()
                        # ======Bill Bottom======
                        self.bill_bottom()

                        fp=open(f'bill/{str(self.invoice)}.txt','w')
                        fp.write(self.txt_bill_area.get("1.0",END))
                        fp.close()
                        messagebox.showinfo("Saved","Bill has been generated and saved.",parent=self.root)
                        self.chk_print=1
        
        def bill_top(self):
                self.invoice=int(time.strftime('%H%M%S')) + int(time.strftime("%d%m%Y"))

                bill_top_temp=f'''
\t\tClassic Cleaners
Phone No. 0302-8009788, Karachi Shop#1,\nTauheed Commercial Plot#35-C, St-25
Customer Name: {self.var_cname.get()} Bill No.{str(self.invoice)}
Date:{date.today()} Delivery Date:{date.today() + timedelta(3)}
{str("="*47)}
Product Name  QTY \tPrice
{str("="*47)}
        '''
                self.txt_bill_area.delete('1.0',END)
                self.txt_bill_area.insert('1.0',bill_top_temp)

        def bill_bottom(self):
                self.advan = self.var_adv.get()
                self.balance= float(self.bill_amnt) - (self.var_adv.get())
                
                self.balance= float(self.bill_amnt) - float(self.var_adv.get())
                self.lbl_discount.config(text=f'Advance\n{self.var_adv.get()}')
                self.lbl_net_pay.config(text=f'Balance\n{str(self.balance)}')
                bill_bottom_temp=f'''
{str("="*47)}
Bill Amount\t\t\tRs.{self.bill_amnt}
Advance\t\t\tRs.{self.advan}
Balance\t\t\t\tRs.{float(self.bill_amnt) - self.advan}
{str("="*47)}\n
        '''
                self.txt_bill_area.insert(END,bill_bottom_temp)

        def bill_middle(self):
                con=sqlite3.connect(database=r'ims.db')
                cur=con.cursor()
                try:
                        for row in self.cart_list:
                                pid=row[0]
                                name=row[1]
                                qty=int(row[4])-int(row[3])
                                if int(row[3])==int(row[4]):
                                        status='Inactive'
                                if int(row[3])!=int(row[4]):
                                        status='Active'
                                
                                price=float(row[2])*int(row[3])
                                price=str(price)
                                self.txt_bill_area.insert(END,"\n"+name+"\t\t\t"+row[3]+"\tRs."+price)
                                # =================Update product in product table===========================
                                cur.execute('Update product set qty=?,status=? where pid=?',(
                                        qty,
                                        status,
                                        pid
                                ))
                                con.commit()
                        con.close()
                        self.show()
                except Exception as ex:
                        messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
              
        def clear_cart(self):
                self.var_pid.set("")
                self.var_pname.set("")
                self.var_price.set("")
                self.var_qty.set("")
                self.lbl_inStock.config(text=f"In Stock")
                self.var_stock.set("")
               
        def clear_all(self):
                del self.cart_list[:]
                self.var_cname.set("")
                self.var_contact.set("")
                self.txt_bill_area.delete("1.0",END)
                self.cartTitle.config(text=f"Cart Total Products: [0]")
                self.var_search.set("")
                self.var_adv.set("")
                self.clear_cart()
                self.show()
                self.show_cart()

        def update_date_time(self):
                time_=time.strftime("%I:%M:%S")
                date=time.strftime("%d-%m-%Y")
                self.lbl_clock.config(text=f"Welcome\t\t Date: {str(date)}\t\t Time: {str(time_)}")
                self.lbl_clock.after(200,self.update_date_time)

        def print_bill(self):
                if self.chk_print==1:
                        messagebox.showinfo("Print","Please wait while printing",parent=self.root)
                        new_file=tempfile.mktemp('.txt')
                        open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
                        os.startfile(new_file,'print')

                else:
                        messagebox.showerror("Print","Please generate bill to print.",parent=self.root)


        def logout(self):
                self.root.destroy()
                os.system("python login.py")
                        
if __name__=="__main__":
    root = Tk()
    obj=BillClass(root)
    root.mainloop() 