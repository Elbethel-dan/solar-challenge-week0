# ☀️ Moonlight Solar Energy Assessment

This task focuses on analyzing solar energy data to help MoonLight Energy Solutions identify regions with high solar potential. It involves profiling, cleaning, and exploring datasets from multiple countries, detecting patterns and anomalies through EDA and statistical analysis, and comparing metrics like GHI, DNI, and DHI across regions. The final step includes building an interactive Streamlit dashboard to visualize insights, enabling data-driven recommendations for solar investment and sustainability planning.

---

## ⚙️ Reproduce this environment

To set up and reproduce this project locally, follow the steps below:

## 1. Clone the repository
```bash
   git clone https://github.com/Elbethel-dan/solar-challenge-week0.git
```
## 2. Create and activate a virtual environment (recommended)

   **For macOS / Linux**
   ```bash
     python3 -m venv week0
     source week0/bin/activate
   ```

   **For Windows**
   ```bash
     python -m venv week0
     week0\Scripts\activate
   ```
## 3. Install dependencies
  ```bash
     pip install -r requirements.txt
 ```
# West Africa Solar Potential Dashboard

An **interactive Streamlit dashboard** comparing solar radiation (GHI, DNI, DHI) across **Benin, Sierra Leone, and Togo** using **cleaned solar energy data**.

Live app: [https://solar-challenge-week0.streamlit.app](https://solar-challenge-week0-h4yobtuwm7thk4nq4gt58h.streamlit.app/)

---

## Features

- **Interactive filters**: Select countries & metric (GHI/DNI/DHI)
- **Box plots**, **bar charts**, **daily profiles**, **capacity factor**, **temperature impact**
- **Data loaded from Google Drive** (no local files needed)
- **Clean, professional UI** with sidebar status
- **Fully deployed on Streamlit Cloud**
  
## To run the Streamlit app
   ```bash
      streamlit run app/main.py
   ```
   
