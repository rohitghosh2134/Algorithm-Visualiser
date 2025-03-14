import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib.patches as patches

SORTING_ALGORITHMS = {
    "Selection Sort": "selection_sort",
    "Bubble Sort": "bubble_sort",
    "Insertion Sort": "insertion_sort",
    "Merge Sort": "merge_sort",
    "Quick Sort": "quick_sort",
    "Heap Sort": "heap_sort",
}

# Sorting Algorithms
def selection_sort(arr, progress_callback):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        progress_callback(arr.copy(), i, min_idx)
        time.sleep(0.1)

def bubble_sort(arr, progress_callback):
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                progress_callback(arr.copy(), j, j + 1)
                time.sleep(0.1)

def insertion_sort(arr, progress_callback):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            progress_callback(arr.copy(), j + 1, i)
            time.sleep(0.1)
        arr[j + 1] = key

def merge_sort(arr, progress_callback):
    def merge(left, right):
        result = []
        while left and right:
            if left[0] < right[0]:
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        result.extend(left or right)
        return result

    def merge_sort_recursive(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = merge_sort_recursive(arr[:mid])
        right = merge_sort_recursive(arr[mid:])
        sorted_arr = merge(left, right)
        progress_callback(sorted_arr, -1, -1)
        time.sleep(0.1)
        return sorted_arr

    sorted_arr = merge_sort_recursive(arr.copy())
    arr[:] = sorted_arr

def quick_sort(arr, progress_callback):
    def quick_sort_recursive(arr, low, high):
        if low < high:
            pivot = partition(arr, low, high)
            quick_sort_recursive(arr, low, pivot - 1)
            quick_sort_recursive(arr, pivot + 1, high)
            progress_callback(arr.copy(), low, high)
            time.sleep(0.1)

    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    quick_sort_recursive(arr, 0, len(arr) - 1)

def heap_sort(arr, progress_callback):
    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)
            progress_callback(arr.copy(), i, largest)
            time.sleep(0.3)

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

def plot_array(arr, title, container, highlight1=None, highlight2=None):
    fig, ax = plt.subplots(figsize=(10, 1))
    ax.set_xlim(-1, len(arr))
    ax.set_ylim(0, 2)
    for idx, num in enumerate(arr):
        ax.text(idx, 1, str(num), ha='center', va='center', fontsize=12, fontweight='bold')
        ax.add_patch(patches.Rectangle((idx - 0.4, 0.5), 0.8, 1, edgecolor='black', facecolor='lightgreen' if idx in [highlight1, highlight2] else 'lightgray'))
    ax.axis('off')
    ax.set_title(title)
    container.pyplot(fig)

def visualize_sorting():
    st.subheader("Sorting Algorithm Visualizer")

    selected_algorithm = st.selectbox("Choose Sorting Algorithm", list(SORTING_ALGORITHMS.keys()))

    if "array" not in st.session_state or st.button("Generate New Array"):
        st.session_state.array = np.random.randint(1, 100, 10)

    arr = st.session_state.array.copy()

    original_chart = st.empty()
    plot_array(arr, "Original Array", original_chart)

    sorting_area = st.empty()
    sorted_array_display = st.empty()

    def update_chart(updated_arr, i, min_idx):
        plot_array(updated_arr, "Sorting in Progress...", sorting_area, i, min_idx)

    if st.button("Start Sorting"):
        globals()[SORTING_ALGORITHMS[selected_algorithm]](arr, update_chart)
        plot_array(arr, "Sorted Array", sorted_array_display)
