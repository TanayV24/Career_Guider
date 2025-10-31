from collections import defaultdict

STREAM_PROFILES = {
    'Science_PCM': {
        'title': 'Science (PCM)',
        'subjects': ['Physics', 'Chemistry', 'Mathematics'],
        'careers': ['Engineering', 'Data Science', 'Architecture', 'Aviation', 'Research Scientist', 'Robotics'],
        'exams': ['JEE Main', 'JEE Advanced', 'BITSAT', 'VITEEE'],
        'skills': ['Analytical thinking', 'Problem-solving', 'Mathematical aptitude'],
        'personality': 'Logical, Systematic, Innovative',
        'resources': ['Khan Academy (Math)', 'Physics Wallah', 'Unacademy'],
        'salary_range': '₹4-15 LPA (starting)',
        'image': 'assets/recommendations/science_pcm.png'
    },

    'Science_PCB': {
        'title': 'Science (PCB)',
        'subjects': ['Physics', 'Chemistry', 'Biology'],
        'careers': ['Medicine', 'Biotech', 'Pharmacy', 'Nursing', 'Research', 'Physiotherapy'],
        'exams': ['NEET', 'AIIMS', 'JIPMER', 'State Medical Tests'],
        'skills': ['Empathy', 'Attention to detail', 'Biological understanding'],
        'personality': 'Caring, Methodical, Patient',
        'resources': ['NCERT Biology', 'Aakash Digital', 'Allen Online'],
        'salary_range': '₹6-25 LPA (starting)',
        'image': 'assets/recommendations/science_pcb.png'
    },

    'Commerce': {
        'title': 'Commerce',
        'subjects': ['Accountancy', 'Economics', 'Business Studies'],
        'careers': ['Chartered Accountant', 'Banking', 'Finance Manager', 'Business Analyst', 'Entrepreneur', 'Stock Market'],
        'exams': ['CA Foundation', 'CPT', 'BBA Entrance', 'CLAT'],
        'skills': ['Numerical ability', 'Business acumen', 'Financial literacy'],
        'personality': 'Practical, Organized, Strategic',
        'resources': ['CA Foundation Videos', 'Investopedia', 'Economic Times'],
        'salary_range': '₹3-12 LPA (starting)',
        'image': 'assets/recommendations/commerce.png'
    },

    'Arts': {
        'title': 'Humanities / Arts',
        'subjects': ['History', 'Political Science', 'Psychology', 'Sociology'],
        'careers': ['Civil Services', 'Journalism', 'Psychology', 'Teaching', 'Social Work', 'Content Writing'],
        'exams': ['UPSC', 'CLAT', 'JNU Entrance', 'DU Entrance'],
        'skills': ['Critical thinking', 'Communication', 'Cultural awareness'],
        'personality': 'Creative, Empathetic, Analytical',
        'resources': ['NCERT Social Science', 'The Hindu', 'Coursera Humanities'],
        'salary_range': '₹3-10 LPA (starting)',
        'image': 'assets/recommendations/arts.png'
    },

    'Diploma': {
        'title': 'Diploma / Polytechnic',
        'subjects': ['Mechanical', 'Electrical', 'Computer Engineering', 'Civil'],
        'careers': ['Junior Engineer', 'Technician', 'Site Supervisor', 'CAD Designer'],
        'exams': ['State Polytechnic Entrance', 'Direct Admission'],
        'skills': ['Hands-on expertise', 'Technical knowledge', 'Practical application'],
        'personality': 'Practical, Skilled, Result-oriented',
        'resources': ['ITI courses', 'NPTEL', 'Skill India'],
        'salary_range': '₹2-6 LPA (starting)',
        'image': 'assets/recommendations/diploma.png'
    }
}


