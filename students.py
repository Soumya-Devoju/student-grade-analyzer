import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load and clean data
df = pd.read_csv('student_marks.csv')
df.columns = df.columns.str.strip()

# Grade and status assignment
def assign_grade(marks):
    if marks >= 50:
        return 'A'
    elif marks >= 40:
        return 'B'
    elif marks >= 30:
        return 'C'
    elif marks >= 20:
        return 'D'
    else:
        return 'F'

df['Grade'] = df['Marks'].apply(assign_grade)
df['Status'] = df['Marks'].apply(lambda x: 'Pass' if x >= 20 else 'Fail')

# Streamlit layout
st.title('📊 Student Grade Analyzer')

# Sidebar filters
st.sidebar.header('Filters')
min_study = st.sidebar.slider('Minimum Study Time', 0.0, 10.0, 0.0)
grade_filter = st.sidebar.multiselect('Select Grades', options=df['Grade'].unique(), default=df['Grade'].unique())

# Filtered data
filtered_df = df[(df['time_study'] >= min_study) & (df['Grade'].isin(grade_filter))]

# Scatter plot: Study Time vs Marks
st.subheader('Study Time vs Marks')
fig1, ax1 = plt.subplots()
ax1.scatter(filtered_df['time_study'], filtered_df['Marks'], color='green', alpha=0.6)
ax1.set_xlabel('Study Time')
ax1.set_ylabel('Marks')
ax1.set_title('Study Time vs Marks Correlation')
st.pyplot(fig1)

# Bar chart: Average Marks by Number of Courses
st.subheader('Average Marks by Number of Courses')
avg_by_courses = filtered_df.groupby('number_courses')['Marks'].mean().reset_index()
fig2, ax2 = plt.subplots()
ax2.bar(avg_by_courses['number_courses'], avg_by_courses['Marks'], color='skyblue')
ax2.set_xlabel('Number of Courses')
ax2.set_ylabel('Average Marks')
ax2.set_title('Average Marks by Course Load')
st.pyplot(fig2)

# Data table
st.subheader('Filtered Student Data')
st.dataframe(filtered_df)

# Export option
st.download_button("Download Filtered Data as CSV", data=filtered_df.to_csv(index=False), file_name="filtered_student_data.csv", mime="text/csv")