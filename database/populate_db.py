import sqlite3
import json
import os

def populate_db():
    db_dir = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(os.path.join(db_dir, 'german_grammar.db'))
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute('DELETE FROM exercises')
    cursor.execute('DELETE FROM sections')
    cursor.execute('DELETE FROM lessons')

    # Insert Lessons
    lessons_data = [
        (1, "Articole și substantive", "Învățarea articolelor și genurilor substantivelor în limba germană"),
        (2, "Pronume personale", "Studiul pronumelor personale și conjugarea verbelor"),
        (3, "Propoziții simple", "Construirea și înțelegerea propozițiilor simple"),
        (4, "Cazul Acuzativ", "Învățarea și utilizarea cazului acuzativ"),
        (5, "Cazul Dativ", "Învățarea și utilizarea cazului dativ"),
        (6, "Prepoziții", "Studiul prepozițiilor în limba germană"),
        (7, "Timpuri verbale", "Perfectul și imperfectul în limba germană"),
        (8, "Verbe modale", "Învățarea și utilizarea verbelor modale"),
        (9, "Conectori", "Studiul conectorilor și ordinea cuvintelor")
    ]

    cursor.executemany('''
    INSERT INTO lessons (lesson_number, title, description)
    VALUES (?, ?, ?)
    ''', lessons_data)

    # Insert sections for each lesson
    sections_data = [
        # Lesson 1: Articole și substantive
        (1, "1.1", "Articolele hotărâte (der, die, das)", "### Articolele hotărâte în germană\n- der (masculin)\n- die (feminin)\n- das (neutru)\n\nExemple:\n- der Mann (bărbatul)\n- die Frau (femeia)\n- das Kind (copilul)"),
        (1, "1.2", "Articolele nehotărâte (ein, eine, ein)", "### Articolele nehotărâte în germană\n- ein (masculin)\n- eine (feminin)\n- ein (neutru)\n\nExemple:\n- ein Tisch (o masă)\n- eine Katze (o pisică)\n- ein Buch (o carte)"),
        (1, "1.3", "Genul substantivelor", "### Genul substantivelor\n- Reguli generale pentru determinarea genului\n- Terminații specifice pentru fiecare gen\n- Excepții importante"),
        (1, "1.4", "Formarea pluralului", "### Formarea pluralului\n- Terminații comune (-e, -en, -er)\n- Modificări ale vocalelor (Umlaut)\n- Cazuri speciale"),

        # Lesson 2: Pronume personale
        (2, "2.1", "Nominativ (ich, du, er, sie, es, wir, ihr, sie/Sie)", "### Pronumele personale în nominativ\n- ich (eu)\n- du (tu)\n- er/sie/es (el/ea/el,ea)\n- wir (noi)\n- ihr (voi)\n- sie/Sie (ei,ele/dumneavoastră)"),
        (2, "2.2", "Conjugarea verbelor regulate în prezent", "### Conjugarea în prezent\n- Terminații: -e, -st, -t, -en, -t, -en\n- Exemple cu verbe uzuale"),
        (2, "2.3", "Verbele sein și haben", "### Verbele sein și haben\n- Conjugarea completă\n- Utilizare în propoziții\n- Exemple practice"),

        # Lesson 3: Propoziții simple
        (3, "3.1", "Ordinea cuvintelor în propoziții", "### Ordinea cuvintelor\n- Poziția verbului în propoziția principală\n- Topica subiect-predicat-complement"),
        (3, "3.2", "Propoziții afirmative", "### Propoziții afirmative\n- Structura de bază\n- Exemple practice"),
        (3, "3.3", "Propoziții interogative", "### Întrebări în germană\n- Cu și fără cuvinte interogative\n- Ordinea cuvintelor în întrebări"),
        (3, "3.4", "Negația cu nicht și kein", "### Negația\n- Utilizarea lui 'nicht'\n- Utilizarea lui 'kein'\n- Poziția negației în propoziție"),

        # Lesson 4: Cazul Acuzativ
        (4, "4.1", "Utilizare și forme", "### Cazul acuzativ\n- Când se folosește\n- Formele articolelor și pronumelor"),
        (4, "4.2", "Prepoziții care cer acuzativul", "### Prepoziții cu acuzativ\n- durch, für, gegen, ohne, um\n- Exemple de utilizare"),
        (4, "3", "Exerciții practice", "### Exerciții practice\n- Transformări de propoziții\n- Completare de spații libere"),

        # Lesson 5: Cazul Dativ
        (5, "5.1", "Utilizare și forme", "### Cazul dativ\n- Când se folosește\n- Formele articolelor și pronumelor"),
        (5, "5.2", "Prepoziții care cer dativul", "### Prepoziții cu dativ\n- aus, bei, mit, nach, seit, von, zu\n- Exemple de utilizare"),
        (5, "5.3", "Pronume în dativ", "### Pronumele în dativ\n- Forme și utilizare\n- Exemple practice"),

        # Lesson 6: Prepoziții
        (6, "6.1", "Prepoziții temporale", "### Prepoziții temporale\n- am, um, in\n- Utilizare cu expresii de timp"),
        (6, "6.2", "Prepoziții locale", "### Prepoziții locale\n- in, auf, an, neben\n- Descrierea poziției"),
        (6, "6.3", "Prepoziții cu acuzativ și dativ", "### Prepoziții cu două cazuri\n- Când folosim acuzativ vs. dativ\n- Exemple practice"),

        # Lesson 7: Timpuri verbale
        (7, "7.1", "Perfectul (Perfekt)", "### Perfectul\n- Formarea cu haben și sein\n- Participiul trecut"),
        (7, "7.2", "Imperfectul (Präteritum)", "### Imperfectul\n- Formarea pentru verbe regulate și neregulate\n- Utilizare"),
        (7, "7.3", "Verbe regulate vs. neregulate", "### Tipuri de verbe\n- Conjugări regulate\n- Liste de verbe neregulate importante"),

        # Lesson 8: Verbe modale
        (8, "8.1", "können, müssen, dürfen", "### Primele verbe modale\n- Conjugare și utilizare\n- Exemple practice"),
        (8, "8.2", "wollen, sollen, mögen", "### Alte verbe modale\n- Conjugare și utilizare\n- Exemple practice"),
        (8, "8.3", "Utilizare și conjugare", "### Utilizarea verbelor modale\n- Poziția în propoziție\n- Combinații cu infinitiv"),

        # Lesson 9: Conectori
        (9, "9.1", "und, oder, aber", "### Conectori coordonatori\n- Utilizare și exemple\n- Nu modifică ordinea cuvintelor"),
        (9, "9.2", "weil, dass, ob", "### Conectori subordonatori\n- Modifică ordinea cuvintelor\n- Exemple practice"),
        (9, "9.3", "Ordinea cuvintelor după conectori", "### Reguli de topică\n- După conectori coordonatori\n- După conectori subordonatori")
    ]

    cursor.executemany('''
    INSERT INTO sections (lesson_id, section_number, title, content)
    VALUES (?, ?, ?, ?)
    ''', sections_data)

    # Insert some example exercises
    exercises_data = [
        # Exercises for Lesson 1
        (1, "Care este articolul corect pentru 'Buch'?", "das", "multiple", 
         json.dumps(["der", "die", "das"]), "Buch (carte) este un substantiv neutru."),
        (1, "Care este pluralul pentru 'Haus'?", "Häuser", "fill", 
         None, "Substantivele care se termină în -s primesc umlauts și terminația -er."),
        
        # Exercises for Lesson 2
        (4, "Conjugă verbul 'sein' la persoana a II-a singular:", "bist", "fill", 
         None, "Forma corectă pentru 'du' este 'bist'."),
        
        # Exercises for Lesson 3
        (7, "Aranjează cuvintele: 'Schule, in, gehe, ich, die'", "Ich gehe in die Schule.", "fill",
         None, "Verbul trebuie să fie în poziția a doua în propoziție.")
    ]

    cursor.executemany('''
    INSERT INTO exercises (section_id, question, correct_answer, exercise_type, options, explanation)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', exercises_data)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    populate_db()
