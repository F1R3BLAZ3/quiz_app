from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.models import User, QuizQuestion, QuizResult
from app.forms import LoginForm, RegistrationForm, QuestionForm
from werkzeug.security import generate_password_hash, check_password_hash
from app.services.quiz_service import get_random_questions

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check your username and password.', 'danger')

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        user = User(username=form.username.data, password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    quiz_results = QuizResult.query.filter_by(user_id=current_user.id).order_by(QuizResult.timestamp.desc()).all()
    return render_template('dashboard.html', user=current_user, quiz_results=quiz_results)

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    questions = get_random_questions(20)  # Get a random set of 20 questions

    if not questions:
        flash('No questions available for the quiz.', 'warning')
        return redirect(url_for('dashboard'))

    form = QuestionForm()  # Create an empty form instance for CSRF token

    if request.method == 'POST':
        print(request.form)  # Debugging line to log form data

        score = 0
        total_questions = len(questions)

        # Store the user's answers for analysis
        user_answers = {}

        for question in questions:
            selected_answer = request.form.get(f'question_{question.id}')
            print(f'Question ID: {question.id}, Selected Answer: {selected_answer}, Correct Answer ID: {question.correct_answer_id}')  # Debugging line
            user_answers[question.id] = selected_answer
            if selected_answer and selected_answer == str(question.correct_answer_id):
                score += 1

        # Save the quiz result to the database
        result = QuizResult(user_id=current_user.id, score=score, total_questions=total_questions)
        db.session.add(result)
        db.session.commit()

        # Store results in the session for analysis
        session['score'] = score
        session['total_questions'] = total_questions
        session['questions'] = [
            {
                'question_text': question.question_text,
                'correct_answer_id': question.correct_answer_id,
                'user_answer': user_answers.get(question.id),
                'correct_answer_text': [
                    question.answer_a, 
                    question.answer_b, 
                    question.answer_c, 
                    question.answer_d
                ][question.correct_answer_id - 1]  # Get the correct answer text
            } for question in questions
        ]

        flash(f'You scored {score} out of {total_questions}.', 'success')
        return redirect(url_for('quiz_results'))

    return render_template('quiz.html', questions=questions, form=form)  # Pass form to template

@app.route('/quiz/results', methods=['GET', 'POST'])
@login_required
def quiz_results():
    # Assuming we pass the score and questions when redirecting to this route
    score = session.get('score', 0)
    total_questions = session.get('total_questions', 0)
    questions = session.get('questions', [])
    
    # Clear session data after displaying results
    session.pop('score', None)
    session.pop('total_questions', None)
    session.pop('questions', None)

    return render_template('quiz_results.html', score=score, total_questions=total_questions, questions=questions)

@app.route('/add_question', methods=['GET', 'POST'])
@login_required
def add_question():
    form = QuestionForm()
    if form.validate_on_submit():
        question = QuizQuestion(
            question_text=form.question_text.data,
            answer_a=form.answer_a.data,
            answer_b=form.answer_b.data,
            answer_c=form.answer_c.data,
            answer_d=form.answer_d.data,
            correct_answer_id=int(form.correct_answer_id.data)
        )
        db.session.add(question)
        db.session.commit()
        flash('Question added successfully!', 'success')
        return redirect(url_for('add_question'))

    return render_template('add_question.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('home'))
