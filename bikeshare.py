import time
import pandas as pd
import numpy as np

# define global variables
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january','february','march','april','may','june','all']


def get_filters():
    
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
 
    # get user input for city
    city = input("\nPlease choose one of the following cities you would like to analyze: Chicago, New York City, Washington: ").lower()
    while city not in ('chicago','new york city','washington'):
        city = input('\nYour entry is not valid.\nPlease choose one of the following cities: Chicago, New York City, Washington: ').lower()
    example = pd.read_csv(CITY_DATA[city])
    print('\nYou chose to analyze the dataset for {}.\nHere you can see a snippet of the dataset:\n\n'.format(city.capitalize()), example.head(5))

    # get user input for month
    month=input('\n Which month do you like to analyze? \n Please select between January, February, March, April, May, June. You can also choose to analyze all of them by typing "all": ').lower()
    while month not in MONTHS:
        month = input('\n Your entry is not valid.\n Please choose one of the following options: January, February, March, April, May, June, All: ').lower()    

    # get user input for day
    day=input('\n Which day of week do you like to analyze? \n Please select between Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday. You can also choose to analyze all of them by typing "all": ').title()
    while day not in ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All'):
        day = input('\n Your entry is not valid.\n Please choose one of the following options: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, All: ').title()

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    
    return df


def time_stats(df):
    
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = MONTHS[df['month'].mode()[0]-1].title()

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour    
    popular_hour = df['hour'].mode()[0]

    print("The most frequent times of starting a travel are:\n\n Month: {}\n Day: {}\n Hour: {}:00".format(popular_month,popular_day,popular_hour))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_count = df['Start Station'].value_counts()[popular_start_station]
    print('The most popular start station is {} with {} trips.'.format(popular_start_station, popular_start_count))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    popular_end_count = df['Start Station'].value_counts()[popular_start_station]
    print('The most popular end station is {} with {} trips.'.format(popular_end_station, popular_end_count))

    # display most frequent combination of start station and end station trip
    print('The most popular route is from {} to {}.'.format(df.groupby(['Start Station','End Station']).size().idxmax()[0], df.groupby(['Start Station','End Station']).size().idxmax()[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def trip_duration_stats(df, city):
    
    """Displays statistics on the total and average trip duration."""

    # ask users whether they want so see trip duration statistics
    option = input('If you want to see some statistics about the trip duration, please type in "yes": ')
    start_time = time.time()
    
   # convert the Start and End Time column to datetime
    if option == 'yes':
        print('\nCalculating Trip Duration...\n')
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])

        # display total travel time
        df['Travel Time'] =    df['End Time']-   df['Start Time']
        print('The total travel time in', city.title(), 'in your chosen timeframe is', df['Travel Time'].sum(),'hours.')

        # display mean travel time
        print('\nThe average time of a bike rental is', str(df['Travel Time'].mean()).split(".")[0],'hours.')

        print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def user_stats(df, city):
    
    """Displays statistics on bikeshare users."""
    
    # ask users whether they want so see user statistics
    option = input('If you want to see some statistics about the bikeshare users, please type in "yes": ')

    if option == 'yes':
        print('\nCalculating User Stats...\n')

        start_time = time.time()

        # display counts of user types
        user_types = df['User Type'].value_counts()
        print('User Types: \n')

        for i in range(len(user_types)):
            user_type = user_types.index[i]
            user_count = user_types[i]

            print(' {}: {}'.format(user_type, user_count))

        # display counts of gender
        if city in ('chicago','new york city'):
            print('\nGender distribution: \n')
            user_genders = df['Gender'].value_counts()
            for i in range(len(user_genders)):
                gender = user_genders.index[i]
                gender_count = user_genders[i]
                print(' {}: {}'.format(gender, gender_count))

        # display earliest, most recent, and most common year of birth
            print('\nThe youngest renter was born in the year',int(df['Birth Year'].max()))

            print('The oldest renter was born in the year',int(df['Birth Year'].min()))

            print('Most of our renters were born in the year',int(df['Birth Year'].mode()[0]))

        print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)
 

def raw_data(df):

    """
    Asks user if he wants to see some lines from the raw data with his specified filters.
    If yes, first 5 lines of raw data are shown.
    User will be asked if he would like to see more lines until he says no.
    """
    # delete added rows
    df = df.drop(["month","day_of_week","hour"], axis=1)
    
    rows_start = 1
    rows_end = 6

    # ask users whether they want so see raw data
    print('\nDo you want to see some raw data?\n')
          
    while True:
        raw_data = input('Please enter "yes": ')
        if raw_data == 'yes':
            print('\n', df.iloc[rows_start : rows_end])
            rows_start += 5
            rows_end += 5
        
            print('\nDo you want to see more lines?')
            continue
        else:
            break
  
  
def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df, city)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter "yes" or "no".\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()