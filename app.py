import streamlit as st
import matplotlib.pyplot as plt

st.title("Hello, Streamlit!")
st.write("This is my first Streamlit app.")

def fifo(self):
        page_faults = 0
        memory = []
        for page in self.reference_string:
            if page not in memory:
                if len(memory) < self.frames:
                    memory.append(page)
                else:
                    memory.pop(0)
                    memory.append(page)
                page_faults += 1
        return page_faults

#added lru functionality
#this function used to store pages that are recently used with min time 
#when there is no enough memory to store the pages, we'll see less recently used page and replace it with current page

def lru(self):
        page_faults = 0
        memory = []
        recent_usage = {}#stores  time, to check least recently used page 
        for i, page in enumerate(self.reference_string): #list of pages that algo will enumerate
            if page not in memory:
                if len(memory) < self.frames:
                    memory.append(page)
                else:
                    lru_page = min(memory, key=lambda p: recent_usage.get(p, float('-inf')))#gets most recently used page
                    memory.remove(lru_page)
                    memory.append(page)
                page_faults += 1
            recent_usage[page] = i
        return page_faults


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


