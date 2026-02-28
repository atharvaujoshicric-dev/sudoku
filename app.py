import streamlit as st
import numpy as np
import random
import os

st.set_page_config(page_title="Sudoku Roast Edition", layout="centered")

# ------------------------------
# Gen Z Taunts
# ------------------------------
GENZ_TAUNTS = [
    "Bro really thought that was correct 💀",
    "That move was illegal… just like your WiFi speed.",
    "Confidence level: 100. Accuracy level: 0.",
    "Are you solving Sudoku or inventing new math?",
    "This ain’t it chief.",
    "Brain.exe has stopped working.",
    "You almost had it… almost.",
    "Sudoku watching you like 👁👄👁",
    "That number said 'not today'.",
    "It’s giving… wrong."
]

# ------------------------------
# Sudoku Generator
# ------------------------------
def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    if num in board[:, col]:
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    if num in board[start_row:start_row+3, start_col:start_col+3]:
        return False
    return True

def solve_board(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_full_board():
    board = np.zeros((9,9), dtype=int)
    solve_board(board)
    return board

def remove_numbers(board, difficulty):
    removed = {"Easy":30, "Medium":40, "Hard":50}
    puzzle = board.copy()
    cells = list(range(81))
    random.shuffle(cells)
    for i in cells[:removed[difficulty]]:
        puzzle[i//9][i%9] = 0
    return puzzle

# ------------------------------
# Solved Counter Persistence
# ------------------------------
COUNTER_FILE = "solved_count.txt"

def get_solved_count():
    if not os.path.exists(COUNTER_FILE):
        return 0
    with open(COUNTER_FILE, "r") as f:
        return int(f.read())

def increment_solved_count():
    count = get_solved_count() + 1
    with open(COUNTER_FILE, "w") as f:
        f.write(str(count))

# ------------------------------
# Initialize Session
# ------------------------------
if "solution" not in st.session_state:
    full_board = generate_full_board()
    st.session_state.solution = full_board
    st.session_state.puzzle = remove_numbers(full_board, "Easy")
    st.session_state.difficulty = "Easy"
    st.session_state.completed = False

# ------------------------------
# UI
# ------------------------------
st.title("🧠 Sudoku: Roast Edition")

difficulty = st.selectbox(
    "Select Difficulty",
    ["Easy", "Medium", "Hard"],
    index=["Easy","Medium","Hard"].index(st.session_state.difficulty)
)

if difficulty != st.session_state.difficulty:
    full_board = generate_full_board()
    st.session_state.solution = full_board
    st.session_state.puzzle = remove_numbers(full_board, difficulty)
    st.session_state.difficulty = difficulty
    st.session_state.completed = False

if st.button("🔄 New Game"):
    full_board = generate_full_board()
    st.session_state.solution = full_board
    st.session_state.puzzle = remove_numbers(full_board, difficulty)
    st.session_state.completed = False

st.write("Fill the empty cells. Wrong move = public humiliation.")

# ------------------------------
# Sudoku Grid
# ------------------------------
user_input = np.zeros((9,9), dtype=int)

for i in range(9):
    cols = st.columns(9)
    for j in range(9):
        if st.session_state.puzzle[i][j] != 0:
            cols[j].markdown(f"### {st.session_state.puzzle[i][j]}")
            user_input[i][j] = st.session_state.puzzle[i][j]
        else:
            value = cols[j].text_input(
                "",
                key=f"{i}-{j}",
                max_chars=1
            )
            if value.isdigit():
                user_input[i][j] = int(value)

# ------------------------------
# Check Button
# ------------------------------
if st.button("✅ Check Solution"):
    correct = True
    for i in range(9):
        for j in range(9):
            if user_input[i][j] != st.session_state.solution[i][j]:
                correct = False

    if correct:
        if not st.session_state.completed:
            increment_solved_count()
            st.session_state.completed = True
        st.success("YOU ATE THAT. Sudoku defeated. 🏆")
    else:
        st.error(random.choice(GENZ_TAUNTS))

# ------------------------------
# Show Solved Count
# ------------------------------
st.markdown("---")
st.subheader("🏆 Total Successful Solves:")
st.write(get_solved_count())
