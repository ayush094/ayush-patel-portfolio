"""Single source of truth for the resume content.

Both the DOCX and PDF builders read from this module, so the editable source
and the downloadable PDF never drift apart.

Verified against:
  - Ayush_Patel_Resume.pdf (CGPA 8.44, internship years, certifications, projects)
  - the previous resume (Oct 2025 start date, RAG/HR chatbot, SQL Server, FastAPI)
"""

NAME = "AYUSH PATEL"

HEADLINE = "Backend Software Engineer  |  Python · Django · REST APIs · PostgreSQL"

CONTACT = "Ahmedabad, India  ·  +91 72111 62350  ·  ayushgajera094@gmail.com"

LINKS = "buildwithayush.in  ·  github.com/ayush094  ·  linkedin.com/in/ayush-patel-53a920257"

SUMMARY = (
    "Backend-focused software developer with professional experience building Python and "
    "Django applications, REST APIs and relational data layers for enterprise systems. "
    "Works with Django REST Framework, PostgreSQL and Microsoft SQL Server, and delivers "
    "with Docker and Docker Compose. Also contributes to RAG-based AI features using LLMs "
    "and hybrid search. Looking for backend engineering roles where clean API design and "
    "reliable data handling matter."
)

EXPERIENCE = [
    {
        "title": "Software Developer — SrashtaSoft",
        "meta": "Ahmedabad, India  ·  Oct 2025 – Present",
        "bullets": [
            "Develop and maintain backend applications in Python and Django for enterprise business workflows.",
            "Design, implement and integrate REST APIs with Django REST Framework, including serialisation, validation and service integration.",
            "Work with PostgreSQL and Microsoft SQL Server on schema changes, migrations and SQL query optimisation for business reporting.",
            "Build and maintain Docker and Docker Compose environments to keep development and deployment consistent.",
            "Contribute to an AI-powered HR chatbot using retrieval-augmented generation (RAG), hybrid search and LLM integration; improve retrieval quality and answer grounding.",
            "Debug backend issues, support application testing and deployment, and collaborate with the team to deliver features and resolve defects.",
        ],
    },
    {
        "title": "Python Development Intern — Pyonix Technology",
        "meta": "2025",
        "bullets": [
            "Built backend logic and REST endpoints with Python and Django for web applications.",
            "Optimised database queries and improved API performance.",
            "Worked with the team on backend structure to keep application code maintainable.",
        ],
    },
    {
        "title": "Microsoft Data & AI Intern — Microsoft & CloudThat",
        "meta": "2024",
        "bullets": [
            "Applied AI/ML fundamentals and data handling techniques across Azure cloud workflows and data pipelines.",
            "Gained hands-on exposure to cloud-based data engineering and machine learning deployment practices.",
        ],
    },
]

PROJECTS = [
    {
        "title": "Enterprise ERP Platform",
        "tech": "Python · Django · DRF · PostgreSQL · React",
        "bullets": [
            "Backend development for an ERP platform covering contracts, work orders, maintenance, billing and operational alerts.",
            "Implemented REST APIs and role-based access control across business modules; client and internal details generalised.",
        ],
    },
    {
        "title": "AI-Powered Resume Screening & Recruiter Assistant",
        "tech": "Python · Django · React · LLMs · RAG · OCR",
        "bullets": [
            "Built a recruitment workflow that parses resumes, extracts candidate data, matches candidates to jobs and runs initial screening.",
            "Used OCR and LLM-based extraction with retrieval-augmented generation to ground matches in job requirements.",
        ],
    },
    {
        "title": "AI-Powered Database Chatbot (NL2SQL)",
        "tech": "Django · PostgreSQL · Docker Compose · LLMs",
        "bullets": [
            "Converts natural-language questions into validated SQL, with a JSON-based validation step before execution.",
            "Containerised with Docker Compose for a reproducible development and deployment setup.",
        ],
    },
    {
        "title": "SK Beauty — E-commerce Platform",
        "tech": "Django REST Framework · React · PostgreSQL · Razorpay",
        "bullets": [
            "Full-stack e-commerce platform with Google OAuth sign-in, Razorpay payments and product management workflows.",
            "Live at shreekrishnabeautyproducts.vercel.app.",
        ],
    },
]

SKILLS = [
    ("Languages", "Python, SQL, JavaScript, C"),
    ("Backend", "Django, Django REST Framework, REST APIs, FastAPI, Flask"),
    ("Databases", "PostgreSQL, Microsoft SQL Server, MySQL, SQLAlchemy"),
    (
        "AI & Search",
        "LLMs, Retrieval-Augmented Generation (RAG), Hybrid Search, Semantic Search, NL2SQL, OCR",
    ),
    ("DevOps & Tools", "Docker, Docker Compose, Jenkins, Git, Postman"),
    ("Supporting", "Redis, Celery, MQTT, React, NumPy, Pandas, scikit-learn, OpenCV"),
]

EDUCATION = [
    {
        "title": "B.Tech, Computer Engineering — Shree Swaminarayan Institute of Technology, Ahmedabad (GTU)",
        "meta": "2022 – 2026  ·  CGPA: 8.44 / 10",
    },
    {
        "title": "HSC, Science Stream — Sheth Nanubhai Vidhyamandir, Ahmedabad (GSEB)",
        "meta": "2021 – 2022  ·  72.67%",
    },
]

CERTIFICATIONS = [
    "Microsoft Data & AI Internship Certification — Microsoft & CloudThat, 2024",
    "Python Development Internship Certification — Pyonix Technology, 2025",
]
