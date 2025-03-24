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


reference_string = st.text_input("Enter Reference String (comma-separated)", "7,0,1,2,0,3,4,2,3,0,3,2")
frames = st.number_input("Enter Number of Frames", min_value=1, value=3, step=1)
algorithm = st.selectbox("Choose Algorithm", ["FIFO", "LRU", "Optimal"])

st.button("Run Simulation")

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