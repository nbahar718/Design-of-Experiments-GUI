import pandas as pd
import tkinter as tk
from tkinter import *
import os
from openpyxl import load_workbook
from scipy.stats.distributions import norm
from doepy import build, read_write


#############################################################################
######################## DOEPy PARAMETERS ###################################
#############################################################################

# Defining a dictionary of factor values
data_dict = {'Pressure':[40,55,70],
             'Temperature':[290, 320, 350],
             'Flow rate':[0.2,0.4],
             'Time':[5,8],
            'pH':[3,3.5,4]}


class DOEApp:
    def __init__(self, master):
        canvas = tk.Canvas(master, height=600, width=600, bg="#263D42")
        canvas.pack()
        frame = tk.Frame(master, bg='white')
        frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
        self.label = tk.Label(frame, text = "Choose the DOE Method")
        self.label.pack(anchor='w')

        global openCSVFile
        global openExcelFile
        openCSVFile = tk.Button(frame, text="Open CSV File", padx=10, pady=5, fg="white", bg="#263D42",
                                command=self.open_csv_file)
        openCSVFile.pack()
        openExcelFile = tk.Button(frame, text="Open Excel File", padx=10, pady=5, fg="white",
                                bg="#263D42", command=self.open_excel_file)
        openExcelFile.pack()
        openExcelFile['state']='disabled'

        tk.Checkbutton(frame, text = "Full Factorial",bg='white',
                   command = self.full_factorial).pack(anchor='w')

        tk.Checkbutton(frame, text = "2-Level Fractional Factorial",bg='white',
                   command = self.two_level_fractional_factorial).pack(anchor='w')

        tk.Checkbutton(frame, text = "Plackett-Burman",bg='white',
                   command = self.plackett_burman).pack(anchor='w')

        tk.Checkbutton(frame, text = "Sukharev Grid",bg='white',
                   command = self.sukharev_grid).pack(anchor='w')

        tk.Checkbutton(frame, text = "Box-Behnken",bg='white',
                   command = self.box_behnken).pack(anchor='w')

        tk.Checkbutton(frame, text = "Box-Wilson Center-Faced",bg='white',
                   command = self.box_wilson_center_faced).pack(anchor='w')

        tk.Checkbutton(frame, text = "Box-Wilson Center-Inscribed",bg='white',
                   command = self.box_wilson_center_inscribed).pack(anchor='w')

        tk.Checkbutton(frame, text = "Box-Wilson Center-Circumscribed",bg='white',
                   command = self.box_wilson_center_circumscribed).pack(anchor='w')

        tk.Checkbutton(frame, text = "Latin Hypercube Simple",bg='white',
                   command = self.latin_hypercube_simple).pack(anchor='w')

        tk.Checkbutton(frame, text = "Space Filling Latin Hypercube",bg='white',
                   command = self.latin_hypercube_space_filling).pack(anchor='w')

        tk.Checkbutton(frame, text = "Random k-means Cluster",bg='white',
                   command = self.random_k_means_cluster).pack(anchor='w')

        tk.Checkbutton(frame, text = "Maximin Reconstruction",bg='white',
                   command = self.maximin_reconstruction).pack(anchor='w')

        tk.Checkbutton(frame, text = "Halton Sequence Based",bg='white',
                   command = self.halton_sequence_based).pack(anchor='w')

        tk.Checkbutton(frame, text = "Uniform Random Matrix",bg='white',
                   command = self.uniform_random_matrix).pack(anchor='w')

        tk.Button(frame, text="Confirm DOE Methods and Open Output File", padx=10, pady=5, fg="white", bg="#263D42", command = self.confirm).pack()


    def open_csv_file(self):
        csvfilepath = filedialog.askopenfilename(title="Choose Source CSV File",
                                                filetypes=(("Comma-separated values (CSV) files","*.csv"),("All files", "*.*")))
        global data_dict
        data_dict=read_write.read_variables_csv(csvfilepath)

        openExcelFile['state']='active'


    def open_excel_file(self):
        global excelfilepath
        excelfilepath = filedialog.askopenfilename(title="Choose Target Excel File",
                                filetypes=(("Excel files","*.xlsx"),("All files", "*.*")))
        global writer
        writer = pd.ExcelWriter(excelfilepath, engine = 'xlsxwriter')

    def full_factorial(self):
        ####### DOEPy full-factorial ################################################
        DOEPya = round(build.full_fact(data_dict),2)
        dfDOEPya = pd.DataFrame(DOEPya)
        dfDOEPya.to_excel(writer, sheet_name="Full Factorial")


    def two_level_fractional_factorial(self):
        ####### DOEPy 2-Level fractional-factorial ###################################
        DOEPyb = round(build.frac_fact_res(data_dict),2)
        dfDOEPyb = pd.DataFrame(DOEPyb)
        dfDOEPyb.to_excel(writer, sheet_name="2-L Frac Fact")


    def plackett_burman(self):
        ####### DOEPy Plackett-Burman ##################################################
        DOEPyc = round(build.plackett_burman(data_dict),2)
        dfDOEPyc = pd.DataFrame(DOEPyc)
        dfDOEPyc.to_excel(writer, sheet_name="Plackett-Burman")


    def sukharev_grid(self):
        ####### DOEPy Sukharev Grid ####################################################
        sample_no = int(input("Enter number of samples: "))
        DOEPyd = round(build.sukharev(data_dict,num_samples = sample_no),2)
        dfDOEPyd = pd.DataFrame(DOEPyd)
        dfDOEPyd.to_excel(writer, sheet_name="Sukharev Grid")


    def box_behnken(self):
        ####### DOEPy Box-Behnken ######################################################
        DOEPye = round(build.box_behnken(data_dict),2)
        dfDOEPye = pd.DataFrame(DOEPye)
        dfDOEPye.to_excel(writer, sheet_name="Box-Behnken")


    def box_wilson_center_faced(self):
        ####### DOEPy Box-Wilson Center-Faced ###########################################
        DOEPyf1 = round(build.central_composite(data_dict,face='ccf'),2)
        dfDOEPyf1 = pd.DataFrame(DOEPyf1)
        dfDOEPyf1.to_excel(writer, sheet_name="Box-Wilson Center-Faced")


    def box_wilson_center_inscribed(self):
        ####### DOEPy Box-Wilson Center-Inscribed ######################################
        DOEPyf2 = round(build.central_composite(data_dict,face='cci'),2)
        dfDOEPyf2 = pd.DataFrame(DOEPyf2)
        dfDOEPyf2.to_excel(writer, sheet_name="Box-Wilson Center-Inscribed")


    def box_wilson_center_circumscribed(self):
        ####### DOEPy Box-Wilson Center-Circumscribed ##################################
        DOEPyf3 = round(build.central_composite(data_dict,face='ccc'),2)
        dfDOEPyf3 = pd.DataFrame(DOEPyf3)
        dfDOEPyf3.to_excel(writer, sheet_name="Box-Wilson Center-Circumscribed")


    def latin_hypercube_simple(self):
        ####### DOEPy Latin Hypercube Simple ############################################
        DOEPyg1 = round(build.lhs(data_dict,num_samples = 12),2)
        dfDOEPyg1 = pd.DataFrame(DOEPyg1)
        dfDOEPyg1.to_excel(writer, sheet_name="Latin Hypercube (LH) simple")


    def latin_hypercube_space_filling(self):
        ####### DOEPy Space-Filling Latin Hypercube #####################################
        DOEPyg2 = round(build.space_filling_lhs(data_dict,num_samples = 12),2)
        dfDOEPyg2 = pd.DataFrame(DOEPyg2)
        dfDOEPyg2.to_excel(writer, sheet_name="Space Filling LH")


    def random_k_means_cluster(self):
        ####### DOEPy Random k-means cluster ############################################
        DOEPyh = round(build.random_k_means(data_dict,num_samples = 12),2)
        dfDOEPyh = pd.DataFrame(DOEPyh)
        dfDOEPyh.to_excel(writer, sheet_name="Random k-means Cluster")


    def maximin_reconstruction(self):
        ####### DOEPy Maximin reconstruction ############################################
        DOEPyi = round(build.maximin(data_dict,num_samples = 12),2)
        dfDOEPyi = pd.DataFrame(DOEPyi)
        dfDOEPyi.to_excel(writer, sheet_name="Maximin Reconstruction")


    def halton_sequence_based(self):
        ####### DOEPy Halton sequence based ############################################
        DOEPyj = round(build.halton(data_dict,num_samples = 12),2)
        dfDOEPyj = pd.DataFrame(DOEPyj)
        dfDOEPyj.to_excel(writer, sheet_name="Halton Sequence Based")


    def uniform_random_matrix(self):
        ####### DOEPy Uniform random matrix ############################################
        DOEPyk = round(build.uniform_random(data_dict,num_samples = 12),2)
        dfDOEPyk = pd.DataFrame(DOEPyk)
        dfDOEPyk.to_excel(writer, sheet_name="Uniform Random Matrix")


    def confirm(self):
        writer.save()
        writer.close()
        os.startfile(excelfilepath)


def main():
    root = Tk()
    app = DOEApp(root)
    root.mainloop()


if __name__ == "__main__": main()
