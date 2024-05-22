# Conversion type
# sql -> df : pd.read_sql()
# csv -> df : pd.read_csv(".csv")
# json -> df : pd.read_json(".json")
# df -> csv : df.to_csv(".csv", index=False)
# df -> sql : df.to_sql("<table_name>", sqlite_connection, if_exists="replace", index_label="index")
# df -> json : df.to_json(".json", indent=4, orient="records")
# dict -> df : pd.DataFrame(<dict>)
# df -> dict : df.to_dict()





import pandas as pd
## csv -> df
file = pd.read_csv("mtcars.csv")
# 4 cars with 3 attributes
four_cars = file[:4][["brand", "mpg", "wt"]].to_dict(orient="list")



## df -> csv
file.to_csv("mtcars_ind.csv", index=True)
print(file.to_csv())



## dict -> df
four_cars = {
    'brand': ['Mazda RX4', 'Mazda RX4 Wag', 'Datsun 710', 'Hornet 4 Drive'],
    'mpg': [21.0, 21.0, 22.8, 21.4],
    'wt': [2.62, 2.875, 2.32, 3.215],
}


mtcars_pd = pd.DataFrame(four_cars)
mtcars_pd[mtcars_pd["wt"] > 2.5]

mtcars_pd.to_csv("mtcars_pd.csv", index=True)

## df –> dict
mtcars_pd.to_dict()
mtcars_pd.to_dict("list")
mtcars_pd.to_dict("records")





# Create an in-memory SQLite database.
from sqlalchemy import create_engine
engine = create_engine('sqlite://', echo=False)
mtcars_pd.to_sql(name='emplo_db_name', con=engine)

# Fetch data from in-memory database.
from sqlalchemy import text
with engine.connect() as conn:
    conn.execute(text("SELECT * FROM emplo_db_name")).fetchall()


# merge with another df -> db
## df -> db # Save database to SQLite3
from sqlalchemy import create_engine
engine = create_engine('sqlite:///mtcars_4.db', echo=True)
sqlite_connection = engine.connect()
mtcars_pd.to_sql("mtcars", sqlite_connection, if_exists="replace", index_label="index")
sqlite_connection.close()


## db -> df
from sqlalchemy import create_engine
engine = create_engine('sqlite:///mtcars_4.db', echo=True)
with engine.connect() as conn, conn.begin():
    mtcars_from_db = pd.read_sql("mtcars", conn, index_col="index")
mtcars_from_db










# mtcars
import pandas as pd

mtcars = pd.read_csv('https://gist.githubusercontent.com/ZeccaLehn/4e06d2575eb9589dbe8c365d61cb056c/raw/64f1660f38ef523b2a1a13be77b002b98665cdfe/mtcars.csv')
mtcars.columns
mtcars.rename(columns={'Unnamed: 0':'brand'}, inplace=True)

## df -> csv
mtcars.to_csv("mtcars.csv", index=False)

## df -> db
from sqlalchemy import create_engine
engine = create_engine('sqlite:///mtcars.db')
sqlite_connection = engine.connect()
mtcars.to_sql("mtcars", sqlite_connection, if_exists="replace")
sqlite_connection.close()








## df -> json
mtcars.to_json("mtcars.json", indent=4, orient="records")

emp_data = {
    'name': ['John', 'Alice', 'Bob', 'Emma'],
    'managerId': [1, 2, 2, 1],
    'salary': [50000, 60000, 55000, 48000]
}
emp_df = pd.DataFrame(emp_data)
emp_df.to_json("employee.json", indent=4, orient="records")




## json -> df
mtcars_read = pd.read_json("mtcars.json")








