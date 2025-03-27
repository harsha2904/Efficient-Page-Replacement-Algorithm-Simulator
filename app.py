import streamlit as st
import matplotlib.pyplot as plt
from collections import deque, Counter

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


#added lru functionality
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
#this function used to store pages that are recently used with min time 
#when there is no enough memory to store the pages, we'll see less recently used page and replace it with current page
#lru fixed 

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

def plot_results(results):
    labels, faults, hits = zip(*[(algo, faults, hits) for algo, faults, hits, _ in results])
    fig, ax = plt.subplots()
    ax.bar(labels, faults, color='red', label='Page Faults')
    ax.bar(labels, hits, bottom=faults, color='green', label='Page Hits')
    ax.set_xlabel("Algorithms")
    ax.set_ylabel("Counts")
    ax.set_title("Page Replacement Algorithm Comparison")
    ax.legend()
    st.pyplot(fig)


def main():
    st.title("Efficient Page Replacement Algorithm Simulator")
    length = st.number_input("Enter the length of the trace:", min_value=1, step=1)
    manual = st.radio("Do you want to enter pages manually?", ("Yes", "No"))
    
    if manual == "Yes":
        pages = st.text_area("Enter space-separated page references:")
        pages = list(map(int, pages.split())) if pages else []
    else:
        import random
        pages = [random.randint(1, 10) for _ in range(length)]
        st.write("Generated Page References:", pages)
    
    frames = st.number_input("Enter the number of frames:", min_value=1, step=1)
    
    algorithms = {"FIFO": fifo, "LRU": lru, "LFU": lfu, "MFU": mfu, "Optimal": optimal}
    selected_algos = st.multiselect("Select algorithms to run:", list(algorithms.keys()), default=list(algorithms.keys()))
    
    if st.button("Run Simulation"):
        results = [(name, *func(pages, frames)) for name, func in algorithms.items() if name in selected_algos]
        
        for name, faults, hits, frame_updates in results:
            total = faults + hits
            st.subheader(f"{name} Algorithm")
            st.text_area("Frame Updates", '\n'.join(frame_updates), height=200)
            st.write(f"Page Faults: {faults}, Page Hits: {hits}")
            st.write(f"Miss Ratio: {faults / total:.2%}, Hit Ratio: {hits / total:.2%}")
        
        plot_results(results)

if __name__ == "__main__":
    main()







