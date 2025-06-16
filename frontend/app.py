import streamlit as st
import requests

st.title("Course Picker")
option = st.sidebar.selectbox("Choose an option", ["Register", "Login", "Student Dashboard", "Admin Panel"])

if option == "Register":
    st.header("Register")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    cluster = st.number_input("Cluster Points")
    
    if st.button("Register"):
        response = requests.post("http://localhost:8000/register", json={
            "name": name,
            "email": email,
            "password": password,
            "cluster_points": cluster
        })
        if response.status_code == 200:
            st.success("🎉 Registration successful! You can now login.")
        else:
            try:
                st.error(response.json().get("detail", "❌ Registration failed. Please try again."))
            except ValueError:
                st.error("❌ Registration failed. Server did not return valid JSON.")

elif option == "Login":
    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        response = requests.post("http://localhost:8000/token", data={
            "username": email,
            "password": password
        })
        if response.status_code == 200:
            st.success("✅ Login successful! You can now view your dashboard.")
        else:
            try:
                st.error(response.json().get("detail", "❌ Login failed. Please check your credentials."))
            except ValueError:
                st.error("❌ Login failed. Server did not return valid JSON.")

elif option == "Student Dashboard":
    st.header("Personalized Course Recommendations")
    email = st.text_input("Enter your registered email")
    
    if st.button("Get My Courses"):
        response = requests.get(f"http://localhost:8000/recommend/{email}")
        if response.status_code == 200:
            courses = response.json()
            if courses:
                for course in courses:
                    st.subheader(course['title'])
                    st.markdown(f"**Description:** {course['description']}")
                    st.markdown(f"**Expected Pay:** {course['expected_pay']}")
                    st.markdown(f"**Industries:** {course['industries']}")
                    st.markdown(f"**Skills Needed:** {course['skills_needed']}")
                    st.success("🎉 Congratulations! This course suits you.")
            else:
                st.info("No recommended courses found for your cluster points.")
        else:
            try:
                st.error(response.json().get("detail", "Student not found or error occurred."))
            except ValueError:
                st.error("Failed to fetch course recommendations.")

elif option == "Admin Panel":
    st.header("Manage Courses")
    title = st.text_input("Course Title")
    description = st.text_area("Description")
    min_cluster = st.number_input("Minimum Cluster")
    expected_pay = st.text_input("Expected Pay")
    industries = st.text_area("Industries")
    skills = st.text_area("Skills Needed")

    if st.button("Add Course"):
        response = requests.post("http://localhost:8000/courses", json={
            "title": title,
            "description": description,
            "min_cluster": min_cluster,
            "expected_pay": expected_pay,
            "industries": industries,
            "skills_needed": skills
        })
        if response.status_code == 200:
            st.success("✅ Course added successfully!")
        else:
            st.error("❌ Failed to add course.")
