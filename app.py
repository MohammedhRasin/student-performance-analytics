import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Performance Analytics", page_icon="📊", layout="wide")

@st.cache_data
def sample_data():
    return pd.read_csv("data/student_performance.csv")

def prepare(df):
    df=df.copy()
    cols=["Attendance_Percent","Study_Hours_Per_Day","Assignment_Score","Internal_Mark","Previous_Semester_Mark","Final_Mark"]
    for c in cols:
        if c in df.columns: df[c]=pd.to_numeric(df[c],errors="coerce")
    if "Performance_Level" not in df.columns:
        df["Performance_Level"]=df["Final_Mark"].apply(lambda x:"High" if x>=75 else ("Medium" if x>=50 else "Low"))
    return df

st.title("📊 Student Performance Analytics")
st.caption("Interactive data analysis dashboard")

with st.sidebar:
    st.header("Data Source")
    uploaded=st.file_uploader("Upload CSV",type=["csv"])
    use_sample=st.checkbox("Use sample dataset",value=uploaded is None)

data=prepare(pd.read_csv(uploaded) if uploaded is not None and not use_sample else sample_data())
required=["Attendance_Percent","Study_Hours_Per_Day","Assignment_Score","Internal_Mark","Previous_Semester_Mark","Final_Mark"]
missing=[c for c in required if c not in data.columns]
if missing:
    st.error("Missing required columns: "+", ".join(missing)); st.stop()

with st.sidebar:
    st.header("Filters")
    if "Department" in data.columns:
        ds=sorted(data["Department"].dropna().unique()); sel=st.multiselect("Department",ds,default=ds); data=data[data["Department"].isin(sel)]
    ls=["High","Medium","Low"]; sel2=st.multiselect("Performance Level",ls,default=ls); data=data[data["Performance_Level"].isin(sel2)]

st.subheader("Overview")
a,b,c,d=st.columns(4)
a.metric("Students",len(data)); b.metric("Average Final Mark",f"{data.Final_Mark.mean():.1f}"); c.metric("Average Attendance",f"{data.Attendance_Percent.mean():.1f}%"); d.metric("Avg Study Hours",f"{data.Study_Hours_Per_Day.mean():.1f} h")

t1,t2,t3,t4=st.tabs(["📈 Performance","🔍 Factors","🧹 Data Quality","📋 Dataset"])
with t1:
    c1,c2=st.columns(2)
    with c1:
        st.markdown("#### Performance Distribution"); counts=data.Performance_Level.value_counts().reindex(["High","Medium","Low"]).fillna(0); fig,ax=plt.subplots(); ax.bar(counts.index,counts.values); ax.set_ylabel("Students"); st.pyplot(fig); plt.close(fig)
    with c2:
        st.markdown("#### Final Mark Distribution"); fig,ax=plt.subplots(); ax.hist(data.Final_Mark.dropna(),bins=15); ax.set_xlabel("Final Mark"); ax.set_ylabel("Students"); st.pyplot(fig); plt.close(fig)
    if "Department" in data.columns: st.markdown("#### Department-wise Average Final Mark"); st.bar_chart(data.groupby("Department").Final_Mark.mean().sort_values(ascending=False))
with t2:
    st.markdown("#### Attendance vs Final Mark"); fig,ax=plt.subplots()
    for lv in ["High","Medium","Low"]:
        p=data[data.Performance_Level==lv]; ax.scatter(p.Attendance_Percent,p.Final_Mark,label=lv,alpha=.6)
    ax.set_xlabel("Attendance (%)"); ax.set_ylabel("Final Mark"); ax.legend(); st.pyplot(fig); plt.close(fig)
    st.markdown("#### Study Hours vs Final Mark"); fig,ax=plt.subplots(); ax.scatter(data.Study_Hours_Per_Day,data.Final_Mark,alpha=.6); ax.set_xlabel("Study Hours / Day"); ax.set_ylabel("Final Mark"); st.pyplot(fig); plt.close(fig)
    st.markdown("#### Correlation Matrix"); st.dataframe(data[required].corr().round(2),use_container_width=True)
with t3:
    q=pd.DataFrame({"Column":data.columns,"Missing Values":[int(data[c].isna().sum()) for c in data.columns],"Unique Values":[int(data[c].nunique()) for c in data.columns],"Data Type":[str(data[c].dtype) for c in data.columns]}); st.dataframe(q,use_container_width=True); st.write("Duplicate rows:",int(data.duplicated().sum()))
with t4:
    st.dataframe(data,use_container_width=True,height=500); st.download_button("Download filtered CSV",data.to_csv(index=False).encode(),"filtered_student_performance.csv","text/csv")
st.divider(); st.caption("Student Performance Analytics • Data Analysis Project")