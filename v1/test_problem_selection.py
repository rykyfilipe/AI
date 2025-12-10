#!/usr/bin/env python
# -*- coding: utf-8 -*-

from v2 import ContentGenerator

gen = ContentGenerator()

print("=== TEST: Problem Selection Question ===\n")
for i in range(3):
    bundle = gen.generate_problem_selection_question()
    print(f'--- Test {i+1} ---')
    print(bundle.question_text)
    print(f'Problem: {bundle.topic_info["problem"]}')
    print(f'Instance: {bundle.topic_info["instance"]}')
    print(f'Correct Answer: {bundle.correct_answer_text}\n')
    print("-" * 80)
