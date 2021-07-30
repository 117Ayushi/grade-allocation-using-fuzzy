import tkinter as tk
from tkinter import filedialog
from tkinter import *
import pandas as pd
from fcmeans import FCM

root= tk.Tk()

def displayExcel(df):
    if df is not None:
        text.insert('end', str(df.head(len(df.index))) + '\n')


def get_grade(x,max_grade_f,max_grade_e,max_grade_d_minus,max_grade_d,max_grade_c_minus,max_grade_c,max_grade_b_minus,max_grade_b,max_grade_a_minus,max_grade_a):
    if(x<max_grade_f):
        return 'F'
    elif(x<max_grade_e and x>=max_grade_f):
        return 'E'
    elif(x<max_grade_d_minus and x>=max_grade_e):
        return 'D-'
    elif(x<max_grade_d and x>=max_grade_d_minus):
        return 'D'
    elif(x<max_grade_c_minus and x>=max_grade_d):
        return 'C-'
    elif(x<max_grade_c and x>=max_grade_c_minus):
        return 'C'
    elif(x<max_grade_b_minus and x>=max_grade_c):
        return 'B-'
    elif(x<max_grade_b and x>=max_grade_b_minus):
        return 'B'
    elif(x<max_grade_a_minus and x>=max_grade_b):
        return 'A-'
    elif(x<max_grade_a and x>=max_grade_a_minus):
        return 'A'
    else:
        return 'OutOfBound'


def getGrades(df,entry11,entry12,entry13,entry14,entry15,entry16,entry17,entry18,entry19,entry20):
        max_grade_f = int(entry11.get())
        max_grade_e = int(entry12.get())
        max_grade_d_minus = int(entry13.get())
        max_grade_d = int(entry14.get())
        max_grade_c_minus = int(entry15.get())
        max_grade_c = int(entry16.get())
        max_grade_b_minus = int(entry17.get())
        max_grade_b = int(entry18.get())
        max_grade_a_minus = int(entry19.get())
        max_grade_a = int(entry20.get())
        df['EXPECTED GRADES'] = df['Total150'].apply(lambda x:get_grade(x,max_grade_f,max_grade_e,max_grade_d_minus,max_grade_d,max_grade_c_minus,max_grade_c,max_grade_b_minus,max_grade_b,max_grade_a_minus,max_grade_a))
        df.to_excel('output.xlsx')
        displayExcel(df)

def getExcel():
    global df
    import_file_path = filedialog.askopenfilename()
    df = pd.read_excel (import_file_path)

