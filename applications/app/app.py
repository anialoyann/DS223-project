import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timezone

if "ab_step" not in st.session_state:
    st.session_state.ab_step = "select_segment"  
if "selected_segment" not in st.session_state:
    st.session_state.selected_segment = None  
if "test_goal" not in st.session_state:
    st.session_state.test_goal = None 
if "package_type" not in st.session_state:
    st.session_state.package_type = None 
if "engagement_strategy" not in st.session_state:
    st.session_state.engagement_strategy = None 
if "results_ready" not in st.session_state:
    st.session_state.results_ready = False 
if "customer_details" not in st.session_state:
    st.session_state.customer_details = {} 

API_URL = "http://api:8000"  # Adjust to your backend API's URL

def reset_app():
    st.session_state.ab_step = "select_segment"
    st.session_state.selected_segment = None
    st.session_state.test_strategy = None
    st.session_state.package_type = None
    st.session_state.engagement_strategy = None
    st.session_state.results_ready = False
    st.session_state.customer_details = {}

def fetch_data(endpoint, filters=None):
    """Fetch data from a specific endpoint with optional filters."""
    try:
        response = requests.get(f"{API_URL}/{endpoint}/")
        if response.status_code == 200:
            data = pd.DataFrame(response.json())
            if filters:
                for key, value in filters.items():
                    if key in data.columns:
                        data = data[data[key].str.lower() == value.lower()]
            return data
        else:
            st.error(f"Failed to fetch data from {endpoint}: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching data from {endpoint}: {e}")
        return pd.DataFrame()

def add_customer_to_backend(name, email, location, sub_id):
    if not sub_id:
        raise ValueError("subscription_id is required")
    
    payload = {
        "name": name,
        "email": email,
        "location": location,  
        "subscription_id": sub_id
    }
    response = requests.post(f"{API_URL}/customers/", json=payload)
    return response

st.sidebar.title("Menu")
page = st.sidebar.radio(
    "Navigation",
    ["General", "Dashboard", "Start A/B Testing", "Settings"],
)


if page == "General":
    st.title("Welcome!")
    st.write("Here, you can add a new customer.")

    name = st.text_input("Customer's Name")
    email = st.text_input("Customer's Email Address")
    location = st.text_input("Customer's Location")
    subscription_id = st.text_input("Customer's Subscription ID")

    if st.button("Add the Customer"):
        if name and subscription_id and email:
            if subscription_id.isdigit():  # Validate that subscription ID is numeric
                response = add_customer_to_backend(name, email, location, sub_id=subscription_id)
                if response.status_code == 200:
                    st.success("Customer was added successfully!")
                else:
                    st.error(f"Failed to add customer. Error: {response.text}")
            else:
                st.warning("Subscription ID must be a number.")
        else:
            st.warning("Please fill in all the information.")

elif page == "Dashboard":
    st.title("Welcome to the Dashboard!")
    col1, col2 = st.columns(2)

    # Placeholder 1: Segments Table
    with col1:
        st.subheader("Customer Segments")
        segments_data = fetch_data("segments")
        if not segments_data.empty:
            st.table(segments_data.rename(columns={
                "segment_id": "Segment ID", 
                "segment_name": "Segment Name", 
                "segment_description": "Segment Description"
            }))
        else:
            st.write("No segments data available.")

    # Placeholder 2: Frequency Chart for Customer Segments
    with col2:
        st.subheader("Segment Frequency Chart")
        customer_segments_data = fetch_data("customer_segments")
        if not customer_segments_data.empty:
            # Calculate frequency of each segment_id
            frequency = customer_segments_data["segment_id"].value_counts().reset_index()
            frequency.columns = ["Segment ID", "Frequency"]
            
            # Merge with segment names for better labeling
            if not segments_data.empty:
                frequency = frequency.merge(
                    segments_data[["segment_id", "segment_name"]],
                    left_on="Segment ID",
                    right_on="segment_id",
                    how="left"
                )
                frequency["Segment Name"] = frequency["segment_name"]
                frequency = frequency[["Segment Name", "Frequency"]]
            else:
                frequency["Segment Name"] = frequency["Segment ID"]

            st.bar_chart(frequency.set_index("Segment Name")["Frequency"])
        else:
            st.write("No customer segment data available.")

elif page == "Settings":
    st.title("Settings")
    st.subheader("Need help?")
    st.write("Click on the link below to access the documentation:")
    doc_url = "https://link.will.be.here.url"
    st.markdown(f"{doc_url}", unsafe_allow_html=True)

