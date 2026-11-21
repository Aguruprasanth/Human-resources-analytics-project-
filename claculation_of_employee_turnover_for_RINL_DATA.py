import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"C:\Users\aguru\OneDrive\Documents\RINL_employee_turnover_dataset.csv")

df.head()

df.shape
df.info()
df.isnull().sum()
df.duplicated().sum()

#overall employee turnover rate 

overall_turnover = df["Turnover_Status"].mean() * 100
print(f"Overall Turnover Rate: {overall_turnover:.2f}%")

turnover_count = df["Turnover_Status"].sum()
retained_count = len(df) - turnover_count

print(f"Turnover Count: {turnover_count}")
print(f"Retained Count: {retained_count}")

#visual representation of turnoverrate 

labels = ["Retained", "Turnover"]
sizes = [retained_count, turnover_count]

plt.figure(figsize=(6,6))
plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=["#4CAF50", "#F44336"])
plt.title("Overall Employee Turnover")
plt.show()

#Turnover rate by department 

dept_turnover = df.groupby("Department")["Turnover_Status"].mean().sort_values(ascending=False) * 100
print(dept_turnover)

dept_turnover_df = dept_turnover.reset_index()
dept_turnover_df.columns = ["Department", "Turnover_Rate"]
dept_turnover_df

#visual representation 

plt.figure(figsize=(10,6))
sns.barplot(data=dept_turnover_df, x="Turnover_Rate", y="Department", palette="Reds_r")
plt.title("Turnover Rate by Department")
plt.xlabel("Turnover Rate (%)")
plt.ylabel("Department")
plt.show()

#employee turnover rate by job role

role_turnover = df.groupby("Job_Role")["Turnover_Status"].mean().sort_values(ascending=False) * 100
role_turnover_df = role_turnover.reset_index()
role_turnover_df.columns = ["Job_Role", "Turnover_Rate"]

print(role_turnover_df)

#graphical represenatation 

plt.figure(figsize=(12,8))
sns.barplot(data=role_turnover_df, x="Turnover_Rate", y="Job_Role", palette="Blues_r")
plt.title("Turnover Rate by Job Role")
plt.xlabel("Turnover Rate (%)")
plt.ylabel("Job Role")
plt.show()

#Turnover by age_group

df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[21, 30, 40, 50, 60],
    labels=["22-30", "31-40", "41-50", "51-59"]
)

age_turnover = df.groupby("Age_Group", observed=True)["Turnover_Status"].mean() * 100
age_turnover_df = age_turnover.reset_index()
age_turnover_df.columns = ["Age_Group", "Turnover_Rate"]

print(age_turnover_df)

#graphical representation

plt.figure(figsize=(8,5))
sns.barplot(data=age_turnover_df, x="Age_Group", y="Turnover_Rate", palette="viridis")
plt.title("Turnover Rate by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Turnover Rate (%)")
plt.show()

#turnover rate by tenure 

df["Tenure_Group"] = pd.cut(
    df["Tenure_at_RINL_Years"],
    bins=[-1, 1, 3, 5, 10, 40],
    labels=["0-1", "2-3", "4-5", "6-10", "10+"]
)

tenure_turnover = df.groupby("Tenure_Group", observed=True)["Turnover_Status"].mean() * 100
tenure_turnover_df = tenure_turnover.reset_index()
tenure_turnover_df.columns = ["Tenure_Group", "Turnover_Rate"]

print(tenure_turnover_df)

#graphical representation

plt.figure(figsize=(8,5))
sns.barplot(data=tenure_turnover_df, x="Tenure_Group", y="Turnover_Rate", palette="magma")
plt.title("Turnover Rate by Tenure")
plt.xlabel("Tenure Group")
plt.ylabel("Turnover Rate (%)")
plt.show()

#Turnover by salary group

df["Salary_Group"] = pd.cut(
    df["Monthly_Salary_INR"],
    bins=[0, 35000, 50000, 70000, 1000000],
    labels=["Low", "Medium", "High", "Very High"]
)

salary_turnover = df.groupby("Salary_Group", observed=True)["Turnover_Status"].mean() * 100
salary_turnover_df = salary_turnover.reset_index()
salary_turnover_df.columns = ["Salary_Group", "Turnover_Rate"]

print(salary_turnover_df)

#graphical representation 

plt.figure(figsize=(8,5))
sns.barplot(data=salary_turnover_df, x="Salary_Group", y="Turnover_Rate", palette="coolwarm")
plt.title("Turnover Rate by Salary Group")
plt.xlabel("Salary Group")
plt.ylabel("Turnover Rate (%)")
plt.show()

#turnover rate by job satisfaction

