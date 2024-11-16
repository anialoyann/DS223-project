import streamlit as st

# Initialize session state variables
if "ab_step" not in st.session_state:
    st.session_state.ab_step = "select_segment"  # Default step
if "selected_segment" not in st.session_state:
    st.session_state.selected_segment = None  # To store the selected segment
if "selected_strategy" not in st.session_state:
    st.session_state.selected_strategy = None  # To store the selected strategy


# Helper function to reset the app
def reset_app():
    st.session_state.ab_step = "select_segment"
    st.session_state.selected_segment = None
    st.session_state.selected_strategy = None


# Sidebar Navigation
st.sidebar.title("Menu")
st.sidebar.subheader("General")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Start A/B Testing", "Settings"],
)

# Dashboard Page
if page == "Dashboard":
    st.title("Welcome to the Dashboard!")
    st.write("This is the main dashboard page.")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Placeholder for Chart or Info Block 1")
    with col2:
        st.write("Placeholder for Chart or Info Block 2")

# Settings Page
elif page == "Settings":
    st.title("Settings")
    st.write("Adjust your app preferences here.")

# A/B Testing Page
elif page == "Start A/B Testing":
    # Step 1: Select Customer Segment
    if st.session_state.ab_step == "select_segment":
        st.title("Start A/B Testing")
        st.subheader("Step 1: Select a Customer Segment")

        # Dropdown to select a customer segment
        selected_segment = st.selectbox(
            "Choose a segment:",
            ["Lost Cause", "Vulnerable Customers", "Free Riders", "Star Customers"],
        )

        # Button to proceed
        if st.button("Proceed to Strategy Selection"):
            st.session_state.selected_segment = selected_segment
            st.session_state.ab_step = "select_strategy"  # Move to the next step

    # Step 2: Select Strategy
    elif st.session_state.ab_step == "select_strategy":
        st.title("Start A/B Testing")
        st.subheader(f"Step 2: Selected Segment: {st.session_state.selected_segment}")

        # Dropdown to select A/B testing strategy
        selected_strategy = st.selectbox(
            "Choose your A/B testing strategy:",
            ["By Genre", "By Movie", "Upgrade Subscription"],
        )

        # Button to confirm strategy
        if st.button("Proceed to Configure Details"):
            st.session_state.selected_strategy = selected_strategy
            st.session_state.ab_step = "configure_details"  # Move to the next step

    # Step 3: Configure Strategy Details
    elif st.session_state.ab_step == "configure_details":
        st.title("Start A/B Testing")
        st.subheader(f"Step 3: Selected Strategy: {st.session_state.selected_strategy}")

        if st.session_state.selected_strategy == "By Genre":
            st.write("Select genres to target for this A/B test.")
            genres = st.multiselect(
                "Choose genres:",
                ["Action", "Comedy", "Drama", "Horror", "Romance"],
            )
            st.write(f"Selected Genres: {genres}")

        elif st.session_state.selected_strategy == "By Movie":
            st.write("Select movies to target for this A/B test.")
            movies = st.multiselect(
                "Choose movies:",
                ["Inception", "Titanic", "The Dark Knight", "Avatar", "The Godfather"],
            )
            st.write(f"Selected Movies: {movies}")

        elif st.session_state.selected_strategy == "Upgrade Subscription":
            st.write("Select a subscription level for the upgrade.")
            subscription_level = st.radio(
                "Choose the subscription level:",
                ["Basic", "Premium", "Family"],
            )
            st.write(f"Selected Subscription Level: {subscription_level}")

        # Confirm and Launch
        if st.button("Confirm and Launch A/B Test"):
            st.success(
                f"A/B Test launched successfully for '{st.session_state.selected_segment}' with the '{st.session_state.selected_strategy}' strategy!"
            )
            reset_app()