if page == "Start A/B Testing":
    if st.session_state.ab_step == "select_segment":
        st.title("Start A/B Testing")
        st.subheader("Step 1: Select a Customer Segment")

        segments_data = fetch_data("segments")
        if not segments_data.empty:
            selected_segment = st.selectbox("Choose a segment:", segments_data["segment_name"].unique())

            if st.button("Proceed to Goal Selection"):
                st.session_state.selected_segment = selected_segment
                st.session_state.ab_step = "select_goal"
        else:
            st.error("No segments available to select.")

    elif st.session_state.ab_step == "select_goal":
        st.title("Start A/B Testing")
        st.subheader(f"Step 2: Selected Segment: {st.session_state.selected_segment}")
        st.subheader("Choose the Goal of the Test")

        goals_data = fetch_data("ab_tests", filters={"segment_name": st.session_state.selected_segment})
        if not goals_data.empty:
            test_goal = st.selectbox("Select the goal:", goals_data["goal"].unique())

            if st.button("Proceed"):
                st.session_state.test_goal = test_goal
                if test_goal.lower() == "subscription":
                    st.session_state.ab_step = "select_package"
                elif test_goal.lower() == "engagement":
                    st.session_state.ab_step = "select_engagement_strategy"
        else:
            st.error("No goals available for the selected segment.")

    elif st.session_state.ab_step == "select_package":
        st.title("Start A/B Testing")
        st.subheader(f"Step 3: Selected Goal: {st.session_state.test_goal}")
        st.subheader("Choose a Subscription Package")

        package_type = st.selectbox("Select a package type:", ["Basic", "Premium", "Family"])
        price = st.number_input("Enter the package price:", min_value=0, value=10)

        if st.button("Confirm and Launch A/B Test"):
            st.session_state.package_type = package_type
            st.session_state.price = price

            ab_tests_data = fetch_data("ab_tests", filters={"goal": "subscription"})
            if not ab_tests_data.empty:
                results = ab_tests_data["text_skeleton"].apply(
                    lambda x: x.replace("(insert your subscription plan here)", package_type)
                             .replace("(insert your price here)", f"{price} dollars")
                )
                st.session_state.results_ready = True
                st.session_state.results = results.tolist()
                st.session_state.ab_step = "results_ready"
            else:
                st.error("No A/B test skeletons available for Subscription.")

    elif st.session_state.ab_step == "select_engagement_strategy":
        st.title("Start A/B Testing")
        st.subheader(f"Step 3: Selected Goal: {st.session_state.test_goal}")
        st.subheader("Choose an Engagement Strategy")

        engagement_strategy = st.selectbox("Select a strategy:", ["By Genre", "By Movie"])

        context_value = None
        if engagement_strategy == "By Genre":
            genres_data = fetch_data("movies", filters={"type": "movie_genre"})
            if not genres_data.empty:
                context_value = st.selectbox("Select a genre:", genres_data["movie_genre"].unique())
        elif engagement_strategy == "By Movie":
            movies_data = fetch_data("movies", filters={"type": "movie_name"})
            if not movies_data.empty:
                context_value = st.selectbox("Select a movie:", movies_data["movie_name"].unique())

        if st.button("Confirm and Launch A/B Test"):
            st.session_state.engagement_strategy = engagement_strategy
            st.session_state.context_value = context_value

            ab_tests_data = fetch_data("ab_tests", filters={"goal": "engagement", "targeting" : engagement_strategy})
            if not ab_tests_data.empty:
                results = ab_tests_data["text_skeleton"].apply(
                    lambda x: x.replace("(insert the movie here)", context_value)
                             .replace("(insert your genre)", context_value)
                )
                st.session_state.results_ready = True
                st.session_state.results = results.tolist()
                st.session_state.ab_step = "results_ready"
            else:
                st.error("No A/B test skeletons available for Engagement.")

    elif st.session_state.ab_step == "results_ready":
        st.title("A/B Test Results")
        st.subheader(f"Results for Segment: {st.session_state.selected_segment}")

        if "results" in st.session_state and st.session_state.results:
            st.write("Here are the generated messages:")
            for result in st.session_state.results:
                st.markdown(f"- {result}")
        else:
            st.write("No results available.")

        st.subheader("You will see the results in 2 minutes.")
        if st.button("View the results"):
            st.session_state.ab_step = "view_results"

    elif st.session_state.ab_step == "view_results":
        st.title("A/B Testing Results")
        st.subheader("Graphical Results")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Placeholder 1**")
            data_1 = pd.DataFrame({
                "X": [1, 2, 3, 4],
                "Y": [2, 4, 6, 8]
            })
            st.line_chart(data_1.set_index('X'))

        with col2:
            st.write("**Placeholder 2**")
            data_2 = pd.DataFrame({
                "X": [1, 2, 3, 4],
                "Y": [8, 6, 4, 2]
            })
            st.line_chart(data_2.set_index('X'))

        st.subheader("P-Value")
        st.write("P value is ...")  

        if st.button("Refresh and Start Again"):
            reset_app()  
            st.session_state.ab_step = "select_segment"
            st.experimental_rerun()
