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
    "Sudoku watching you like 👁👄👁",
    "It’s giving… wrong."
]

# ------------------------------
# Sudoku Logic
# ------------------------------
def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    if num in board[:, col]:
        return False
    start_row, start_col = 3*(row//3), 3*(col//3)
    if num in board[start_row:start_row+3, start_col:start_col+3]:
        return False
    return True

def solve_board(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                nums = list(range(1,10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board,row,col,num):
                        board[row][col]=num
                        if solve_board(board):
                            return True
                        board[row][col]=0
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
# Solved Counter
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
    full = generate_full_board()
    st.session_state.solution = full
    st.session_state.puzzle = remove_numbers(full, "Easy")
    st.session_state.difficulty = "Easy"
    st.session_state.completed = False

# ------------------------------
# UI
# ------------------------------
st.title("🧠 Sudoku – Roast Edition")

difficulty = st.selectbox(
    "Difficulty",
    ["Easy","Medium","Hard"],
    index=["Easy","Medium","Hard"].index(st.session_state.difficulty)
)

if difficulty != st.session_state.difficulty:
    full = generate_full_board()
    st.session_state.solution = full
    st.session_state.puzzle = remove_numbers(full, difficulty)
    st.session_state.difficulty = difficulty
    st.session_state.completed = False

if st.button("🔄 New Game"):
    full = generate_full_board()
    st.session_state.solution = full
    st.session_state.puzzle = remove_numbers(full, difficulty)
    st.session_state.completed = False

# ------------------------------
# OG GRID STYLE
# ------------------------------
st.markdown("""
<style>
.sudoku-grid {
    display: grid;
    grid-template-columns: repeat(9, 50px);
    grid-template-rows: repeat(9, 50px);
    gap: 0px;
}
.cell {
    width: 50px;
    height: 50px;
    text-align: center;
    font-size: 20px;
    border: 1px solid #999;
}
.cell input {
    width: 100%;
    height: 100%;
    text-align: center;
    font-size: 20px;
    border: none;
}
.bold-right {
    border-right: 3px solid black !important;
}
.bold-bottom {
    border-bottom: 3px solid black !important;
}
.bold-left {
    border-left: 3px solid black !important;
}
.bold-top {
    border-top: 3px solid black !important;
}
</style>
""", unsafe_allow_html=True)

user_input = np.zeros((9,9), dtype=int)

st.markdown('<div class="sudoku-grid">', unsafe_allow_html=True)

for i in range(9):
    for j in range(9):
        value = st.session_state.puzzle[i][j]
        classes = "cell"
        if j % 3 == 2 and j != 8:
            classes += " bold-right"
        if i % 3 == 2 and i != 8:
            classes += " bold-bottom"
        if j == 0:
            classes += " bold-left"
        if i == 0:
            classes += " bold-top"

        if value != 0:
            st.markdown(f'<div class="{classes}"><b>{value}</b></div>', unsafe_allow_html=True)
            user_input[i][j] = value
        else:
            key = f"{i}-{j}"
            val = st.text_input("", key=key, max_chars=1)
            if val.isdigit():
                user_input[i][j] = int(val)

st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------
# Check
# ------------------------------
if st.button("✅ Check Solution"):
    if np.array_equal(user_input, st.session_state.solution):
        if not st.session_state.completed:
            increment_solved_count()
            st.session_state.completed = True
        st.success("YOU ATE THAT. Sudoku defeated. 🏆")
    else:
        st.error(random.choice(GENZ_TAUNTS))

# ------------------------------
# Counter Display
# ------------------------------
st.markdown("---")
st.subheader("🏆 Total Successful Solves")
st.write(get_solved_count())
