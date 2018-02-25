import random
from enum import Enum

import discord


class Status(Enum):
    QUIZZ_SLEEP = 0
    QUIZZ_ACTIVE = 1
    QUIZZ_RIGHT_ANSWER = 2



def read_file():
    file = open("../ressources/quizz_ressources/questions.txt", 'r')
    questions = file.readlines()
    file.close()
    return questions


class Quizz(object):
    all_questions = read_file()
    channel = discord.Object(id="405665341977395211")
    q_and_a = None
    question = None
    answer_question = None

    def __init__(self, status):
        self.status = status

    def generate_question_answer(self):
        self.q_and_a = self.random_question(self.all_questions).split('?')
        self.question = self.q_and_a[0]
        self.answer_question = self.answer(self.q_and_a).upper()

    @staticmethod
    def answer(questions):
        # answer = questions[1]
        return questions[1][:-1]  # without \n

    @staticmethod
    def random_question(questions):
        index = random.randint(0, 5019)
        return questions[index]
