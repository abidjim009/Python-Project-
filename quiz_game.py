import os
import time

def clear():
    # Clear the console (Windows/macOS/Linux)
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPress Enter to continue...")
    clear()

print("="*50)
print("WELCOME TO THE COMPUTER QUIZ!".center(50))
print("="*50)

playing = input("\nDo you want to play? (yes/no): ")

if playing.lower() != "yes":
    print("\nGoodbye!")
    quit()

clear()
print("Great! Let's begin :)")
score = 0

# List of questions and options
questions = [
    {
        "question": "What does CPU stand for?",
        "options": ["Central Process Unit", "Central Processing Unit", "Computer Personal Unit", "Central Peripheral Unit"],
        "answer": "b"
    },
    {
        "question": "What does GPU stand for?",
        "options": ["General Processing Unit", "Graphics Performance Unit", "Graphics Processing Unit", "Graphical Power Unit"],
        "answer": "c"
    },
    {
        "question": "What does RAM stand for?",
        "options": ["Random Access Memory", "Readily Available Memory", "Read Access Module", "Rapid Action Memory"],
        "answer": "a"
    },
    {
        "question": "What does PSU stand for?",
        "options": ["Power System Unit", "Power Supply Unit", "Processing Storage Unit", "Peripheral Supply Unit"],
        "answer": "b"
    },
    {
        "question": "What does HTML stand for?",
        "options": ["HyperText Markup Language", "HighText Machine Language", "HyperTabular Markup Language", "None of these"],
        "answer": "a"
    },
    {
        "question": "What does HTTP stand for?",
        "options": ["HyperText Transfer Protocol", "Hyperlink Transfer Protocol", "Hyperlink Text Transfer Protocol", "Home Transfer Text Protocol"],
        "answer": "a"
    },
    {
        "question": "What does SSD stand for?",
        "options": ["Solid State Drive", "Super Speed Drive", "Static Storage Device", "Solid Storage Disk"],
        "answer": "a"
    },
    {
        "question": "What does BIOS stand for?",
        "options": ["Basic Integrated Operating System", "Basic Input Output System", "Binary Input Output System", "Basic Internal Output Setup"],
        "answer": "b"
    },
    {
        "question": "What does URL stand for?",
        "options": ["Uniform Resource Locator", "Universal Reference Link", "Uniform Resource Link", "Universal Resource Locator"],
        "answer": "a"
    },
    {
        "question": "What does LAN stand for?",
        "options": ["Local Area Network", "Long Area Network", "Light Access Node", "Large Area Net"],
        "answer": "a"
    },
]

# Quiz loop
for i, q in enumerate(questions):
    print(f"\nQuestion {i+1}: {q['question']}")
    print(f"a) {q['options'][0]}")
    print(f"b) {q['options'][1]}")
    print(f"c) {q['options'][2]}")
    print(f"d) {q['options'][3]}")
    answer = input("Your answer (a/b/c/d): ").lower()

    if answer == q['answer']:
        print("✅ Correct!")
        score += 1
    else:
        print("❌ Incorrect!")
    pause()

# Final score
print("="*50)
print("QUIZ COMPLETED".center(50))
print("="*50)
print(f"\nYou got {score} out of {len(questions)} questions correct!")
print(f"Your score: {(score / len(questions)) * 100:.2f}%")

if score == 10:
    print("🎉 Excellent work!")
elif score >= 7:
    print("👍 Good job!")
elif score >= 5:
    print("🙂 Not bad, but room to improve.")
else:
    print("😕 Keep practicing!")
