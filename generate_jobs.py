import pandas as pd

from pathlib import Path



jobs = [

    # CYBERSECURITY (10)
    {

        "job_id": 1, "job_title": "Cybersecurity Analyst",

        "category": "Cybersecurity",

        "description": "Monitor security threats, analyze vulnerabilities and protect computer systems.",

        "skills": "Python, Linux, Networking, Wireshark, Nmap, SIEM, Cybersecurity",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Monitor networks, investigate security alerts and identify vulnerabilities."

    },

    {

        "job_id": 2, "job_title": "SOC Analyst",

        "category": "Cybersecurity",

        "description": "Monitor security operations and investigate suspicious activities.",

        "skills": "SIEM, Networking, Linux, Cybersecurity, Python, Wireshark",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Analyze security logs and respond to potential incidents."

    },

    {

        "job_id": 3, "job_title": "Penetration Tester",

        "category": "Cybersecurity",

        "description": "Perform authorized security testing to discover application and network vulnerabilities.",

        "skills": "Kali Linux, Python, Nmap, Burp Suite, Metasploit, Networking",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Conduct penetration tests and document security weaknesses."

    },

    {

        "job_id": 4, "job_title": "Security Engineer",

        "category": "Cybersecurity",

        "description": "Design and maintain secure systems, networks and infrastructure.",

        "skills": "Python, Linux, Networking, Firewalls, Cloud Security, Cybersecurity",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Implement security controls and improve infrastructure protection."

    },

    {

        "job_id": 5, "job_title": "Application Security Analyst",

        "category": "Cybersecurity",

        "description": "Identify vulnerabilities in software applications and secure development processes.",

        "skills": "Python, Java, OWASP, Burp Suite, SQL, Cybersecurity",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Review application security and perform vulnerability assessments."

    },

    {

        "job_id": 6, "job_title": "Digital Forensics Analyst",

        "category": "Cybersecurity",

        "description": "Investigate digital evidence and analyze security incidents.",

        "skills": "Linux, Cybersecurity, Networking, Python, Digital Forensics",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Collect, preserve and analyze digital evidence."

    },

    {

        "job_id": 7, "job_title": "Network Security Analyst",

        "category": "Cybersecurity",

        "description": "Protect networks using monitoring, firewalls and security technologies.",

        "skills": "Networking, TCP/IP, Wireshark, Firewalls, Linux, Nmap",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Monitor network traffic and investigate suspicious connections."

    },

    {

        "job_id": 8, "job_title": "Cloud Security Analyst",

        "category": "Cybersecurity",

        "description": "Protect cloud platforms, workloads and infrastructure.",

        "skills": "AWS, Azure, Linux, Networking, IAM, Cloud Security",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Review cloud permissions and monitor cloud security."

    },

    {

        "job_id": 9, "job_title": "Threat Intelligence Analyst",

        "category": "Cybersecurity",

        "description": "Research cyber threats and identify emerging attack techniques.",

        "skills": "Cybersecurity, Python, Linux, Networking, Threat Intelligence, SIEM",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Analyze threat information and prepare security reports."

    },

    {

        "job_id": 10, "job_title": "Vulnerability Assessment Analyst",

        "category": "Cybersecurity",

        "description": "Identify and assess vulnerabilities in systems and networks.",

        "skills": "Nmap, Linux, Python, Networking, Nessus, Cybersecurity",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Perform vulnerability scans and track remediation."

    },



    # SOFTWARE DEVELOPMENT (10)
    {

        "job_id": 11, "job_title": "Python Developer",

        "category": "Software Development",

        "description": "Build software applications and backend services using Python.",

        "skills": "Python, Django, Flask, SQL, Git, REST API",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Develop Python applications and maintain code."

    },

    {

        "job_id": 12, "job_title": "Java Developer",

        "category": "Software Development",

        "description": "Develop enterprise applications using Java and object-oriented programming.",

        "skills": "Java, Spring Boot, SQL, OOP, Git, REST API",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Develop and test Java-based applications."

    },

    {

        "job_id": 13, "job_title": "Frontend Developer",

        "category": "Software Development",

        "description": "Build responsive user interfaces for web applications.",

        "skills": "HTML, CSS, JavaScript, React, Bootstrap, Git",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Create responsive websites and interactive interfaces."

    },

    {

        "job_id": 14, "job_title": "Backend Developer",

        "category": "Software Development",

        "description": "Build server-side applications, APIs and database systems.",

        "skills": "Python, Java, SQL, Node.js, REST API, Git",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Develop APIs and manage server-side logic."

    },

    {

        "job_id": 15, "job_title": "Full Stack Developer",

        "category": "Software Development",

        "description": "Develop complete web applications across frontend and backend.",

        "skills": "HTML, CSS, JavaScript, React, Node.js, SQL, Git",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Build and maintain full-stack web applications."

    },

    {

        "job_id": 16, "job_title": "C++ Developer",

        "category": "Software Development",

        "description": "Develop high-performance applications using C++ and data structures.",

        "skills": "C++, Data Structures, Algorithms, OOP, Git",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Write efficient code and debug software."

    },

    {

        "job_id": 17, "job_title": "Mobile App Developer",

        "category": "Software Development",

        "description": "Develop mobile applications for Android and cross-platform devices.",

        "skills": "Java, Kotlin, Flutter, Dart, Android, Git",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Build, test and maintain mobile applications."

    },

    {

        "job_id": 18, "job_title": "Software Tester",

        "category": "Software Development",

        "description": "Test software applications and identify functional defects.",

        "skills": "Manual Testing, Selenium, Python, SQL, Test Automation",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Prepare test cases and report software defects."

    },

    {

        "job_id": 19, "job_title": "DevOps Developer",

        "category": "Software Development",

        "description": "Automate software development, deployment and infrastructure workflows.",

        "skills": "Linux, Docker, Kubernetes, Git, Jenkins, Python",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Maintain CI/CD pipelines and automate deployments."

    },

    {

        "job_id": 20, "job_title": "API Developer",

        "category": "Software Development",

        "description": "Design and develop REST APIs for software applications.",

        "skills": "Python, Flask, Django, REST API, SQL, JSON",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Create and document application programming interfaces."

    },



    # DATA AND ANALYTICS (10)
    {

        "job_id": 21, "job_title": "Data Analyst",

        "category": "Data & Analytics",

        "description": "Analyze datasets and generate reports using programming and visualization tools.",

        "skills": "Python, SQL, Excel, Pandas, NumPy, Power BI, Matplotlib",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Clean data, analyze trends and prepare reports."

    },

    {

        "job_id": 22, "job_title": "Business Intelligence Analyst",

        "category": "Data & Analytics",

        "description": "Create business reports and dashboards using analytical tools.",

        "skills": "SQL, Power BI, Tableau, Excel, Data Visualization",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Build dashboards and communicate business insights."

    },

    {

        "job_id": 23, "job_title": "Data Engineer",

        "category": "Data & Analytics",

        "description": "Build data pipelines and maintain data processing infrastructure.",

        "skills": "Python, SQL, Spark, Hadoop, AWS, ETL",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Develop data pipelines and manage data workflows."

    },

    {

        "job_id": 24, "job_title": "Database Analyst",

        "category": "Data & Analytics",

        "description": "Analyze database performance and maintain structured data.",

        "skills": "SQL, MySQL, PostgreSQL, Excel, Database Management",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Maintain databases and analyze stored information."

    },

    {

        "job_id": 25, "job_title": "Reporting Analyst",

        "category": "Data & Analytics",

        "description": "Prepare operational reports and data visualizations.",

        "skills": "Excel, SQL, Power BI, Python, Data Visualization",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Generate reports and track performance metrics."

    },

    {

        "job_id": 26, "job_title": "Business Analyst",

        "category": "Data & Analytics",

        "description": "Analyze business requirements and translate them into technical solutions.",

        "skills": "SQL, Excel, Power BI, Communication, Data Analysis",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Gather requirements and prepare business analysis reports."

    },

    {

        "job_id": 27, "job_title": "Data Quality Analyst",

        "category": "Data & Analytics",

        "description": "Validate datasets and improve data accuracy and consistency.",

        "skills": "Python, SQL, Excel, Pandas, Data Cleaning",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Identify data errors and maintain data quality."

    },

    {

        "job_id": 28, "job_title": "SQL Developer",

        "category": "Data & Analytics",

        "description": "Develop SQL queries and optimize relational databases.",

        "skills": "SQL, MySQL, PostgreSQL, Database Management, Python",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Write queries and improve database performance."

    },

    {

        "job_id": 29, "job_title": "Data Visualization Analyst",

        "category": "Data & Analytics",

        "description": "Present complex data through interactive charts and dashboards.",

        "skills": "Python, Matplotlib, Plotly, Power BI, Tableau, Pandas",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Create visual reports and interactive dashboards."

    },

    {

        "job_id": 30, "job_title": "ETL Developer",

        "category": "Data & Analytics",

        "description": "Build extract transform and load workflows for data systems.",

        "skills": "SQL, Python, ETL, AWS, Spark, Data Warehousing",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Develop and maintain data integration pipelines."

    },



    # AI AND MACHINE LEARNING (10)
    {

        "job_id": 31, "job_title": "Machine Learning Engineer",

        "category": "AI & Machine Learning",

        "description": "Develop machine learning models using Python and machine learning frameworks.",

        "skills": "Python, Machine Learning, Scikit-learn, TensorFlow, Pandas, NumPy",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Train, evaluate and deploy machine learning models."

    },

    {

        "job_id": 32, "job_title": "AI Engineer",

        "category": "AI & Machine Learning",

        "description": "Develop artificial intelligence applications and intelligent software systems.",

        "skills": "Python, NLP, Machine Learning, Deep Learning, TensorFlow, PyTorch",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Build and integrate AI-powered applications."

    },

    {

        "job_id": 33, "job_title": "NLP Engineer",

        "category": "AI & Machine Learning",

        "description": "Build natural language processing applications and text analysis systems.",

        "skills": "Python, NLP, NLTK, spaCy, Machine Learning, Deep Learning",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Develop text classification and language processing systems."

    },

    {

        "job_id": 34, "job_title": "Computer Vision Engineer",

        "category": "AI & Machine Learning",

        "description": "Develop image processing and computer vision applications.",

        "skills": "Python, OpenCV, TensorFlow, PyTorch, Deep Learning",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Build image recognition and visual detection systems."

    },

    {

        "job_id": 35, "job_title": "AI Research Assistant",

        "category": "AI & Machine Learning",

        "description": "Support AI research and experiment with machine learning algorithms.",

        "skills": "Python, Machine Learning, NumPy, Pandas, Research",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Assist with experiments and research documentation."

    },

    {

        "job_id": 36, "job_title": "Deep Learning Engineer",

        "category": "AI & Machine Learning",

        "description": "Develop neural network models for complex prediction tasks.",

        "skills": "Python, Deep Learning, TensorFlow, PyTorch, Neural Networks",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Design and optimize deep learning models."

    },

    {

        "job_id": 37, "job_title": "AI Application Developer",

        "category": "AI & Machine Learning",

        "description": "Integrate AI models into web and software applications.",

        "skills": "Python, Flask, Streamlit, APIs, Machine Learning, Git",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Build user-facing applications powered by AI."

    },

    {

        "job_id": 38, "job_title": "ML Data Analyst",

        "category": "AI & Machine Learning",

        "description": "Prepare datasets and analyze data for machine learning projects.",

        "skills": "Python, Pandas, NumPy, Scikit-learn, SQL, Data Cleaning",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Prepare training datasets and evaluate data quality."

    },

    {

        "job_id": 39, "job_title": "Generative AI Developer",

        "category": "AI & Machine Learning",

        "description": "Develop applications using large language models and generative AI.",

        "skills": "Python, NLP, APIs, Machine Learning, PyTorch, Prompt Engineering",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Build and evaluate generative AI applications."

    },

    {

        "job_id": 40, "job_title": "AI Model Evaluator",

        "category": "AI & Machine Learning",

        "description": "Evaluate machine learning model performance and prediction quality.",

        "skills": "Python, Scikit-learn, Pandas, NumPy, Machine Learning",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Test models and document performance results."

    },



    # CLOUD AND NETWORKING (10)
    {

        "job_id": 41, "job_title": "Cloud Engineer",

        "category": "Cloud & Networking",

        "description": "Manage cloud infrastructure and cloud-based services.",

        "skills": "AWS, Azure, Linux, Docker, Kubernetes, Networking",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Deploy and maintain cloud infrastructure."

    },

    {

        "job_id": 42, "job_title": "Network Engineer",

        "category": "Cloud & Networking",

        "description": "Configure and troubleshoot computer networks.",

        "skills": "Networking, CCNA, TCP/IP, Routing, Switching, Linux",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Maintain network connectivity and troubleshoot faults."

    },

    {

        "job_id": 43, "job_title": "AWS Cloud Associate",

        "category": "Cloud & Networking",

        "description": "Support cloud deployment and AWS infrastructure services.",

        "skills": "AWS, Linux, Python, Networking, Cloud Computing",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Assist with AWS resources and cloud deployments."

    },

    {

        "job_id": 44, "job_title": "Azure Cloud Engineer",

        "category": "Cloud & Networking",

        "description": "Deploy and manage Microsoft Azure cloud resources.",

        "skills": "Azure, Linux, Networking, Docker, Cloud Computing",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Manage Azure services and monitor cloud infrastructure."

    },

    {

        "job_id": 45, "job_title": "Network Administrator",

        "category": "Cloud & Networking",

        "description": "Maintain network devices, connectivity and infrastructure.",

        "skills": "Networking, TCP/IP, Linux, Routing, Switching, Firewalls",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Configure network devices and resolve connectivity issues."

    },

    {

        "job_id": 46, "job_title": "DevOps Engineer",

        "category": "Cloud & Networking",

        "description": "Automate infrastructure and manage continuous integration pipelines.",

        "skills": "Linux, Docker, Kubernetes, AWS, Jenkins, Git, Python",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Automate builds, testing and software deployment."

    },

    {

        "job_id": 47, "job_title": "System Administrator",

        "category": "Cloud & Networking",

        "description": "Maintain computer systems, servers and operating environments.",

        "skills": "Linux, Windows Server, Networking, Bash, Security",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Manage servers and troubleshoot system issues."

    },

    {

        "job_id": 48, "job_title": "Cloud Support Associate",

        "category": "Cloud & Networking",

        "description": "Provide technical support for cloud services and infrastructure.",

        "skills": "AWS, Azure, Linux, Networking, Troubleshooting",

        "experience_level": "Fresher", "min_experience": 0,

        "responsibilities": "Resolve cloud service issues and assist customers."

    },

    {

        "job_id": 49, "job_title": "Infrastructure Engineer",

        "category": "Cloud & Networking",

        "description": "Maintain IT infrastructure, servers and network systems.",

        "skills": "Linux, Networking, AWS, Docker, Windows Server",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Maintain infrastructure availability and performance."

    },

    {

        "job_id": 50, "job_title": "Kubernetes Administrator",

        "category": "Cloud & Networking",

        "description": "Manage containerized applications and Kubernetes clusters.",

        "skills": "Kubernetes, Docker, Linux, AWS, Networking, YAML",

        "experience_level": "Junior", "min_experience": 1,

        "responsibilities": "Deploy and monitor containerized applications."

    }

]



df = pd.DataFrame(jobs)



output_path = Path(__file__).resolve().parent / "data" / "jobs.csv"

df.to_csv(output_path, index=False)



print("===================================")

print(" JOB DATASET GENERATED SUCCESSFULLY")

print("===================================")

print("Total job profiles:", len(df))

print("\nJobs by category:")

print(df["category"].value_counts().to_string())

print("\nExperience levels:")

print(df["experience_level"].value_counts().to_string())

print("\nSaved to:", output_path)
