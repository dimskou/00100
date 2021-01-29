import time
import tkinter as tk
from itertools import combinations
from tkinter import *

import networkx


# Συνάρτηση για Φόρτωση και επίλυση του προβλήματος
def readSTU(event):
#Δυναμική εισαγωγή των περιόδων και πυκνότητας για χρήση προς σύγκριση με τα υπολογιζόμενα
    diathesimes_periodoi = 0
    density_arx=0
    print(event)
    if event == "car-f-92.stu":
        diathesimes_periodoi = 32
        density_arx=0.14
    elif event == "car-s-91.stu":
        diathesimes_periodoi = 35
        density_arx = 0.13
    elif event == "ear-f-83.stu":
        diathesimes_periodoi = 24
        density_arx = 0.27
    elif event == "hec-s-92.stu":
        diathesimes_periodoi = 18
        density_arx = 0.42
    elif event == "kfu-s-93.stu":
        diathesimes_periodoi = 20
        density_arx = 0.06
    elif event == "lse-f-91.stu":
        diathesimes_periodoi = 18
        density_arx = 0.06
    elif event == "pur-s-93.stu":
        diathesimes_periodoi = 42
        density_arx = 0.03
    elif event == "rye-s-93.stu":
        diathesimes_periodoi = 23
        density_arx = 0.07
    elif event == "sta-f-83.stu":
        diathesimes_periodoi = 13
        density_arx = 0.14
    elif event == "toy_e5_s6.stu":
        diathesimes_periodoi = 3
        density_arx = 0.4
    elif event == "tre-s-92.stu":
        diathesimes_periodoi = 23
        density_arx = 0.18
    elif event == "uta-s-92.stu":
        diathesimes_periodoi = 35
        density_arx = 0.13
    elif event == "ute-s-92.stu":
        diathesimes_periodoi = 10
        density_arx = 0.08
    elif event == "yor-f-83.stu":
        diathesimes_periodoi = 21
        density_arx = 0.29

    # Ορισμός Μεταβλητών
    maxLesson = 0
    num_mathites = 0
    egrafes = 0
    commonSet = set() #Κάθε τιµή στο σύνολο υπάρχει µόνο µια ϕορά και δεν είναι είναι ταξινοµηµένη κατά οποιονδήποτε τρόπο
    filename = event

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
        # Υπολογισμός πλήθος μαθητών
        num_mathites = num_mathites + 1

        # Διαχωριζμός των γραμμών και άρα και των μαθητών
        grammh = line.split(" ")

        # μετατροπή απο string σε int
        for i in range(0, len(grammh)):
            if isinstance(grammh[i], str) and grammh[i] != '':
                grammh[i] = int(grammh[i])
                if grammh[i] > maxLesson:
                    maxLesson = grammh[i]
                # Υπολογισμός Εγγραφών
                egrafes = egrafes + 1


        # αναζήτηση των πιθανών συνδυασμών
        comb = combinations(grammh, 2)
		#εισαγωγή των συνδυασμών σε set
        for c in list(comb):
            commonSet.add(c)

    # Υπολογισμός της πυκνότητας  (υπολογίζεται διαιρώντας τον αριθμό των στοιχείων του πίνακα συγκρούσεων που
    # έχουν την τιμή 1 με το συνολικό πλήθος των στοιχείων του πίνακα)

    # Υπολογισμός όλων των θέσεων του πίνακα
    maxArray = maxLesson * maxLesson

    # Υπολογισμός πυκνότητας
    density = round(((len(commonSet) * 2) / maxArray),2)

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

    
	# Αποθήκευση των αποτελεσμάτων και εξαγωγή σε αρχεία sol υπολογισμός μέγιστης πυκνότητας για σύγκριση Σωστού Λάθους
    f = open(filename[:-4] + ".sol", "w")
    max_period = 0
    for exam in graphColored:
        f.write(str(exam) + "\t" + str(graphColored[exam]) + "\n")
        if graphColored[exam]> max_period:
            max_period = graphColored[exam]
    f.close()

    final_str = 'Οι Εξετάσεις είναι: %s \nΟι Φοιτητές είναι: %s \nΟι Εγγραφές είναι: %s \nΟι Περίοδοι είναι: %s \nΗ πυκνότητα είναι: %s  ' % (
    maxLesson, num_mathites, egrafes,max_period+1, density)
    label['text'] = final_str
    if (max_period+1) <= diathesimes_periodoi and density<=density_arx:
        mylabel6['text'] = 'Σωστό'
    elif density>density_arx or (max_period+1) < diathesimes_periodoi:
        mylabel6['text'] = 'Λάθος στην πυκνότητα. Έπρεπε: %s \tΕνώ είναι: %s' % (density_arx, density)
    elif density<density_arx or (max_period+1) > diathesimes_periodoi:
        mylabel6['text'] = 'Λάθος στις περιόδους. Έπρεπε: %s \tΕνώ είναι %s' % (diathesimes_periodoi,max_period+1)
    elif density>density_arx and (max_period+1) > diathesimes_periodoi:
        mylabel6['text'] = 'Λάθη! Περίοδοι και Πυκνότητα %s Έπρεπε: %s \tΕνώ είναι %s' % (diathesimes_periodoi,density_arx, max_period + 1,density)
    # end time
    end = time.time()

    # total time taken
    print(f"Runtime of the program is {end - start}")


