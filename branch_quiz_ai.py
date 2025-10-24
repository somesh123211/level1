# branch_quiz_ai.py

quiz_topics = {
    "AI": {
        1: [
            "Fundamentals of Artificial Intelligence",
            "Data Structures and Algorithms",
            "Database Management Systems"
        ],
        2: [
            "Machine Learning Basics",
            "Neural Networks and Deep Learning",
            "Natural Language Processing"
        ],
        3: [
            "Reinforcement Learning",
            "Computer Vision",
            "AI Ethics and Applications"
        ],
        4: [
            "Theory of Computation",
            "Artificial Intelligence Principles and Techniques",
            "Numerical Methods for Optimization"
        ],
        5: [
            "Machine Learning",
            "Design and Analysis of Algorithms",
            "Linear Algebra and Calculus"
        ],
        6: [
            "Applied Neural Networks",
            "Software Engineering and Project Management",
            "AI for Everyone"
        ],
        7: [
            "Operating System",
            "Cloud Computing",
            "Discrete Mathematics"
        ],
        8: [
            "Expert Systems in Artificial Intelligence",
            "Usage of IoT in Edge Computing",
            "Statistics and Probability"
        ],
        9: [
            "Modern Web Technologies",
            "Digital Electronics",
            "Modern Computer Architecture"
        ],
        10: [
            "Data Preprocessing and EDA",
            "Object-Oriented Programming",
            "Java Programming"
        ],
        11: [
            "Data Engineering and Programming",
            "Natural Language Processing and Chatbots",
            "Logic Building and Problem Solving with C"
        ],
        12: [
            "Computer Architecture and Organization",
            "Usage of Libraries and APIs in Python",
            "Computational Statistics"
        ],
        13: [
            "Mathematics for Machine Learning",
            "Advanced Machine Learning",
            "Advanced Python for Data Science"
        ],
        14: [
            "Data Engineering and Mining",
            "Natural Language Processing",
            "Computer Vision"
        ],
        15: [
            "Advanced Linear Algebra and Calculus",
            "AI Knowledge Representation and Reasoning",
            "Applied Mathematics-3 and Optimization Techniques"
        ]

    },

    "CSE": {
        1: [
            "Programming Fundamentals (C, C++, Python)",
            "Operating System Concepts",
            "Computer Networks"
        ],
        2: [
            "Object-Oriented Programming",
            "Software Engineering",
            "Compiler Design"
        ],
        3: [
            "Distributed Systems",
            "Cloud Computing",
            "Data Mining and Big Data"
        ],
        4: [
            "Design and Analysis of Algorithms",
            "Operating Systems",
            "Computer Networks"
        ],
        5: [
            "Software Engineering",
            "Theory of Computation",
            "Web Technologies"
        ],
        6: [
            "Compiler Design",
            "Data Mining and Warehousing",
            "Mobile Application Development"
        ],
        7: [
            "Machine Learning",
            "Artificial Intelligence",
            "Cloud Computing"
        ],
        8: [
            "Deep Learning",
            "Big Data Analytics",
            "Internet of Things (IoT)"
        ],
        9: [
            "Cybersecurity and Ethical Hacking",
            "Blockchain Technology",
            "Parallel and Distributed Computing"
        ],
        10: [
            "Natural Language Processing",
            "Computer Vision",
            "Quantum Computing Fundamentals"
        ],
        11: [
            "Augmented Reality and Virtual Reality",
            "Human Computer Interaction",
            "Information Retrieval Systems"
        ],
        12: [
            "Software Project Management",
            "Data Visualization and Analytics",
            "Digital Image Processing"
        ],
        13: [
            "Reinforcement Learning",
            "Edge and Fog Computing",
            "DevOps and Cloud Deployment"
        ],
        14: [
            "AI Ethics and Responsible Computing",
            "Computational Intelligence",
            "Full Stack Web Development"
        ],
        15: [
            "Advanced Topics in AI and ML",
            "Entrepreneurship and Innovation",
            "Capstone Project / Industry Internship"
        ]

    },

    "Civil": {
        1: [
            "Building Materials and Construction",
            "Surveying Fundamentals",
            "Strength of Materials"
        ],
        2: [
            "Structural Analysis",
            "Concrete Technology",
            "Transportation Engineering"
        ],
        3: [
            "Environmental Engineering",
            "Geotechnical Engineering",
            "Hydraulic Structures and Water Resources"
        ],
        4: [
            "Fluid Mechanics",
            "Strength of Materials",
            "Structural Analysis I"
        ],
        5: [
            "Geotechnical Engineering",
            "Concrete Technology",
            "Highway Engineering"
        ],
        6: [
            "Structural Analysis II",
            "Environmental Engineering",
            "Transportation Engineering"
        ],
        7: [
            "Design of Reinforced Concrete Structures",
            "Water Resources Engineering",
            "Soil Mechanics and Foundation Engineering"
        ],
        8: [
            "Design of Steel Structures",
            "Irrigation and Hydraulic Structures",
            "Environmental Impact Assessment"
        ],
        9: [
            "Construction Planning and Management",
            "Remote Sensing and GIS Applications",
            "Hydrology and Water Management"
        ],
        10: [
            "Finite Element Analysis in Civil Engineering",
            "Earthquake Engineering",
            "Urban Transportation Systems"
        ],
        11: [
            "Advanced Concrete Technology",
            "Bridge Engineering",
            "Building Services and Maintenance"
        ],
        12: [
            "Computer-Aided Design (CAD) in Civil Engineering",
            "Project Estimation and Costing",
            "Smart City Infrastructure"
        ],
        13: [
            "Sustainable Construction Materials",
            "Disaster Management and Mitigation",
            "Geotechnical Earthquake Engineering"
        ],
        14: [
            "Structural Health Monitoring",
            "Advanced Surveying and 3D Mapping",
            "Water Supply and Wastewater Engineering"
        ],
        15: [
            "Construction Automation and Robotics",
            "Artificial Intelligence in Civil Engineering",
            "Project Management and Entrepreneurship"
        ]

    },

    "Mechanical": {
        1: [
            "Engineering Mechanics",
            "Thermodynamics",
            "Fluid Mechanics"
        ],
        2: [
            "Theory of Machines",
            "Heat Transfer",
            "Machine Design"
        ],
        3: [
            "Industrial Engineering",
            "Robotics and Automation",
            "Refrigeration and Air Conditioning"
        ],
        4: [
            "Manufacturing Processes",
            "Theory of Machines",
            "Strength of Materials"
        ],
        5: [
            "Applied Thermodynamics",
            "Machine Design",
            "Heat and Mass Transfer"
        ],
        6: [
            "Dynamics of Machinery",
            "Metrology and Quality Control",
            "Refrigeration and Air Conditioning"
        ],
        7: [
            "Finite Element Analysis",
            "Automobile Engineering",
            "Industrial Engineering and Management"
        ],
        8: [
            "Robotics and Automation",
            "Renewable Energy Systems",
            "Mechatronics"
        ],
        9: [
            "Fluid Machinery",
            "Advanced Manufacturing Systems",
            "Energy Conversion Techniques"
        ],
        10: [
            "Computational Fluid Dynamics",
            "Product Design and Development",
            "Engineering Optimization"
        ],
        11: [
            "Vibration and Noise Control",
            "Smart Materials and Structures",
            "Power Plant Engineering"
        ],
        12: [
            "Computer-Aided Design (CAD)",
            "Computer-Aided Manufacturing (CAM)",
            "Rapid Prototyping and 3D Printing"
        ],
        13: [
            "Advanced Thermal Engineering",
            "Industrial Automation",
            "Additive Manufacturing"
        ],
        14: [
            "Robotics and Control Systems",
            "Design for Manufacturing and Assembly",
            "Sustainable Energy Systems"
        ],
        15: [
            "Maintenance Engineering",
            "Artificial Intelligence in Manufacturing",
            "Project Management and Entrepreneurship"
        ]

    },

    "Electrical": {
        1: [
            "Basic Electrical Engineering",
            "DC Machines and Transformers",
            "Electrical Measurements"
        ],
        2: [
            "Power Systems",
            "Control Systems",
            "Power Electronics"
        ],
        3: [
            "Electrical Drives and Applications",
            "Renewable Energy Systems",
            "Smart Grid and IoT in Electrical Engineering"
        ]
    },

    "IT": {
        1: [
            "Computer Fundamentals",
            "Web Technologies (HTML, CSS, JavaScript)",
            "Database Concepts"
        ],
        2: [
            "Cloud Computing",
            "Cyber Security Fundamentals",
            "Data Analytics and Visualization"
        ],
        3: [
            "Blockchain Technology",
            "Internet of Things (IoT)",
            "DevOps and Automation"
        ]
    }
}
