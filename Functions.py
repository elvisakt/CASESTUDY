import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import calendar
import random

def morn_aft(time) -> str:
    """
    Function to determine wether a time correspond to Morning or Afternoon

    Parameters:
    - time: A datetime.time type.
    
    Returns:
    - str : 'Morning' or 'Afternoon'.
    """
    if time.hour < 13:
        return 'Morning'
    else:
        return 'Afternoon'
    
def create_session_id(x):
    """
    Function generation a concatenated string out of event_id, date and period variables
    """
    return x['event_id'] + '_' + x['date'].strftime('%Y-%m-%d') + '_' + x['period']

def generate_logs_with_session(path : str) -> pd.DataFrame:
    """
    This function takes a path of str type and return a datrame with session_id.

    Parameters:
    - path: A string representation the path to sample.cvs file.
    
    Returns:
    - pd.DataFrame : DataFrame containing the parsed data.
    """
    logs = pd.read_csv(path)
    # Converting 'sent_at' vatiables to date
    logs['sent_at'] = pd.to_datetime(logs["sent_at"])
    # Breaking the sent_at variables into Date, year, month, hour and min
    logs['date'] = logs["sent_at"].dt.date
    logs['year'] = logs["sent_at"].dt.year
    logs['month'] = logs["sent_at"].dt.month
    logs['day'] = logs["sent_at"].dt.day
    logs['time'] = logs['sent_at'].dt.time
    # let's delete the sent_at variable and the question_id variable that will not serve our analysis.
    # axis = 1 target the columns
    logs = logs.drop('sent_at', axis = 1)
    logs = logs.drop('question_id', axis = 1)
    logs['period'] = logs["time"].apply(morn_aft)
    logs['session_id'] = logs.apply(create_session_id, axis = 1)

    return logs

def number_answer_per_Sessions_viz(logs) :
    """
    Procedure drawing a horizontal barplot showing the amount of answers per sessions.

    Parameters: 
    - logs: A dataFrame of logs with session_id assigned

    """
    nb_session = logs['session_id'].value_counts().sort_index(ascending=False)
    # Sorting the count to have a better view for our graph
    nb_session.sort_values(ascending=False, inplace=True)
    fig = plt.figure(figsize=(10,10))
    plt.grid(axis='x', linestyle='--', alpha = 0.3) #alpha for the transparence
    bars = plt.barh(nb_session.index, nb_session, color = 'teal', height=0.7, linewidth = 0.5, edgecolor = 'black', alpha = 0.6)
    #adding exact value to the bars
    for bar in bars:
        plt.text(
            bar.get_width()+ 4,               # x-coordinate + 4 padding
            bar.get_y() + bar.get_height()/2,  # y-coordinate
            f'{int(bar.get_width())}',      # label
            va='center', ha='left',         # alignment
            fontsize=8, color='black'
        )
    #customization
    plt.xlabel('Number of answers', fontsize=12)
    plt.ylabel('Sessions', fontsize=12)
    plt.yticks(fontsize=8)
    plt.title('Number of answers per Session')
    plt.tight_layout() # Adjusting the layout 

    plt.show()

def top5_users_activity_per_month_viz(logs) :
    """
    Procedure drawing a Line Graph showing the amount of sessions top 5 users have participated in throughout the year

    Parameters: 
    - logs: A dataFrame of logs with session_id assigned
    """

    # Select the top 5 active users
    users_activity = logs.groupby('user')['session_id'].nunique().reset_index()
    users_activity.columns = ['user', 'number_session']
    #nlargest select the n line with the highest columns values
    top5 = users_activity.nlargest(5,columns= "number_session")
    top5_ids = top5['user']
    top5_ids
    # Creating a DataFrame with data only for the top 5 users
    df_filtered = logs[logs['user'].isin(top5_ids)]
    # Grouping by users and counting unique session_id by group
    unique_session_per_users = df_filtered.groupby(['user','month'])['session_id'].nunique().reset_index()
    # Renaming column name for clarity
    unique_session_per_users.columns = ['user','month','number_session']
    # Sorting the data in descending order
    unique_session_per_users.sort_values(by=['user','month','number_session'], ascending= False, inplace=True)
    plt.figure(figsize=(12, 6))
    # Creating a line for each user on the same figure
    for user in unique_session_per_users['user'].unique():
        user_data = unique_session_per_users[unique_session_per_users['user'] == user]  # Filter data for the current user
        # Plotting each line for the unique users
        plt.plot(user_data['month'], user_data['number_session'], marker='o', label=f'User {user}')

    # Adding labels and title
    plt.title('Number of Sessions per top 5 Users for Each Month')
    plt.xlabel('Month')
    plt.ylabel('Number of Sessions')
    plt.legend(title='Users')
    plt.grid(linestyle='--', alpha = 0.3)
    plt.tight_layout()
    plt.show()

def generate_dates(year : int, month : int):
    """
    Function generating dates within the specified year and month
    """
    num_days = calendar.monthrange(year, month)[1]  # Get the number of days in the month
    return [datetime(year, month, day).strftime('%Y-%m-%d') for day in range(1, num_days + 1)]

def generate_fake_logs(seed : int) -> pd.DataFrame :
    """
    Function generating fake logs DataFrame ready to be used.

    Parameters:
    - seed : int affecting the volume of the datasets created
    """
    # Define the user IDs and event IDs
    user_ids = [5112, 5530, 373, 6728, 2476, 6043, 9025, 8890, 1286, 6451]
    event_ids = [
        '64def4568ed12f4c710d9b21', '630304fa712d3b81ef1dc293', 
        '6303d811c0b317ffad239e24', '64d09b2d61d1c572fe4f481e', 
        '64a11873b2dc91df2c41ab20', '64a171d318c21cbd209fa2b4', 
        '630ea3f338d12f4c710d9b21', '6303d811c0b317ffad239e24'
    ]

    # Create an empty list to hold the data
    data = []

    # Generate data for each month
    for month in range(1, 13):  # 1 to 12 for January to December
        dates = generate_dates(2021, month)  # Generate dates for the month
        for date in dates:
            # Randomly select users and event IDs for each date
            num_sessions = random.randint(1, seed)  # Number of sessions for this date
            for _ in range(num_sessions):
                user = random.choice(user_ids)
                event_id = random.choice(event_ids)
                period = 'Morning' if random.choice([True, False]) else 'Afternoon'
                data.append([user, event_id, date, period])

    # Create DataFrame from the generated data
    columns = ['user', 'event_id', 'date', 'period']
    expanded_df = pd.DataFrame(data, columns=columns)
    expanded_df['date'] = pd.to_datetime(expanded_df["date"])
    expanded_df['month'] = expanded_df["date"].dt.month
    expanded_df['session_id'] = expanded_df.apply(create_session_id, axis = 1)
    return expanded_df
