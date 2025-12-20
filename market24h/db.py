import psycopg2
import pandas as pd
import streamlit as st

def get_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres.vmrlghpogwttgbtnuysa",
        password="!C4QkNyrUc9b8Ah",
        host="aws-0-us-west-2.pooler.supabase.com",
        port=5432
    )

def save_dataframe(df, table_name):
    conn = get_connection()
    cur = conn.cursor()
    # Create table if not exists
    columns = ', '.join([f'"{col}" TEXT' for col in df.columns])
    cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns});')
    # Insert data
    for row in df.itertuples(index=False):
        values = ', '.join([f"'{str(val)}'" for val in row])
        cur.execute(f'INSERT INTO {table_name} VALUES ({values});')
    conn.commit()
    cur.close()
    conn.close()
