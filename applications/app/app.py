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
    """
    Resets the session state for the A/B testing process, returning to the initial segment selection step.
    """
    st.session_state.ab_step = "select_segment"
    st.session_state.selected_segment = None
    st.session_state.test_goal = None
    st.session_state.package_type = None
    st.session_state.engagement_strategy = None
    st.session_state.results_ready = False
    st.session_state.customer_details = {}

def fetch_data(endpoint, filters=None):
    """
    Fetches data from the given API endpoint with optional filters.

    **Parameters:**
    - `endpoint (str)`: The API endpoint to fetch data from.
    - `filters (dict, optional)`: A dictionary of filters to apply on the data.

    **Returns:**
    - `pd.DataFrame`: A pandas DataFrame with the fetched data. An empty DataFrame is returned in case of failure.

    **Raises:**
    - `requests.exceptions.RequestException`: If there's an issue with the request, it raises an exception.
    """
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

def get_max_experiment_id_data():
    """
    Fetches A/B test results data and returns the rows with the maximum experiment ID.

    **Parameters:**
    - No parameters.

    **Returns:**
    - `pd.DataFrame`: The filtered data containing rows with the maximum experiment ID.

    **Raises:**
    - `Exception`: If no data is fetched or the dataset is empty, an error is logged.
    """

    ab_test_results_data = fetch_data("ab_test_results")

    if not ab_test_results_data.empty:
        max_experiment_id = ab_test_results_data['experiment_id'].max()
        max_experiment_data = ab_test_results_data[ab_test_results_data['experiment_id'] == max_experiment_id]
        return max_experiment_data
    else:
        st.error("No data fetched or empty dataset.")
        return pd.DataFrame()

def add_customer_to_backend(name, email, location, sub_id):
    """
    Adds a new customer to the backend database.

    **Parameters:**
    - `name (str)`: Customer's name.
    - `email (str)`: Customer's email.
    - `location (str)`: Customer's location.
    - `sub_id (str)`: Customer's subscription ID.

    **Returns:**
    - `Response`: The response from the API after adding the customer.

    **Raises:**
    - `ValueError`: If the subscription ID is empty or invalid, an exception is raised.
    """
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

def get_barchart_data(data, ab_test_ids):
    """
    Generates bar chart data based on A/B test results for each test ID.

    **Parameters:**
    - `data (pd.DataFrame)`: The data containing A/B test results.
    - `ab_test_ids (list)`: A list of A/B test IDs to filter the data by.

    **Returns:**
    - `pd.DataFrame`: The data formatted for a bar chart.
    - `list`: List of customer IDs for each A/B test.

    **Raises:**
    - `KeyError`: If the specified columns or values are missing in the data, it may raise an error.
    """
    bar_chart_data = []
    customer_ids = []

    for ab_test_id in ab_test_ids:
        filtered = data[data['ab_test_id'] == ab_test_id]
        counts = filtered['clicked_link'].value_counts()
        
        true_count = counts.get(True, 0)  # Access counts directly by key 'True'
        false_count = counts.get(False, 0)  # Access counts directly by key 'False'

        bar_chart_data.append({
            "Clicked Link": "True",
            "Frequency": true_count
        })
        bar_chart_data.append({
            "Clicked Link": "False",
            "Frequency": false_count
        })

        # Collect customer IDs for the current ab_test_id
        customer_ids.append(filtered['customer_id'].unique())

    return pd.DataFrame(bar_chart_data), customer_ids

def send_emails(segment_name, text_skeleton_1, text_skeleton_2, ab_test_id_a, ab_test_id_b):
    """
    Sends emails using the given parameters.

    **Parameters:**
    - `segment_name (str)`: The name of the customer segment.
    - `text_skeleton_1 (str)`: The first email template.
    - `text_skeleton_2 (str)`: The second email template.
    - `ab_test_id_a (int)`: The A/B test ID for version A.
    - `ab_test_id_b (int)`: The A/B test ID for version B.

    **Returns:**
    - `Response`: The response from the API after sending the emails.

    **Raises:**
    - `requests.exceptions.RequestException`: If there's an issue with the request, it raises an exception.
    """
    response = requests.post(
        f"{API_URL}/send-emails",
        json={
            "segment_name": segment_name,
            "text_skeleton_1": text_skeleton_1,
            "text_skeleton_2": text_skeleton_2,
            "ab_test_id_a" : int(ab_test_id_a),
            "ab_test_id_b" : int(ab_test_id_b)
        }
    )
    return response

