import streamlit as st
from algorithms.sorting import visualize_sorting
from algorithms.pathfinding import visualize_pathfinding

st.set_page_config(page_title="Algorithm Visualizer", layout="wide")

# Home Page
def main():
    st.title("Algorithm Visualizer")

    st.markdown("## Select a Visualizer:")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔢 Sorting Algorithms"):
            st.session_state.page = "sorting"

    with col2:
        if st.button("🛤️ Pathfinding Algorithms"):
            st.session_state.page = "pathfinding"

    # Navigate to selected page
    if "page" in st.session_state:
        if st.session_state.page == "sorting":
            visualize_sorting()
        elif st.session_state.page == "pathfinding":
            visualize_pathfinding()

if __name__ == "__main__":
    main()
