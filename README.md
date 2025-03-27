# Efficient Page Replacement Algorithm Simulator

This project is a web-based simulator for comparing various page replacement algorithms used in operating systems. Built using **Streamlit**, the application allows users to visualize and analyze how different algorithms handle memory management.



## Features

- **Simulate Multiple Algorithms**:
  - First-In-First-Out (FIFO)
  - Least Recently Used (LRU)
  - Least Frequently Used (LFU)
  - Most Frequently Used (MFU)
  - Optimal Replacement
- **Customizable Input**:
  - Manually enter page reference sequences.
  - Automatically generate random page sequences of specified length.
- **Adjustable Frame Count**: Modify the number of available frames to observe the performance impact.
- **Step-by-Step Execution Logs**: Detailed logging of memory states after each page reference.
- **Performance Metrics**: Analyze page faults, page hits, and hit ratio for each algorithm.
- **Graphical Comparison**: Compare algorithm performance using bar charts.

## Installation

### Prerequisites
Ensure you have Python installed on your system. You can check by running:

```bash
python --version
```

### Clone the Repository

```bash
git clone https://github.com/yourusername/page-replacement-simulator.git
cd page-replacement-simulator
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

Run the application using:

```bash
streamlit run app.py
```

Once the application starts, you can select algorithms, input reference sequences, set the frame count, and analyze the results through the UI.

## Application Structure

- **`app.py`**: Main script for running the Streamlit application.
- **Algorithm Implementations**: Each algorithm is defined as a function handling page requests.
- **Graphing Functions**: Used to visualize comparative performance.
