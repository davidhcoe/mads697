# Upward Mobility Streamlit App
This app is a component of the [Upward Mobility](http://upwardmobility.pythonanywhere.com/) web site. 

This app presents the data findings from the research done for the Upward Mobility capstone project. See the [blog](http://upwardmobility.pythonanywhere.com/blog) on the Upward Mobility site to learn more.

## How this app works

- When the app starts, `main.py` is run. This file is resonsible for sorting which page the user intends to target based on the url parameters.
- `national.py` presents the national map with overview statistics
- `county_details.py` presents a breakdown of the county to view the details of each Upward Mobility domain

### Running the app

Use the following command to start the app:

```
streamlit run main.py
```

By default, the population metric is show on the national map. This can be changed by adjusting the metric parameter to one of the column names in the dataset. For example:

[http://localhost:8501/?metric=crime_rate](http://localhost:8501/?metric=crime_rate) to see crime rates

[http://localhost:8501/?metric=median_family_income](http://localhost:8501/?metric=median_family_income) to see median family income

Links from the national map will direct you to the county_details page, which parses the `fips` parameter.

Click [here](http://localhost:8501/?page=picker) to view the county picker page and find your optimal county.

### Pro Tip
Add the `debug=true` value to the query string to change the targeted URL from the hosted Upward Mobility app to your local machine.
