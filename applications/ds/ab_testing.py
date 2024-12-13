import pandas as pd
from sqlalchemy import create_engine, text
from scipy.stats import chi2_contingency

# Database connection URL 
DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/ds223_gp_db"

# Create the engine
engine = create_engine(DATABASE_URL)

# Function to conduct A/B testing

def conduct_ab_test(experiment_id):
    """
    Conduct an A/B test based on the experiment_id.

    This function fetches the A/B test results for a given experiment from the database,
    calculates click-through rates for two test groups, and performs a chi-square test to
    determine whether there is a statistically significant difference in performance between the groups.
    It then updates the `experiments` table with the p-value of the test.

    **Parameters:**
    - `experiment_id (int)`: The ID of the experiment to conduct the A/B test on.

    **Returns:**
    - `p_value (float)`: The p-value resulting from the chi-square test, indicating the statistical significance.
    
    **Raises:**
    - Prints messages indicating various errors such as insufficient data, invalid A/B test setup, or invalid chi-square test.
    """
    # Fetch A/B test results filtered by experiment_id
    ab_test_results_query = f"""
    SELECT *
    FROM ab_test_results
    WHERE experiment_id = {experiment_id};
    """
    ab_test_results_df = pd.read_sql(ab_test_results_query, con=engine)

    if ab_test_results_df.empty:
        print(f"No results found for experiment_id: {experiment_id}")
        return

    ab_test_ids = ab_test_results_df['ab_test_id'].unique()

    if len(ab_test_ids) != 2:
        print("A/B test requires exactly two test variants. Invalid data.")
        return

    group_1 = ab_test_results_df[ab_test_results_df['ab_test_id'] == ab_test_ids[0]]
    group_2 = ab_test_results_df[ab_test_results_df['ab_test_id'] == ab_test_ids[1]]

    # Calculate click counts for each group
    group_1_clicks = group_1['clicked_link'].sum()
    group_2_clicks = group_2['clicked_link'].sum()

    # Calculate total exposures (rows in each group)
    group_1_total = len(group_1)
    group_2_total = len(group_2)

    if group_1_total == 0 or group_2_total == 0:
        print("Insufficient data in one of the groups. A/B testing cannot proceed.")
        return

    # Prepare contingency table for chi-square test
    contingency_table = [
        [group_1_clicks, group_1_total - group_1_clicks],
        [group_2_clicks, group_2_total - group_2_clicks]
    ]
    print("Contingency Table")
    print(contingency_table)
    
    if any(value == 0 for row in contingency_table for value in row):
        print("The contingency table contains zero frequencies, which makes the chi-square test invalid.")
        return
    chi2, p_value, _, _ = chi2_contingency(contingency_table)

    # Update the experiments table with the p-value
    update_query = text("""
        UPDATE experiments
        SET p_value = :p_value
        WHERE experiment_id = :experiment_id;
    """)
    with engine.connect() as connection:
        with connection.begin():  # Start a transaction
            connection.execute(update_query, {"p_value": float(p_value), "experiment_id": experiment_id})


    print(f"Experiment ID: {experiment_id}")
    print(f"Group 1 Click Rate: {group_1_clicks / group_1_total:.2%}")
    print(f"Group 2 Click Rate: {group_2_clicks / group_2_total:.2%}")
    print(f"Chi-Square Test p-value: {p_value:.4f}")

    if p_value < 0.05:
        print("Result: Statistically significant difference. One group performs better.")
    else:
        print("Result: No statistically significant difference between the groups.")

    return p_value