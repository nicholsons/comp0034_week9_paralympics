from paralympics_app.paralympic_dash_app.create_charts import top_ten_gold_data


def test_top_ten_gold_has_ten_results():
    """
    GIVEN the top_ten_gold_data() function
    WHEN the function is called
    THEN the resulting dataframe has 10 rows (i.e. the length of the index is 10)
    """
    df = top_ten_gold_data()
    assert len(df.index) == 10