# Δημιουργία GUI μενού για το πρόγραμμα

root = Tk()
root.title('Χρονοπρογραμματισμός εξετάσεων Πανεπιστημίου')
root.geometry("600x600")

mylabel1 = Label(root, text="1. Φόρτωση Προβλήματος επιλογή:")
mylabel1.grid(row=0, column=1, padx=10, pady=10, sticky=W)
mylabel2 = Label(root, text="2. Φόρτωση Λύσης")
mylabel2.grid(row=1, column=1, padx=10, pady=10, sticky=W)
mylabel3 = Label(root, text="3. Επίλυση Προβλήματος")
mylabel3.grid(row=2, column=1, padx=10, pady=10, sticky=W)
mylabel4 = Label(root, text="4. Μαζική επίλυση Προβλήματος")
mylabel4.grid(row=3, column=1, padx=10, pady=10, sticky=W)
mylabel5 = Label(root, text="Αποτέλεσμα σύγκρισης με δεδομένα πίνακα ")
mylabel5.grid(row=4, column=1, padx=10, pady=10, sticky=W)
mylabel6 = tk.Label(root, text="")
mylabel6.grid(row=4, column=2, padx=10, pady=10, sticky=W)

def button_load_prob():
    f_name = clicked.get()
    readSTU(f_name)


def button_loadall(options):
    for option in options:
        readSTU(option)


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
    "yor-f-83.stu"
]

clicked = StringVar()
clicked.set(options[0])

drop = OptionMenu(root, clicked, *options)
drop.grid(row=0, column=2, padx=10, pady=10)

Button_load = Button(root, text='Επίλυση Προβλήματος', command=button_load_prob)
Button_load.grid(row=2, column=2, padx=10, pady=10)

Go_button_All = Button(root, text='Διάβασε όλα τα αρχεία και έξοδο σε .sol', command=lambda: button_loadall(options))
Go_button_All.grid(row=3, column=2, padx=10, pady=10)

frame = LabelFrame(root, text="Αποτέλεσμα Φόρτωσης λύσης", padx=2, pady=2, bg='#80c1ff', bd=5)
frame.place(relx=0.8, rely=0.5, relwidth=0.7, relheight=0.3, anchor='ne')

label = tk.Label(frame, font=('Courier', 10), anchor='w', justify='left', bd=4)
label.place(relwidth=1, relheight=0.7)

root.mainloop()
