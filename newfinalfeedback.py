from fpdf import FPDF
import pandas as pd
import os
import tkinter as tk
from tkinter import Label
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from io import BytesIO


def generate_clicked():
  link = entry.get()
  fileLink = link
  
  HODname = entryHOD.get()
  Dept = entryDept.get()

  fb = pd.read_excel(fileLink)
  replacement_dict = {"Excellent": 4, "Good": 3,"Average":2,"Below Average":1}
  fb = fb.replace(replacement_dict)

  no_of_students = fb.shape[0]

  fb.rename(columns = {'Practical Batch':'Batch'}, inplace = True)
  cols = len(fb.axes[1])

  Number_of_sub = 0
  Number_of_prac = 0
  for i in range(cols):
      column_name = fb.columns[i]
      column_name = column_name[0:3]
      if column_name == 'Sub' :
          Number_of_sub += 1
      elif column_name == 'Pra':
          Number_of_prac += 1
      else:
          i += 1

  subject = ['subject1', 'subject2', 'subject3','subject4','subject5','subject6', 'subject7', 'subject8','subject9','subject10']
  practical = ['practical1', 'practical2', 'practical3','practical4','practical5','practical6', 'practical7', 'practical8','practical9','practical10']
  
  subject_data = ['subject_data1', 'subject_data2', 'subject_data3','subject_data4','subject_data5','subject_data6', 'subject_data7', 'subject_data8','subject_data9','subject_data10']
  practical_data_final_ = ['practical_data_final_1', 'practical_data_final_2', 'practical_data_final_3','practical_data_final_4','practical_data_final_5','practical_data_final_6', 'practical_data_final_7', 'practical_data_final_8','practical_data_final_9','practical_data_final_10']

  sub_no=0
  prac_no=0

  for i in range(cols):
    column_name = fb.columns[i]
    column_name = column_name[0:3]
    if column_name == 'Sub' :
        subject[sub_no]=fb.iloc[:,i:i+19]
        sub_no += 1
    elif column_name == 'Pra':
        practical[prac_no]=fb.iloc[:,i:i+6]
        prac_no += 1
    else:
        i += 1

  for i in range ( Number_of_sub ):
    subject[i].columns=['Subject','Teacher','Progressive coverage of the syllabus','Understanding of lecture delivered','Knowledge of the subject','Preparation for the class','Ability to hold your interest','Voice and gestures','Interaction by the way of questions','Language clarity and explanation','Use of Reference Books & PowerPoint /Multimedia / Animations etc',
    'Clarity in board writing','Class control',
    'Regularity in conducting classes','Remarks or discussions on tests, assignments',
    'Home assignments / class tests are relevant & adequate','Overall impression',
    'Ability to motivate students',
    'Availability for help and consultations']

  for i in range ( Number_of_prac ):
    practical[i].columns=['Practical Subject','Teacher','Availability in the Lab','Explanation of Theory','ProcedurePractical knowledge of the subject','Your understanding of experiment']

  z = 0

  for z in range(Number_of_sub):
    calculate = subject[z]
    subject_data[z]=pd.read_csv("./template.csv")

    subject_data[z]['Subject'] = subject_data[z]['Subject'].astype(str)
    subject_data[z]['Teacher'] = subject_data[z]['Teacher'].astype(str)

    counter = 2
    while counter < 19:
        name = calculate.columns[counter]
        no_of_4 = (calculate[name] == 4 ).sum()
        no_of_3 = (calculate[name] == 3 ).sum()
        no_of_2 = (calculate[name] == 2 ).sum()
        no_of_1 = (calculate[name] == 1 ).sum()

        subject_data[z].iloc[ counter-2 , 1 ] = calculate.iloc[0,0]
        subject_data[z].iloc[ counter-2 , 2 ] = calculate.iloc[0,1]
        subject_data[z].iloc[ counter-2 , 4 ] = no_of_4
        subject_data[z].iloc[ counter-2 , 5 ] = no_of_3
        subject_data[z].iloc[ counter-2 , 6 ] = no_of_2
        subject_data[z].iloc[ counter-2 , 7 ] = no_of_1
        counter += 1

  z = 0
  i = 0
  for z in range(Number_of_sub):
    calculate = subject_data[z]
    for i in range ( 17 ):
        out = (calculate.iloc[i,4]*4+calculate.iloc[i,5]*3+calculate.iloc[i,6]*2+calculate.iloc[i,7]*1)/(calculate.iloc[i,4]+calculate.iloc[i,5]+calculate.iloc[i,6]+calculate.iloc[i,7])
        calculate.iloc[i,8] = round(out,2)

 
  practical_data = ['practical_data1', 'practical_data2', 'practical_data3','practical_data4','practical_data5','practical_data6', 'practical_data7', 'practical_data8','practical_data9','practical_data10']
  i = 0 
  for i in range ( 10 ):
    practical_data[i] = practical[1].head(0)

  i=0
  final_prac_no=0
  for i in range ( prac_no ):
    c = practical[i].iloc[:,1].nunique()
    final_prac_no += c


  int = 0
  for j in range ( Number_of_prac ):
    m = practical[j].iloc[:,1].unique()
    l = practical[j].iloc[:,1].nunique()
    i=0
    for i in range (l):
        for b in range ( no_of_students ):
            if( practical[j].iloc[b,1] == m[i] ):
                practical_data[int] = practical_data[int]._append(practical[j].iloc[b])
        int+=1

  total_prac_feedbacks = int
  total_sub_feedbacks = Number_of_sub
  total_feedbacks = total_sub_feedbacks + total_prac_feedbacks

  practical_data_final_ = ['practical_data_final_1', 'practical_data_final_2', 'practical_data_final_3','practical_data_final_4','practical_data_final_5','practical_data_final_6', 'practical_data_final_7', 'practical_data_final_8','practical_data_final_9','practical_data_final_10']


  z = 0

  for z in range(total_prac_feedbacks):
    calculate = practical_data[z]
    practical_data_final_[z]=pd.read_csv("./template_practical.csv")

    practical_data_final_[z]['Practical'] = practical_data_final_[z]['Practical'].astype(str)
    practical_data_final_[z]['Teacher'] = practical_data_final_[z]['Teacher'].astype(str)

    counter = 2
    while counter < 6:
        name = calculate.columns[counter]
        no_of_4 = (calculate[name] == 4 ).sum()
        no_of_3 = (calculate[name] == 3 ).sum()
        no_of_2 = (calculate[name] == 2 ).sum()
        no_of_1 = (calculate[name] == 1 ).sum()
        practical_data_final_[z].iloc[ counter-2 , 1 ] = calculate.iloc[0,0]
        practical_data_final_[z].iloc[ counter-2 , 2 ] = calculate.iloc[0,1]
        practical_data_final_[z].iloc[ counter-2 , 4 ] = no_of_4
        practical_data_final_[z].iloc[ counter-2 , 5 ] = no_of_3
        practical_data_final_[z].iloc[ counter-2 , 6 ] = no_of_2
        practical_data_final_[z].iloc[ counter-2 , 7 ] = no_of_1
        counter += 1

  z = 0

  for z in range(total_prac_feedbacks):
    calculate = practical_data_final_[z]
    i = 0
    for i in range ( 4 ):
        out = (calculate.iloc[i,4]*4+calculate.iloc[i,5]*3+calculate.iloc[i,6]*2+calculate.iloc[i,7]*1)/(calculate.iloc[i,4]+calculate.iloc[i,5]+calculate.iloc[i,6]+calculate.iloc[i,7])
        calculate.iloc[i,8] = round(out,2)
         

  def generate_sub_feedback():
    # folder_path = os.path.join('C:/', 'SubjectFeedbacks')
    folder_path1 = os.path.join('C:/', 'SubjectFeedbacksPdf')
    # os.mkdir(folder_path)
    os.mkdir(folder_path1)
    i=0
    for i in range (total_sub_feedbacks):
        temp_feedback = subject_data[i]
        subject = temp_feedback.iloc[0,1] 
        teacher = temp_feedback.iloc[0,2]
        tempfeedback = pd.read_excel("./printable_template1.xlsx") #for final Grading
        tempgrading = pd.read_excel("./finalGrading1.xlsx")

        filename = subject +"-"+ teacher

        tempfeedback.iloc[0,1] = subject
        tempfeedback.iloc[1,1] = teacher

        ii = 1
        for ii in range(17):
            tempfeedback.iloc[ii+3,2] = temp_feedback.iloc[ii,4]
            tempfeedback.iloc[ii+3,3] = temp_feedback.iloc[ii,5]
            tempfeedback.iloc[ii+3,4] = temp_feedback.iloc[ii,6]
            tempfeedback.iloc[ii+3,5] = temp_feedback.iloc[ii,7]
            tempfeedback.iloc[ii+3,6] = temp_feedback.iloc[ii,8]

        Subject_Knowledge = round((temp_feedback.loc[0, 'Average grading']+temp_feedback.loc[1,'Average grading']+temp_feedback.loc[2,'Average grading']+temp_feedback.loc[3,'Average grading'])/4,2)
        Communication_Presentation_Skills = round((temp_feedback.loc[4, 'Average grading']+temp_feedback.loc[5,'Average grading']+temp_feedback.loc[4,'Average grading']+temp_feedback.loc[7,'Average grading'])/4,2)
        Use_of_Teaching_Aids = round((temp_feedback.loc[5, 'Average grading']+temp_feedback.loc[9,'Average grading'])/2,2)
        Class_Room_Discipline = round((temp_feedback.loc[10, 'Average grading']+temp_feedback.loc[11,'Average grading'])/2,2)
        Evaluation = round((temp_feedback.loc[12, 'Average grading']+temp_feedback.loc[13,'Average grading'])/2,2)
        Behavior = round((temp_feedback.loc[14, 'Average grading']+temp_feedback.loc[15,'Average grading']+temp_feedback.loc[14,'Average grading'])/3,2)

        Overall_Grading = round((Subject_Knowledge + Communication_Presentation_Skills + Use_of_Teaching_Aids + Class_Room_Discipline + Evaluation + Behavior)/6,2)

        tempgrading.loc[0, 'Average Grading'] = Subject_Knowledge
        tempgrading.loc[1, 'Average Grading'] = Communication_Presentation_Skills
        tempgrading.loc[2, 'Average Grading'] = Use_of_Teaching_Aids
        tempgrading.loc[3, 'Average Grading'] = Class_Room_Discipline
        tempgrading.loc[4, 'Average Grading'] = Evaluation
        tempgrading.loc[5, 'Average Grading'] = Behavior
        tempgrading.loc[4, 'Average Grading'] = Overall_Grading

        
        tempgrading['Remark'] = tempgrading['Remark'].astype(str)

        l=0
        for l in range (7):
            if (tempgrading.loc[l, 'Average Grading']>=3.5):
                tempgrading.loc[l, 'Remark'] = 'Excellent'
            elif (tempgrading.loc[l, 'Average Grading']>=3):
                tempgrading.loc[l, 'Remark'] = 'Good'
            elif (tempgrading.loc[l, 'Average Grading']>=2.5):
                tempgrading.loc[l, 'Remark'] = 'Average'
            else :
                tempgrading.loc[l, 'Remark'] = 'Below Average'

        # output_file_path = f'C:/SubjectFeedbacks/{filename}.xlsx'
        # with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
            # tempfeedback.to_excel(writer, sheet_name='Sheet1', index=False, header=False)
            # tempgrading.to_excel(writer, sheet_name='Sheet2', index=False)

            class PDFWithHTML(FPDF):

                def header(self):
                    pdf.set_font("Helvetica", style='I', size=7)
                    pdf.cell(210, 6, text="Sinhgad Technical Education Soceity's", border=0, align='C', fill=False)
                    pdf.ln()
                    pdf.set_font("Helvetica", style='B', size=15)
                    pdf.cell(210, 6, text="Sinhgad College of Engineering, Pune", border=0, align='C', fill=False)
                    pdf.ln()
                    pdf.set_font("Helvetica", style='', size=10)
                    pdf.cell(210, 6, text="DEPARTMENT OF "+Dept, border=0, align='C', fill=False)
                    pdf.ln()

                def add_colored_cell(self, width, text, border=1, fill_color=None, text_color=(0, 0, 0)):
                    self.set_fill_color(*fill_color) if fill_color else self.set_fill_color(254, 254, 255)
                    self.set_text_color(*text_color)
                    self.cell(width, 4, text, border=border, fill=True,align='C')    

                def add_colored_cell2(self, width, text, border=1, fill_color=None, text_color=(0, 0, 0)):
                    self.set_fill_color(*fill_color) if fill_color else self.set_fill_color(200, 254, 255)
                    self.set_text_color(*text_color)
                    self.cell(width, 4, text, border=border, fill=True,align='C')

                def footer(self):
                    pdf.set_font("Helvetica", style='B', size=8)
                    # pdf.cell(210, 6, text="Sinhgad Technical Education Soceity's", border=0, align='L', fill=False)
                    pdf.cell(15, 8, text=teacher, border=0, align='L', fill=False)
                    pdf.cell(150, 8, text=HODname, border=0, align='R', fill=False)
                    pdf.ln()
                    pdf.cell(15, 8, text="Assistant Professor  ", border=0, align='L', fill=False)
                    pdf.cell(150, 8, text="Head of Department", border=0, align='R', fill=False)

             # Create instance of FPDF class with landscape A4 size
            pdf = PDFWithHTML(orientation='P', unit='mm', format='A4')
    
            # Add a page
            pdf.add_page()
    
            # Set font
            # pdf.set_font("Helvetica", size=6)
    
            # Set column widths (in percentage of total width)
            column_widths = [7, 70, 23, 23, 23, 23, 23]
            column_widths2 = [169, 23]

            # pdf.cell(width, height=0, txt='', border=0, ln=0, align='', fill=False, link='')

            pdf.set_font("Helvetica", style='', size=6)
            pdf.cell(15, 3, text="Subject - ", border=0, align='', fill=False)
            pdf.cell(60, 3, text=subject, border=0, align='', fill=False)
            pdf.ln()

            pdf.cell(15, 6, text="Teacher - ", border=0, align='', fill=False)
            pdf.cell(60, 6, text=teacher, border=0, align='', fill=False)
            pdf.ln()
            pdf.ln()

            # Headers
            pdf.set_font("Helvetica", style='B', size=6)
            pdf.add_colored_cell(column_widths[0], "Sr.", fill_color=(242, 73, 132))
            pdf.add_colored_cell(column_widths[1], "Parameters", fill_color=(242, 73, 132))
            pdf.add_colored_cell(column_widths[2], "Excellent (N1)", fill_color=(242, 73, 132))
            pdf.add_colored_cell(column_widths[3], "Good (N2)", fill_color=(242, 73, 132))
            pdf.add_colored_cell(column_widths[4], "Average (N3)", fill_color=(242, 73, 132))
            pdf.add_colored_cell(column_widths[5], "Below Average (N4)", fill_color=(242, 73, 132))
            pdf.add_colored_cell(column_widths[6], "Average grading", fill_color=(242, 73, 132))
            pdf.ln()

            # Your table content using manual cell creation
            pdf.set_font("Helvetica", size=6)
            # Example row:
            pdf.cell(column_widths[0], 4, "1",align='C',border=1)
            pdf.cell(column_widths[1], 4, " Progressive coverage of the syllabus",border=1)
            pdf.cell(column_widths[2], 4, str(round(temp_feedback.iloc[0,4])),align='C',border=1)
            pdf.cell(column_widths[3], 4, str(round(temp_feedback.iloc[0,5])),align='C',border=1)
            pdf.cell(column_widths[4], 4, str(round(temp_feedback.iloc[0,6])),align='C',border=1)
            pdf.cell(column_widths[5], 4, str(round(temp_feedback.iloc[0,7])),align='C',border=1)
            pdf.cell(column_widths[6], 4, str(temp_feedback.iloc[0,8]),align='C',border=1)
            pdf.ln()


            pdf.cell(column_widths[0], 4, "2",align='C',border=1)
            pdf.cell(column_widths[1], 4, " Understanding of lecture delivered",border=1)
            pdf.cell(column_widths[2], 4, str(round(temp_feedback.iloc[1,4])),align='C',border=1)
            pdf.cell(column_widths[3], 4, str(round(temp_feedback.iloc[1,5])),align='C',border=1)
            pdf.cell(column_widths[4], 4, str(round(temp_feedback.iloc[1,6])),align='C',border=1)
            pdf.cell(column_widths[5], 4, str(round(temp_feedback.iloc[1,7])),align='C',border=1)
            pdf.cell(column_widths[6], 4, str(temp_feedback.iloc[1,8]),align='C',border=1)
            pdf.ln()


            pdf.cell(column_widths[0], 4, "3",align='C',border=1)
            pdf.cell(column_widths[1], 4, " Knowledge of the subject",border=1)
            pdf.cell(column_widths[2], 4, str(round(temp_feedback.iloc[2,4])),align='C',border=1)
            pdf.cell(column_widths[3], 4, str(round(temp_feedback.iloc[2,5])),align='C',border=1)
            pdf.cell(column_widths[4], 4, str(round(temp_feedback.iloc[2,6])),align='C',border=1)
            pdf.cell(column_widths[5], 4, str(round(temp_feedback.iloc[2,7])),align='C',border=1)
            pdf.cell(column_widths[6], 4, str(temp_feedback.iloc[2,8]),align='C',border=1)
            pdf.ln()


            pdf.cell(column_widths[0], 4, "4",align='C',border=1)
            pdf.cell(column_widths[1], 4, " Preparation for the class",border=1)
            pdf.cell(column_widths[2], 4, str(round(temp_feedback.iloc[3,4])),align='C',border=1)
            pdf.cell(column_widths[3], 4, str(round(temp_feedback.iloc[3,5])),align='C',border=1)
            pdf.cell(column_widths[4], 4, str(round(temp_feedback.iloc[3,6])),align='C',border=1)
            pdf.cell(column_widths[5], 4, str(round(temp_feedback.iloc[3,7])),align='C',border=1)
            pdf.cell(column_widths[6], 4, str(temp_feedback.iloc[3,8]),align='C',border=1)
            pdf.ln()


            pdf.add_colored_cell2(column_widths2[0], "Subject Knowledge Average: [(1) + (2) + (3) + (4)]/4", fill_color=(120, 230, 245))
            pdf.add_colored_cell2(column_widths2[1], str(Subject_Knowledge), fill_color=(120, 230, 245))
            pdf.ln()

            pdf.cell(column_widths[0], 4, "5",align='C',border=1)
            pdf.cell(column_widths[1], 4, " Ability to hold your interest",border=1)
            pdf.cell(column_widths[2], 4, str(round(temp_feedback.iloc[4,4])),align='C',border=1)
            pdf.cell(column_widths[3], 4, str(round(temp_feedback.iloc[4,5])),align='C',border=1)
            pdf.cell(column_widths[4], 4, str(round(temp_feedback.iloc[4,6])),align='C',border=1)
            pdf.cell(column_widths[5], 4, str(round(temp_feedback.iloc[4,7])),align='C',border=1)
            pdf.cell(column_widths[6], 4, str(temp_feedback.iloc[4,8]),align='C',border=1)
            pdf.ln()


            pdf.cell(column_widths[0], 4, "6",align='C',border=1)
            pdf.cell(column_widths[1], 4, " Voice and gestures",border=1)
            pdf.cell(column_widths[2], 4, str(round(temp_feedback.iloc[5,4])),align='C',border=1)
            pdf.cell(column_widths[3], 4, str(round(temp_feedback.iloc[5,5])),align='C',border=1)
            pdf.cell(column_widths[4], 4, str(round(temp_feedback.iloc[5,6])),align='C',border=1)
            pdf.cell(column_widths[5], 4, str(round(temp_feedback.iloc[5,7])),align='C',border=1)
            pdf.cell(column_widths[6], 4, str(temp_feedback.iloc[5,8]),align='C',border=1)
            pdf.ln()


            pdf.cell(column_widths[0], 4, "7",align='C',border=1)
            pdf.cell(column_widths[1], 4, " Interaction by the way of questions",border=1)
            pdf.cell(column_widths[2], 4, str(round(temp_feedback.iloc[4,4])),align='C',border=1)
            pdf.cell(column_widths[3], 4, str(round(temp_feedback.iloc[4,5])),align='C',border=1)
            pdf.cell(column_widths[4], 4, str(round(temp_feedback.iloc[4,6])),align='C',border=1)
            pdf.cell(column_widths[5], 4, str(round(temp_feedback.iloc[4,7])),align='C',border=1)
            pdf.cell(column_widths[6], 4, str(temp_feedback.iloc[4,8]),align='C',border=1)
            pdf.ln()


            pdf.cell(column_widths[0], 4, "8",align='C',border=1)
            pdf.cell(column_widths[1], 4, " Language clarity and explanation",border=1)
            pdf.cell(column_widths[2], 4, str(round(temp_feedback.iloc[7,4])),align='C',border=1)
            pdf.cell(column_widths[3], 4, str(round(temp_feedback.iloc[7,5])),align='C',border=1)
            pdf.cell(column_widths[4], 4, str(round(temp_feedback.iloc[7,6])),align='C',border=1)
            pdf.cell(column_widths[5], 4, str(round(temp_feedback.iloc[7,7])),align='C',border=1)
            pdf.cell(column_widths[6], 4, str(temp_feedback.iloc[7,8]),align='C',border=1)
            pdf.ln()


            pdf.add_colored_cell2(column_widths2[0], "Communication/Presentation Skills: [(5) + (6) + (7) + (8)]/4", fill_color=(120, 230, 245))
            pdf.add_colored_cell2(column_widths2[1], str(Communication_Presentation_Skills), fill_color=(120, 230, 245))
            pdf.ln()


            pdf.cell(column_widths[0], 4, "9",align='C',border=1)
            pdf.cell(column_widths[1], 4, " Use of Reference Books & PowerPoint /Multimedia / Animations etc.",border=1)
            pdf.cell(column_widths[2], 4, str(round(temp_feedback.iloc[5,4])),align='C',border=1)
            pdf.cell(column_widths[3], 4, str(round(temp_feedback.iloc[5,5])),align='C',border=1)
            pdf.cell(column_widths[4], 4, str(round(temp_feedback.iloc[5,6])),align='C',border=1)
            pdf.cell(column_widths[5], 4, str(round(temp_feedback.iloc[5,7])),align='C',border=1)
            pdf.cell(column_widths[6], 4, str(temp_feedback.iloc[5,8]),align='C',border=1)
            pdf.ln()


            pdf.cell(column_widths[0], 4, "10",align='C',border=1)
            pdf.cell(column_widths[1], 4, " Clarity in board writing",border=1)
            pdf.cell(column_widths[2], 4, str(round(temp_feedback.iloc[9,4])),align='C',border=1)
            pdf.cell(column_widths[3], 4, str(round(temp_feedback.iloc[9,5])),align='C',border=1)
            pdf.cell(column_widths[4], 4, str(round(temp_feedback.iloc[9,6])),align='C',border=1)
            pdf.cell(column_widths[5], 4, str(round(temp_feedback.iloc[9,7])),align='C',border=1)
            pdf.cell(column_widths[6], 4, str(temp_feedback.iloc[9,8]),align='C',border=1)
            pdf.ln()


            pdf.add_colored_cell2(column_widths2[0], "Use of Teaching Aids: [(9) + (10)]/2", fill_color=(120, 230, 245))
            pdf.add_colored_cell2(column_widths2[1], str(Use_of_Teaching_Aids), fill_color=(120, 230, 245))
            pdf.ln()


            pdf.cell(column_widths[0], 4, "11",align='C',border=1)
            pdf.cell(column_widths[1], 4, " Class control",border=1)
            pdf.cell(column_widths[2], 4, str(round(temp_feedback.iloc[10,4])),align='C',border=1)
            pdf.cell(column_widths[3], 4, str(round(temp_feedback.iloc[10,5])),align='C',border=1)
            pdf.cell(column_widths[4], 4, str(round(temp_feedback.iloc[10,6])),align='C',border=1)
            pdf.cell(column_widths[5], 4, str(round(temp_feedback.iloc[10,7])),align='C',border=1)
            pdf.cell(column_widths[6], 4, str(temp_feedback.iloc[10,8]),align='C',border=1)
            pdf.ln()


            pdf.cell(column_widths[0], 4, "12",align='C',border=1)
            pdf.cell(column_widths[1], 4, " Regularity in conducting classes",border=1)
            pdf.cell(column_widths[2], 4, str(round(temp_feedback.iloc[11,4])),align='C',border=1)
            pdf.cell(column_widths[3], 4, str(round(temp_feedback.iloc[11,5])),align='C',border=1)
            pdf.cell(column_widths[4], 4, str(round(temp_feedback.iloc[11,6])),align='C',border=1)
            pdf.cell(column_widths[5], 4, str(round(temp_feedback.iloc[11,7])),align='C',border=1)
            pdf.cell(column_widths[6], 4, str(temp_feedback.iloc[11,8]),align='C',border=1)
            pdf.ln()


            pdf.add_colored_cell2(column_widths2[0], "Class Room Discipline: [(11) + (12)]/2", fill_color=(120, 230, 245))
            pdf.add_colored_cell2(column_widths2[1], str(Class_Room_Discipline), fill_color=(120, 230, 245))
            pdf.ln()


            pdf.cell(column_widths[0], 4, "13",align='C',border=1)
            pdf.cell(column_widths[1], 4, " Remarks or discussions on tests, assignments",border=1)
            pdf.cell(column_widths[2], 4, str(round(temp_feedback.iloc[12,4])),align='C',border=1)
            pdf.cell(column_widths[3], 4, str(round(temp_feedback.iloc[12,5])),align='C',border=1)
            pdf.cell(column_widths[4], 4, str(round(temp_feedback.iloc[12,6])),align='C',border=1)
            pdf.cell(column_widths[5], 4, str(round(temp_feedback.iloc[12,7])),align='C',border=1)
            pdf.cell(column_widths[6], 4, str(temp_feedback.iloc[12,8]),align='C',border=1)
            pdf.ln()


            pdf.cell(column_widths[0], 4, "14",align='C',border=1)
            pdf.cell(column_widths[1], 4, " Home assignments / class tests are relevant & adequate",border=1)
            pdf.cell(column_widths[2], 4, str(round(temp_feedback.iloc[13,4])),align='C',border=1)
            pdf.cell(column_widths[3], 4, str(round(temp_feedback.iloc[13,5])),align='C',border=1)
            pdf.cell(column_widths[4], 4, str(round(temp_feedback.iloc[13,6])),align='C',border=1)
            pdf.cell(column_widths[5], 4, str(round(temp_feedback.iloc[13,7])),align='C',border=1)
            pdf.cell(column_widths[6], 4, str(temp_feedback.iloc[13,8]),align='C',border=1)
            pdf.ln()


            pdf.add_colored_cell2(column_widths2[0], "Evaluation: [(13) + (14)]/2", fill_color=(120, 230, 245))
            pdf.add_colored_cell2(column_widths2[1], str(Evaluation), fill_color=(120, 230, 245))
            pdf.ln()


            pdf.cell(column_widths[0], 4, "15",align='C',border=1)
            pdf.cell(column_widths[1], 4, " Overall impression",border=1)
            pdf.cell(column_widths[2], 4, str(round(temp_feedback.iloc[14,4])),align='C',border=1)
            pdf.cell(column_widths[3], 4, str(round(temp_feedback.iloc[14,5])),align='C',border=1)
            pdf.cell(column_widths[4], 4, str(round(temp_feedback.iloc[14,6])),align='C',border=1)
            pdf.cell(column_widths[5], 4, str(round(temp_feedback.iloc[14,7])),align='C',border=1)
            pdf.cell(column_widths[6], 4, str(temp_feedback.iloc[14,8]),align='C',border=1)
            pdf.ln()


            pdf.cell(column_widths[0], 4, "16",align='C',border=1)
            pdf.cell(column_widths[1], 4, " Ability to motivate students",border=1)
            pdf.cell(column_widths[2], 4, str(round(temp_feedback.iloc[15,4])),align='C',border=1)
            pdf.cell(column_widths[3], 4, str(round(temp_feedback.iloc[15,5])),align='C',border=1)
            pdf.cell(column_widths[4], 4, str(round(temp_feedback.iloc[15,6])),align='C',border=1)
            pdf.cell(column_widths[5], 4, str(round(temp_feedback.iloc[15,7])),align='C',border=1)
            pdf.cell(column_widths[6], 4, str(temp_feedback.iloc[15,8]),align='C',border=1)
            pdf.ln()


            pdf.cell(column_widths[0], 4, "17",align='C',border=1)
            pdf.cell(column_widths[1], 4, " Availability for help and consultations",border=1)
            pdf.cell(column_widths[2], 4, str(round(temp_feedback.iloc[14,4])),align='C',border=1)
            pdf.cell(column_widths[3], 4, str(round(temp_feedback.iloc[14,5])),align='C',border=1)
            pdf.cell(column_widths[4], 4, str(round(temp_feedback.iloc[14,6])),align='C',border=1)
            pdf.cell(column_widths[5], 4, str(round(temp_feedback.iloc[14,7])),align='C',border=1)
            pdf.cell(column_widths[6], 4, str(temp_feedback.iloc[14,8]),align='C',border=1)
            pdf.ln()


            pdf.add_colored_cell2(column_widths2[0], "Behavior: [(15) + (16) + (17)]/3", fill_color=(120, 230, 245))
            pdf.add_colored_cell2(column_widths2[1], str(Behavior), fill_color=(120, 230, 245))
            pdf.ln()

            # pdf.add_colored_cell2(column_widths2[0], "Overall Average", fill_color=(120, 230, 245))
            # pdf.add_colored_cell2(column_widths2[1], str(Overall_Grading), fill_color=(120, 230, 245))
            # pdf.ln()


            pdf.set_font("Helvetica", style='', size=5)
            pdf.cell(300, 4, text="Points Assigned: Excellent:4 , Good:3 , Average 2, Below Average: 1", border=0, align='L', fill=False)
            pdf.ln()
            pdf.cell(300,4, text="Average Grading= (4 x N1 + 3 x N2 + 2x N3 + 1x N4)/(N1+N2+N3+N4)", border=0, align='L', fill=False)
            pdf.ln()
            pdf.ln()
            pdf.ln()

            column_widths = [10.5, 70, 35, 35]
            column_widths2 = [80.5, 35,35]

            # pdf.set_font("Helvetica", style='', size=6)
            # pdf.cell(15, 4, text="Subject - ", border=0, align='', fill=False)
            # pdf.cell(60, 4, text=subject, border=0, align='', fill=False)
            # pdf.ln()

            # pdf.cell(15, 4, text="Teacher - ", border=0, align='', fill=False)
            # pdf.cell(60, 4, text=teacher, border=0, align='', fill=False)
            # pdf.ln()

            #Headings
            pdf.set_font("Helvetica", style='B', size=6)
            # pdf.cell(column_widths[4], 5, "",align='C',border=0)
            pdf.add_colored_cell(column_widths[0], "Sr.", fill_color=(242, 73, 132))
            pdf.add_colored_cell(column_widths[1], "Parameters", fill_color=(242, 73, 132))
            pdf.add_colored_cell(column_widths[2], "Average Grading", fill_color=(242, 73, 132))
            pdf.add_colored_cell(column_widths[3], "Remark", fill_color=(242, 73, 132))
            pdf.ln()


            pdf.set_font("Helvetica", style='', size=6)
            # pdf.cell(column_widths[4], 5, "",align='C',border=0)
            pdf.cell(column_widths[0], 5, "1",align='C',border=1)
            pdf.cell(column_widths[1], 5, " Subject Knowledge",border=1)
            pdf.cell(column_widths[2], 5, str(Subject_Knowledge),align='C',border=1)
            if (Subject_Knowledge >=3.5):
                R = "Excellent"
            elif (Subject_Knowledge >=3):
                R = "Good"
            elif (Subject_Knowledge >=2.5):
                R = "Average"
            else :
                R = "Below Average"
            pdf.cell(column_widths[3], 5, str(R),align='C',border=1)
            pdf.ln()
            

            # pdf.cell(column_widths[4], 5, "",align='C',border=0)
            pdf.cell(column_widths[0], 5, "2",align='C',border=1)
            pdf.cell(column_widths[1], 5, " Communication/Presentation Skills",border=1)
            pdf.cell(column_widths[2], 5, str(Communication_Presentation_Skills),align='C',border=1)
            if (Communication_Presentation_Skills >=3.5):
                R = "Excellent"
            elif (Communication_Presentation_Skills >=3):
                R = "Good"
            elif (Communication_Presentation_Skills >=2.5):
                R = "Average"
            else :
                R = "Below Average"
            pdf.cell(column_widths[3], 5, str(R),align='C',border=1)
            pdf.ln()


            # pdf.cell(column_widths[4], 5, "",align='C',border=0)
            pdf.cell(column_widths[0], 5, "3",align='C',border=1)
            pdf.cell(column_widths[1], 5, " Use of Teaching Aids",border=1)
            pdf.cell(column_widths[2], 5, str(Use_of_Teaching_Aids),align='C',border=1)
            if (Use_of_Teaching_Aids >=3.5):
                R = "Excellent"
            elif (Use_of_Teaching_Aids >=3):
                R = "Good"
            elif (Use_of_Teaching_Aids >=2.5):
                R = "Average"
            else :
                R = "Below Average"
            pdf.cell(column_widths[3], 5, str(R),align='C',border=1)
            pdf.ln()


            # pdf.cell(column_widths[4], 5, "",align='C',border=0)
            pdf.cell(column_widths[0], 5, "4",align='C',border=1)
            pdf.cell(column_widths[1], 5, " Class Room Discipline",border=1)
            pdf.cell(column_widths[2], 5, str(Class_Room_Discipline),align='C',border=1)
            if (Class_Room_Discipline >=3.5):
                R = "Excellent"
            elif (Class_Room_Discipline >=3):
                R = "Good"
            elif (Class_Room_Discipline >=2.5):
                R = "Average"
            else :
                R = "Below Average"
            pdf.cell(column_widths[3], 5, str(R),align='C',border=1)
            pdf.ln()


            # pdf.cell(column_widths[4], 5, "",align='C',border=0)
            pdf.cell(column_widths[0], 5, "5",align='C',border=1)
            pdf.cell(column_widths[1], 5, " Evaluation",border=1)
            pdf.cell(column_widths[2], 5, str(Evaluation),align='C',border=1)
            if (Evaluation >=3.5):
                R = "Excellent"
            elif (Evaluation >=3):
                R = "Good"
            elif (Evaluation >=2.5):
                R = "Average"
            else :
                R = "Below Average"
            pdf.cell(column_widths[3], 5, str(R),align='C',border=1)
            pdf.ln()


            # pdf.cell(column_widths[4], 5, "",align='C',border=0)
            pdf.cell(column_widths[0], 5, "6",align='C',border=1)
            pdf.cell(column_widths[1], 5, " Behavior",border=1)
            pdf.cell(column_widths[2], 5, str(Behavior),align='C',border=1)
            if (Behavior >=3.5):
                R = "Excellent"
            elif (Behavior >=3):
                R = "Good"
            elif (Behavior >=2.5):
                R = "Average"
            else :
                R = "Below Average"
            pdf.cell(column_widths[3], 5, str(R),align='C',border=1)
            pdf.ln()


            # pdf.cell(column_widths[4], 5, "",align='C',border=0)
            pdf.set_font("Helvetica", style='B', size=6)
            pdf.add_colored_cell2(column_widths2[0], "Overall Grading = Sum / 6", fill_color=(120, 230, 245))
            pdf.add_colored_cell2(column_widths2[1], str(Overall_Grading), fill_color=(120, 230, 245))
            if (Overall_Grading >=3.5):
                R = "Excellent"
            elif (Overall_Grading >=3):
                R = "Good"
            elif (Overall_Grading >=2.5):
                R = "Average"
            else :
                R = "Below Average"
            pdf.add_colored_cell2(column_widths2[2], str(R), fill_color=(120, 230, 245))
            pdf.ln()


            # pdf.set_font("Helvetica", style='', size=5)
            pdf.set_font("Helvetica", style='', size=5)
            
            pdf.cell(300, 4, text="Remarks : Excellent>=3.5 , Good>=3 , Average>=2.5, Below Average<2.5", border=0, align='L', fill=False)
            pdf.ln()
            pdf.ln()
            pdf.ln()
            pdf.ln()
            pdf.ln()
            pdf.ln()
            pdf.ln()
            pdf.ln()


            # Save the pdf with name .pdf
            pdf.output(f"C:/SubjectFeedbacksPdf/{filename}.pdf")

  generate_sub_feedback()


  def generate_pract_feedback():
    # folder_path = os.path.join('C:/', 'PracticalFeedbacks')
    folder_path1 = os.path.join('C:/', 'PracticalFeedbackspdf')
    # os.mkdir(folder_path)
    os.mkdir(folder_path1)
    i = 0
    for i in range ( total_prac_feedbacks ):

        temp_feedback = practical_data_final_[i]

        practical = temp_feedback.iloc[0,1]
        teacher = temp_feedback.iloc[0,2]

        tempfeedback_prac = pd.read_excel("./practicalGradingTemplate.xlsx") #for final Grading

        filename = practical +"-"+ teacher

        tempfeedback_prac.iloc[0,1] = practical
        tempfeedback_prac.iloc[1,1] = teacher

        Overall_Grading = round(sum(temp_feedback['Average grading'])/4,2)           
                        
        iii = 1
        for iii in range(4):
            tempfeedback_prac.iloc[iii+3,2] = temp_feedback.iloc[iii,4]
            tempfeedback_prac.iloc[iii+3,3] = temp_feedback.iloc[iii,5]
            tempfeedback_prac.iloc[iii+3,4] = temp_feedback.iloc[iii,6]
            tempfeedback_prac.iloc[iii+3,5] = temp_feedback.iloc[iii,7]
            tempfeedback_prac.iloc[iii+3,6] = temp_feedback.iloc[iii,8]

        l=1
        for l in range (4):
            if (temp_feedback.loc[l,'Average grading'] >=3.5):
                tempfeedback_prac.iloc[l+3,7] = "Excellent"
            elif (temp_feedback.loc[l,'Average grading'] >=3):
                tempfeedback_prac.iloc[l+3,7] = "Good"
            elif (temp_feedback.loc[l,'Average grading'] >=2.5):
                tempfeedback_prac.iloc[l+3,7] = "Average"
            else :
                tempfeedback_prac.iloc[l+3,7] = "Below Average"

        # output_file_path = f'C:/PracticalFeedbacks/{filename}.xlsx'

        # tempfeedback_prac.to_excel(output_file_path, index=False, header=False)

    
        class PDFWithHTML(FPDF):

            def header(self):
                pdf.set_font("Helvetica", style='I', size=8)
                pdf.cell(210, 6, text="Sinhgad Technical Education Soceity's", border=0, align='C', fill=False)
                pdf.ln()
                pdf.set_font("Helvetica", style='B', size=15)
                pdf.cell(210, 6, text="Sinhgad College of Engineering, Pune", border=0, align='C', fill=False)
                pdf.ln()
                pdf.set_font("Helvetica", style='', size=10)
                pdf.cell(210, 8, text="DEPARTMENT OF "+Dept, border=0, align='C', fill=False)
                pdf.ln()
                pdf.ln()
                pdf.ln()

            def add_colored_cell(self, width, text, border=1, fill_color=None, text_color=(0, 0, 0)):
                self.set_fill_color(*fill_color) if fill_color else self.set_fill_color(2510, 2510, 255)
                self.set_text_color(*text_color)
                self.cell(width, 10, text, border=border, fill=True,align='C')    

            def add_colored_cell2(self, width, text, border=1, fill_color=None, text_color=(0, 0, 0)):
                self.set_fill_color(*fill_color) if fill_color else self.set_fill_color(200, 2510, 255)
                self.set_text_color(*text_color)
                self.cell(width, 10, text, border=border, fill=True,align='C')

            def footer(self):
                pdf.set_font("Helvetica", style='', size=5)
                pdf.cell(210, 5, text="Points Assigned: Excellent:4 , Good:3 , Average 2, Below Average: 1", border=0, align='L', fill=False)
                pdf.ln()
                pdf.cell(210, 5, text="Remarks : Excellent>=3.5 , Good>=3 , Average>=2.5, Below Average<2.5", border=0, align='L', fill=False)
                pdf.ln()
                pdf.ln()
                pdf.ln()
                pdf.ln()
                pdf.ln()
                pdf.set_font("Helvetica", style='B', size=8)
                # pdf.cell(210, 6, text="Sinhgad Technical Education Soceity's", border=0, align='L', fill=False)
                pdf.cell(15, 8, text=teacher, border=0, align='L', fill=False)
                pdf.cell(150, 8, text=HODname, border=0, align='R', fill=False)
                pdf.ln()
                pdf.cell(15, 8, text="Assistant Professor  ", border=0, align='L', fill=False)
                pdf.cell(150, 8, text="Head of Department", border=0, align='R', fill=False)
                
    
        pdf = PDFWithHTML(orientation='p', unit='mm', format='A4')
        pdf.add_page()

        column_widths = [10, 53, 21, 21, 21, 21, 21, 21]
        column_widths2 = [147, 21, 21]
        # column_widths = [10, 100, 33, 33, 33, 33, 33]
        # column_widths2 = [242, 33]  

        pdf.set_font("Helvetica", style='', size=7)
        pdf.cell(15, 4, text="Practical - ", border=0, align='', fill=False)
        pdf.cell(60, 4, text=practical, border=0, align='', fill=False)
        pdf.ln()

        pdf.cell(15, 4, text="Teacher - ", border=0, align='', fill=False)
        pdf.cell(60, 4, text=teacher, border=0, align='', fill=False)
        pdf.ln()
        pdf.ln()
        pdf.ln()


        pdf.set_font("Helvetica", style='B', size=6)
        pdf.add_colored_cell(column_widths[0], "Sr.", fill_color=(242, 73, 132))
        pdf.add_colored_cell(column_widths[1], "Parameters", fill_color=(242, 73, 132))
        pdf.add_colored_cell(column_widths[2], "Excellent (N1)", fill_color=(242, 73, 132))
        pdf.add_colored_cell(column_widths[3], "Good (N2)", fill_color=(242, 73, 132))
        pdf.add_colored_cell(column_widths[4], "Average (N3)", fill_color=(242, 73, 132))
        pdf.add_colored_cell(column_widths[5], "Below Average (N4)", fill_color=(242, 73, 132))
        pdf.add_colored_cell(column_widths[6], "Average grading", fill_color=(242, 73, 132))
        pdf.add_colored_cell(column_widths[7], "Remark", fill_color=(242, 73, 132))
        pdf.ln()


        pdf.set_font("Helvetica", size=7)

        pdf.cell(column_widths[0], 10, "1",align='C',border=1)
        pdf.cell(column_widths[1], 10, " Availability in the Lab",border=1)
        pdf.cell(column_widths[2], 10, str(round(temp_feedback.iloc[0,4])),align='C',border=1)
        pdf.cell(column_widths[3], 10, str(round(temp_feedback.iloc[0,5])),align='C',border=1)
        pdf.cell(column_widths[4], 10, str(round(temp_feedback.iloc[0,6])),align='C',border=1)
        pdf.cell(column_widths[5], 10, str(round(temp_feedback.iloc[0,7])),align='C',border=1)
        pdf.cell(column_widths[6], 10, str(temp_feedback.iloc[0,8]),align='C',border=1)
        if (temp_feedback.iloc[0,8] >=3.5):
            R = "Excellent"
        elif (temp_feedback.iloc[0,8] >=3):
            R = "Good"
        elif (temp_feedback.iloc[0,8] >=2.5):
            R = "Average"
        else :
            R = "Below Average"
        pdf.cell(column_widths[7], 10, str(R),align='C',border=1)
        
        pdf.ln()


        pdf.cell(column_widths[0], 10, "2",align='C',border=1)
        pdf.cell(column_widths[1], 10, "Explanation of Theory, Procedure",border=1)
        pdf.cell(column_widths[2], 10, str(round(temp_feedback.iloc[1,4])),align='C',border=1)
        pdf.cell(column_widths[3], 10, str(round(temp_feedback.iloc[1,5])),align='C',border=1)
        pdf.cell(column_widths[4], 10, str(round(temp_feedback.iloc[1,6])),align='C',border=1)
        pdf.cell(column_widths[5], 10, str(round(temp_feedback.iloc[1,7])),align='C',border=1)
        pdf.cell(column_widths[6], 10, str(temp_feedback.iloc[1,8]),align='C',border=1)
        # pdf.cell(column_widths[7], 10, str(temp_feedback.iloc[0,9]),align='C',border=1)
        if (temp_feedback.iloc[1,8] >=3.5):
            R = "Excellent"
        elif (temp_feedback.iloc[1,8] >=3):
            R = "Good"
        elif (temp_feedback.iloc[1,8] >=2.5):
            R = "Average"
        else :
            R = "Below Average"
        pdf.cell(column_widths[7], 10, str(R),align='C',border=1)
        pdf.ln()


        pdf.cell(column_widths[0], 10, "3",align='C',border=1)
        pdf.cell(column_widths[1], 10, " Practical knowledge of the subject",border=1)
        pdf.cell(column_widths[2], 10, str(round(temp_feedback.iloc[2,4])),align='C',border=1)
        pdf.cell(column_widths[3], 10, str(round(temp_feedback.iloc[2,5])),align='C',border=1)
        pdf.cell(column_widths[4], 10, str(round(temp_feedback.iloc[2,6])),align='C',border=1)
        pdf.cell(column_widths[5], 10, str(round(temp_feedback.iloc[2,7])),align='C',border=1)
        pdf.cell(column_widths[6], 10, str(temp_feedback.iloc[2,8]),align='C',border=1)
        # pdf.cell(column_widths[7], 10, str(temp_feedback.iloc[0,9]),align='C',border=1)
        if (temp_feedback.iloc[2,8] >=3.5):
            R = "Excellent"
        elif (temp_feedback.iloc[2,8] >=3):
            R = "Good"
        elif (temp_feedback.iloc[2,8] >=2.5):
            R = "Average"
        else :
            R = "Below Average"
        pdf.cell(column_widths[7], 10, str(R),align='C',border=1)
        pdf.ln()


        pdf.cell(column_widths[0], 10, "4",align='C',border=1)
        pdf.cell(column_widths[1], 10, "Your understanding of experiment",border=1)
        pdf.cell(column_widths[2], 10, str(round(temp_feedback.iloc[3,4])),align='C',border=1)
        pdf.cell(column_widths[3], 10, str(round(temp_feedback.iloc[3,5])),align='C',border=1)
        pdf.cell(column_widths[4], 10, str(round(temp_feedback.iloc[3,6])),align='C',border=1)
        pdf.cell(column_widths[5], 10, str(round(temp_feedback.iloc[3,7])),align='C',border=1)
        pdf.cell(column_widths[6], 10, str(temp_feedback.iloc[3,8]),align='C',border=1)
        # pdf.cell(column_widths[7], 10, str(temp_feedback.iloc[0,9]),align='C',border=1)
        if (temp_feedback.iloc[3,8] >=3.5):
            R = "Excellent"
        elif (temp_feedback.iloc[3,8] >=3):
            R = "Good"
        elif (temp_feedback.iloc[3,8] >=2.5):
            R = "Average"
        else :
            R = "Below Average"
        pdf.cell(column_widths[7], 10, str(R),align='C',border=1)
        pdf.ln()


        pdf.add_colored_cell2(column_widths2[0], "Overall Grading ", fill_color=(120, 230, 245))
        pdf.add_colored_cell2(column_widths2[1], str(Overall_Grading), fill_color=(120, 230, 245))
        if (Overall_Grading >=3.5):
            R = "Excellent"
        elif (Overall_Grading >=3):
            R = "Good"
        elif (Overall_Grading >=2.5):
            R = "Average"
        else :
            R = "Below Average"
        pdf.add_colored_cell2(column_widths2[2], str(R), fill_color=(120, 230, 245))
        # pdf.cell(column_widths[7], 10, str(R),align='C',border=1)
        pdf.ln()
        pdf.ln()

        pdf.output(f"C:/PracticalFeedbackspdf/{filename}.pdf")

  generate_pract_feedback()
  
  teachers = set() #set of teachers name
  iii=0
  for iii in range (total_sub_feedbacks):
      teachers.add(subject_data[iii].iloc[0,2])
  iii=0
  for iii in range (total_prac_feedbacks):
      teachers.add(practical_data_final_[iii].iloc[0,2])
    
  subjects = set() #set of subjects and practicals name
  iii=0
  for iii in range (total_sub_feedbacks):
      subjects.add(subject_data[iii].iloc[0,1])
  iii=0
  for iii in range (total_prac_feedbacks):
      subjects.add(practical_data_final_[iii].iloc[0,1])

  new_window_staff = tk.Toplevel()
  new_window_staff.title("Teachers & Subjects")
  
  body_label_Teachers = Label(new_window_staff, text="Teachers", font=("Arial", 13, "bold"))
  body_label_Teachers.pack(pady=(4,2))
  for t in teachers:
        label = tk.Label(new_window_staff, text=t, font=("Arial", 8))
        label.pack()

  body_label_Students = Label(new_window_staff, text="Subjects", font=("Arial", 13, "bold"))
  body_label_Students.pack(pady=(4,2))
  for s in subjects:
        label = tk.Label(new_window_staff, text=s, font=("Arial", 8))
        label.pack()

  def start_clicked():
    teacher=entry2.get()
    subject=entry3.get()
    i = 0
    for i in range ( total_sub_feedbacks ):
      temp_feedback = subject_data[i]
      if( temp_feedback.iloc[0,1] == subject and temp_feedback.iloc[0,2] == teacher ):
        #   print("Subject and Teacher Found")

          
          temp_feedback.iloc[:,3] = ["Syllabus Coverage","Understanding of lecture ","Subject Knowledge","Preparation for Class","Ability to hold interest","Voice & Gestures","Interaction by questions","Language Clearity","Use of References","Board Writting","Class Controll","Regular classes","Discussions on tests","Home Assignment","Overall Impression","Ability to Motivate","Availability for help"] 

        #   window_width = 800
        #   window_height = 600

          new_window1 = tk.Toplevel()
          new_window1.title("Feedback Plot")

          padding_frame = tk.Frame(new_window1)
          padding_frame.pack(padx=25, pady=30)
          
          fig, ax = plt.subplots(figsize=(20, 15))
          sns.barplot(data=temp_feedback, y="Parameters", x="Average grading", ax=ax)
          ax.set_xlim(0, 4)
    
        #   new_window1.geometry(f"{window_width}x{window_height}")  

          canvas = FigureCanvasTkAgg(fig, master=padding_frame)  
          canvas.draw()
          canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    new_window1 = tk.Toplevel()
    new_window1.title("Feedback Plot")
    body_labelWrongInputs = Label(new_window1, text="Wrong Inputs", font=("Arial", 15, "bold"))
    body_labelWrongInputs1 = Label(new_window1, text="Give correct inputs for Visualization", font=("Arial", 10, "italic"))
    body_labelWrongInputs.pack()
    body_labelWrongInputs1.pack()

  def start1_clicked():
    teacher=entry12.get()
    subject=entry13.get()
    i = 0
    for i in range ( total_prac_feedbacks ):
      temp_feedback = practical_data_final_[i]
      if( temp_feedback.iloc[0,1] == subject and temp_feedback.iloc[0,2] == teacher ):
        #   print("Subject and Teacher Found")

        #   new_window = tk.Toplevel()
        #   new_window.title("Feedback Plot")
          
        #   window_width = 800
        #   window_height = 600

          temp_feedback.iloc[:,3] = ["Availability in Lab","Practical Explanation","Practical knowledge","Understanding of experiment"] 
          new_window = tk.Toplevel()
          new_window.title("Feedback Plot")


          new_window.resizable(True, True)  # True for both width and height


          padding_frame = tk.Frame(new_window)
          padding_frame.pack(padx=25, pady=30)

          fig, ax = plt.subplots(figsize=(20, 15))
          sns.barplot(data=temp_feedback, y="Parameters", x="Average grading", ax=ax)
          ax.set_xlim(0, 4)
            
          canvas = FigureCanvasTkAgg(fig, master=padding_frame)  
          canvas.draw()
          canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)          
    new_window1 = tk.Toplevel()
    new_window1.title("Feedback Plot")
    body_labelWrongInputs = Label(new_window1, text="Wrong Inputs", font=("Arial", 15, "bold"))
    body_labelWrongInputs1 = Label(new_window1, text="Give correct inputs for Visualization", font=("Arial", 10, "italic"))
    body_labelWrongInputs.pack()
    body_labelWrongInputs1.pack()  
   
  def credit_clicked():
    new_window3 = tk.Toplevel()
    new_window3.title("Credits")
    heading_label_credit = Label(new_window3, text="Devloped by BE project group 2023-24", font=("Arial", 20, "bold"))
    heading_label_credit.pack(pady=(8, 12))
    heading_label_credit1 = Label(new_window3, text="Group number 29", font=("Arial", 12, "bold"))
    heading_label_credit1.pack(pady=(5, 5))
    heading_label_credit_teachers = Label(new_window3, text="Teachers", font=("Arial", 12, "bold"))
    credit_guid = Label(new_window3, text="Project Guid - Mrs. A. D. Tawlare", font=("Arial", 8))
    credit_reviewer1 = Label(new_window3, text="Project Reviewer 1 - Mrs. T. H. Patil", font=("Arial", 8))
    credit_reviewer2 = Label(new_window3, text="Project Reviewer 2 - Mr. A. G. Rao", font=("Arial", 8))
    heading_label_credit_students = Label(new_window3, text="Students", font=("Arial", 12, "bold"))
    credit_Student1 = Label(new_window3, text="Vaibhav Jagadale", font=("Arial", 8))
    credit_Student2 = Label(new_window3, text="Aditi Kalel", font=("Arial", 8))
    credit_Student3 = Label(new_window3, text="Anushka Kute", font=("Arial", 8))
    credit_Student4 = Label(new_window3, text="Arti Gunjal", font=("Arial", 8))
    heading_label_credit_teachers.pack(pady=(3,5))
    credit_guid.pack()
    credit_reviewer1.pack()
    credit_reviewer2.pack()
    heading_label_credit_students.pack(pady=(3,5))
    credit_Student1.pack()
    credit_Student2.pack()
    credit_Student3.pack()
    credit_Student4.pack()

  body_label1 = Label(root, text="Feedback generated")
  body_label2 = Label(root, text="Check your C drive")
  body_label1.pack()
  body_label2.pack()

  body_label11 = Label(root, text="Subject Feedback Visualization", font=("Arial", 15, "bold"))
  body_label11.pack()
  body_label10 = Label(root, text="Enter Subject name ", font=("Arial", 12))
  body_label10.pack()
  entry3 = tk.Entry(root, width=50)
  entry3.pack(padx=10, pady=10)
  body_label9 = Label(root, text="Enter Subject Teacher's name ", font=("Arial", 12))
  body_label9.pack()
  entry2 = tk.Entry(root, width=50)
  entry2.pack(padx=10, pady=10)
  start_button = tk.Button(root, text="Start", command=start_clicked)
  start_button.pack(pady=(5,10))


  body_label111 = Label(root, text="Practical Feedback Visualization", font=("Arial", 15, "bold"))
  body_label111.pack()
  body_label110 = Label(root, text="Enter Practical Subject name ", font=("Arial", 12))
  body_label110.pack()
  entry13 = tk.Entry(root, width=50)
  entry13.pack(padx=10, pady=10)
  body_label19 = Label(root, text="Enter Lab Teacher's name ", font=("Arial", 12))
  body_label19.pack()
  entry12 = tk.Entry(root, width=50)
  entry12.pack(padx=10, pady=10)
  start1_button = tk.Button(root, text="Start", command=start1_clicked)
  start1_button.pack(pady=(5,10))
  credit_button = tk.Button(root, text="Credits", command=credit_clicked)
  credit_button.pack(side='right')


# Create the main window
root = tk.Tk()
root.title("Feedback Generator")

# Create the entry widget for the link

# Heading
heading_label = Label(root, text="Feedback Generator", font=("Arial", 25, "bold"))
heading_label.pack(pady=(15, 20))

body_labelDept = Label(root, text="Department Name (BLOCK LETTERS)", font=("Arial", 10, "italic"))
body_labelDept.pack()
entryDept = tk.Entry(root, width=50)
entryDept.pack(padx=10, pady=5)

body_labelHOD = Label(root, text="Write Name of the HOD", font=("Arial", 10, "italic"))
body_labelHOD.pack()
entryHOD = tk.Entry(root, width=50)
entryHOD.pack(padx=10, pady=5)

# Body text
body_label = Label(root, text="Past your link below", font=("Arial", 10, "italic"))
body_label.pack()
entry = tk.Entry(root, width=150)
entry.pack(padx=10, pady=10)

# Create the generate button
generate_button = tk.Button(root, text="Generate", command=generate_clicked)
generate_button.pack(pady=(10,20))


# Run the main loop
root.mainloop()