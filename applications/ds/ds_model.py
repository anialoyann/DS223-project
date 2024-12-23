import pandas as pd
from sqlalchemy import create_engine, text
import numpy as np
import warnings 
warnings.filterwarnings("ignore")


# Database connection URL
DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/ds223_gp_db"


def calculate_customer_segments():
    """
    Calculate customer segments based on a scoring system using adjusted thresholds.
    Automatically assigns customers with no engagement data to segment ID 1 (Lost Cause).
    
    This function:
    - Fetches customer, engagement, and subscription data from the database.
    - Aggregates the engagement data for each customer.
    - Assigns a recency score based on the time since the customer's last engagement.
    - Scores each customer based on frequency, session duration, monetary value (subscription price), 
      likes, and dislikes.
    - Segments customers into categories such as 'Lost Cause', 'Vulnerable Customers', 'Free Riders', and 'Star Customers'.
    - Updates the `customer_segments` table with the new segment assignments.

    **Returns:**
    - `final_table (DataFrame)`: The final `customer_segments` table with customer IDs, segment IDs, and customer segment IDs.
    
    **Raises:**
    - Prints warnings if engagement data is missing or any customers have no interactions with the system.
    """
    # Database connection URL
    DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/ds223_gp_db"
    delete_customer_segments_table()
    # Create the engine
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        # Query necessary columns
        customers_df = pd.read_sql(
            "SELECT customer_id, created_at, updated_at, subscription_id FROM customers", 
            con=connection
        )
        print(f"Number of customers currently: {len(customers_df)}")
        engagements_df = pd.read_sql(
            "SELECT customer_id, engagement_id, session_date, session_duration, watched_fully, like_status FROM engagements", 
            con=connection
        )
        subscriptions_df = pd.read_sql(
            """
            SELECT 
                subscriptions.subscription_id, 
                subscriptions.price, 
                customers.customer_id 
            FROM subscriptions
            JOIN customers 
                ON subscriptions.subscription_id = customers.subscription_id
            """, 
            con=connection
        )

        # Aggregating metrics per customer_id
        engagements_agg = engagements_df.groupby('customer_id').agg(
            frequency=('engagement_id', 'count'),
            total_duration=('session_duration', 'sum'),
            watched_fully_true=('watched_fully', lambda x: (x == True).sum()),
            watched_fully_false=('watched_fully', lambda x: (x == False).sum()),
            liked_count=('like_status', lambda x: (x == 'Liked').sum()),
            disliked_count=('like_status', lambda x: (x == 'Disliked').sum()),
            last_session_date=('session_date', 'max')  # Latest session date
        ).reset_index()

        # Calculate recency (days since last session)
        current_date = pd.Timestamp.now()
        engagements_agg['recency'] = (current_date - pd.to_datetime(engagements_agg['last_session_date'])).dt.days

        # Join with subscription data
        data = pd.merge(engagements_agg, customers_df, on='customer_id', how='right')
        data = pd.merge(data, subscriptions_df, on='customer_id', how='left')
        data['monetary'] = data['price']  # Use subscription price as monetary value

        # Fill missing engagement data for customers without engagements
        data['frequency'].fillna(0, inplace=True)
        data['total_duration'].fillna(0, inplace=True)
        data['watched_fully_true'].fillna(0, inplace=True)
        data['watched_fully_false'].fillna(0, inplace=True)
        data['liked_count'].fillna(0, inplace=True)
        data['disliked_count'].fillna(0, inplace=True)
        data['last_session_date'].fillna(current_date, inplace=True)
        data['recency'].fillna(9999, inplace=True)  # Assign a high recency value for customers without sessions

        # Define scoring functions
        def score_frequency(value):
            if value < 2:
                return 1
            elif value <= 4:
                return 3
            elif value <= 7:
                return 5
            elif value <= 10:
                return 8
            else:
                return 10

        def score_duration(value):
            if value < 200:
                return 1
            elif value <= 600:
                return 3
            elif value <= 900:
                return 5
            elif value <= 1500:
                return 8
            else:
                return 10

        def score_monetary(value):
            if value == 5:
                return 1
            elif value <= 7:
                return 3
            elif value <= 9:
                return 7
            else:
                return 10

        def score_liked_count(value):
            if value == 0:
                return 1
            elif value == 1:
                return 3
            elif value <= 3:
                return 5
            elif value <= 5:
                return 8
            else:
                return 10

        def score_disliked_count(value):
            if value == 0:
                return 10
            elif value <= 2:
                return 7
            elif value <= 4:
                return 5
            else:
                return 2

        # Apply scoring
        data['score_frequency'] = data['frequency'].apply(score_frequency)
        data['score_duration'] = data['total_duration'].apply(score_duration)
        data['score_monetary'] = data['monetary'].apply(score_monetary)
        data['score_liked_count'] = data['liked_count'].apply(score_liked_count)
        data['score_disliked_count'] = data['disliked_count'].apply(score_disliked_count)

        # Calculate total score
        data['total_score'] = (
            data['score_frequency'] +
            data['score_duration'] +
            data['score_monetary'] +
            data['score_liked_count'] +
            data['score_disliked_count']
        )

        # Assign segments based on total score
        def assign_segment(score, has_engagements):
            if not has_engagements:
                return 1  # Lost Cause
            elif score <= 15:
                return 1  # Lost Cause
            elif score <= 25:
                return 2  # Vulnerable Customers
            elif score <= 30:
                return 3  # Free Riders
            else:
                return 4  # Star Customers

        data['has_engagements'] = data['frequency'] > 0
        data['segment_id'] = data.apply(lambda row: assign_segment(row['total_score'], row['has_engagements']), axis=1)

        # Generate sequential customer_segment_id starting from 1
        data['customer_segment_id'] = range(1, len(data) + 1)

        # Prepare data for insertion into customer_segments table
        customer_segments_data = data[['customer_segment_id', 'customer_id', 'segment_id']]

        # Perform deletion and insertion
        customer_ids = customer_segments_data['customer_id'].tolist()
        connection.execute(
            text("DELETE FROM customer_segments WHERE customer_id = ANY(:customer_ids)"),
            {'customer_ids': customer_ids}
        )
        customer_segments_data.to_sql('customer_segments', con=engine, if_exists='append', index=False)
    
    # Return the final customer_segments table
    with engine.connect() as connection:
        final_table = pd.read_sql("SELECT * FROM customer_segments", con=connection)
    
    return final_table




