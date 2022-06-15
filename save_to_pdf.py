from fpdf import FPDF, HTMLMixin
import PyPDF2 
from os import path
import csv

from numpy import append

def check_for_duplicated_date(config_file, date):
    str_date = [str(date)]
    if path.exists('config.csv'):
        with open(config_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row == str_date:
                    return False
            return True
    else:
        return True

def csv_write(date, brain_dump_box, priorities_table, timeboxtable):
    str_date = [str(date)]
    if path.exists('config.csv'):
        with open('config.csv', 'a+', newline='') as f:
            writer = csv.writer(f)
            if check_for_duplicated_date('config.csv', date):
                writer.writerow(str_date)
            
    else:
        with open('config.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(str_date)
    

def load_temp_csv(date, brain_dump_box, priorities_table, timeboxtable):
    str_date = [str(date)]
    
    if path.exists('temp.csv'):
        row_count = 0
        with open('temp.csv', 'r') as file:
            row_count = sum(1 for row in file)  
        
        with open('temp.csv', 'r') as file:
            reader = csv.reader(file)
            row = next(reader)  
            if row == str_date:
                if row_count > 1:
                    row = next(reader)
                    brain_dump_box.text = str(row[0])

                    row = next(reader)
                    for i in range(0, len(priorities_table)):
                        priorities_table[i].text = row[i]

                    row = next(reader)
                    for i in range(0, len(timeboxtable)):
                        timeboxtable[i].text = row[i]
                    
    else:
        with open('temp.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(str_date)

def save_temp_csv(date, brain_dump_box, priorities_table, timeboxtable):
    str_date = [str(date)]
    
    prority_string = []
    for x in priorities_table:
            prority_string.append(x.text)
               
    timeboxtable_string = []
    for x in timeboxtable:
            timeboxtable_string.append(x.text)
    
    with open('temp.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(str_date)
        writer.writerow([brain_dump_box.text])
        writer.writerow(prority_string)
        writer.writerow(timeboxtable_string)


def new_page(date, brain_dump_box, priorities_table, timeboxtable, name_of_pdf):
    pdf = FPDF()
    pdf.add_page()

    # Date
    pdf.set_font("Arial", 'B', size = 15)
    pdf.cell(200, 5, txt = str(date) + "        ", ln = 1, align = 'R')
    # pdf.cell(txt = str(date), ln = 1, align = 'R')

    # Title
    pdf.set_font("Arial", 'B', size = 20)
    pdf.cell(200, 10, txt = "The Time Box", ln = 1, align = 'C')

    # Top Priorities
    cnt = 1
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(100, 10, txt = "Top Priorities: ", ln = 2, align = 'L')
    pdf.set_font('Arial', "B", 12)
    for x in priorities_table:
            pdf.cell(200, 6, txt = "    " + str(cnt) + ". " + x.text, ln = 2, align = 'L')
            cnt += 1
    
    # Time Box Table      
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(100, 10, txt = "Time Box Table: ", ln = 2, align = 'L')

    pdf.set_font('Arial', "B", 10)
    len_of_table = int(len(timeboxtable)/2)
    cnt = 0
    line_height = pdf.font_size * 2.5

    # :00 and :30
    pdf.multi_cell(pdf.epw / 16, line_height, "  ", new_x="RIGHT", new_y="TOP", align='C', max_line_height=pdf.font_size)
    pdf.multi_cell(pdf.epw / 2.5, line_height, ":00", border='B', new_x="RIGHT", new_y="TOP", align='C', max_line_height=pdf.font_size)
    pdf.multi_cell(pdf.epw / 2.5, line_height, ":30", border='B', new_x="RIGHT", new_y="TOP", align='C', max_line_height=pdf.font_size)
    pdf.ln(line_height)

    
    # Table
    for x in range(0, len_of_table):
        pdf.multi_cell(pdf.epw / 16, line_height, str(x + 7), border='R', new_x="RIGHT", new_y="TOP", align='C', max_line_height=pdf.font_size)

        if timeboxtable[cnt].text == timeboxtable[cnt+1].text and timeboxtable[cnt].text != "":
            pdf.set_fill_color(194, 199, 123)
            pdf.multi_cell(4*pdf.epw / 5, line_height, timeboxtable[cnt].text, border='B,R', new_x="RIGHT", new_y="TOP", align='C', max_line_height=pdf.font_size, fill=True)
        else:
            pdf.set_fill_color(112, 158, 96)
            if timeboxtable[cnt].text != "":
                pdf.multi_cell(pdf.epw / 2.5, line_height, timeboxtable[cnt].text, border='B', new_x="RIGHT", new_y="TOP", align='C', max_line_height=pdf.font_size, fill=True)
            else:
                pdf.multi_cell(pdf.epw / 2.5, line_height, timeboxtable[cnt].text, border='B', new_x="RIGHT", new_y="TOP", align='C', max_line_height=pdf.font_size)
            if timeboxtable[cnt+1].text != "":    
                pdf.multi_cell(pdf.epw / 2.5, line_height, timeboxtable[cnt+1].text, border=1, new_x="RIGHT", new_y="TOP", align='C', max_line_height=pdf.font_size, fill=True)
            else:
                pdf.multi_cell(pdf.epw / 2.5, line_height, timeboxtable[cnt+1].text, border=1, new_x="RIGHT", new_y="TOP", align='C', max_line_height=pdf.font_size)
        pdf.ln(line_height)
        cnt += 2

    # Brain Dump
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(100, 10, txt = "Brain Dump: ", ln = 2, align = 'L')
    pdf.set_font('Arial', "B", 12)
    pdf.multi_cell(4*pdf.epw / 5, line_height, brain_dump_box.text, new_x="RIGHT", new_y="TOP", align='C', max_line_height=pdf.font_size)
    pdf.ln(20)
    
    pdf.output(name_of_pdf)
    print("File save successfully!") 


def save_to_pdf(date, brain_dump_box, priorities_table, timeboxtable):
    name_of_pdf = str(date.isocalendar().year) + "_" + date.strftime("%B") + "_week:" + str(date.isocalendar().week) + ".pdf"
    print(name_of_pdf)

    if path.exists(name_of_pdf):

        if check_for_duplicated_date('config.csv', date) == False:
            pdf_file = open(name_of_pdf,'rb')
            read_file = PyPDF2.PdfFileReader(pdf_file)
            num_pages = read_file.numPages
            wrote_pdf = PyPDF2.PdfFileWriter()

            for pageNum in range(0,num_pages-1):
                pageObj = read_file.getPage(pageNum)
                wrote_pdf.addPage(pageObj)

            output_pdf = open(name_of_pdf,'wb')

            wrote_pdf.write(output_pdf)
            output_pdf.close()
            pdf_file.close()

        new_page(date, brain_dump_box, priorities_table, timeboxtable, "temp.pdf")
        mergeFile = PyPDF2.PdfFileMerger()
        mergeFile.append(PyPDF2.PdfFileReader(name_of_pdf, 'rb'))
        mergeFile.append(PyPDF2.PdfFileReader('temp.pdf', 'rb'))
        mergeFile.write(name_of_pdf)

    else:
        new_page(date, brain_dump_box, priorities_table, timeboxtable, name_of_pdf)

    csv_write(date, brain_dump_box, priorities_table, timeboxtable)

        


