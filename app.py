import streamlit as st

from utils.file_parser import extract_text_from_file
from utils.ollama_client import generate_questions


# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="EduLens",
    page_icon="📚"
)

st.title("📚 EduLens")
st.write("AI-powered study material and weak topic detector")


# ---------------- SIDEBAR ----------------

st.sidebar.header("⚙️ Settings")

model = st.sidebar.text_input(
    "Ollama Model",
    value="llama3.2:3b"
)

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Medium", "Hard"]
)

num_questions = st.sidebar.slider(
    "Number of Questions",
    1,
    10,
    5
)

categories = st.sidebar.multiselect(
    "Categories",
    [
        "Concept Understanding",
        "Concept Application",
        "Analysis",
        "Problem Solving"
    ],
    default=["Concept Understanding"]
)


# ---------------- NEW TEST BUTTON ----------------

if st.sidebar.button("🔄 Generate New Test"):

    st.session_state.pop("questions", None)
    st.session_state.pop("answers", None)
    st.session_state.pop("submitted", None)

    st.rerun()


# ---------------- FILE UPLOAD ----------------

uploaded_file = st.file_uploader(
    "📂 Upload your study material",
    type=["pdf", "pptx", "ppt", "txt", "docx"]
)


# ---------------- READ FILE ----------------

if uploaded_file:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    try:

        material = extract_text_from_file(uploaded_file)

        st.write("### 📖 Study Material")

        st.write(material[:1000])

    except Exception as e:

        st.error(
            f"Could not read the file: {e}"
        )

        st.stop()


    # ---------------- GENERATE QUESTIONS ----------------

    if st.button("📝 Generate Questions"):

        with st.spinner("Generating questions..."):

            try:

                questions = generate_questions(
                    material,
                    difficulty,
                    num_questions,
                    categories,
                    model
                )

                st.session_state.questions = questions
                st.session_state.answers = {}
                st.session_state.submitted = False

                st.success(
                    "Questions generated successfully!"
                )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

                st.stop()


# ---------------- DISPLAY TEST ----------------

if "questions" in st.session_state:

    st.header("📝 Test")

    for i, q in enumerate(
        st.session_state.questions
    ):

        st.subheader(
            f"Question {i + 1}"
        )

        st.write(
            q["question"]
        )

        answer = st.radio(
            "Choose your answer:",
            q["options"],
            key=f"answer_{i}"
        )

        st.session_state.answers[i] = answer

        st.caption(
            f"Category: {q.get('category', 'General')} | "
            f"Topic: {q.get('topic', 'General')} | "
            f"Marks: {q.get('marks', 1)}"
        )


    # ---------------- SUBMIT TEST ----------------

    if st.button("✅ Submit Test"):

        score = 0
        weak_topics = []

        for i, q in enumerate(
            st.session_state.questions
        ):

            user_answer = (
                st.session_state.answers.get(i)
            )

            if user_answer == q["correct_answer"]:

                score += q.get(
                    "marks",
                    1
                )

            else:

                weak_topics.append(
                    q.get(
                        "topic",
                        "General"
                    )
                )


        # Total marks

        total = sum(
            q.get("marks", 1)
            for q in st.session_state.questions
        )


        # Percentage

        percentage = (
            score / total
        ) * 100


        st.session_state.submitted = True


        # ---------------- RESULT ----------------

        st.header("📊 Performance Report")

        st.write(
            f"### Score: {score} / {total}"
        )

        st.write(
            f"### Percentage: {percentage:.1f}%"
        )


        # ---------------- PERFORMANCE ----------------

        if percentage >= 80:

            st.success(
                "🎉 Excellent performance!"
            )

        elif percentage >= 50:

            st.warning(
                "👍 Good attempt! Keep practicing."
            )

        else:

            st.error(
                "⚠️ You need more practice."
            )


        # ---------------- WEAK TOPICS ----------------

        st.subheader(
            "📌 Topics You Need to Improve"
        )

        if weak_topics:

            # Remove duplicates

            weak_topics = list(
                dict.fromkeys(
                    weak_topics
                )
            )

            for topic in weak_topics:

                st.write(
                    f"🔸 **{topic}**"
                )

            st.info(
                "Revise these topics from your "
                "uploaded study material."
            )

        else:

            st.success(
                "🎉 No weak topics detected!"
            )


        # ---------------- SUGGESTIONS ----------------

        st.subheader(
            "💡 Suggestions"
        )

        if percentage < 50:

            st.write(
                "• Review the basic concepts first."
            )

            st.write(
                "• Practice questions from the weak topics."
            )

            st.write(
                "• Take another test after revision."
            )

        elif percentage < 80:

            st.write(
                "• Revise the questions you answered incorrectly."
            )

            st.write(
                "• Practice application-based questions."
            )

            st.write(
                "• Take another test to improve your score."
            )

        else:

            st.write(
                "• Your concepts are strong."
            )

            st.write(
                "• Try a harder difficulty level."
            )

            st.write(
                "• Practice analysis and problem-solving questions."
            )


        # ---------------- SOURCE ----------------
        # ---------------- STUDY SOURCES ----------------

        st.subheader("📚 Recommended Study Resources")

        st.write(
            "Use these resources to revise your weak topics "
            "and understand concepts better."
        )

        st.markdown(
            "🔹 [GeeksforGeeks](https://www.geeksforgeeks.org/) "
            "— Programming, DSA, Java, Python, DBMS and AI/ML"
        )

        st.markdown(
            "🔹 [Khan Academy](https://www.khanacademy.org/) "
            "— Mathematics, Science, Economics and Computing"
        )

        st.markdown(
            "🔹 [Coursera](https://www.coursera.org/) "
            "— Online courses and university-level learning"
        )

        st.markdown(
            "🔹 [edX](https://www.edx.org/) "
            "— University courses and academic subjects"
        )

        st.markdown(
            "🔹 [MIT OpenCourseWare](https://ocw.mit.edu/) "
            "— Free MIT course materials"
        )

        st.markdown(
            "🔹 [NPTEL](https://nptel.ac.in/) "
            "— Engineering and technical courses from IITs and IISc"
        )

        st.markdown(
            "🔹 [ChatGPT](https://chatgpt.com/) "
            "— Ask for explanations, examples and study help"
        )

        st.caption(
            "These are recommended learning resources. "
            "The test questions are generated from your uploaded study material."
        )
                