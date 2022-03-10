from posixpath import split
from re import sub
from urllib import request
from flask import redirect, url_for
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from tkinter import *
from matplotlib.pyplot import text
import requests
import threading
import time
import phonenumbers
import tkinter.messagebox



from PIL import Image, ImageTk
import json

import requests


import  penzi_support
import backend





class Toplevel1:

    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        top.geometry("690x680+271+26")
        top.minsize(1, 1)
        top.maxsize(1351, 738)
        top.resizable(1,  1)
        top.title("PENZI")
        top.configure(background="#d8d8d8")
        top.configure(highlightcolor="#ffffff")

        self.top = top

        def delete():
                if self.Text1.get("1.0","end-1c") == "" and self.Text2.get("1.0","end-1c") == "" and self.Text3.get("1.0","end-1c")  == "":
                        tkinter.messagebox.showerror("FAILURE", "FIELDS ARE ALREADY EMPTY")
                else:
                        self.Text1.delete("1.0","end-1c")
                        self.Text2.delete("1.0","end-1c")
                        self.Text3.delete("1.0","end-1c")
                        self.Message1.config(text = "")

        
        def submit():

                global user_message, proceed_registration
                proceed_registration = False
                activation_header = "penzi"
                start_header = "start"
                details_header = "details"
                next_message = "next"
                
                user_sender = self.Text1.get("1.0","end-1c")
                user_message = self.Text2.get("1.0","end-1c")
                user_receiver = self.Text3.get("1.0","end-1c")

                user_message = user_message.lower()

                user_sender = phonenumbers.parse(user_sender, "KE")
                user_sender=phonenumbers.format_number(user_sender, phonenumbers.PhoneNumberFormat.E164)
                
                unfiltered_message = [user_message]

                
                def start_activation():
                        
                        data = json.dumps({"status": "active"})
                        headers = {'Content-type': 'application/json', 'Acceept': 'text/plain'}
                        requests.put(f"http://127.0.0.1:8007/update_status/{user_sender}", headers = headers, data = data)
                      

                def start_process():                                                
                                                        
                        message1 = requests.get(f"http://127.0.0.1:8007/get_message_start/{user_sender}")                    
                        message1 = message1.text
                        unfiltered_m = [message1]
                        for item in unfiltered_m:
                                header, name, age, gender, county, town = item.split("#")
                        data = json.dumps({"name": name, "age": age, "gender": gender, "county": county, "town": town, "number": user_sender})
                        headers = {'Content-type': 'application/json',
                                'Acceept': 'text/plain'}
                        requests.post(
                                "http://127.0.0.1:8007/post_start_user", headers = headers, data = data
                        )
                        self.Message1.config(text = "")
                        time.sleep(5)
                        
                        penzi_number = 2
                        headers = {'Content-type': 'application/json', 'Acceept': 'text/plain'}
                        response2 = requests.get(f"http://127.0.0.1:8007/get_penzi_message_start/{penzi_number}", headers=headers)
                        response2 = response2.text
                        self.Message1.config(text=response2)
                        time.sleep(60)
                        
                        if proceed_registration:
                            exit
                        else:
                            start_activation()
                            self.Message1.config(text = "")
                            time.sleep(3)
                            penzi_number = 4
                            response4 = requests.get(f"http://127.0.0.1:8007/get_penzi_message_start/{penzi_number}", headers=headers)
                            response4 = response4.text
                            self.Message1.config(text=response4)         
                        


                def details():
                        global proceed_registration
                        proceed_registration = True
                        self.Message1.config(text = "")
                        # tkinter.messagebox.showinfo("DETAILS", "DETAILS FUNCTION HAS BEEN EXECUTED")
                        message2 = requests.get(f"http://127.0.0.1:8007/get_message_details/{user_sender}")                    
                        message2 = message2.text
                        unfiltered_m = [message2]
                        for item in unfiltered_m:
                                header, education_level, profession, marital_status, religion, tribe = item.split("#")
                        data = json.dumps({"education_level": education_level, "profession": profession, "marital_status": marital_status, "religion": religion, "tribe": tribe})
                        headers = {'Content-type': 'application/json',
                                'Acceept': 'text/plain'}
                        requests.put(f"http://127.0.0.1:8007/patch_user_details/{user_sender}", headers = headers, data = data)
                        print(education_level)
                        print(profession)
                        print(marital_status)
                        time.sleep(5)
                        penzi_number = 3
                        headers = {'Content-type': 'application/json', 'Acceept': 'text/plain'}
                        response3 = requests.get(f"http://127.0.0.1:8007/get_penzi_message_start/{penzi_number}", headers=headers)
                        response3 = response3.text
                        self.Message1.config(text=response3)
                        time.sleep(30)
                        if proceed_registration == False:
                            exit
                        else:
                            start_activation()
                            self.Message1.config(text = "")
                            time.sleep(3)
                            penzi_number = 4
                            response4 = requests.get(f"http://127.0.0.1:8007/get_penzi_message_start/{penzi_number}", headers=headers)
                            response4 = response4.text
                            self.Message1.config(text=response4)



                def myself_description():
                        global proceed_registration
                        proceed_registration = False
                        self.Message1.config(text = "")
                        # tkinter.messagebox.showinfo("MYSELF", "MYSELF FUNCTION HAS BEEN EXECUTED")
                        message2 = requests.get(f"http://127.0.0.1:8007/get_message_myself/{user_sender}")                    
                        message2 = message2.text
                        unfiltered_m = [message2]
                        for item in unfiltered_m:
                                header, description = item.split()
                        print(header)
                        print(description)
                        data = json.dumps({"sender_number": user_sender, "description": description})
                        headers = {'Content-type': 'application/json',
                                'Acceept': 'text/plain'}
                        requests.put(f"http://127.0.0.1:8007/patch_user_myself/{user_sender}", headers = headers, data = data)                        
                        time.sleep(5)
                        start_activation()
                        penzi_number = 5
                        headers = {'Content-type': 'application/json', 'Acceept': 'text/plain'}
                        response3 = requests.get(f"http://127.0.0.1:8007/get_penzi_message_start/{penzi_number}", headers=headers)
                        response3 = response3.text
                        self.Message1.config(text=response3)




                def start_next():
                            print("I'm here")
                            global i, j, total, rem
                            a1 = ""
                            b1 = ""
                            c1 = ""
                            d1 = ""
                            rem = 0
                            total = totals
                            j = 0
                            i = 0

                            if total <= 3 and total > 0:
                                
                                try:
                                
                                    for names in list1:
                                        name = list1[i].get('name')
                                        for details in list1:
                                            age = list1[i].get('age')
                                            number = list1[i].get('number')
                                            new_number = number[4:]
                                            i = i + 1
                                            d1 += str(f" {name}, aged {age}, 0{new_number},  ")
                                            print(d1)
                                            break
                                except IndexError:
                                    a1 += str("There are no more partners to find a match. Try changing your matching criteria")            
                                    self.Message1.config(text=(f"{d1}\n{a1}"))
                                    exit

                            elif total == 0:
                                a1 += str("There are no matches found. Try changing your match criteria")
                                self.Message1.config(text=a1)



                            else:
                                print("I'm now here")
                                for names in list1:
                                    if i > 2:
                                        rem = total - j
                                        b1 += str(f" Send NEXT to 5001 to receive details of the remaining {rem} matches.")
                                        break

                                    else: 

                                        name = list1[i].get('name')
                                        for details in list1:
                                            age = list1[i].get('age')
                                            number = list1[i].get('number')
                                            number = str(number)
                                            new_number = number[3:]
                                            c1 += str(f" {name}, aged {age}, 0{new_number},  ")
                                            i = i + 1
                                            j = j + 1
                                            break
                            self.Message1.config(text=(f"{c1}\n{b1}"))            
                          


                    
                        

                def next():
                        print("inside next >>")
                        
                        global k,i,j,total, rem
                        a1 = ""
                        b1 = ""
                        c1 = ""
                        d1 = ""
                        k = i + 2
                        print(f"rem => {rem}")
                        if rem <= 3 and rem > 0:
                                
                            try:
                                    print("Entered try statement...")
                                    for names in list1:
                                        name = list1[i].get('name')
                                        for details in list1:
                                            age = list1[i].get('age')
                                            number = list1[i].get('number')
                                            number = str(number)
                                            new_number = number[3:]
                                            i = i + 1
                                            d1 += str(f" {name}, aged {age}, 0{new_number},  ")
                                            break
                                    
                                            
                            except IndexError:
                                print("In except statement")
                                a1 += str(" There are no more people to find a match. Try changing your matching criteria.")            
                                self.Message1.config(text=(f"{d1}\n{a1}"))
                                time.sleep(5)
                                exit

                            else:
                                print("In else statement")
                                a1 += str(" There are no more people to find a match. Try changing your matching criteria.")            
                                self.Message1.config(text=(f"{d1}\n{a1}"))
                                time.sleep(5) 

                        elif j == 0:
                            a1 += str("There are no matches found. Try changing your match criteria")
                            self.Message1.config(text=a1)
                            exit
                        
                        
                        else:
                                
                                for names in list1:
                                    if i > k:
                                            rem = total - j
                                            b1 += str(f" Send NEXT to 5001 to receive details of the remaining {rem} matches.")
                                            break

                                    else: 

                                        name = list1[i].get('name')
                                        for details in list1:
                                            age = list1[i].get('age')
                                            number = list1[i].get('number')
                                            number = str(number)
                                            new_number = number[3:]
                                            c1 += str(f" {name}, aged {age}, 0{new_number},  ")
                                            i = i + 1
                                            j = j + 1
                                            break

                        self.Message1.config(text=(f"{c1}\n{b1}"))


                def match():
                        global gender, list1,age1,age2,totals,req
                        self.Message1.config(text = "")
                        # tkinter.messagebox.showinfo("MATCH", "MATCH FUNCTION HAS BEEN EXECUTED")
                        message2 = requests.get(f"http://127.0.0.1:8007/get_message_match/{user_sender}")                    
                        message2 = message2.text
                        message2 = message2.replace("#","-")
                        
                        unfiltered_m = [message2]
                        for item in unfiltered_m:
                                header, age1, age2, county = item.split("-")
                                
                        print(header)
                        print(county)
                        age1 = int(age1)
                        age2 = int(age2)
                        headers = {'Content-type': 'application/json', 'Acceept': 'text/plain'}
                        gender = requests.get(f"http://127.0.0.1:8007/get_gender/{user_sender}", headers = headers)
                        gender = gender.text
                        if gender == "male":
                                gender = "female"
                        else:
                                gender = "male"
                        headers = {'Content-type': 'application/json', 'Acceept': 'text/plain'}
                        count_result = requests.get(f"http://127.0.0.1:8007/search_test_number/{age1}/{age2}/{county}/{gender}", headers = headers)                        
                        count_result = count_result.text
                        count_result = int(count_result)

                        time.sleep(5)
                        if gender == "female":
                                match_request1 = f"We have {count_result} ladies who match your choice! We will send you details of 3 of them shortly. To get more details about a lady, SMS her number e.g 0722123456 to 5001"
                        else:   
                                gender == "male"
                                match_request1 = f"We have {count_result} guys who match your choice! We will send you details of 3 of them shortly. To get more details about a guy, SMS his number e.g 0722123456 to 5001"
                        self.Message1.config(text=match_request1)
                        time.sleep(5)
                        global totals
                        totals = requests.get(f"http://127.0.0.1:8007/search_test_number/{age1}/{age2}/{county}/{gender}")
                        totals = totals.text
                        totals = int(totals)
                        req =requests.get(f"http://127.0.0.1:8007/search_query/{age1}/{age2}/{county}/{gender}")
                        
                        req = req.text
                        
                        list1 = json.loads(req)
                        
                        start_next()


                def describe_match():
                        global user_message
                        user_message1 = phonenumbers.parse(user_message, "KE")
                        user_message1 = phonenumbers.format_number(user_message1, phonenumbers.PhoneNumberFormat.E164)
                        join = ""
                        print(user_message1)
                        req =requests.get(f"http://127.0.0.1:8007/describe_by_number/{user_message1}")
                        req = req.text
                        list1 = json.loads(req)
                        print(type(list1["number"]))
                        join += str(list1["name"]+" aged "+str(list1["age"])+", "+list1["county"]+" county, "+list1["education_level"]+" level of education,"
                                        +"  "+list1["profession"]+", "+list1["marital_status"]+", "+list1["religion"]+", "+list1["tribe"]+"\n"+
                                        "Send DESCRIBE +"+ str(list1["number"])+ " to get more details about "+ list1["name"] )
                        self.Message1.config(text = join)
                        
                       

                def match_description():
                        link = ""
                        req =requests.get(f"http://127.0.0.1:8007/describe_by_number/{description}")
                        req = req.text
                        list1 = json.loads(req)
                        link += str(list1["name"]+" describes themselves as "+list1["description"])
                        self.Message1.config(text = link)
                






                if user_message == activation_header:
                        penzi_number = 1
                        headers = {'Content-type': 'application/json', 'Acceept': 'text/plain'}
                        response1 = requests.get(f"http://127.0.0.1:8007/get_penzi_message_start/{penzi_number}", headers=headers)
                        response1 = response1.text
                        self.Message1.config(text=response1)

                elif user_message == next_message:
                    
                        next()

                elif len(user_message) == 10:

                        describe_match()

                else:

                        try:
                                for item in unfiltered_message:
                                        header, item1, item2, item3, item4, item5 = item.split("#")

                        except ValueError:
                                try:
                                        for item in unfiltered_message:
                                                header, description = item.split()

                                        if header == "myself":
                                                data = json.dumps({"sender_number": user_sender ,"message_myself": user_message, "receiver_shortcode": user_receiver})
                                                headers = {'Content-type': 'application/json',
                                                        'Acceept': 'text/plain'}
                                                requests.post(f"http://127.0.0.1:8007/post_message_myself", headers=headers, data=data )
                                                myself_description()

                                        elif header == "describe":
                                                match_description()
                                except ValueError:
                                        try:
                                                message2 = user_message.replace("#","-")
                                                unfiltered_message = [message2]
                                                for item in unfiltered_message:
                                                        header, age1, age2, county = item.split("-")
                                                print(header)
                                                print(county)
                                                data = json.dumps({"sender_number": user_sender, "match_message": user_message, "receiver_shortcode": user_receiver})
                                                headers = {'Content-type': 'application/json',
                                                'Acceept': 'text/plain'}
                                                requests.post(f"http://127.0.0.1:8007/post_message_match", headers=headers, data=data )
                                                match()
                                        
                                        except:
                                                tkinter.messagebox.showerror("ERROR"," INVALID MESSAGE SYNTAX, PLEASE TRY AGAIN")
                                                print("Message entered is of a wrong format")

                        else:
                        
                                if header == start_header:
                                        data = json.dumps({"header": header, "sender_number": user_sender, "message": user_message,
                                                        "receiver_shortcode": user_receiver})
                                        headers = {'Content-type': 'application/json',
                                                'Acceept': 'text/plain'}
                                        requests.post(
                                        "http://127.0.0.1:8007/post_start", headers=headers, data=data, )
                                        # data = json.dumps({"status": "inactive"})
                                        # headers = {'Content-type': 'application/json', 'Acceept': 'text/plain'}
                                        # requests.put(f"http://127.0.0.1:8007/update_status/{user_sender}", headers = headers, data = data)
                                        
                                        start_process()                                                        

                                elif header == details_header:
                                       
                                        # tkinter.messagebox.showinfo("INFO", "DETAILS HEADER DETECTED")
                                        data = json.dumps({"sender_number": user_sender, "message_details": user_message, "receiver_shortcode": user_receiver})
                                        headers = {'Content-type': 'application/json',
                                                'Acceept': 'text/plain'}
                                        requests.post(f"http://127.0.0.1:8007/post_message_details", headers=headers, data=data, )
                                      
                                        details()

                                

                                        

                               


                                        
                                                                

        
                                                        

                                       
                                        

                                        


        self.Button1 = tk.Button(self.top)
        self.Button1.place(relx=0.029, rely=0.676, height=53, width=133)
        self.Button1.configure(background="#27d897")
        self.Button1.configure(borderwidth="2")
        self.Button1.configure(compound='left')
        self.Button1.configure(font="-family {Roboto Mono} -size 11 -weight bold")
        self.Button1.configure(foreground="#ffffff")
        self.Button1.configure(text='''CLEAR''')
        self.Button1.configure(command=delete)

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.Labelframe1 = tk.LabelFrame(self.top)
        self.Labelframe1.place(relx=0.257, rely=0.646, relheight=0.322
                , relwidth=0.723)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(text='''---''')

        self.Label4 = tk.Label(self.Labelframe1)
        self.Label4.place(relx=0.08, rely=0.228, height=38, width=176
                , bordermode='ignore')
        self.Label4.configure(anchor='w')
        self.Label4.configure(compound='left')
        self.Label4.configure(font="-family {Roboto Mono} -size 10")
        self.Label4.configure(text='''Enter Sender Number:''')

        self.Label5 = tk.Label(self.Labelframe1)
        self.Label5.place(relx=0.186, rely=0.594, height=25, width=126
                , bordermode='ignore')
        self.Label5.configure(anchor='w')
        self.Label5.configure(compound='left')
        self.Label5.configure(cursor="fleur")
        self.Label5.configure(font="-family {Roboto Mono} -size 10")
        self.Label5.configure(text='''Enter Message:''')

        self.Label6 = tk.Label(self.Labelframe1)
        self.Label6.place(relx=0.02, rely=0.822, height=25, width=210
                , bordermode='ignore')
        self.Label6.configure(anchor='w')
        self.Label6.configure(compound='left')
        self.Label6.configure(font="-family {Roboto Mono} -size 10")
        self.Label6.configure(text='''Enter Receiver shortcode:''')

        self.Text1 = tk.Text(self.Labelframe1)
        self.Text1.place(relx=0.441, rely=0.183, relheight=0.155, relwidth=0.513
                , bordermode='ignore')
        self.Text1.configure(background="white")
        self.Text1.configure(font="TkTextFont")
        self.Text1.configure(selectbackground="blue")
        self.Text1.configure(selectforeground="white")
        self.Text1.configure(wrap="word")

        self.Text2 = tk.Text(self.Labelframe1)
        self.Text2.place(relx=0.441, rely=0.411, relheight=0.292, relwidth=0.513
                , bordermode='ignore')
        self.Text2.configure(background="white")
        self.Text2.configure(font="TkTextFont")
        self.Text2.configure(selectbackground="blue")
        self.Text2.configure(selectforeground="white")
        self.Text2.configure(wrap="word")

        self.Text3 = tk.Text(self.Labelframe1)
        self.Text3.place(relx=0.441, rely=0.776, relheight=0.155, relwidth=0.513
                , bordermode='ignore')
        self.Text3.configure(background="white")
        self.Text3.configure(font="TkTextFont")
        self.Text3.configure(selectbackground="blue")
        self.Text3.configure(selectforeground="white")
        self.Text3.configure(wrap="word")

        def new_thread():
                threading.Thread(target=submit).start()

        
        self.Button2 = tk.Button(self.top)
        self.Button2.place(relx=0.032, rely=0.871, height=53, width=133)
        self.Button2.configure(background="#27d897")
        self.Button2.configure(command=new_thread)
        self.Button2.configure(borderwidth="2")
        self.Button2.configure(compound='left')
        self.Button2.configure(font="-family {Roboto Mono} -size 11 -weight bold")
        self.Button2.configure(foreground="#ffffff")
        self.Button2.configure(text='''SEND''')

        self.Message1 = tk.Message(self.top)
        self.Message1.place(relx=0.255, rely=0.368, relheight=0.269
                , relwidth=0.709)
        self.Message1.configure(background="#ffffff")
        self.Message1.configure(padx="1")
        self.Message1.configure(pady="1")
        self.Message1.configure(width=475)
        

        self.Canvas1 = tk.Canvas(self.top)
        self.Canvas1.place(relx=0.0, rely=-0.015, relheight=0.09, relwidth=1.001)

        self.Canvas1.configure(background="#27d897")
        self.Canvas1.configure(borderwidth="2")
        self.Canvas1.configure(relief="ridge")
        self.Canvas1.configure(selectbackground="blue")
        self.Canvas1.configure(selectforeground="white")

        self.Label1 = tk.Label(self.Canvas1)
        self.Label1.place(relx=0.434, rely=0.328, height=21, width=75)
        self.Label1.configure(anchor='w')
        self.Label1.configure(background="#27d891")
        self.Label1.configure(compound='left')
        self.Label1.configure(font="-family {Roboto Mono} -size 12 -weight bold")
        self.Label1.configure(foreground="#ffffff")
        self.Label1.configure(text='''WELCOME''')

        self.Custom1 = penzi_support.Custom(self.top)
        self.Custom1.place(relx=0.159, rely=0.221, relheight=0.084
                , relwidth=0.125)
        


        
        



        

def start_up():
    penzi_support.main()

if __name__ == '__main__':
    penzi_support.main()
