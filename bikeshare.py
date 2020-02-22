import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Which city are you interested in, Chicago, New York City, or Washington? Specify only one\n").lower()
    while city not in CITY_DATA.keys():
        city = input("Sorry, I don't recognize city '{}'. Please specify Chicago, New York City, or Washington\n".format(city)).lower()

    # get user input for month (all, january, february, ... , june)
    months_including_all = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input("Which month are you interested in? We have data for January through June. If all, enter all\n").lower()
    while month not in months_including_all:
        month = input("Sorry, I don't recognize month '{}'. Format should be full name and is not case sensitive. E.g., January. Can you re-enter?\n".format(month)).lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days_including_all = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input("Which day of the week are you interested in? If all, enter all\n").lower()
    while day not in days_including_all:
        day = input("Sorry, I don't recognize day '{}'. Format should be full name of day and is not case sensitive. E.g., Monday. Please re-enter\n".format(day)).lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # cols Start Time,End Time,Trip Duration,Start Station,End Station,User Type,Gender,Birth Year
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time from string to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # create cols with month and name of day of week
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # test statements
    # print(df.loc[0:10, ['Start Time', 'month', 'day_of_week']])

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july']
        month_int = int(months.index(month)+1)

        # filter by month to create the new dataframe
        df = df[df['month'] == month_int]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print("\t Most common month: {} (n={}) ".format(most_common_month,
        df['month'].value_counts().loc[most_common_month]))

    # display the most common day of week
    print("\t Most common day of week: {}".format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    print("\t Most common start hour: {}".format(df['start_hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mc_start_station = df['Start Station'].mode()[0]
    print("\t Most common start station: {} (n={})".format(mc_start_station,
        df['Start Station'].value_counts().loc[mc_start_station]))

    # display most commonly used end station
    print("\t Most common end station: {}".format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    route = df['Start Station'] + "--" + df['Start Station']
    print("\t Most common start-end station combination: {}".format(route.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("\t Total travel time: {} seconds".format(df['Trip Duration'].sum()))

    # display mean travel time
    print("\t Average travel time: {} seconds".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Count by user type:")
    print(df['User Type'].value_counts())

    # Display counts of gender
    print("\nCount by user gender:")
    print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    print("\nEarliest year of birth: {}".format(int(df['Birth Year'].min())))
    print("Most recent year of birth: {}".format(int(df['Birth Year'].max())))
    print("Most common year of birth: {}".format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_five_raw(df):
    """Displays five rows of raw data; prompts user to show additional 5 rows until they enter 'no'"""

    show_raw = input("\nWould you like to see 5 rows of data? Enter yes or no\n")
    i = 0
    while show_raw == "yes":
        print(df[i:i+5])
        i += 5
        show_raw = input("\nWould you like 5 more rows? Yes or no\n")

def main():
    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        show_five_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
