import random
import json
import os

# Quiz data structure
questions = [
    {
        "question": "What gas do plants absorb from the atmosphere for photosynthesis?",
        "options": {
            "A": "Oxygen",
            "B": "Nitrogen",
            "C": "Carbon dioxide",
            "D": "Hydrogen"
        },
        "answer": "C"
    },
    {
        "question": "What part of the cell contains genetic material?",
        "options": {
            "A": "Cytoplasm",
            "B": "Nucleus",
            "C": "Mitochondria",
            "D": "Ribosome"
        },
        "answer": "B"
    },
    {
        "question": "Who developed the theory of general relativity?",
        "options": {
            "A": "Isaac Newton",
            "B": "Stephen Hawking",
            "C": "Albert Einstein",
            "D": "Galileo Galilei"
        },
        "answer": "C"
    },
    {
        "question": "What is the main function of red blood cells in the human body?",
        "options": {
            "A": "To fight infection",
            "B": "To produce hormones",
            "C": "To carry oxygen",
            "D": "To digest food"
        },
        "answer": "C"
    },
    {
        "question": "Which planet is known as the 'Red Planet'?",
        "options": {
            "A": "Venus",
            "B": "Mars",
            "C": "Jupiter",
            "D": "Saturn"
        },
        "answer": "B"
    }
]

# High scores file
HIGH_SCORES_FILE = "high_scores.json"

def load_high_scores():
    """Load high scores from file or return empty list if file doesn't exist"""
    if os.path.exists(HIGH_SCORES_FILE):
        with open(HIGH_SCORES_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_high_scores(scores):
    """Save high scores to file"""
    with open(HIGH_SCORES_FILE, 'w') as file:
        json.dump(scores, file)

def add_high_score(name, score, total):
    """Add a new high score to the list and save it"""
    scores = load_high_scores()
    percentage = (score / total) * 100
    scores.append({"name": name, "score": score, "total": total, "percentage": percentage})
    # Sort by percentage descending
    scores.sort(key=lambda x: x["percentage"], reverse=True)
    # Keep only top 5 scores
    scores = scores[:5]
    save_high_scores(scores)

def display_high_scores():
    """Display the current high scores"""
    scores = load_high_scores()
    if not scores:
        print("\nNo high scores yet!")
        return
    
    print("\n=== HIGH SCORES ===")
    for i, score in enumerate(scores, 1):
        print(f"{i}. {score['name']}: {score['score']}/{score['total']} ({score['percentage']:.1f}%)")

def randomize_options(question_data):
    """Randomize the order of options while keeping track of the correct answer"""
    options = list(question_data["options"].items())
    random.shuffle(options)
    
    # Create new options dictionary with new keys (A-D)
    new_options = {}
    option_letters = ["A", "B", "C", "D"]
    answer_mapping = {}
    
    for i, (old_key, value) in enumerate(options):
        new_key = option_letters[i]
        new_options[new_key] = value
        if old_key == question_data["answer"]:
            answer_mapping[old_key] = new_key
    
    return {
        "question": question_data["question"],
        "options": new_options,
        "answer": answer_mapping.get(question_data["answer"], question_data["answer"])
    }

def ask_question(question_data):
    """Ask a single question and return whether the answer was correct"""
    print("\n" + question_data["question"])
    for option, text in question_data["options"].items():
        print(f"{option}: {text}")
    
    while True:
        user_answer = input("Your answer (A-D): ").upper()
        if user_answer in ["A", "B", "C", "D"]:
            break
        print("Invalid input. Please enter A, B, C, or D.")
    
    correct = user_answer == question_data["answer"]
    if correct:
        print("Correct!")
    else:
        print(f"Wrong! The correct answer is {question_data['answer']}.")
    
    return correct

def grade_quiz(score, total):
    """Calculate and display the quiz results"""
    percentage = (score / total) * 100
    
    print(f"\n=== RESULTS ===")
    print(f"You scored {score} out of {total} ({percentage:.1f}%)")
    
    if percentage >= 80:
        print("Excellent!")
    elif percentage >= 50:
        print("Good job!")
    else:
        print("Keep practicing!")

def run_quiz():
    """Main function to run the quiz"""
    print("Welcome to Task0 Quiz App")
    print("Answer each question by entering A, B, C, or D\n")
    
    # Randomize question order and options
    randomized_questions = random.sample(questions, len(questions))
    processed_questions = [randomize_options(q) for q in randomized_questions]
    score = 0
    
    for question in processed_questions:
        if ask_question(question):
            score += 1
    
    total = len(questions)
    grade_quiz(score, total)
    
    # High score tracking
    name = input("\nEnter your name for the high score board: ").strip()
    if name:  # Only save if name is not empty
        add_high_score(name, score, total)
    
    display_high_scores()

def main():
    while True:
        run_quiz()
        
        while True:
            choice = input("\nWould you like to try again? (Y/N): ").upper()
            if choice in ["Y", "N"]:
                break
            print("Please enter Y or N.")
        
        if choice == "N":
            print("\nThanks for playing! Goodbye!")
            break

if __name__ == "__main__":
    main()