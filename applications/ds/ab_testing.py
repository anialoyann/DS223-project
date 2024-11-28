import pandas as pd
from sqlalchemy import create_engine
from scipy.stats import chi2_contingency

# Database connection URL 
DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/ds223_gp_db"

# Create the engine
engine = create_engine(DATABASE_URL)

# Load A/B test data
ab_tests_df = pd.read_sql("SELECT * FROM ab_tests", con=engine)

# Load A/B test results data
ab_test_results_df = pd.read_sql("SELECT * FROM ab_test_results", con=engine)

# Function to conduct A/B testing
def conduct_ab_test(segment_name, goal):
    # Filter customers by segment
    query = f"""
    SELECT c.customer_id
    FROM customer_segments cs
    JOIN segments s ON cs.segment_id = s.segment_id
    JOIN customers c ON cs.customer_id = c.customer_id
    WHERE s.segment_name = '{segment_name}';
    """
    customers_in_segment = pd.read_sql(query, con=engine)
    
    if customers_in_segment.empty:
        print(f"No customers found for the segment: {segment_name}")
        return
    
    # Filter A/B test data by goal
    ab_test_options = ab_tests_df[ab_tests_df['goal'] == goal]
    
    if ab_test_options.empty:
        print(f"No A/B test options available for goal: {goal}")
        return

    print(f"Conducting A/B test for segment '{segment_name}' and goal '{goal}'")

    # For simplicity, assign Variant 1 and Variant 2 based on the test_skeleton
    variant_1 = ab_test_options[ab_test_options['test_variant'] == 1]
    variant_2 = ab_test_options[ab_test_options['test_variant'] == 2]

    if variant_1.empty or variant_2.empty:
        print("Both test variants are not available. A/B testing cannot be conducted.")
        return

    # Filter results for the A/B test IDs
    test_ids = ab_test_options['ab_test_id'].tolist()
    filtered_results = ab_test_results_df[ab_test_results_df['ab_test_id'].isin(test_ids)]

    # Join with customer IDs in the segment
    results_in_segment = filtered_results[filtered_results['customer_id'].isin(customers_in_segment['customer_id'])]

    # Separate results by variants
    variant_1_results = results_in_segment[results_in_segment['ab_test_id'] == variant_1.iloc[0]['ab_test_id']]
    variant_2_results = results_in_segment[results_in_segment['ab_test_id'] == variant_2.iloc[0]['ab_test_id']]

    # Calculate click counts
    variant_1_clicks = variant_1_results['clicked_link'].sum()
    variant_2_clicks = variant_2_results['clicked_link'].sum()

    # Calculate total exposures (customers in segment who were shown each variant)
    variant_1_total = len(variant_1_results)
    variant_2_total = len(variant_2_results)

    # Avoid division by zero
    if variant_1_total == 0 or variant_2_total == 0:
        print("Insufficient data for one of the variants. A/B testing cannot be conducted.")
        return

    # Calculate click rates
    variant_1_click_rate = variant_1_clicks / variant_1_total
    variant_2_click_rate = variant_2_clicks / variant_2_total

    # Prepare contingency table for chi-square test
    contingency_table = [
        [variant_1_clicks, variant_1_total - variant_1_clicks],
        [variant_2_clicks, variant_2_total - variant_2_clicks]
    ]

    chi2, p_value, _, _ = chi2_contingency(contingency_table)

    # Insert experiment into the 'experiments' table
    with engine.connect() as connection:
        result = connection.execute("INSERT INTO experiments (p_value) VALUES (%s) RETURNING experiment_id;", (p_value,))
        experiment_id = result.fetchone()[0]

    # Update the 'ab_test_results' table with the experiment_id
    ab_test_results_df.loc[ab_test_results_df['ab_test_id'].isin(test_ids), 'experiment_id'] = experiment_id

    print(f"\nVariant 1 Click Rate: {variant_1_click_rate:.2%}")
    print(f"Variant 2 Click Rate: {variant_2_click_rate:.2%}")
    print(f"Chi-Square Test p-value: {p_value:.4f}")

    if p_value < 0.05:
        print("Result: Statistically significant difference. Choose the better performing variant.")
        better_variant = "Variant 1" if variant_1_click_rate > variant_2_click_rate else "Variant 2"
        print(f"Better Performing Variant: {better_variant}")
    else:
        print("Result: No statistically significant difference between the variants.")

    print(f"Experiment ID: {experiment_id} recorded successfully.")

# Example usage
segment_name = "Star Customers"  # Choose the segment
goal = "subscription"  # Choose the goal: 'subscription' or 'engagement'

conduct_ab_test(segment_name, goal)
