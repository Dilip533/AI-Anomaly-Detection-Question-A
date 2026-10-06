# Personal Intelligence Note

## Question A
I chose Isolation Forest for Level 1 because it is an unsupervised anomaly detector and does not require a separate anomaly classifier. I rejected a simple fixed heart-rate threshold because walking normally increases heart rate and would create false alarms.

For Level 2 I wrote the rolling z-score detector and metric calculation myself. My reason for using a rolling window is that the sensor baseline changes over time.

For Level 3 my prediction was that doubling the window from 300 to 600 seconds would reduce silent-drift recall. With seed 2506, recall changed from 0.014 to 0.000, so the prediction was correct.

## Question C
I chose SQLite because it is simple to demonstrate the required SQL operations locally. I rejected using only CSV files because the question specifically asks for a database schema and SQL queries.

The final database stores one alert per anomaly event. This is more useful than storing one alert for every anomalous second because one event should normally create one alert.

## AI usage declaration
I used ChatGPT to help structure the implementation, explain the assignment requirements and check the code. I tested the generated code with my personal seed 2506 and changed the implementation after testing. One weak point in the first version was that it inserted one alert for every anomalous reading; I found this because the SQL output produced thousands of alerts per user. I changed it to create one alert at the start of each contiguous anomaly event.

I also checked the generated dataset and reran the scripts before using the final numbers.
