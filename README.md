# FoodieeDash – Restaurant Analytics Dashboard

FoodieeDash is a simple restaurant order management and analytics dashboard built using Python and Streamlit. The application allows users to place food orders and helps restaurant administrators analyze sales and customer preferences using a visual dashboard.

# Problem
Small restaurants often manage orders manually or with simple spreadsheets. This makes it difficult to:
Track sales
Understand customer preferences
Analyze business performance
FoodieeDash provides a simple system to record orders and generate useful insights from the collected data.

# Why It Matters
Restaurant owners need quick access to information such as:
Total sales
Popular dishes
Order trends
This project demonstrates how a lightweight dashboard can help businesses make better decisions using data.

# Technical Approach
The application is built using the following technologies:
Python for backend logic
Streamlit for building the web interface
Pandas for data processing
CSV file storage for saving order data
Streamlit charts for data visualization
Orders placed by users are stored in a CSV file. The admin dashboard reads this data and generates charts and statistics.

# System Architecture
User Interface (Streamlit)
→ Order Input System
→ CSV Data Storage
→ Data Processing with Pandas
→ Admin Analytics Dashboard

# Results
The dashboard provides the following features:
Record food orders
Track total revenue
Identify popular menu items
View sales trends through charts
This helps restaurant owners understand their business performance quickly.

# How to Run the Project
1. Clone the repository
git clone https://github.com/surajpoddar13/FoodieeDash.git
cd FoodieeDash

2. Install dependencies
pip install -r requirements.txt

3. Run the application
streamlit run app.py

# The application will open in your browser at:
http://localhost:8501

# Future Improvements
Possible improvements include:

Using a database instead of CSV storage
Adding user authentication
Improving analytics and reporting features
Deploying the application on cloud platforms

https://github.com/user-attachments/assets/c6e64256-2fe1-4fa0-bde9-503a4256d986
