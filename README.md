# Student Performance Analytics

Interactive Streamlit data-analysis dashboard for exploring student academic performance.

## Features
- CSV upload and sample dataset
- KPI dashboard
- Department and performance filters
- Performance distribution
- Final-mark distribution
- Department-wise analysis
- Attendance vs final mark
- Study hours vs final mark
- Correlation matrix
- Missing-value and duplicate checks
- Filtered CSV download

## Run locally

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Required CSV columns

- Attendance_Percent
- Study_Hours_Per_Day
- Assignment_Score
- Internal_Mark
- Previous_Semester_Mark
- Final_Mark

Optional columns: Student_ID, Department, Gender, Performance_Level.

The included dataset is synthetic demonstration data and should not be presented as real institutional student data.
