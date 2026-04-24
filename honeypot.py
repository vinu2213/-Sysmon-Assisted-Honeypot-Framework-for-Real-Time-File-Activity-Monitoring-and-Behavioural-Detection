import os

def create_honeypot():
    path = "honeypot_folder"
    os.makedirs(path, exist_ok=True)

    files = {
        "passwords.txt": "User passwords",
        "bank_details.txt": "Bank account info",
        "employee_data.txt": "Employee salary data",
        "confidential.txt": "Top secret data"
    }

    for file, content in files.items():
        with open(os.path.join(path, file), "w") as f:
            f.write(content)

    return "Honeypot files created successfully!"