import streamlit as st
import pandas as pd
from data_utils import load_data
data = load_data()

st.title("Supermarket OLAP Dashboard")

data = load_data()


st.header("Dataset Preview")
st.write(data.head())

st.header("Basic Statistics")
st.write(data.describe())


st.header("Slice Operation")

category = st.selectbox("Choose a category", data["Kategoria e produktit"].unique())
slice_df = data[data["Kategoria e produktit"] == category]
st.write(slice_df)

city = st.selectbox("Choose a city", data["Qyteti"].unique())
slice_df = data[data["Qyteti"] == city]
st.write(slice_df)

st.header("Dice Operation")

categories = st.multiselect("Category", data["Kategoria e produktit"].unique())
cities = st.multiselect("City", data["Qyteti"].unique())
gender = st.multiselect("Gender", data["Gjinia"].unique())

dice_df = data.copy()

if categories:
    dice_df = dice_df[dice_df["Kategoria e produktit"].isin(categories)]

if cities:
    dice_df = dice_df[dice_df["Qyteti"].isin(cities)]

if gender:
    dice_df = dice_df[dice_df["Gjinia"].isin(gender)]

st.write(dice_df)

# Group and Summarize
st.header("Group & Summarize")

group_col = st.selectbox("Group by", [
    "Qyteti",
    "Gjinia",
    "Kategoria e produktit",
    "Menyra e pageses"
])

data["Te ardhura bruto"] = (
    data["Te ardhura bruto"]
    .astype(str)
    .str.replace("Lek", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)

data["Te ardhura bruto"] = pd.to_numeric(data["Te ardhura bruto"], errors="coerce")


summary = data.groupby(group_col)["Te ardhura bruto"].sum()

st.bar_chart(summary)

avg_rating = data.groupby(group_col)["Vleresimi"].mean()
st.write(avg_rating)

# Drill Down
# Convert Data column
data["Data"] = pd.to_datetime(data["Data"], format="%m/%d/%Y")

# Extract year and month
data["Year"] = data["Data"].dt.year
data["Month"] = data["Data"].dt.month
data["Month_Name"] = data["Data"].dt.month_name()

# Drill Down
st.header("Drill Down")
year = st.selectbox("Choose a year", data["Year"].unique())

filtered = data[data["Year"] == year]

monthly = filtered.groupby("Month_Name")["Te ardhura bruto"].sum()

st.bar_chart(monthly)

st.header("Drill Down (Category → Payment Method)")

category = st.selectbox("Kategoria", data["Kategoria e produktit"].unique())
filtered = data[data["Kategoria e produktit"] == category]

payment = st.selectbox("Menyra e pageses", filtered["Menyra e pageses"].unique())

result = filtered[filtered["Menyra e pageses"] == payment]

st.write(result)


# Kthe te arshurat nga text ne numeric
data["Te ardhura bruto"] = (
    data["Te ardhura bruto"]
    .astype(str)
    .str.replace("Lek", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)

data["Te ardhura bruto"] = pd.to_numeric(data["Te ardhura bruto"], errors="coerce")

#Compare
st.header("Compare Months")

month1 = st.selectbox("Muaji 1", data["Month_Name"].unique())
month2 = st.selectbox("Muaji 2", data["Month_Name"].unique())

rev1 = data[data["Month_Name"] == month1]["Te ardhura bruto"].sum()
rev2 = data[data["Month_Name"] == month2]["Te ardhura bruto"].sum()

st.write(f"{month1}: {rev1:,.2f} Lek")
st.write(f"{month2}: {rev2:,.2f} Lek")

st.header("Compare Categories")

cat1 = st.selectbox("Category 1", data["Kategoria e produktit"].unique())
cat2 = st.selectbox("Category 2", data["Kategoria e produktit"].unique())

rev1 = data[data["Kategoria e produktit"] == cat1]["Te ardhura bruto"].sum()
rev2 = data[data["Kategoria e produktit"] == cat2]["Te ardhura bruto"].sum()

st.write(f"{cat1}: {rev1} Lek")
st.write(f"{cat2}: {rev2} Lek")


from groq import Groq
from prompts import SYSTEM_PROMPT

st.header("💬 Ask your data (AI Assistant)")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

user_input = st.text_input("Write your question in natural language")

if user_input:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            temperature=0
        )

        generated_code = response.choices[0].message.content.strip()

        
        if "```" in generated_code:
            parts = generated_code.split("```")
            if len(parts) >= 2:
                generated_code = parts[1]

        generated_code = generated_code.replace("python", "").strip()

        st.subheader("Generated Code")
        st.code(generated_code, language="python")

        # Ekzekuto kodin
        local_vars = {"data": data}
        exec(generated_code, {}, local_vars)

        if "result" in local_vars:
            result = local_vars["result"]

            st.subheader("Result")

            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
                if result.shape[1] == 2:
                    st.bar_chart(result)
            else:
                st.write(result)
        else:
            st.error("The generated code did not return a variable named 'result'.")

    except Exception as e:
        st.error(f"Error: {e}")