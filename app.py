import streamlit as st
import numpy as np
import pandas as pd
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
# Solve Counter
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
# Initialize Game
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
    "Select Difficulty",
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
# Convert to DataFrame
# ------------------------------
puzzle_df = pd.DataFrame(st.session_state.puzzle)
solution = st.session_state.solution

# Replace 0 with blank
puzzle_df = puzzle_df.replace(0, "")

st.markdown("### Fill the grid. Wrong solution = roast.")

edited_df = st.data_editor(
    puzzle_df,
    num_rows="fixed",
    use_container_width=False,
    key="sudoku_editor"
)

# ------------------------------
# Check Solution
# ------------------------------
if st.button("✅ Check Solution"):
    try:
        user_array = edited_df.replace("", 0).astype(int).values

        if np.array_equal(user_array, solution):
            if not st.session_state.completed:
                increment_solved_count()
                st.session_state.completed = True
            st.success("YOU ATE THAT. Sudoku defeated. 🏆")
        else:
            st.error(random.choice(GENZ_TAUNTS))

    except:
        st.error("Fill all cells with numbers 1-9.")

# ------------------------------
# Display Solve Count
# ------------------------------
st.markdown("---")
st.subheader("🏆 Total Successful Solves")
st.write(get_solved_count())
