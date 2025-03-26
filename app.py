import streamlit as st
import matplotlib.pyplot as plt

st.title("Hello, Streamlit!")
st.write("This is my first Streamlit app.")

#added fifo functionality
def fifo(pages, frames):
    memory, page_faults, page_hits = deque(), 0, 0
    frame_updates = []
    
    for page in pages:
        if page in memory:
            page_hits += 1
        else:
            page_faults += 1
            if len(memory) == frames:
                memory.popleft()
            memory.append(page)
        frame_updates.append(f"{page} : {' '.join(map(str, memory))}")
    
    return page_faults, page_hits, frame_updates


#added lru functionality
#this function used to store pages that are recently used with min time 
#when there is no enough memory to store the pages, we'll see less recently used page and replace it with current page
#lru fixed 
def lru(pages, frames):
    memory, page_faults, page_hits = [], 0, 0
    frame_updates = []
    
    for page in pages:
        if page in memory:
            page_hits += 1
            memory.remove(page)
        else:
            page_faults += 1
            if len(memory) == frames:
                memory.pop(0)
        memory.append(page)
        frame_updates.append(f"{page} : {' '.join(map(str, memory))}")
    
    return page_faults, page_hits, frame_updates


#added lfu with some fixes
def lfu(pages, frames):
    memory, freq, page_faults, page_hits = [], Counter(), 0, 0
    frame_updates = []
    
    for page in pages:
        if page in memory:
            page_hits += 1
        else:
            page_faults += 1
            if len(memory) == frames:
                least_used = min(memory, key=lambda p: freq[p])
                memory.remove(least_used)
            memory.append(page)
        freq[page] += 1
        frame_updates.append(f"{page} : {' '.join(map(str, memory))}")
    
    return page_faults, page_hits, frame_updates

#added mfu function
def mfu(pages, frames):
    memory, freq, page_faults, page_hits = [], Counter(), 0, 0
    frame_updates = []
    
    for page in pages:
        if page in memory:
            page_hits += 1
        else:
            page_faults += 1
            if len(memory) == frames:
                most_used = max(memory, key=lambda p: freq[p])
                memory.remove(most_used)
            memory.append(page)
        freq[page] += 1
        frame_updates.append(f"{page} : {' '.join(map(str, memory))}")
    
    return page_faults, page_hits, frame_updates

#optimal funtion is added
def optimal(pages, frames):
    memory, page_faults, page_hits = [], 0, 0
    frame_updates = []

    for i, page in enumerate(pages):
        if page in memory:
            page_hits += 1
        else:
            page_faults += 1
            if len(memory) == frames:
                future_use = {}
                for mem_page in memory:
                    try:
                        future_use[mem_page] = pages[i+1:].index(mem_page)
                    except ValueError:
                        future_use[mem_page] = float('inf')
                page_to_replace = max(future_use, key=future_use.get)
                memory.remove(page_to_replace)
            memory.append(page)
        frame_updates.append(f"{page} : {' '.join(map(str, memory))}")
    
    return page_faults, page_hits, frame_updates


reference_string = st.text_input("Enter Reference String (comma-separated)", "7,0,1,2,0,3,4,2,3,0,3,2")
frames = st.number_input("Enter Number of Frames", min_value=1, value=3, step=1)
algorithm = st.selectbox("Choose Algorithm", ["FIFO", "LRU", "Optimal"])

try:
    reference_list = list(map(int, reference_string.split(',')))

    if st.button("Run Simulation"):
        simulator = PageReplacement(frames, reference_list)

        if algorithm == "FIFO":
            page_faults = simulator.fifo()
        elif algorithm == "LRU":
            page_faults = simulator.lru()
        else:
            page_faults = simulator.optimal()

        st.success(f"Total Page Faults ({algorithm}): {page_faults}")

        # Visualization
        results = {
            "FIFO": simulator.fifo(),
            "LRU": simulator.lru(),
            "Optimal": simulator.optimal()
        }

        fig, ax = plt.subplots()
        ax.bar(results.keys(), results.values(), color=['blue', 'green', 'red'])
        ax.set_xlabel("Algorithm")
        ax.set_ylabel("Page Faults")
        ax.set_title("Page Replacement Algorithm Comparison")
        st.pyplot(fig)

except ValueError:
    st.error("Invalid input! Please enter numbers separated by commas.")


