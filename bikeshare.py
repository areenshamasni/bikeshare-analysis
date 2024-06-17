import time
import pandas as pd

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    print("Hello! Let's explore some US bikeshare data!")
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington? ").strip().lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please enter Chicago, New York City, or Washington.")
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Which month? January, February, March, April, May, June or 'all' for no filter: ").strip().lower()
        if month in months:
            break
        else:
            print("Invalid input. Please enter a valid month or 'all'.")
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or 'all' for no filter: ").strip().lower()
        if day in days:
            break
        else:
            print("Invalid input. Please enter a valid day or 'all'.")
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    popular_month = df['month'].mode()[0]
    print(f'Most Popular Month: {popular_month}')
    popular_day = df['day_of_week'].mode()[0]
    print(f'Most Popular Day: {popular_day}')
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(f'Most Popular Start Hour: {popular_hour}')
    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    popular_start_station = df['Start Station'].mode()[0]
    print(f'Most Commonly Used Start Station: {popular_start_station}')
    popular_end_station = df['End Station'].mode()[0]
    print(f'Most Commonly Used End Station: {popular_end_station}')
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    popular_trip = df['trip'].mode()[0]
    print(f'Most Common Trip: {popular_trip}')
    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_duration = df['Trip Duration'].sum()
    print(f'Total Travel Time: {total_duration} seconds')
    mean_duration = df['Trip Duration'].mean()
    print(f'Mean Travel Time: {mean_duration} seconds')
    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user_types = df['User Type'].value_counts()
    print(f'User Types:\n{user_types}')
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f'\nGender Counts:\n{gender_counts}')
    else:
        print('\nGender Counts: No data available for this month.')
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]
        print(f'\nEarliest Year of Birth: {earliest_year}')
        print(f'Most Recent Year of Birth: {most_recent_year}')
        print(f'Most Common Year of Birth: {common_year}')
    else:
        print('\nYear of Birth: No data available for this month.')
    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def display_raw_data(df):
    row = 0
    while True:
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no.\n').strip().lower()
        if view_data == 'yes':
            print(df.iloc[row:row+5])
            row += 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()
