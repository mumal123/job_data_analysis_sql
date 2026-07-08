
import os
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

load_dotenv() 
 
REQUIRED_VARS = ["PGHOST", "PGDATABASE", "PGUSER", "PGPASSWORD"]
missing = [v for v in REQUIRED_VARS if not os.getenv(v)]
if missing:
    raise RuntimeError(
        f"Missing required env vars: {', '.join(missing)}. "
        f"Copy .env.example to .env and fill in your credentials."
    )
 
DB_CONFIG = {
    "host": os.getenv("PGHOST"),
    "dbname": os.getenv("PGDATABASE"),
    "user": os.getenv("PGUSER"),
    "password": os.getenv("PGPASSWORD"),
    "port": os.getenv("PGPORT", "5432"),
}

SQL_DIR = os.path.dirname(os.path.abspath(__file__)) 
IMG_DIR = os.path.join(SQL_DIR, "images")
os.makedirs(IMG_DIR, exist_ok=True)
sns.set_theme(style="whitegrid")


def run_sql_file(conn, filename: str) -> pd.DataFrame:

    path = os.path.join(SQL_DIR, filename)
    with open(path, "r") as f:
        query = f.read()
    return pd.read_sql(query, conn)


def save_barh(df: pd.DataFrame, title: str, xlabel: str, filename: str, top_n: int = 10):
    
    label_col, value_col = df.columns[0], df.columns[1]
    plot_df = df.head(top_n).sort_values(value_col)

    plt.figure(figsize=(9, 6))
    sns.barplot(data=plot_df, x=value_col, y=label_col, color="#1F3864")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("")
    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, filename)
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved {out_path}")


def main():
    conn = psycopg2.connect(**DB_CONFIG)

    # 1. Top paying jobs -> bar chart
    df1 = run_sql_file(conn, "1top_paying_jobs.sql")
    save_barh(
        df1, "Top Paying Data Analyst Postings", "Annual Salary ($)",
        "top_paying_jobs.png",
    )

    # 3. Most in-demand skills -> bar chart
    df3 = run_sql_file(conn, "3most_in_demand_skills.sql")
    save_barh(
        df3, "Most In-Demand Skills", "Number of Postings",
        "most_in_demand_skills.png",
    )

    # 4. Top skills based on salary -> bar chart
    df4 = run_sql_file(conn, "4top_skills_based_on_salary.sql")
    save_barh(
        df4, "Top Skills by Average Salary", "Average Annual Salary ($)",
        "top_skills_by_salary.png",
    )


    conn.close()
    print("\nDone. All charts saved to ./images/")


if __name__ == "__main__":
    main()