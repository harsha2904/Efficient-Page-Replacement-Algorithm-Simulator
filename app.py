import streamlit as st
import matplotlib.pyplot as plt
from collections import deque, Counter

def FIFO(page_sequence, num_frames):
    frame_queue = deque()
    misses = 0
    hits = 0
    history_log = []
    
    for current in page_sequence:
        if current in frame_queue:
            hits += 1
        else:
            misses += 1
            if len(frame_queue) >= num_frames:
                frame_queue.popleft()
            frame_queue.append(current)
        history_log.append(f"Page {current} → Memory: {' | '.join(map(str, frame_queue))}")
    
    return misses, hits, history_log

def LRU(page_refs, frame_count):
    memory_stack = []
    fault_count = 0
    hit_count = 0
    step_details = []
    
    for reference in page_refs:
        if reference in memory_stack:
            hit_count += 1
            memory_stack.remove(reference)
        else:
            fault_count += 1
            if len(memory_stack) >= frame_count:
                memory_stack.pop(0)
        memory_stack.append(reference)
        step_details.append(f"Reference {reference} → Current frames: {' '.join(map(str, memory_stack))}")
    
    return fault_count, hit_count, step_details

def LFU(page_accesses, max_frames):
    active_frames = []
    frequency = Counter()
    faults = 0
    successful = 0
    timeline = []
    
    for acc in page_accesses:
        if acc in active_frames:
            successful += 1
        else:
            faults += 1
            if len(active_frames) >= max_frames:
                least_frequent = min(active_frames, key=lambda x: frequency[x])
                active_frames.remove(least_frequent)
            active_frames.append(acc)
        frequency[acc] += 1
        timeline.append(f"Access {acc} → Memory state: {' '.join(map(str, active_frames))}")
    
    return faults, successful, timeline

def MFU(page_requests, frame_limit):
    cached = []
    usage_count = Counter()
    page_faults = 0
    cache_hits = 0
    operation_log = []
    
    for request in page_requests:
        if request in cached:
            cache_hits += 1
        else:
            page_faults += 1
            if len(cached) >= frame_limit:
                most_used = max(cached, key=lambda x: usage_count[x])
                cached.remove(most_used)
            cached.append(request)
        usage_count[request] += 1
        operation_log.append(f"Request {request} → Cache: {' '.join(map(str, cached))}")
    
    return page_faults, cache_hits, operation_log

def OPTIMAL(page_stream, available_frames):
    current_frames = []
    misses = 0
    hits = 0
    execution_trace = []

    for idx, page in enumerate(page_stream):
        if page in current_frames:
            hits += 1
        else:
            misses += 1
            if len(current_frames) >= available_frames:
                future_access = {}
                for frame in current_frames:
                    try:
                        future_access[frame] = page_stream[idx+1:].index(frame)
                    except ValueError:
                        future_access[frame] = float('inf')
                to_evict = max(future_access.items(), key=lambda x: x[1])[0]
                current_frames.remove(to_evict)
            current_frames.append(page)
        execution_trace.append(f"Page {page} → Frames: {' '.join(map(str, current_frames))}")
    
    return misses, hits, execution_trace

def Plot(algorithm_results):
    names, fault_data, hit_data = zip(*[(name, faults, hits) for name, faults, hits, _ in algorithm_results])
    
    fig, axis = plt.subplots(figsize=(10, 6))
    axis.bar(names, fault_data, color='#ff7f0e', label='Page Faults')
    axis.bar(names, hit_data, bottom=fault_data, color='#1f77b4', label='Page Hits')
    
    axis.set_xlabel("Page Replacement Strategies")
    axis.set_ylabel("Performance Metrics")
    axis.set_title("Comparative Analysis of Page Replacement Algorithms")
    axis.legend(loc='upper right')
    
    st.pyplot(fig)

def Execute():
    st.header("Efficient Page Replacement Algorithms Simulator")
    
    sequence_length = st.slider("Select reference sequence length:", 1, 50, 10)
    input_method = st.selectbox("Page reference input method:", ["Manual Entry", "Auto-generated"])
    
    if input_method == "Manual Entry":
        page_input = st.text_input("Enter page references (space-separated):")
        pages = list(map(int, page_input.split())) if page_input else []
    else:
        import random
        pages = [random.randint(1, 10) for _ in range(sequence_length)]
        st.code(f"Generated sequence: {pages}")
    
    frame_count = st.number_input("Number of available frames:", min_value=1, max_value=10, value=3)
    
    algorithm_map = {
        "First-In-First-Out": FIFO,
        "Least Recently Used": LRU,
        "Least Frequently Used": LFU,
        "Most Frequently Used": MFU,
        "Optimal Replacement": OPTIMAL
    }
    
    selected = st.multiselect("Select algorithms:", options=list(algorithm_map.keys()), default=list(algorithm_map.keys()))
    
    if st.button("Execute Algorithms"):
        performance_data = []
        
        for algo_name in selected:
            func = algorithm_map[algo_name]
            faults, hits, details = func(pages, frame_count)
            performance_data.append((algo_name, faults, hits, details))
            
            st.subheader(algo_name)
            st.text_area("Execution Details", '\n'.join(details), height=200)
            st.metric("Page Faults", faults)
            st.metric("Page Hits", hits)
            st.metric("Hit Ratio", f"{hits/(hits+faults):.1%}")
        
        Plot(performance_data)

if __name__ == "__main__":
    Execute()