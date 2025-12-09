import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Student Rank Calculator", layout="wide")

st.title("🎓 Student Score & Rank Calculator")

# 2. Input: Number of Students and Subjects
col1, col2 = st.columns(2)
with col1:
    num_students = st.number_input("Number of Students", min_value=1, value=3, step=1)
with col2:
    num_subjects = st.number_input("Number of Subjects", min_value=1, value=4, step=1)

# 3. Setup Data Structure
student_indices = [f"Student {i+1}" for i in range(num_students)]
subject_columns = [f"Subject {i+1}" for i in range(num_subjects)]

# Initialize an empty DataFrame with 0s
df_template = pd.DataFrame(0, index=student_indices, columns=subject_columns)

st.write("### 📝 Enter Scores Below")
st.info("Click on any cell in the table to edit the score.")

# 4. Data Entry Grid
scores_df = st.data_editor(df_template, width='stretch')

# 5. Calculation Logic
if st.button("Calculate Results"):
    st.write("---")
    st.subheader("📊 Final Report")

    result_df = scores_df.copy()

    # A. Use sum function to find Total
    result_df['Total Score'] = result_df.sum(axis=1)

    # B. Find Percentage
    max_possible_score = num_subjects * 100
    result_df['Percentage (%)'] = (result_df['Total Score'] / max_possible_score) * 100
    result_df['Percentage (%)'] = result_df['Percentage (%)'].round(2)

    # C. Rank Calculation
    result_df['Rank'] = result_df['Total Score'].rank(ascending=False, method='min')
    result_df['Rank'] = result_df['Rank'].astype(int)  # Convert to int (Fix #4)

    # Reorder Columns
    cols = ['Rank', 'Total Score', 'Percentage (%)'] + subject_columns
    result_df = result_df[cols]

    # Sort by Rank (Fix #5)
    result_df = result_df.sort_values(by='Rank').reset_index().rename(columns={"index": "Student"})

    # Display Final Table
    st.dataframe(result_df, use_container_width=True)

    # Highlight Topper
    top_student = result_df.iloc[0]['Student']
    st.success(f"🏆 The class topper is **{top_student}** with {result_df.iloc[0]['Percentage (%)']}%")

    # -------- Feature #2: EXPORT BUTTON --------
    csv = result_df.to_csv(index=False)
    st.download_button(
        label="⬇ Download Results as txt",
        data=csv,
        file_name="student_results.txt",
        mime="text/csv"
    )