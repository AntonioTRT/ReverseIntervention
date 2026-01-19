"""
Data Manager Module
Handles reading and writing question data from/to CSV file.
Manages question state and retrieval.
"""

import csv
import random
from pathlib import Path
from typing import List, Dict, Optional, Any


class DataManager:
    """Manages question data persistence and retrieval from CSV."""

    def __init__(self, csv_path: str = "questions.csv"):
        """
        Initialize the DataManager.

        Args:
            csv_path (str): Path to the CSV file containing questions.
        """
        self.csv_path = Path(csv_path)
        self.questions: List[Dict[str, Any]] = []
        self.load_questions()

    def load_questions(self) -> None:
        """
        Load all questions from the CSV file into memory.
        Converts 'used' column to boolean and 'id', 'category', 'difficulty' to int.

        Raises:
            FileNotFoundError: If CSV file does not exist.
            ValueError: If CSV structure is invalid.
        """
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

        self.questions = []
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                if reader.fieldnames != ['id', 'question', 'category', 'difficulty', 'used', 'correct_answer']:
                    raise ValueError("CSV structure doesn't match expected columns")

                for row in reader:
                    question = {
                        'id': int(row['id']),
                        'question': row['question'],
                        'category': int(row['category']),
                        'difficulty': int(row['difficulty']),
                        'used': row['used'].lower() == 'true',
                        'correct_answer': row['correct_answer'].lower() == 'yes'
                    }
                    self.questions.append(question)
        except (csv.Error, ValueError) as e:
            raise ValueError(f"Error parsing CSV file: {e}")

    def save_questions(self) -> None:
        """
        Save all questions back to the CSV file.
        Overwrites the file with current state of questions.

        Raises:
            IOError: If unable to write to file.
        """
        try:
            with open(self.csv_path, mode='w', newline='', encoding='utf-8') as file:
                fieldnames = ['id', 'question', 'category', 'difficulty', 'used', 'correct_answer']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

                for question in self.questions:
                    writer.writerow({
                        'id': question['id'],
                        'question': question['question'],
                        'category': question['category'],
                        'difficulty': question['difficulty'],
                        'used': str(question['used']),
                        'correct_answer': 'Yes' if question['correct_answer'] else 'No'
                    })
        except IOError as e:
            raise IOError(f"Error writing to CSV file: {e}")

    def get_all_questions(self) -> List[Dict[str, Any]]:
        """
        Get all questions.

        Returns:
            List[Dict]: List of all question dictionaries.
        """
        return [q.copy() for q in self.questions]

    def get_unused_questions(self) -> List[Dict[str, Any]]:
        """
        Get all questions that haven't been used yet.

        Returns:
            List[Dict]: List of unused question dictionaries.
        """
        return [q.copy() for q in self.questions if not q['used']]

    def get_random_unused_question(self) -> Optional[Dict[str, Any]]:
        """
        Get a random unused question.

        Returns:
            Optional[Dict]: A random unused question or None if all used.
        """
        unused = self.get_unused_questions()
        if not unused:
            return None
        return random.choice(unused).copy()

    def mark_question_used(self, question_id: int) -> bool:
        """
        Mark a question as used.

        Args:
            question_id (int): The ID of the question to mark as used.

        Returns:
            bool: True if successful, False if question not found.
        """
        for question in self.questions:
            if question['id'] == question_id:
                question['used'] = True
                return True
        return False

    def reset_all_questions(self) -> None:
        """
        Reset all questions to unused state.
        Useful for starting a new game.
        """
        for question in self.questions:
            question['used'] = False

    def get_question_by_id(self, question_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific question by ID.

        Args:
            question_id (int): The ID of the question.

        Returns:
            Optional[Dict]: Question dictionary or None if not found.
        """
        for question in self.questions:
            if question['id'] == question_id:
                return question.copy()
        return None

    def get_unused_count(self) -> int:
        """
        Get count of unused questions.

        Returns:
            int: Number of unused questions.
        """
        return sum(1 for q in self.questions if not q['used'])

    def get_total_count(self) -> int:
        """
        Get total count of questions.

        Returns:
            int: Total number of questions.
        """
        return len(self.questions)
