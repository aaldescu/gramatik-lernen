import streamlit as st
import os
import sqlite3
import xmltodict
import markdown
import pandas as pd
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Învățarea Gramaticii",
    page_icon="📚",
    layout="wide"
)

# Initialize database
def init_db():
    conn = sqlite3.connect('database/progress.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_progress
        (user_id TEXT, 
         chapter_id TEXT,
         exercise_id TEXT,
         score INTEGER,
         completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
         PRIMARY KEY (user_id, exercise_id))
    ''')
    conn.commit()
    return conn

# Load theory content
def load_theory(chapter_path):
    with open(chapter_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return markdown.markdown(content, extensions=['markdown.extensions.fenced_code', 'markdown.extensions.tables', 'mdx_math'])

# Load exercise content
def load_exercise(exercise_path):
    with open(exercise_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return xmltodict.parse(content)

# Get user progress
def get_progress(conn, user_id):
    df = pd.read_sql_query(
        "SELECT chapter_id, COUNT(*) as completed_exercises, AVG(score) as avg_score "
        "FROM user_progress WHERE user_id = ? GROUP BY chapter_id",
        conn,
        params=(user_id,)
    )
    return df

# Save progress
def save_progress(conn, user_id, chapter_id, exercise_id, score):
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO user_progress (user_id, chapter_id, exercise_id, score)
        VALUES (?, ?, ?, ?)
    ''', (user_id, chapter_id, exercise_id, score))
    conn.commit()

# Main app
def main():
    # Initialize database connection
    conn = init_db()

    # Sidebar for navigation
    st.sidebar.title("Navigare")
    
    # Simple user management (can be expanded)
    if 'user_id' not in st.session_state:
        st.session_state.user_id = 'default_user'
    
    # Main sections
    section = st.sidebar.radio("Mergi la", ["Teorie", "Exerciții", "Progres"])

    if section == "Teorie":
        st.title("📖 Secțiuni Teoretice")
        
        # List all theory chapters
        theory_path = Path("theory")
        chapters = sorted([d for d in theory_path.iterdir() if d.is_dir()],
                        key=lambda x: int(x.name.split('_')[0]))
        
        for chapter in chapters:
            with st.expander(f"Capitolul {chapter.name.split('_')[0]}: {chapter.name.split('_', 1)[1].replace('_', ' ')}"):
                lessons = sorted(chapter.glob("*.md"))
                for lesson in lessons:
                    if st.button(f"📝 {lesson.stem.split('_', 1)[1].replace('_', ' ')}", key=lesson.stem):
                        st.markdown(load_theory(lesson), unsafe_allow_html=True)

    elif section == "Exerciții":
        st.title("✍️ Exerciții Practice")
        
        # List all exercise files
        exercises_path = Path("exercises")
        theory_path = Path("theory")
        exercise_files = sorted(exercises_path.glob("ex_*.xml"),
                              key=lambda x: (int(x.stem.split('_')[1]), int(x.stem.split('_')[2])))
        
        for ex_file in exercise_files:
            chapter_num = ex_file.stem.split('_')[1]
            lesson_num = ex_file.stem.split('_')[2]
            
            # Get chapter and lesson names from theory folder
            try:
                # Find matching chapter folder
                chapter_folder = next(d for d in theory_path.iterdir() 
                                   if d.is_dir() and d.name.startswith(f"{chapter_num}_"))
                chapter_name = chapter_folder.name.split('_', 1)[1].replace('_', ' ')
                
                # Find matching lesson file
                lesson_file = next(f for f in chapter_folder.glob("*.md") 
                                 if f.stem.startswith(f"{chapter_num}.{lesson_num}"))
                lesson_name = lesson_file.stem.split('_', 1)[1].replace('_', ' ')
                
                expander_title = f"Capitolul {chapter_num}: {chapter_name} - Lecția {lesson_num}: {lesson_name}"
            except (StopIteration, IndexError):
                expander_title = f"Capitolul {chapter_num} - Lecția {lesson_num}"
            
            with st.expander(expander_title):
                exercise_data = load_exercise(ex_file)
                assessment_items = exercise_data['assessmentTest']['assessmentItems']['assessmentItem']
                
                # Ensure we have a list of items
                if not isinstance(assessment_items, list):
                    assessment_items = [assessment_items]
                
                for item in assessment_items:
                    # Get interaction type
                    interaction_type = next(iter([k for k in item['itemBody'].keys() if k.endswith('Interaction')]))
                    interaction = item['itemBody'][interaction_type]
                    
                    # Display prompt
                    st.markdown(f"**{interaction['prompt']}**")
                    
                    # Handle different interaction types
                    if interaction_type == 'choiceInteraction':
                        choices = interaction['simpleChoice']
                        if not isinstance(choices, list):
                            choices = [choices]
                        
                        # Determine if multiple or single choice
                        max_choices = interaction.get('@maxChoices', '1')
                        is_multiple = int(max_choices) > 1
                        
                        # Create options dictionary
                        options = {choice['#text']: choice['@identifier'] for choice in choices}
                        
                        if is_multiple:
                            selected = st.multiselect(
                                "Selectează toate răspunsurile corecte:",
                                options.keys(),
                                key=f"{ex_file.stem}_{item['@identifier']}"
                            )
                        else:
                            selected = st.radio(
                                "Selectează un răspuns:",
                                options.keys(),
                                key=f"{ex_file.stem}_{item['@identifier']}"
                            )
                        
                    elif interaction_type == 'textEntryInteraction':
                        selected = st.text_input(
                            "Introdu răspunsul tău:",
                            key=f"{ex_file.stem}_{item['@identifier']}"
                        )
                        options = {selected: selected} if selected else {}
                    
                    # Check answer button
                    if st.button("Verifică Răspunsul", key=f"check_{ex_file.stem}_{item['@identifier']}"):
                        correct_values = item['responseDeclaration']['correctResponse']['value']
                        if not isinstance(correct_values, list):
                            correct_values = [correct_values]
                        
                        if interaction_type == 'choiceInteraction':
                            if is_multiple:
                                selected_ids = [options[s] for s in selected]
                                is_correct = set(selected_ids) == set(correct_values)
                            else:
                                is_correct = options.get(selected, '') in correct_values
                        else:  # textEntryInteraction
                            is_correct = selected in correct_values
                        
                        if is_correct:
                            st.success("Corect! 🎉")
                            score = 100
                        else:
                            st.error("Incorect. Încearcă din nou!")
                            score = 0
                        
                        # Save progress
                        save_progress(conn, st.session_state.user_id, chapter_num, item['@identifier'], score)
                    
                    st.markdown("---")
    else:  # Progress section
        st.title("📊 Progresul Tău")
        
        progress_df = get_progress(conn, st.session_state.user_id)
        
        if not progress_df.empty:
            # Display overall statistics
            st.subheader("Statistici Generale")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Capitole Începute", len(progress_df))
                
            with col2:
                st.metric("Scor Mediu", f"{progress_df['avg_score'].mean():.1f}%")
            
            # Display progress table
            st.subheader("Progres pe Capitole")
            progress_df.columns = ['Capitol', 'Exerciții Completate', 'Scor Mediu']
            progress_df['Scor Mediu'] = progress_df['Scor Mediu'].round(1)
            st.dataframe(progress_df)
            
            # Display progress chart
            st.subheader("Grafic Progres")
            st.bar_chart(progress_df.set_index('Capitol')['Scor Mediu'])
        else:
            st.info("Nu ai încă niciun progres înregistrat. Începe să rezolvi exerciții!")

if __name__ == "__main__":
    main()