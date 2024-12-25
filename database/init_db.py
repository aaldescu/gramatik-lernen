import sqlite3
import os

def init_db():
    # Create database directory if it doesn't exist
    db_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    db_path = os.path.join(db_dir, 'german_grammar.db')
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)

    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create lessons table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_number INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        duration_minutes INTEGER DEFAULT 90,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create sections table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_id INTEGER,
        section_number TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT,
        duration_minutes INTEGER DEFAULT 30,
        FOREIGN KEY (lesson_id) REFERENCES lessons (id)
    )
    ''')

    # Create exercises table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        section_id INTEGER,
        question TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        exercise_type TEXT NOT NULL,
        options TEXT,  -- JSON string for multiple choice options
        explanation TEXT,
        FOREIGN KEY (section_id) REFERENCES sections (id)
    )
    ''')

    # Create user_progress table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        lesson_id INTEGER,
        section_id INTEGER,
        exercise_id INTEGER,
        completed BOOLEAN DEFAULT FALSE,
        score INTEGER,
        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (lesson_id) REFERENCES lessons (id),
        FOREIGN KEY (section_id) REFERENCES sections (id),
        FOREIGN KEY (exercise_id) REFERENCES exercises (id)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
