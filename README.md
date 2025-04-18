# 📌 Dream Job AI

## 🚀 Overview
This project is an interactive Streamlit-based web application designed to assist users in transitioning into AI careers. It provides:
- 📖 **Study Material**: Fetches YouTube links for learning subjects.
- 💼 **Job Finder**: Finds job listings based on location and job title.
- 🛤️ **Career Counseling**: Provides AI career recommendations based on user input.
- 🏆 **Roadmap Generator**: Creates a structured learning pathway based on specialization, time commitment, and salary expectations.

---

## 🛠 Tech Stack
- **Python**: Core programming language
- **Streamlit**: Interactive UI framework
- **Cohere API**: Chat-based AI responses
- **LangChain**: Cohere-powered conversational models
- **Google Search API**: Fetches relevant YouTube links and job postings
- **Dotenv**: Environment variable management
- **Requests**: API calls for location-based job searches

---

## 📥 Installation & Setup

1. **Clone the Repository**
   ```sh
   git clone https://github.com/HrithikRai/AI_career_buddy.git
   cd ai-career-roadmap
   ```

2. **Create a Virtual Environment (Optional but Recommended)**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   - Create a `.env` file and add:
   ```sh
   COHERE_API_KEY=your_cohere_api_key
   ```

5. **Run the Application**
   ```sh
   streamlit run app.py
   ```

---

## 📂 Project Structure
```
📦 ai-career-roadmap
 ┣ 📜 app.py                # Main Streamlit app
 ┣ 📜 requirements.txt       # Required dependencies
 ┣ 📜 .env.example           # Example environment variables
 ┣ 📜 README.md              # Project documentation
 ┗ 📂 modules
     ┣ 📜 career_counselor.py # AI-driven career recommendations
     ┣ 📜 job_finder.py       # Fetches job listings based on location
     ┣ 📜 study_material.py   # Gets YouTube study links
     ┣ 📜 roadmap_generator.py # Builds learning roadmaps
```

---

## 🎯 Features & Functionality

### 1️⃣ **AI-Powered Career Counseling**
- Users answer a series of questions about their background and interests.
- The system recommends an ideal AI career path.
- Suggested specializations for skill development.

### 2️⃣ **Personalized Learning Roadmap**
- Generates a weekly roadmap for upskilling.
- Lists essential tools and skills.
- Guides on portfolio building for job readiness.
- Predicts potential salary hikes.

### 3️⃣ **Smart Job Finder**
- Uses location-based search to fetch jobs.
- Provides at least 5 job links for each query.
- Summarizes job descriptions for better clarity.

### 4️⃣ **Study Material Fetcher**
- Retrieves YouTube video links for given subjects.
- Ensures diverse topics are covered for well-rounded learning.

---

## 📸 Screenshots
(Include some screenshots of the UI here)

---

## 🤝 Contributing
Pull requests are welcome! If you'd like to contribute:
1. Fork this repository.
2. Create a new feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m 'Added feature XYZ'`).
4. Push the branch (`git push origin feature-name`).
5. Open a Pull Request.

---

## 📜 License
This project is licensed under the MIT License.

---

## 👨‍💻 Author
**[Hrithik Rai Saxena](https://www.linkedin.com/in/hrithikraisaxena/)**
**[Rishi Rai Saxena](https://www.linkedin.com/in/rishi-rai-saxena/)**
