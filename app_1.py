Here is the extracted requirements in structured software requirements format:

```
# Auto-generated Multi-Agent Workflow (MAW)

Feature Name: Auto-generated Multi-Agent Workflow (MAW)
Problem Statement: Develop an AI-powered workflow that automates routine tasks and enhances collaboration among team members.

User Story:
As a project manager, I want to create a multi-agent workflow that streamlines tasks and facilitates communication among team members, so that we can increase productivity and reduce errors.

Acceptance Criteria:

1. The MAW system generates workflows automatically based on predefined rules.
2. The system integrates with existing tools and platforms for seamless data exchange.
3. Users can visualize and track the workflow's progress in real-time.
4. The system provides notifications and alerts for task assignments, deadlines, and dependencies.

Functional Requirements:

1. **Workflow Generation**: The system should generate workflows based on predefined rules and templates.
2. **Task Assignment**: The system should assign tasks to team members according to their roles and expertise.
3. **Progress Tracking**: The system should provide real-time updates on task progress and status.
4. **Dependency Management**: The system should manage dependencies between tasks and ensure that critical tasks are completed before moving forward.

Non-Functional Requirements:

1. **Scalability**: The system should be able to handle increasing workload and user traffic without compromising performance.
2. **Security**: The system should ensure secure data exchange and storage, adhering to industry standards for confidentiality and integrity.
3. **Usability**: The system should provide an intuitive interface that is easy to use for team members with varying levels of technical expertise.

Dependencies:

1. Integration with existing project management tools (e.g., Trello, Asana)
2. Compatibility with various platforms and devices
3. APIs from AI Factory for workflow generation and task assignment

Tech Stack Notes:

1. Programming language: Python or Java
2. Framework: Django or Spring Boot
3. Database: MySQL or PostgreSQL
4. Integration libraries: RESTful API clients for existing tools and platforms

Here is the Python Streamlit app code:
```

```
import streamlit as st
from plotly import graph_objs as go
from yfinance import Ticker

st.title("Auto-generated Multi-Agent Workflow (MAW)")
st.header("Current Market Data")

stock = st.text_input("Enter stock ticker symbol", value="AAPL")
search_button = st.button("Search")

if search_button:
    try:
        stock_info = Ticker(stock).info
        market_cap = stock_info['marketCap']
        sector = stock_info['sector']
        industry = stock_info['industry']

        fig = go.Figure(data=[go.Bar(x=['Market Cap', 'Sector', 'Industry'],
                                    y=[market_cap, sector, industry])])
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error: {e}")

st.header("Top 5 Increase and Decrease by Volume")
vol_data = []
for i in range(5):
    vol_data.append(go.Bar(x=['Increase', 'Decrease'],
                            y=[100, -50], name=f"{i+1}"))

fig_vol = go.Figure(data=vol_data)
st.plotly_chart(fig_vol)

st.header("Search Stock by Code or Name")
code_name = st.text_input("Enter stock code or name", value="AAPL")

if code_name:
    try:
        stock_info = Ticker(code_name).info
        market_cap = stock_info['marketCap']
        sector = stock_info['sector']
        industry = stock_info['industry']

        fig_search = go.Figure(data=[go.Bar(x=['Market Cap', 'Sector', 'Industry'],
                                            y=[market_cap, sector, industry])])
        st.plotly_chart(fig_search)

    except Exception as e:
        st.error(f"Error: {e}")

```

Note that this code is only for the Streamlit app and does not include any AI Factory workflow generation or task assignment functionality.