def compute_customer_statistics():
    """
    Compute and return summary statistics for key engagement and subscription metrics.
    
    This function:
    - Fetches engagement and subscription data from the database.
    - Aggregates engagement data for each customer.
    - Computes summary statistics for various metrics including frequency, session duration, likes, dislikes, and monetary value.

    **Returns:**
    - `stats (dict)`: A dictionary containing summary statistics for the engagement and subscription metrics.
    
    **Raises:**
    - Prints any errors related to missing or invalid data during the aggregation process.
    """
    # Create the engine
    
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        # Query necessary columns
        engagements_df = pd.read_sql(
            "SELECT customer_id, engagement_id, session_duration, watched_fully, like_status FROM engagements", 
            con=connection
        )
        subscriptions_df = pd.read_sql(
            """
            SELECT 
                subscriptions.subscription_id, 
                subscriptions.price, 
                customers.customer_id 
            FROM subscriptions
            JOIN customers 
                ON subscriptions.subscription_id = customers.subscription_id
            """, 
            con=connection
        )
        
        # Aggregating metrics per customer_id
        engagements_agg = engagements_df.groupby('customer_id').agg(
            frequency=('engagement_id', 'count'),
            total_duration=('session_duration', 'sum'),
            watched_fully_true=('watched_fully', lambda x: (x == True).sum()),
            watched_fully_false=('watched_fully', lambda x: (x == False).sum()),
            liked_count=('like_status', lambda x: (x == 'Liked').sum()),
            no_action_count=('like_status', lambda x: (x == 'No Action').sum()),
            disliked_count=('like_status', lambda x: (x == 'Disliked').sum())
        ).reset_index()
        
        # Join with subscription data for monetary calculation
        engagements_agg = engagements_agg.merge(subscriptions_df, on='customer_id', how='left')
        engagements_agg['monetary'] = engagements_agg['price']
        
        # Calculate summary statistics for key columns
        stats = {
            'frequency': engagements_agg['frequency'].describe(),
            'total_duration': engagements_agg['total_duration'].describe(),
            'monetary': engagements_agg['monetary'].describe(),
            'watched_fully_true': engagements_agg['watched_fully_true'].describe(),
            'watched_fully_false': engagements_agg['watched_fully_false'].describe(),
            'liked_count': engagements_agg['liked_count'].describe(),
            'disliked_count': engagements_agg['disliked_count'].describe(),
            'no_action_count': engagements_agg['no_action_count'].describe()
        }
        
        # Print statistics for inspection
        print("\nCustomer Metrics Summary Statistics:")
        for key, value in stats.items():
            print(f"\nStatistics for {key}:\n{value}\n")
        
        return stats
    

def delete_customer_segments_table():
    """
    Deletes all contents of the customer_segments table and commits the transaction.
    
    This function:
    - Establishes a connection to the database.
    - Deletes all rows in the `customer_segments` table to reset it before inserting new data.
    
    **Raises:**
    - Prints a confirmation message once the rows are deleted successfully.
    """
    # Create the engine
    engine = create_engine(DATABASE_URL)
    
    # Connect to the database and delete table contents
    with engine.begin() as connection:  # Automatically handles commit/rollback
        connection.execute(text("DELETE FROM customer_segments;"))
        print("Deleted all rows from the customer_segments table.")

