import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

# ----------------- FUNCTION TO GENERATE PDF --------------------
def generate_pdf(df):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 750, "Student Result Report")

    pdf.setFont("Helvetica", 12)
    y = 720

    # Table header
    pdf.drawString(40, y, "Student")
    pdf.drawString(180, y, "Total")
    pdf.drawString(260, y, "Percentage")
    pdf.drawString(360, y, "Rank")

    y -= 20

    for _, row in df.iterrows():
        pdf.drawString(40, y, str(row["Student"]))
        pdf.drawString(180, y, str(row["Total Score"]))
        pdf.drawString(260, y, f"{row['Percentage (%)']}%")
        pdf.drawString(360, y, str(row["Rank"]))
        y -= 20

        if y < 40:  # New page if space is over
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y = 750

    pdf.save()
    buffer.seek(0)
    return buffer

# ----------------- STREAMLIT UI --------------------

st.set_page_config(page_title="Student Rank Calculator", layout="wide")

st.title("🎓 Student Score & Rank Calculator")

# Input
col1, col2 = st.columns(2)
with col1:
    num_students = st.number_input("Number of Students", min_value=1, value=3, step=1)
with col2:
    num_subjects = st.number_input("Number of Subjects", min_value=1, value=4, step=1)

# Prepare table
student_indices = [f"Student {i+1}" for i in range(num_students)]
subject_columns = [f"Subject {i+1}" for i in range(num_subjects)]

df_template = pd.DataFrame(0, index=student_indices, columns=subject_columns)

st.write("### 📝 Enter Scores Below")
scores_df = st.data_editor(df_template, width="stretch")

# Calculate
if st.button("Calculate Results"):
    st.write("---")
    st.subheader("📊 Final Report")

    result_df = scores_df.copy()
    result_df["Total Score"] = result_df.sum(axis=1)

    max_possible = num_subjects * 100
    result_df["Percentage (%)"] = (result_df["Total Score"] / max_possible) * 100
    result_df["Percentage (%)"] = result_df["Percentage (%)"].round(2)

    result_df["Rank"] = result_df["Total Score"].rank(ascending=False, method="min").astype(int)

    cols = ["Rank", "Total Score", "Percentage (%)"] + subject_columns
    result_df = result_df[cols]

    result_df = (
        result_df.sort_values(by="Rank")
        .reset_index()
        .rename(columns={"index": "Student"})
    )

    st.dataframe(result_df, use_container_width=True)

    top_student = result_df.iloc[0]["Student"]
    st.success(f"🏆 Topper: **{top_student}** with {result_df.iloc[0]['Percentage (%)']}%")

    # ---------------- PDF Download ----------------
    pdf_file = generate_pdf(result_df)

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_file,
        file_name="student_results.pdf",
        mime="application/pdf"
    )
