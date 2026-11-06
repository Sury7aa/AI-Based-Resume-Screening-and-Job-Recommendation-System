
import re

SKILLS_DATABASE = [
    # Programming languages
    "Python", "Java", "JavaScript", "TypeScript",
    "C++", "C", "C#", "Kotlin", "Dart", "PHP", "Ruby",
    "Go", "R", "Bash",

    # Web development
    "HTML", "CSS", "React", "Node.js",
    "Django", "Flask", "Spring Boot",
    "Bootstrap", "REST API", "JSON",
    "Frontend Development", "Backend Development",

    # Databases
    "SQL", "MySQL", "PostgreSQL", "MongoDB",
    "Oracle", "Database Management",
    "Data Warehousing",

    # Data analytics
    "Pandas", "NumPy", "Matplotlib",
    "Power BI", "Tableau", "Excel",
    "Data Analysis", "Data Visualization",
    "Data Cleaning", "ETL", "Spark", "Hadoop",

    # AI and Machine Learning
    "Machine Learning", "Deep Learning",
    "Scikit-learn", "TensorFlow", "PyTorch",
    "NLP", "NLTK", "spaCy", "OpenCV",
    "Neural Networks", "Prompt Engineering",
    "Computer Vision",

    # Cybersecurity
    "Cybersecurity", "Wireshark", "Nmap",
    "Kali Linux", "Burp Suite", "Metasploit",
    "OWASP", "SIEM", "Nessus",
    "Digital Forensics", "Threat Intelligence",
    "Vulnerability Assessment", "Firewalls",
    "Cloud Security", "IAM",

    # Networking
    "Networking", "TCP/IP", "CCNA",
    "Routing", "Switching",

    # Cloud and DevOps
    "AWS", "Azure", "Docker", "Kubernetes",
    "Jenkins", "Git", "Linux",
    "Windows Server", "Cloud Computing",
    "YAML",

    # Software engineering
    "OOP", "Data Structures", "Algorithms",
    "Software Testing", "Manual Testing",
    "Selenium", "Test Automation",
    "Android", "Flutter",

    # Other technical skills
    "Troubleshooting", "Research",
    "Communication"
]


def extract_skills(text):
    found_skills = []
    text = text.lower()

    for skill in SKILLS_DATABASE:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


def analyze_missing_skills(resume_skills, job_skills):
    resume_set = {skill.lower().strip() for skill in resume_skills}

    required_skills = [
        skill.strip()
        for skill in job_skills.split(",")
        if skill.strip()
    ]

    matching_skills = []
    missing_skills = []

    for skill in required_skills:
        if skill.lower() in resume_set:
            matching_skills.append(skill)
        else:
            missing_skills.append(skill)

    return {
        "matching_skills": matching_skills,
        "missing_skills": missing_skills
    }


if __name__ == "__main__":
    sample_resume = """
    Cybersecurity student with knowledge of Python,
    Kali Linux, Networking, Wireshark, Nmap,
    SQL, Machine Learning, Docker and AWS.
    """

    skills = extract_skills(sample_resume)

    print("\nEXTRACTED SKILLS")
    print("----------------")
    print(skills)

    job_skills = "Python, Wireshark, Nmap, SIEM, Burp Suite"

    result = analyze_missing_skills(skills, job_skills)

    print("\nMATCHING SKILLS")
    print(result["matching_skills"])

    print("\nMISSING SKILLS")
    print(result["missing_skills"])
