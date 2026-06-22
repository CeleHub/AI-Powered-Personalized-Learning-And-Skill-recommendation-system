import csv

courses = [
    # AI & TECH
    [1, "Machine Learning Specialization", "Coursera", "AI", "Beginner", "Python,Linear Algebra,Statistics", "3 months"],
    [2, "Deep Learning Specialization", "Coursera", "AI", "Intermediate", "Neural Networks,Python,TensorFlow", "4 months"],
    [3, "AI For Everyone", "Coursera", "AI", "Beginner", "AI Literacy,Business Strategy", "1 month"],
    [4, "The Web Developer Bootcamp", "Udemy", "Web Development", "Beginner", "HTML,CSS,JavaScript,NodeJS", "6 months"],
    [5, "React - The Complete Guide", "Udemy", "Web Development", "Intermediate", "React,JavaScript,Hooks", "3 months"],
    [6, "Google Cybersecurity Certificate", "Coursera", "Cybersecurity", "Beginner", "Linux,Network Security,Python", "6 months"],
    [7, "Data Science Specialization", "Coursera", "Data Science", "Beginner", "R,Data Visualization,Statistics", "5 months"],

    # HEALTHCARE & MEDICINE
    [20, "Anatomy and Physiology Specialization", "Coursera", "Healthcare", "Beginner", "Human Anatomy,Systems,Physiology", "4 months"],
    [21, "Nursing Case Management", "Coursera", "Healthcare", "Intermediate", "Patient Advocacy,Clinical Research", "2 months"],
    [22, "Foundations of Public Health", "Coursera", "Healthcare", "Beginner", "Epidemiology,Policy,Health Promotion", "3 months"],
    [23, "Clinical Research Mastery", "Udemy", "Healthcare", "Intermediate", "Clinical Trials,Ethics,Data Analysis", "4 months"],
    [24, "NMCN Professional Exam Prep (Nursing)", "Medical Academy", "Healthcare", "Advanced", "Nursing Ethics,Midwifery,Nursing Law", "6 months"],
    [25, "MDCN Medical Licensing Exam Prep", "Doctor Hub", "Healthcare", "Advanced", "Internal Medicine,Surgery,Pediatrics", "12 months"],
    [26, "Medical Terminology for Beginners", "Coursera", "Healthcare", "Beginner", "Medical Coding,Terminology", "1 month"],
    [27, "Pediatric Nursing Fundamentals", "Udemy", "Healthcare", "Beginner", "Child Care,Pediatrics", "3 months"],
    [28, "Pharmacy Technician Basics", "Udemy", "Healthcare", "Beginner", "Pharmacology,Prescriptions", "4 months"],

    # LAW & HUMANITIES
    [30, "Introduction to English Common Law", "Coursera", "Law", "Beginner", "Constitutional Law,Legal Systems", "2 months"],
    [31, "Criminal Justice & Law Foundations", "Coursera", "Law", "Beginner", "Criminal Law,Sociology", "3 months"],
    [32, "Contract Law Mastery", "Udemy", "Law", "Intermediate", "Contracts,Trade Law,Negotiation", "4 months"],
    [33, "Nigerian Law School Exam Prep", "Justice Chambers", "Law", "Advanced", "Litigation,Commercial Law,Nigerian Legal System", "9 months"],
    [34, "International Human Rights Law", "Coursera", "Law", "Intermediate", "Human Rights,Global Policy", "3 months"],
    [35, "Psychological First Aid", "Coursera", "Social Science", "Beginner", "Psychology,Mental Health Support", "1 month"],
    [36, "NBA Professional Conduct & Ethics", "Legal Nigeria", "Law", "Advanced", "Legal Ethics,Code of Conduct", "2 months"],

    # BUSINESS, FINANCE & PROFESSIONAL CERTS (NIGERIA)
    [40, "Financial Accounting Fundamentals", "Coursera", "Business", "Beginner", "Bookkeeping,Ledgers,Tax", "3 months"],
    [41, "ICAN Professional Exams (Skill Level)", "ICAN Nigeria", "Business", "Advanced", "Financial Reporting,Audit,Management Accounting", "6 months"],
    [42, "ANAN Professional Diploma in Accounting", "ANAN Nigeria", "Business", "Advanced", "Public Sector Accounting,Treasury Management", "12 months"],
    [43, "CIPM Professional Certification (HR)", "CIPM Nigeria", "Business", "Advanced", "Human Resources,Labor Laws", "8 months"],
    [44, "Chartered Institute of Bankers (CIBN) Prep", "CIBN Nigeria", "Business", "Advanced", "Banking Laws,Finance Management,Ethics", "10 months"],
    [45, "Small Business Management for Entrepreneurs", "Udemy", "Business", "Beginner", "Marketing,Strategy,Fundraising", "2 months"],
    [46, "NIPR Public Relations Certification", "NIPR Nigeria", "Business", "Intermediate", "Public Relations,Media Management", "4 months"],
    [47, "Auditing & Assurance Specialization", "Coursera", "Business", "Intermediate", "Auditing,Internal Controls", "4 months"],
    [48, "Supply Chain Management Specialization", "Coursera", "Business", "Beginner", "Logistics,Procurement,Operations", "5 months"],

    # ENGINEERING & CONSTRUCTION (NIGERIA)
    [50, "AutoCAD for Architects and Engineers", "Udemy", "Engineering", "Beginner", "Drafting,CAD,2D/3D Design", "4 months"],
    [51, "Structural Engineering Basics", "Coursera", "Engineering", "Intermediate", "Statics,Building Materials,Structural Design", "5 months"],
    [52, "COREN Engineering Professional Review Prep", "NSE Nigeria", "Engineering", "Advanced", "Engineering Codes,Ethics,Project Management", "6 months"],
    [53, "ARCON Architectural Professional Exams", "ARCON Nigeria", "Architecture", "Advanced", "Building Design,Urban Planning,Nigeria Building Code", "12 months"],
    [54, "Quantity Surveying: Estimating & Costing", "Udemy", "Engineering", "Intermediate", "Cost Management,Tendering", "3 months"],
    [55, "Safe Site Management (Construction)", "Coursera", "Engineering", "Beginner", "Safety,OSHA,Risk Assessment", "2 months"],
    [56, "Renewable Energy Systems", "Coursera", "Engineering", "Beginner", "Solar Energy,Wind Power", "3 months"],

    # AGRICULTURE & ENVIRONMENT
    [60, "Sustainable Agricultural Land Management", "Coursera", "Agriculture", "Beginner", "Soil Management,Crop Rotation", "3 months"],
    [61, "Agribusiness Management", "Coursera", "Agriculture", "Intermediate", "Food Supply Chain,Agriculture Economics", "4 months"],
    [62, "Food Tech & Security", "EdX", "Agriculture", "Intermediate", "Food Preservation,Security Systems", "3 months"],
    [63, "Animal Husbandry Fundamentals", "Udemy", "Agriculture", "Beginner", "Livestock Management,Veterinary Basics", "2 months"],
    [64, "Environmental Science & Sustainability", "Coursera", "Science", "Beginner", "Climate Change,Renewables", "4 months"],
    [65, "Organic Farming Specialization", "Udemy", "Agriculture", "Beginner", "Organic Methods,Soil Science", "3 months"],

    # ARTS, DESIGN & MEDIA
    [70, "Graphic Design Professional Certificate", "Coursera", "Arts", "Beginner", "Photoshop,Illustration,Layout", "6 months"],
    [71, "Fashion Design Core Skills", "Udemy", "Arts", "Beginner", "Pattern Making,Sewing,Textiles", "5 months"],
    [72, "Mass Communication & Journalism Basics", "Coursera", "Media", "Beginner", "Reporting,Media Ethics", "3 months"],
    [73, "Interior Design Fundamentals", "Udemy", "Arts", "Intermediate", "Space Planning,Colors,Styling", "4 months"],
    [74, "Music Theory Specialization", "Coursera", "Arts", "Beginner", "Harmony,Composition", "3 months"],
    [75, "User Experience (UX) Design", "Coursera", "Arts", "Beginner", "UX Research,Wireframing", "6 months"],

    # EDUCATION & PROJECT MANAGEMENT
    [80, "Foundations of Teaching & Learning", "Coursera", "Education", "Beginner", "Pedagogy,Curriculum,EdTech", "3 months"],
    [81, "Project Management Professional (PMP)", "Coursera", "Business", "Intermediate", "Agile,Waterfall,Project Cycle", "6 months"],
    [82, "NIM Management Certification", "NIM Nigeria", "Business", "Intermediate", "Nigerian Management,Leadership", "4 months"],
    [83, "Effective Classroom Management", "Udemy", "Education", "Intermediate", "Instructional Design,Classroom Ethics", "2 months"]
]

# Cleanup IDs and format
formatted_courses = []
for i, c in enumerate(courses):
    c[0] = i + 1 # Dynamic ID
    formatted_courses.append(c)

with open('data/courses.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["id", "title", "provider", "category", "difficulty", "skills_covered", "duration"])
    writer.writerows(formatted_courses)

print(f"Courses expanded successfully. Total: {len(formatted_courses)}")
