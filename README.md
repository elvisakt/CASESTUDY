# STUDY CASE

## CONTEXT
The goal was to assess my Data Analyst Skills. In order to do so I was provided with a project to realize in python or R. I decided to go with Python. 
I was given two csv files (sample.csv and metadata.csv). The main file, saple.csv contains logs of the Wooclap app. The goal was to reply to the following questions:

- Add a session_id in order to identify sessions and to be able to conduct analysis based on sessions rather than on events.
- Produce a graph enabling to visualize the number of answers emited for each session.
- Produce a graph to see among the top 10% most active users, how many sessions they participated in, each month of the year (Product Manager request).

## REPOSITORY CONTENT
### IMPORTANT FILES
- **Data_Description.ipynb** : Jupyter notebook presenting the full exploration of the sample.csv file and logic behind answer to all the questions above.
- **Functions.py** : Python file regrouping all the documented functions used to answer data cleaning, data manipulation, data visualization problems.
- **PM_Graph** : Python file producing the Product Manager graph request.
- **barplot.py** : Pyhton file producing a horizontal barplot show the distribution of answers per session
- **Data_pipeline_Wooclap.png** : Visuals showing the Data Pipeline proposal.

### OTHER FILES
The other files are csv files, system python files and a requierement.txt file enabling to create safe python env before launching the project.

## PROJECT LAUNCH
In order to safely launch the project, follow these next steps:

- make sure you have python installed
- make sure you have virtualenv installed with : 'pip install -r requirements.txt'
- Create the virtual environment : 'virtualenv venv'
- Activate the environment : 'source venv/bin/activate'
- Install all the requiered packages: 'pip install -r requirements.txt'
- launch python scripts : 'python3 barplot.py' for example.

## COMMENTS
Although it was auhtorized, my usage of chatGPT during this test was really limited to case where I needed more efficiency with producing the code. Therefore, I can attest that more that 95% of the code produced is from my self python and programming skills.

Here is the link towards the chat gpt sessions I used while coding:
- https://chatgpt.com/share/67094603-0dd0-8007-ac8d-205a7f541cff

## PROOF OF CONTEXT FOR DATA PIPELINE TO ANSWER PM REQUEST

## Data Pipeline from Raw Logs to Dashboard (REF : Data_pipeline_Wooclap.png)

### Overview
This contains a data pipeline that transforms raw log CSV files into a dashboard for KPI visualization, accessible by the Product Manager.

### Data Pipeline Flow

1. **Data Ingestion**
   - **Source**: Raw log CSV files generated from the application.
   - **Storage**: Files are stored in **Amazon S3** for durability and easy access.

2. **Data Processing**
   - **Data Transformation**:
     - Orchestrated by **Apache Airflow**. DAG is triggered by S3 Sensor built in Airflow
     - Uses **Python operators** to run scripts that read and process raw CSV files, adding necessary columns like `session_id`.
   - **Loading to Staging**:
     - Transformed data is loaded into a **staging table** in **Amazon Redshift**.

3. **Data Loading**
   - **Incremental Load**:
     - Processes SQL queries (like `INSERT` or `MERGE`) to insert/update data from the staging table into main tables (designed for analytics purposes) in Amazon Redshift.

4. **Data Storage**
   - Processed data is stored in **Amazon Redshift**, structured for efficient querying and analysis. End Views can also be stored.

5. **Data Visualization**
   - **Connect to Power BI**:
     - Establishes a connection between **Power BI** and Amazon Redshift.
   - **Create Dashboards**:
     - Dashboards are built in Power BI to visualize KPIs derived from the processed log data.

6. **Sharing and Access**
   - **Publish to Power BI Service**: Dashboards and reports are published to the Power BI Service.
   - **Sharing**: Dashboards are shared with Product Managers via apps.
   - **Scheduled Refresh**: Automatic refreshes ensure the dashboard is updated as new data arrives.

### Summary Flow
* Raw Log CSV Files (sample.csv) (Amazon S3)

* Data Processing (Apache Airflow & Python)

* Transformed Data storage (Staging Table in Redshift)

* Incremental Load to Main Tables (Amazon Redshift)

* Data Visualization (Power BI)

* Dashboard Access (Power BI Service)

### Requierements to run this Data Pipeline
- Apache Airflow
- Amazon S3
- Amazon Redshift
- Power BI
- Python