js_turnover = df.groupby("Job_Satisfaction")["Turnover_Status"].mean() * 100
js_turnover_df = js_turnover.reset_index()
js_turnover_df.columns = ["Job_Satisfaction", "Turnover_Rate"]

print(js_turnover_df)

#graphical representation 

plt.figure(figsize=(8,5))
sns.barplot(data=js_turnover_df, x="Job_Satisfaction", y="Turnover_Rate", palette="Blues")
plt.title("Turnover Rate by Job Satisfaction")
plt.xlabel("Job Satisfaction")
plt.ylabel("Turnover Rate (%)")
plt.show()

#Turnover by work life balance 

wlb_turnover = df.groupby("Work_Life_Balance")["Turnover_Status"].mean() * 100
wlb_turnover_df = wlb_turnover.reset_index()
wlb_turnover_df.columns = ["Work_Life_Balance", "Turnover_Rate"]

print(wlb_turnover_df)

#graphical representation

plt.figure(figsize=(8,5))
sns.barplot(data=wlb_turnover_df, x="Work_Life_Balance", y="Turnover_Rate", palette="Greens")
plt.title("Turnover Rate by Work-Life Balance")
plt.xlabel("Work-Life Balance")
plt.ylabel("Turnover Rate (%)")
plt.show()

#turnover by overtime

df["Overtime_Group"] = pd.cut(
    df["Overtime_Hours_Month"],
    bins=[-1, 5, 15, 30, 60],
    labels=["Low", "Moderate", "High", "Very High"]
)

ot_turnover = df.groupby("Overtime_Group", observed=True)["Turnover_Status"].mean() * 100
ot_turnover_df = ot_turnover.reset_index()
ot_turnover_df.columns = ["Overtime_Group", "Turnover_Rate"]

print(ot_turnover_df)

#graphical representation

plt.figure(figsize=(8,5))
sns.barplot(data=ot_turnover_df, x="Overtime_Group", y="Turnover_Rate", palette="Oranges")
plt.title("Turnover Rate by Overtime")
plt.xlabel("Overtime Group")
plt.ylabel("Turnover Rate (%)")
plt.show()

#Risk factor analysis
#correlation  with tenure

num_cols = [
    "Age", "Experience_Years", "Tenure_at_RINL_Years", "Monthly_Salary_INR",
    "Job_Satisfaction", "Work_Life_Balance", "Hours_Per_Week", "Performance_Rating",
    "Previous_Jobs_Count", "Training_Hours_Year", "Promotions_Last_3Years",
    "Overtime_Hours_Month", "Career_Development", "Commute_Distance_KM",
    "Safety_Incidents_LastYear", "Turnover_Status"
]

corr = df[num_cols].corr(numeric_only=True)["Turnover_Status"].sort_values(ascending=False)
print(corr)

#heat map 

plt.figure(figsize=(12,8))
sns.heatmap(df[num_cols].corr(numeric_only=True), annot=False, cmap="coolwarm", center=0)
plt.title("Correlation Heatmap")
plt.show()

#rule-based-scoring

def risk_score(row):
    score = 0
    
    if row["Job_Satisfaction"] <= 2:
        score += 2
    if row["Work_Life_Balance"] <= 2:
        score += 2
    if row["Tenure_at_RINL_Years"] < 3:
        score += 2
    if row["Monthly_Salary_INR"] < df["Monthly_Salary_INR"].median():
        score += 1
    if row["Overtime_Hours_Month"] > 30:
        score += 1
    if row["Promotions_Last_3Years"] == 0:
        score += 1
    if row["Career_Development"] <= 2:
        score += 1
    if row["Mentorship_Available"] == "No":
        score += 1
        
    return score

df["Risk_Score"] = df.apply(risk_score, axis=1)

def risk_zone(score):
    if score <= 2:
        return "Low Risk"
    elif score <= 4:
        return "Medium Risk"
    else:
        return "High Risk"

df["Risk_Zone"] = df["Risk_Score"].apply(risk_zone)

df[["Employee_ID", "Risk_Score", "Risk_Zone"]].head()

risk_counts = df["Risk_Zone"].value_counts()
print(risk_counts)

#graphical representation

plt.figure(figsize=(7,5))
sns.countplot(data=df, x="Risk_Zone", order=["Low Risk", "Medium Risk", "High Risk"], palette="Set2")
plt.title("Employee Risk Zones")
plt.xlabel("Risk Zone")
plt.ylabel("Count")
plt.show()

# High-risk employee list

high_risk_employees = df[df["Risk_Zone"] == "High Risk"].sort_values("Risk_Score", ascending=False)

print(high_risk_employees.head(20))