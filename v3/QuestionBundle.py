class QuestionBundle:
    """Holds everything needed: The question text and the computed answer."""

    def __init__(self, question_text, correct_answer_text, topic_info):
        self.question_text = question_text
        self.correct_answer_text = correct_answer_text
        self.topic_info = topic_info

