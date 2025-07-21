import os

folders = [
    "data/bronze", "data/silver", "data/gold",
    "scripts", "warehouse", "notebooks"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

with open(".env", "w") as f:
    f.write("# Plaid API Keys go here\n")

with open("requirements.txt", "w") as f:
    f.write("pandas\nrequests\nsqlalchemy\npyodbc\nplaid-python\npython-dotenv\n")

print("Folder structure and config files initialized.")
