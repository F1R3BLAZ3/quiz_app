import random
from app.models import QuizQuestion

def add_question(question_text, answer_a, answer_b, answer_c, answer_d, correct_answer_id):
    """Add a new question to the pool."""
    question = QuizQuestion(
        question_text=question_text,
        answer_a=answer_a,
        answer_b=answer_b,
        answer_c=answer_c,
        answer_d=answer_d,
        correct_answer_id=correct_answer_id
    )
    return question

def get_random_questions(num_questions):
    """Retrieve a random set of questions from the pool."""
    all_questions = QuizQuestion.query.all()
    return random.sample(all_questions, min(num_questions, len(all_questions)))

def delete_question(question_id):
    """Delete a question by its ID."""
    question = QuizQuestion.query.get(question_id)
    if question:
        db.session.delete(question)
        db.session.commit()
        return True
    return False
