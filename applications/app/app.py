import streamlit as st
import pandas as pd

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


def reset_app():
    st.session_state.ab_step = "select_segment"
    st.session_state.selected_segment = None
    st.session_state.test_strategy = None
    st.session_state.package_type = None
    st.session_state.engagement_strategy = None
    st.session_state.results_ready = False
    st.session_state.customer_details = {}


st.sidebar.title("Menu")
page = st.sidebar.radio(
    "Navigation",
    ["General", "Dashboard", "Start A/B Testing", "Settings"],
)

if page == "General":
    st.title("Welcome!")
    st.write("Here, you can add a new customer.")

    name = st.text_input("Customer's First Name")
    surname = st.text_input("Customer's Last Name")
    email = st.text_input("Customer's Email Adress")

    if st.button("Add the Customer"):
        if name and surname and email:
            customer_data = {
                "Name": name,
                "Surname": surname,
                "Email": email
            }
            st.write("Customer was added successfully!")
            st.write(customer_data)
        else:
            st.warning("Please fill all the information.")


elif page == "Dashboard":
    st.title("Welcome to the Dashboard!")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Customer Segments")
        table_data = pd.DataFrame(columns=["Segment ID", "Segment Name", "Segment Description"])
        st.table(table_data)
    with col2:
        st.write("Segment Frequency Chart")
        data = pd.DataFrame({
            "Segment": ["Lost Cause", "Vulnerable Customers", "Free Riders", "Star Customers"],
            "Frequency": [0, 0, 0, 0]
        })
        st.bar_chart(data.set_index('Segment') ['Frequency'])

elif page == "Settings":
    st.title("Settings")
    st.subheader("Need help?")
    st.write("Click on the link below to access to the documentation:")
    doc_url = "https://link.will.be.here.url"
    st.markdown(f" {doc_url}", unsafe_allow_html = True)


elif page == "Start A/B Testing":
    if st.session_state.ab_step == "select_segment":
        st.title("Start A/B Testing")
        st.subheader("Step 1: Select a Customer Segment")

        selected_segment = st.selectbox(
            "Choose a segment:",
            ["Lost Cause", "Vulnerable Customers", "Free Riders", "Star Customers"],
        )

        if st.button("Proceed to Goal Selection"):
            st.session_state.selected_segment = selected_segment
            st.session_state.ab_step = "select_goal"

    elif st.session_state.ab_step == "select_goal":
        st.title("Start A/B Testing")
        st.subheader(f"Step 2: Selected Segment: {st.session_state.selected_segment}")
        st.subheader("Choose the Goal of the Test")

        test_goal = st.selectbox(
            "Select the goal:",
            ["Subscription", "Engagement"],
        )

        if st.button("Proceed"):
            st.session_state.test_goal = test_goal
            if test_goal == "Subscription":
                st.session_state.ab_step = "select_package"
            elif test_goal == "Engagement":
                st.session_state.ab_step = "select_engagement_strategy"

    elif st.session_state.ab_step == "select_package":
        st.title("Start A/B Testing")
        st.subheader(f"Step 3: Selected Goal: {st.session_state.test_goal}")
        st.subheader("Choose a Subscription Package")

        package_type = st.selectbox(
            "Select a package type:",
            ["Basic", "Premium", "Family"],
        )

        price = st.number_input("Enter the package price:", min_value=0, value=10)

        if st.button("Confirm and Launch A/B Test"):
            st.session_state.package_type = package_type
            st.session_state.results_ready = True
            st.success(f"A/B Test launched successfully with package price: {price}!")
            st.session_state.ab_step = "results_ready" 

    elif st.session_state.ab_step == "select_engagement_strategy":
        st.title("Start A/B Testing")
        st.subheader(f"Step 3: Selected Goal: {st.session_state.test_goal}")
        st.subheader("Choose an Engagement Strategy")

        engagement_strategy = st.selectbox(
            "Select a strategy:",
            ["By Genre", "By Movie"],
        )

        if engagement_strategy == "By Genre":
            genre = st.selectbox(
                "Select a genre:",
                ["Sci-Fi", "Crime", "Action", "Drama", "Comedy", "Fantasy"],
            )
        elif engagement_strategy == "By Movie":
            movie = st.selectbox(
                "Select a movie:",
                [
                    "Inception", "The Godfather", "The Dark Knight", "Pulp Fiction", "Forrest Gump", 
                    "The Matrix", "Fight Club", "Interstellar", "The Lord of the Rings: The Return of the King", 
                    "The Shawshank Redemption"
                ],
            )

        if st.button("Confirm and Launch A/B Test"):
            st.session_state.engagement_strategy = engagement_strategy
            st.session_state.results_ready = True
            st.success("A/B Test launched successfully!")
            st.session_state.ab_step = "results_ready"  

    elif st.session_state.ab_step == "results_ready":
        st.title("You are all set!")
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
