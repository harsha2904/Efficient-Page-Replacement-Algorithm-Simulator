import streamlit as st

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