# Sidebar menu for navigation
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
    st.write("This link provides access to the detailed documentation of the project. It covers the entire system, including the backend API, frontend application, database setup, and the A/B testing workflow.")
    st.write("Click on the link below to access the documentation:")
    doc_url = "https://anialoyann.github.io/DS223-project/"
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
        
        if st.button("Back"):
            reset_app()
            st.experimental_rerun()  # Go back to the initial page

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
        
        if st.button("Back"):
            st.session_state.ab_step = "select_segment"
            st.experimental_rerun()  # Go back to the segment selection page

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

                response = send_emails(
                    st.session_state.selected_segment,
                    st.session_state.results[0],
                    st.session_state.results[1],
                    ab_tests_data["ab_test_id"][0],
                    ab_tests_data["ab_test_id"][1]
                )
                if response.status_code == 200:
                    st.success("Emails sent successfully! Click Again")
                    st.session_state.ab_step = "results_ready"
                else:
                    st.error(f"Failed to send emails: {response.json()['detail']}")
            else:
                st.error("No A/B test skeletons available for Subscription.")

        if st.button("Back"):
            st.session_state.ab_step = "select_goal"
            st.experimental_rerun()  # Go back to goal selection page

    elif st.session_state.ab_step == "select_engagement_strategy":
        st.title("Start A/B Testing")
        st.subheader(f"Step 3: Selected Goal: {st.session_state.test_goal}")
        st.subheader("Choose an Engagement Strategy")

        engagement_strategy = st.selectbox("Select a strategy:", ["by genre", "by movie"])

        context_value = None
        if engagement_strategy == "by genre":
            genres_data = fetch_data("movies", filters={"type": "movie_genre"})
            if not genres_data.empty:
                context_value = st.selectbox("Select a genre:", genres_data["movie_genre"].unique())
        elif engagement_strategy == "by movie":
            movies_data = fetch_data("movies", filters={"type": "movie_name"})
            if not movies_data.empty:
                context_value = st.selectbox("Select a movie:", movies_data["movie_name"].unique())

        if st.button("Confirm and Launch A/B Test"):
            st.session_state.engagement_strategy = engagement_strategy
            st.session_state.context_value = context_value

            ab_tests_data = fetch_data("ab_tests", filters={"goal": "engagement", "targeting": engagement_strategy})
            if not ab_tests_data.empty:
                results = ab_tests_data["text_skeleton"].apply(
                    lambda x: x.replace("(insert the movie here)", context_value)
                    .replace("(insert your genre)", context_value)
                )
                st.session_state.results_ready = True
                st.session_state.results = results.tolist()

                if engagement_strategy == 'by genre':
                    response = send_emails(
                        st.session_state.selected_segment,
                        st.session_state.results[0],
                        st.session_state.results[1],
                        ab_tests_data["ab_test_id"][4],
                        ab_tests_data["ab_test_id"][5]
                    )
                if engagement_strategy == 'by movie':
                    response = send_emails(
                        st.session_state.selected_segment,
                        st.session_state.results[0],
                        st.session_state.results[1],
                        ab_tests_data["ab_test_id"][2],
                        ab_tests_data["ab_test_id"][3]
                    )
                if response.status_code == 200:
                    st.success("Emails sent successfully! Click Again")
                    st.session_state.ab_step = "results_ready"
                else:
                    st.error(f"Failed to send emails: {response.json()['detail']}")
            else:
                st.error("No A/B test skeletons available for Engagement.")

        if st.button("Back"):
            st.session_state.ab_step = "select_goal"
            st.experimental_rerun()  # Go back to goal selection page


    elif st.session_state.ab_step == "results_ready":
        st.title("A/B Test Results")
        st.subheader(f"Results for Segment: {st.session_state.selected_segment}")

        if "results" in st.session_state and st.session_state.results:
            st.write("Here are the generated messages:")
            for result in st.session_state.results:
                st.markdown(f"- {result}")
        else:
            st.write("No results available.")

        st.subheader("You will see the results shortly")
        if st.button("View the results"):
            st.session_state.ab_step = "view_results"

    elif st.session_state.ab_step == "view_results":
        st.title("A/B Testing Results")
        st.subheader("Graphical Results")

        filtered_data = get_max_experiment_id_data()
        st.write(filtered_data)

        ab_test_idx = filtered_data["ab_test_id"].unique()
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Test Version A**")
            if len(ab_test_idx) > 0:
                bar_chart_data_1, customer_ids_1 = get_barchart_data(filtered_data, [ab_test_idx[0]])  # Pass as a list
                st.bar_chart(bar_chart_data_1.set_index("Clicked Link"))

            else:
                st.write("No data available for Test Version A")

        with col2:
            st.write(f"**Test Version B**")
            if len(ab_test_idx) > 1:
                bar_chart_data_2, customer_ids_2 = get_barchart_data(filtered_data, [ab_test_idx[1]])  # Pass as a list
                st.bar_chart(bar_chart_data_2.set_index("Clicked Link"))
                
            else:
                st.write("No data available for Test Version B")


        st.subheader("Results")
        experiment_id = filtered_data["experiment_id"].unique()
        experiments_table = fetch_data("experiments")
        experiments_table = experiments_table[experiments_table["experiment_id"] == int(experiment_id)]
        p_value = experiments_table["p_value"]
        st.write(f"P value for this A/B test is {float(p_value)}")

        if st.button("Refresh and Start Again"):
            reset_app()
            st.session_state.ab_step = "select_segment"
            st.experimental_rerun()
