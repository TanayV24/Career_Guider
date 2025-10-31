SSC_QUESTIONS = [
    {"id": "name", "text": "Hey! What's your name? 😊", "type": "text", "validation": lambda x: isinstance(x, str) and len(x.strip()) >= 2, "error": "Name must be at least 2 characters"},
    {"id": "age", "text": "How old are you?", "type": "age_choice", "options": ["13", "14", "15", "16", "17", "18"], "validation": lambda x: True, "error": "Please select your age"},
    {"id": "location", "text": "Which city/town are you from? 🌍", "type": "text", "validation": lambda x: len(str(x).strip()) > 0, "error": "Please enter your location"},
    {"id": "diploma_interest", "text": "Would you like hands-on, job-ready courses after 10th?", "type": "choice", "options": ["Yes — Diploma/Polytechnic", "No — I'll continue to 11th/12th"]},
    {"id": "fav_subject", "text": "Which subject makes you lose track of time because you enjoy it?", "type": "choice", "options": ["Mathematics", "Physics/Chemistry", "Biology", "Computer/CS", "Commerce/Accounts", "History/Geography", "Languages", "Arts/Music"]},
    {"id": "hobby", "text": "What do you enjoy doing in your free time?", "type": "choice", "options": ["Solving puzzles/coding", "Reading/writing", "Sports/fitness", "Drawing/designing", "Building/fixing things", "Helping people/volunteering"]},
    {"id": "dream_job", "text": "If you could do anything for a career, what would it be?", "type": "text", "validation": lambda x: len(str(x).strip()) > 0, "error": "Please share your dream job"},
    {"id": "strength", "text": "What are you naturally good at?", "type": "choice", "options": ["Numbers & logic", "Creative thinking", "Communication", "Hands-on work", "Problem-solving", "Leadership"]},
    {"id": "study_style", "text": "How do you prefer to learn?", "type": "choice", "options": ["Reading textbooks", "Watching videos", "Doing practical work", "Group discussions", "Self-practice"]},
    {"id": "career_priority", "text": "What matters most to you in a career?", "type": "choice", "options": ["High salary", "Job security", "Creativity & innovation", "Helping society", "Work-life balance", "Fame & recognition"]},
    {"id": "tech_comfort", "text": "How comfortable are you with technology & computers?", "type": "choice", "options": ["Very comfortable — I love tech!", "Somewhat comfortable", "Not very comfortable", "I prefer hands-on/non-tech work"]},
    {"id": "work_preference", "text": "Would you rather work:", "type": "choice", "options": ["Indoors (office/lab)", "Outdoors (field/travel)", "Mix of both", "From home"]},
    {"id": "math_feeling", "text": "How do you feel about mathematics?", "type": "choice", "options": ["Love it! It's my favorite", "It's okay, I can manage", "Not my strong suit", "I struggle with it"]},
    {"id": "future_vision", "text": "Where do you see yourself in 10 years?", "type": "text", "validation": lambda x: len(str(x).strip()) > 0, "error": "Please share your vision"}
]

HSC_QUESTIONS = [
    {"id": "name", "text": "What's your name? 😊", "type": "text", "validation": lambda x: isinstance(x, str) and len(x.strip()) >= 2, "error": "Name must be at least 2 characters"},
    {"id": "age", "text": "How old are you?", "type": "age_choice", "options": ["16", "17", "18", "19", "20"], "validation": lambda x: True, "error": "Please select your age"},
    {"id": "stream", "text": "Which stream did you choose in 11th-12th?", "type": "choice", "options": ["Science (PCM)", "Science (PCB)", "Commerce", "Arts/Humanities", "Vocational/Other"]},
    {"id": "favorite_subject_hsc", "text": "Which subject do you enjoy the most?", "type": "text", "validation": lambda x: len(str(x).strip()) > 0, "error": "Please enter a subject"},
    {"id": "exam_prep", "text": "Are you preparing for any competitive exams?", "type": "choice", "options": ["Yes — JEE/NEET", "Yes — CLAT/CA/Other", "Yes — State entrance exams", "No, not yet", "No, I prefer direct admission"]},
    {"id": "career_clarity", "text": "How clear are you about your career path?", "type": "choice", "options": ["Very clear — I know what I want", "Somewhat clear — narrowed down options", "Confused — need guidance", "Open to exploring options"]},
    {"id": "higher_ed", "text": "What are your plans after 12th?", "type": "choice", "options": ["Engineering/B.Tech", "Medical (MBBS/BDS/etc.)", "Law (LLB)", "Design/Architecture", "Commerce (B.Com/BBA/CA)", "Arts/Humanities (BA)", "Science (B.Sc)", "Unsure yet"]},
    {"id": "interest_area", "text": "Which field excites you the most?", "type": "choice", "options": ["Technology & Innovation", "Healthcare & Medicine", "Business & Entrepreneurship", "Creative Arts & Design", "Social Sciences & Law", "Research & Academia", "Government & Public Service"]},
    {"id": "study_abroad", "text": "Are you considering studying abroad?", "type": "choice", "options": ["Yes, definitely", "Maybe, if opportunities arise", "No, prefer India", "Haven't thought about it"]},
    {"id": "internship_exp", "text": "Have you done any internships or projects?", "type": "choice", "options": ["Yes, multiple", "Yes, one", "No, but planning to", "No, not interested"]},
    {"id": "skill_dev", "text": "What skills are you currently developing?", "type": "text", "validation": lambda x: len(str(x).strip()) > 0, "error": "Please share your skills"},
    {"id": "work_style", "text": "What kind of work environment do you prefer?", "type": "choice", "options": ["Corporate/office job", "Startup/dynamic environment", "Self-employed/freelance", "Research/academic setting", "Field work/travel", "Government/public sector"]},
    {"id": "motivation", "text": "What motivates you the most?", "type": "choice", "options": ["Financial success", "Making a difference", "Personal growth", "Recognition & awards", "Work-life balance", "Innovation & creativity"]},
    {"id": "final_message", "text": "Anything else you'd like to share about your goals or interests?", "type": "text", "validation": lambda x: True, "error": ""}
]

MOTIVATIONAL_QUOTES = [
    "Your future is created by what you do today, not tomorrow! 💪",
    "Every expert was once a beginner. Keep going! 🚀",
    "The best time to plant a tree was 20 years ago. The second best time is now. 🌱",
    "Don't watch the clock; do what it does. Keep going! ⏰",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. 🎯",
    "Believe you can and you're halfway there! ✨"
]

QUESTION_SETS = {
    "SSC": SSC_QUESTIONS,
    "HSC": HSC_QUESTIONS
}