def allocateGrade():
    global df
    global calculation_type
    calculation_type = entry1.get()

    if(calculation_type == '1'):
        df['EXPECTED GRADES'] = df['Total150'].apply(lambda x:get_grade(x,30,45,60,67,75,90,105,120,135,150))
        df.to_excel('output.xlsx')
        displayExcel(df)
    
    elif(calculation_type == '2'):

        label20 = tk.Label(root, text='Enter the Max value for grade A: ')
        label20.config(font=('helvetica', 12))
        canvas1.create_window(450, 20, window=label20)

        entry20 = tk.Entry(root) 
        canvas1.create_window(650, 20, window=entry20) 

        label19 = tk.Label(root, text='Enter the Max value for grade A minus: ')
        label19.config(font=('helvetica', 12))
        canvas1.create_window(450, 50, window=label19)

        entry19 = tk.Entry(root) 
        canvas1.create_window(650, 50, window=entry19)

        label18 = tk.Label(root, text='Enter the Max value for grade B: ')
        label18.config(font=('helvetica', 12))
        canvas1.create_window(450, 80, window=label18)

        entry18 = tk.Entry(root) 
        canvas1.create_window(650, 80, window=entry18)

        label17 = tk.Label(root, text='Enter the Max value for grade B minus: ')
        label17.config(font=('helvetica', 12))
        canvas1.create_window(450, 110, window=label17)

        entry17 = tk.Entry(root) 
        canvas1.create_window(650, 110, window=entry17)

        label16 = tk.Label(root, text='Enter the Max value for grade C: ')
        label16.config(font=('helvetica', 12))
        canvas1.create_window(450, 140, window=label16)

        entry16 = tk.Entry(root) 
        canvas1.create_window(650, 140, window=entry16)

        label15 = tk.Label(root, text='Enter the Max value for grade C minus: ')
        label15.config(font=('helvetica', 12))
        canvas1.create_window(450, 170, window=label15)

        entry15 = tk.Entry(root) 
        canvas1.create_window(650, 170, window=entry15)

        label14 = tk.Label(root, text='Enter the Max value for grade D: ')
        label14.config(font=('helvetica', 12))
        canvas1.create_window(450, 200, window=label14)

        entry14 = tk.Entry(root) 
        canvas1.create_window(650, 200, window=entry14)

        label13 = tk.Label(root, text='Enter the Max value for grade D minus: ')
        label13.config(font=('helvetica', 12))
        canvas1.create_window(450, 230, window=label13)

        entry13 = tk.Entry(root) 
        canvas1.create_window(650, 230, window=entry13)

        label12 = tk.Label(root, text='Enter the Max value for grade E: ')
        label12.config(font=('helvetica', 12))
        canvas1.create_window(450, 260, window=label12)

        entry12 = tk.Entry(root) 
        canvas1.create_window(650, 260, window=entry12)

        label11 = tk.Label(root, text='Enter the Max value for grade F: ')
        label11.config(font=('helvetica', 12))
        canvas1.create_window(450, 290, window=label11)

        entry11 = tk.Entry(root) 
        canvas1.create_window(650, 290, window=entry11)

        calculate = tk.Button(text="Calculate", command=lambda: getGrades(df,entry11,entry12,entry13,entry14,entry15,entry16,entry17,entry18,entry19,entry20), bg='green', fg='white', font=('helvetica', 10, 'bold'))
        canvas1.create_window(530, 320, window=calculate)

    elif(calculation_type == '3'):
        data2 = df[['Total150', 'Total150']]
        fcm = FCM(n_clusters=10)
        fcm.fit(data2)
        fcm_centers = fcm.centers
        predicted_membership = fcm.predict(data2)
        df['EXPECTED GRADES'] = predicted_membership
        fcm_centers.columns = ["Total150","feature"]
        fcm_centers["Cluster_id"] = [0,1,2,3,4,5,6,7,8,9]
        fcm_centers = fcm_centers.sort_values(by="Total150",ascending=[0])
        fcm_centers["Grade"] = ["A","A-","B","B-","C","C-","D","D-","E","F"]
        grade_dict = dict(zip(fcm_centers.Cluster_id, fcm_centers.Grade))
        df = df.replace({'EXPECTED GRADES': grade_dict})
        df.to_excel('output.xlsx')
        displayExcel(df)

    elif(calculation_type == '4'):
        pass

    else:
        print("Wrong Choice entered.")



text = tk.Text(width=800)
text.pack()

canvas1 = tk.Canvas(root, width = 800, height = 600,  relief = 'raised')
canvas1.pack()


label1 = tk.Label(root, text='Grade Allocation')
label1.config(font=('helvetica', 20))
canvas1.create_window(100, 10, window=label1)

label3 = tk.Label(root, text='Choose 1 for default allocation.')
label3.config(font=('helvetica', 12))
canvas1.create_window(100, 100, window=label3)

label4 = tk.Label(root, text='Choose 2 for providing manual grade max number.')
label4.config(font=('helvetica', 12))
canvas1.create_window(100, 130, window=label4)

label5 = tk.Label(root, text='Choose 3 for fuzzy allocation')
label5.config(font=('helvetica', 12))
canvas1.create_window(100, 160, window=label5)

label6 = tk.Label(root, text='Choose 4 for manual change.')
label6.config(font=('helvetica', 12))
canvas1.create_window(100, 190, window=label6)

label2 = tk.Label(root, text='Please Enter Your choice')
label2.config(font=('helvetica', 12))
canvas1.create_window(100, 220, window=label2)

entry1 = tk.Entry (root) 
canvas1.create_window(100, 250, window=entry1)

    
browseButtonExcel = tk.Button(text=" Import Excel File ", command=getExcel, bg='green', fg='white', font=('helvetica', 10, 'bold'))
canvas1.create_window(100, 50, window=browseButtonExcel)
    

processButton = tk.Button(text=' Allocate The Grade ', command=allocateGrade, bg='brown', fg='white', font=('helvetica', 10, 'bold'))
canvas1.create_window(100, 280, window=processButton)


root.mainloop()