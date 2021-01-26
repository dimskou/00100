import time
import tkinter as tk
from itertools import combinations
from tkinter import *

import networkx


#Συνάρτηση για Φόρτωση και επίλυση του προβλήματος
def readSTU(event):
	# Ορισμός Μεταβλητών
	maxLesson = 0
	commonSet = set()
	filename=event
	print (event)

	# Έναρξη υπολογισμού χρόνου εκτέλεσης συνάρτησης
	start = time.time()

	# sleeping for 1 sec to get 10 sec runtime
	time.sleep(1)

	# Άνοιγμα και Ανάγωνση του αρχείου
	file = open(filename, 'r')
	Lines = file.readlines()

	# Για κάθε γραμμή του αρχείου ορίζεται και ένας μαθητής
	for line in Lines:
		line = line.strip()

		# Διαχωριζμός των γραμμών και άρα και των μαθητών
		grammh = line.split(" ")

		# μετατροπή απο string σε int
		for i in range(0, len(grammh)):
			if isinstance(grammh[i], str) and grammh[i]!= '':
				grammh[i] = int(grammh[i])
				if grammh[i] > maxLesson:
					maxLesson = grammh[i]

		# αναζήτηση των πιθανών συνδιασμών
		comb = combinations(grammh, 2)

		for c in list(comb):
			commonSet.add(c)


	# Υπολογισμός της πυκνότητας  (υπολογίζεται διαιρώντας τον αριθμό των στοιχείων του πίνακα συγκρούσεων που
	# έχουν την τιμή 1 με το συνολικό πλήθος των στοιχείων του πίνακα)
	# Υπολογισμός όλων των θέσεων του πίνακα
	maxArray = maxLesson * maxLesson
	# Υπολογισμός πυκνότητας
	density = (len(commonSet) * 2) / maxArray

	# Δημιουργία Γραφήματος με την χρήση της βιβλιοθήκης  networkx
	graph = networkx.Graph()

	# Πρόσθεση των μαθημάτων στο γράφημα
	for i in range(maxLesson):
		graph.add_node(i + 1)

	# Πρόσθεση των συγκρούσεων στο γράφημα
	for common in commonSet:
		graph.add_edge(common[0], common[1])

	# Graph Coloring με την τεχνική smallest last
	graphColored = networkx.coloring.greedy_color(graph, strategy="smallest_last")

	# Αποθήκευση των αποτελεσμάτων και εξαγωγή σε αρχεία sol

	f = open(filename[:-4] +".sol", "w")
	for exam in graphColored:
		f.write(str(exam) + "\t" + str(graphColored[exam]) + "\n")
	f.close()

	final_str = 'Τα  μαθήματα είναι: %s \nΗ πυκνότητα είναι: %s ' % (maxLesson, density)
	label['text'] = final_str

	# end time
	end = time.time()

	# total time taken
	print(f"Runtime of the program is {end - start}")

#Δημιουργία GUI μενού για το πρόγραμμα

root = Tk()
root.title('Χρονοπρογραμματισμός εξετάσεων Πανεπιστημίου')
root.geometry("600x600")

mylabel1=Label(root, text="1. Φόρτωση Προβλήματος επιλογή:")
mylabel1.grid(row=0,column=1,padx=10,pady=10,sticky = W)
mylabel2=Label(root, text="2. Φόρτωση Λύσης")
mylabel2.grid(row=1,column=1,padx=10,pady=10,sticky = W)
mylabel3=Label(root, text="3. Επίλυση Προβλήματος")
mylabel3.grid(row=2,column=1,padx=10,pady=10,sticky = W)
mylabel4=Label(root, text="4. Μαζική επίλυση Προβλήματος")
mylabel4.grid(row=3,column=1,padx=10,pady=10,sticky = W)

def button_load_prob():
	f_name= clicked.get()
	readSTU(f_name)

#def button_loadall(options):
#	for option in options:
#		readSTU(option)

# Drop Down Box

options = [
	"car-f-92.stu",
	"car-s-91.stu",
	"ear-f-83.stu",
	"hec-s-92.stu",
	"kfu-s-93.stu",
	"lse-f-91.stu",
	"pur-s-93.stu",
	"rye-s-93.stu",
	"sta-f-83.stu",
	"toy_e5_s6.stu",
	"tre-s-92.stu",
	"uta-s-92.stu",
	"ute-s-92.stu",
	"ute-s-92.stu",
	"yor-f-83.stu"
]

clicked = StringVar()
clicked.set(options[0])

drop = OptionMenu(root, clicked, *options)
drop.grid(row=0,column=2,padx=10,pady=10)

Button_load= Button(root, text='Φόρτωσε το πρόβλημα', command= button_load_prob)
Button_load.grid(row=0,column=3,padx=10,pady=10)


#Go_button= Button(root, text='Διάβασε Όλα τα αρχεία', command=lambda: button_click(options))
#Go_button.pack()

frame=LabelFrame(root,text="Αποτέλεσμα Φόρτωσης λύσης",padx=2,pady=2,bg='#80c1ff', bd=5)
frame.place(relx=0.8,rely=0.5,relwidth=0.7,relheight=0.2, anchor='ne')

label = tk.Label(frame, font=('Courier',10), anchor='w', justify='left', bd=4)
label.place(relwidth=1, relheight=0.7)

root.mainloop()