class StreamAnalyzer:

    def __init__(self, nlp_engine):
        self.nlp = nlp_engine

    def analyze(self, answers: dict) -> dict:
        scores = defaultdict(float)
        personality_traits = []
        strengths = []

        # SSC specific
        if answers.get('diploma_interest', '').startswith('Yes'):
            scores['Diploma'] += 3.0
            personality_traits.append('Practical & Hands-on')
        else:
            scores['Science_PCM'] += 0.5
            scores['Science_PCB'] += 0.5
            scores['Commerce'] += 0.5
            scores['Arts'] += 0.5

        # Favorite subject mapping
        fav = answers.get('fav_subject', '')
        if 'Math' in fav:
            scores['Science_PCM'] += 2.5
            scores['Commerce'] += 1.0
            strengths.append('Mathematical Thinking')
        elif 'Physics' in fav or 'Chemistry' in fav:
            scores['Science_PCM'] += 2.0
            scores['Science_PCB'] += 1.5
            strengths.append('Scientific Aptitude')
        elif 'Biology' in fav:
            scores['Science_PCB'] += 3.0
            strengths.append('Biological Sciences')
        elif 'Computer' in fav:
            scores['Science_PCM'] += 2.0
            strengths.append('Technology & Computing')
        elif 'Commerce' in fav or 'Account' in fav:
            scores['Commerce'] += 3.0
            strengths.append('Business Acumen')
        elif 'History' in fav or 'Geography' in fav or 'Language' in fav or 'Arts' in fav:
            scores['Arts'] += 2.5
            strengths.append('Humanities & Social Sciences')

        # Work style influence
        work_style = answers.get('work_style', '')
        if 'Problem-solving' in work_style or 'building' in work_style:
            scores['Science_PCM'] += 1.5
            scores['Diploma'] += 1.0
            personality_traits.append('Analytical Problem Solver')
        elif 'Helping people' in work_style:
            scores['Science_PCB'] += 1.5
            scores['Arts'] += 1.0
            personality_traits.append('Empathetic Helper')
        elif 'Creative' in work_style:
            scores['Arts'] += 1.5
            personality_traits.append('Creative Thinker')
        elif 'Managing' in work_style:
            scores['Commerce'] += 1.5
            personality_traits.append('Strategic Organizer')

        # Learning style analysis
        learning = answers.get('learning_style', '')
        if 'Hands-on' in learning:
            scores['Diploma'] += 1.0
            scores['Science_PCM'] += 0.5
        elif 'Visual' in learning:
            scores['Arts'] += 0.5

        # Strength analysis
        strength = answers.get('strength', '')
        if 'Logical' in strength:
            scores['Science_PCM'] += 1.0
            personality_traits.append('Logical Thinker')
        elif 'Communication' in strength:
            scores['Arts'] += 1.0
            scores['Commerce'] += 0.5
            personality_traits.append('Great Communicator')
        elif 'Creativity' in strength:
            scores['Arts'] += 1.0
            personality_traits.append('Creative Mind')
        elif 'Leadership' in strength:
            scores['Commerce'] += 1.0
            personality_traits.append('Natural Leader')
        elif 'Technical' in strength:
            scores['Science_PCM'] += 1.0
            scores['Diploma'] += 0.5
            personality_traits.append('Tech Savvy')

        # HSC specific
        current_stream = answers.get('current_stream', '')
        if 'PCM' in current_stream:
            scores['Science_PCM'] += 3.0
        elif 'PCB' in current_stream:
            scores['Science_PCB'] += 3.0
        elif 'Commerce' in current_stream:
            scores['Commerce'] += 3.0
        elif 'Arts' in current_stream or 'Humanities' in current_stream:
            scores['Arts'] += 3.0

        # Career field preference (HSC only)
        career_field = answers.get('career_field', '')
        if 'Engineering' in career_field or 'Tech' in career_field:
            scores['Science_PCM'] += 2.0
        elif 'Medical' in career_field or 'Healthcare' in career_field:
            scores['Science_PCB'] += 2.5
        elif 'Business' in career_field or 'Finance' in career_field:
            scores['Commerce'] += 2.0
        elif 'Creative' in career_field or 'Design' in career_field:
            scores['Arts'] += 1.5
        elif 'Law' in career_field or 'Civil Services' in career_field:
            scores['Arts'] += 2.0
            scores['Commerce'] += 1.0

        # NLP sentiment analysis
        free_time_text = str(answers.get('free_time', ''))
        sentiment = self.nlp.sentiment_score(free_time_text)
        # If you have a detect_subjects method, use it here
        subjects_found = []
        if hasattr(self.nlp, "detect_subjects"):
            subjects_found = self.nlp.detect_subjects(free_time_text)
        for subj in subjects_found:
            if subj in ['Mathematics', 'Physics', 'Chemistry', 'Computer Science']:
                scores['Science_PCM'] += 0.8
            elif subj == 'Biology':
                scores['Science_PCB'] += 0.8
            elif subj in ['Commerce', 'Accountancy', 'Economics']:
                scores['Commerce'] += 0.8
            elif subj in ['History', 'Geography', 'Arts']:
                scores['Arts'] += 0.8
        if sentiment > 0.3:
            for key in scores:
                scores[key] += 0.3

        # Calculate confidence score
        total_score = sum(scores.values())
        max_score = max(scores.values()) if scores else 0
        confidence = (max_score / total_score * 100) if total_score > 0 else 50

        # Get top recommendation
        if not scores:
            top_stream = 'Science_PCM'
        else:
            top_stream = max(scores, key=scores.get)

        result = STREAM_PROFILES.get(top_stream, {}).copy()
        result['confidence'] = round(confidence, 1)
        result['all_scores'] = dict(scores)
        result['personality_traits'] = personality_traits[:3] if personality_traits else ['Enthusiastic Learner']
        result['strengths'] = strengths[:3] if strengths else ['Quick Learner']

        # Generate detailed analysis
        result['detailed_analysis'] = self.generate_analysis(answers, top_stream, confidence)
        return result

    def generate_analysis(self, answers, stream, confidence):
        """Generate detailed personality and career analysis"""
        analysis = {
            'summary': f"Based on your responses, you show strong alignment with {STREAM_PROFILES[stream]['title']}.",
            'why_recommended': [],
            'career_roadmap': [],
            'next_steps': [],
            'challenges': [],
            'opportunities': []
        }

        # Why recommended
        fav = answers.get('fav_subject', '')
        if stream == 'Science_PCM' and 'Math' in fav:
            analysis['why_recommended'].append("Your love for Mathematics aligns perfectly with engineering and technology careers")
        elif stream == 'Science_PCB' and 'Biology' in fav:
            analysis['why_recommended'].append("Your interest in Biology opens doors to medical and life sciences")
        elif stream == 'Commerce' and 'Commerce' in fav:
            analysis['why_recommended'].append("Your business aptitude makes you ideal for commerce and finance")
        elif stream == 'Arts':
            analysis['why_recommended'].append("Your creative and analytical thinking suits humanities perfectly")
        work_style = answers.get('work_style', '')
        if 'Problem-solving' in work_style:
            analysis['why_recommended'].append("Your problem-solving nature is crucial for technical fields")
        elif 'Helping' in work_style:
            analysis['why_recommended'].append("Your people-oriented approach fits healthcare and social sectors")

        # Career roadmap
        if stream == 'Science_PCM':
            analysis['career_roadmap'] = [
                "Year 1-2: Focus on JEE preparation, build strong foundation in PCM",
                "Year 3-4: Engineering college, participate in hackathons and projects",
                "Year 5+: Internships, specialization, job placements or higher studies"
            ]
        elif stream == 'Science_PCB':
            analysis['career_roadmap'] = [
                "Year 1: Intensive NEET preparation, master Biology concepts",
                "Year 2-6: Medical college (MBBS) or other health programs",
                "Year 7+: Specialization, practice, or research opportunities"
            ]
        elif stream == 'Commerce':
            analysis['career_roadmap'] = [
                "Year 1-2: Build accounting and economics foundation",
                "Year 3-5: CA/BBA/B.Com with internships in firms",
                "Year 6+: Professional certification, corporate roles, or entrepreneurship"
            ]
        else:
            analysis['career_roadmap'] = [
                "Year 1-2: Develop writing, research, and analytical skills",
                "Year 3-5: BA/BBA with internships in media, NGOs, or government",
                "Year 6+: Masters, UPSC preparation, or specialized roles"
            ]

        # Next steps
        analysis['next_steps'] = [
            f"Research top colleges offering {STREAM_PROFILES[stream]['title']} programs",
            f"Start preparing for {', '.join(STREAM_PROFILES[stream]['exams'][:2])}",
            "Connect with professionals in your field of interest through LinkedIn",
            "Join relevant online communities and forums"
        ]

        # Challenges
        if stream == 'Science_PCM':
            analysis['challenges'] = [
                "High competition in engineering entrance exams",
                "Requires strong mathematical and analytical skills",
                "Long study hours and intensive preparation needed"
            ]
        elif stream == 'Science_PCB':
            analysis['challenges'] = [
                "Extremely competitive medical entrance (NEET)",
                "Long duration of medical education (5.5+ years)",
                "High emotional resilience required in healthcare"
            ]
        elif stream == 'Commerce':
            analysis['challenges'] = [
                "CA exams have low pass rates, require dedication",
                "Rapidly changing business environment",
                "Need to stay updated with financial regulations"
            ]
        else:
            analysis['challenges'] = [
                "Perception issues about career prospects in arts",
                "Requires excellent communication and research skills",
                "UPSC and similar exams are highly competitive"
            ]

        # Opportunities
        analysis['opportunities'] = [
            f"Growing demand in {', '.join(STREAM_PROFILES[stream]['careers'][:3])}",
            "International career prospects available",
            "Option for entrepreneurship and innovation",
            "Continuous learning and skill development opportunities"
        ]

        return analysis