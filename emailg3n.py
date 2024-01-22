names = [
    "Liam", "Emma", "Noah", "Olivia", "Oliver", "Ava", "Elijah", "Isabella", "William", "Sophia",
    "James", "Mia", "Benjamin", "Charlotte", "Lucas", "Amelia", "Henry", "Harper", "Alexander", "Evelyn",
    "Michael", "Abigail", "Daniel", "Emily", "Matthew", "Elizabeth", "Aiden", "Sofia", "Jackson", "Avery",
    "Sebastian", "Ella", "David", "Scarlett", "Joseph", "Grace", "Carter", "Chloe", "Owen", "Victoria",
    "Wyatt", "Riley", "John", "Aria", "Jack", "Lily", "Luke", "Zoey", "Jayden", "Lillian",
    "Gabriel", "Addison", "Isaac", "Layla", "Anthony", "Natalie", "Grayson", "Hannah", "Julian", "Brooklyn",
    "Levi", "Zoe", "Christopher", "Penelope", "Joshua", "Eleanor", "Andrew", "Lucy", "Lincoln", "Avery",
    "Mateo", "Ellie", "Ryan", "Skylar", "Jaxon", "Nora", "Nathan", "Leah", "Aaron", "Savannah",
    "Isaac", "Claire", "Henry", "Violet", "Charles", "Stella", "Caleb", "Aurora", "Hunter", "Aurora",
    "Christian", "Hazel", "Eli", "Paisley", "Landon", "Audrey", "Adrian", "Bella", "Jonathan", "Mila"
]

# Random email generation or use a worldlist for the checker
def generate_emails(names):
    with open("generated_emails.txt", "w") as file:
        for name in names:
            for index in range(101):  
                email = f"{name.lower()}{index}@gmail.com\n"
                file.write(email)

generate_emails(names)
