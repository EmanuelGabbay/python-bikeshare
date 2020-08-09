import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    cities = ['chicago', 'new york city', 'washington']
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington)
    while True:
        print('Please choose a city to get data from.')
        print('Options: chicago, new york city, washington')

        city = input('Your pick: ')

        if city.lower() not in cities:
            print('Invalid input!\n')
            continue

        break

    # get user input for month (all, january, february, ... , june)
    while True:
        print('Please choose a month to get data from.')
        print('Options: all, january, february, ... , june')

        month = input('Your pick: ')

        if (month.lower() != 'all') and (month.lower() not in months):
            print('Invalid input!\n')
            continue

        break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        print('Please choose a day to get data from.')
        print('Options: all, monday, tuesday, ... sunday')

        day = input('Your pick: ')

        if (day.lower() != 'all') and (day.lower() not in days):
            print('Invalid input!\n')
            continue

        break

    print('-' * 40)
    return city.lower(), month.lower(), day.lower()


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
    df = pd.read_csv('' + CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

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
    popular_month = (df['month'].mode())[0]
    print('Most Frequent Month:', popular_month)

    # display the most common day of week
    popular_dow = (df['day_of_week'].mode())[0]
    print('Most Frequent Day of the Week:', popular_dow)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = (df['hour'].mode())[0]
    print('Most Frequent Start Hour: {}:00'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = (df['Start Station'].mode())[0]
    print('Most commonly used start station:', popular_start)

    # display most commonly used end station
    popular_end = (df['End Station'].mode())[0]
    print('Most commonly used end station:', popular_end)

    # display most frequent combination of start station and end station trip
    df['Route'] = df['Start Station'] + ' to ' + df['End Station']
    popular_route = (df['Route'].mode())[0]
    print('Most frequent trip: From', popular_route)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print('Total trip duration:', total_duration)

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print('Mean trip duration:', mean_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count of user types:\n', user_types)

    # Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print('Count of gender:\n', gender)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth = df['Birth Year'].min()
        recent_birth = df['Birth Year'].max()
        common_birth = (df['Birth Year'].mode())[0]
        print('Earliest year of birth:', earliest_birth)
        print('Most recent year of birth:', recent_birth)
        print('Most common year of birth:', common_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    """Displays raw data to the user upon request"""

    index = 0

    print('Would you like to see raw data?')

    while True:
        answer = input('Answer: ')
        if answer.lower() == 'yes':
            # displays first 5 rows starting from index variable
            print(df.iloc[index:index + 5].to_string())
            index += 5
            print('Would you like to see 5 more lines of data?')
        elif answer.lower() == 'no':
            return
        else:
            print('Invalid input! Please type \'yes\' or \'no\'')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()