import streamlit as st
import random
import copy
import json
import os

st.set_page_config(page_title="Sudoku But Make It GenZ", layout="centered")

# ---------------------------
# Gen Z Taunts
# ---------------------------

TAUNTS = [
    "Bro really thought that was correct 💀",
    "Nahhh this ain’t it chief 😭",
    "Math left the chat 🧠🚪",
    "Confidence was high, accuracy was low.",
    "Delulu is not the solulu.",
    "You had ONE job.",
    "Brain buffering... please wait.",
    "This ain't kindergarten Sudoku.",
    "Skill issue detected.",
]

# ---------------------------
# Sudoku Generator
# ---------------------------

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                nums = list(range(1,10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_sudoku():
    board = [[0]*9 for _ in range(9)]
    solve(board)

    # remove numbers
    puzzle = copy.deepcopy(board)
    for _ in range(45):  # difficulty
        row = random.randint(0,8)
        col = random.randint(0,8)
        puzzle[row][col] = 0

    return puzzle, board

# ---------------------------
# Solver Count Tracking
# ---------------------------

COUNTER_FILE = "solver_count.json"

def get_solver_count():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            json.dump({"count": 0}, f)
    with open(COUNTER_FILE, "r") as f:
        return json.load(f)["count"]

def increment_solver_count():
    count = get_solver_count() + 1
    with open(COUNTER_FILE, "w") as f:
        json.dump({"count": count}, f)

# ---------------------------
# Session State Setup
# ---------------------------

if "puzzle" not in st.session_state:
    puzzle, solution = generate_sudoku()
    st.session_state.puzzle = puzzle
    st.session_state.solution = solution
    st.session_state.user_grid = copy.deepcopy(puzzle)
    st.session_state.solved = False

# ---------------------------
# UI
# ---------------------------

st.title("🧩 Sudoku But Make It Gen-Z")
st.caption("Solve it if you’re not fake smart.")

solver_count = get_solver_count()
st.metric("🏆 People Who Actually Solved It", solver_count)

# ---------------------------
# Grid Display
# ---------------------------

for i in range(9):
    cols = st.columns(9)
    for j in range(9):
        if st.session_state.puzzle[i][j] == 0:
            value = cols[j].number_input(
                "",
                min_value=1,
                max_value=9,
                step=1,
                key=f"{i}-{j}"
            )
            st.session_state.user_grid[i][j] = value
        else:
            cols[j].markdown(f"### {st.session_state.puzzle[i][j]}")

# ---------------------------
# Check Button
# ---------------------------

if st.button("Check My Genius 🧠"):
    correct = True
    for i in range(9):
        for j in range(9):
            if st.session_state.user_grid[i][j] != st.session_state.solution[i][j]:
                correct = False
                break

    if correct:
        st.success("Okay genius. You ate that. 🧠🔥")
        if not st.session_state.solved:
            increment_solver_count()
            st.session_state.solved = True
    else:
        st.error(random.choice(TAUNTS))

# ---------------------------
# New Game
# ---------------------------

if st.button("New Puzzle 🔄"):
    puzzle, solution = generate_sudoku()
    st.session_state.puzzle = puzzle
    st.session_state.solution = solution
    st.session_state.user_grid = copy.deepcopy(puzzle)
    st.session_state.solved = False
    st.experimental_rerun()
