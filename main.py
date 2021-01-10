from itertools import combinations
import networkx


def readSTU(filename):
    # Ορισμός Μεταβλητών
    maxLesson = 0
    commonSet = set()

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
            if isinstance(grammh[i], str):
                grammh[i] = int(grammh[i])
                if grammh[i] > maxLesson:
                    maxLesson = grammh[i]

        # αναζήτηση των πιθανών συνδιασμών
        comb = combinations(grammh, 2)

        for c in list(comb):
            commonSet.add(c)

    # Αναφορές και εμφάνιση:
    # Αριθμός μαθημάτων
    print("Τα μαθήματα είναι: ", maxLesson)
    # Υπολογισμός της πυκνότητας  (υπολογίζεται διαιρώντας τον αριθμό των στοιχείων του πίνακα συγκρούσεων που
    # έχουν την τιμή 1 με το συνολικό πλήθος των στοιχείων του πίνακα)
    # Υπολογισμός όλων των θέσεων του πίνακα
    maxArray = maxLesson * maxLesson
    # Υπολογισμός πυκνότητας
    density = (len(commonSet) * 2) / maxArray
    print("Η πυκνότητα είναι ", density)

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
    print("Το Graph Coloring είναι:\n", graphColored)

    # Αποθήκευση των αποτελεσμάτων
    f = open("solution " + filename, "w")
    for exam in graphColored:
        f.write(str(exam) + "\t" + str(graphColored[exam]) + "\n")
    f.close()


if __name__ == '__main__':
    # Εισαγωγή του αρχείου με το όνομά του
    readSTU("yor-f-83.stu")
