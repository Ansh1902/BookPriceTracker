import pandas as pd
from constants import DATE, PRICE_DROP_PERCENTAGE

# Get today's date and previous day's date (assuming DATE is formatted as '%d-%b')
current_date = pd.to_datetime(DATE, format='%d_%m_%y')
previous_date = current_date - pd.DateOffset(days=1)

# Generate filenames based on dates
current_filename = f"Books_amazon_goodreads_{current_date.strftime('%d_%m_%y')}.csv"
previous_filename = f"Books_amazon_goodreads_{previous_date.strftime('%d_%m_%y')}.csv"

# Load data into DataFrames
try:
    current_df = pd.read_csv(current_filename)
    previous_df = pd.read_csv(previous_filename)
except FileNotFoundError:
    print(f"CSV file not found for one or both dates: {current_filename}, {previous_filename}")
    exit()

# Initialize a list to store rows that meet the criteria
rows_to_include = []

# Iterate through current day's DataFrame and compare prices with previous day
for index, row in current_df.iterrows():
    try:
        # Assuming 'KindlePrice', 'AudiobookPrice', 'PaperbackPrice' are columns in your CSV
        for category in ['KindlePrice', 'AudiobookPrice', 'HardcoverPrice','PaperBackPrice']:
            current_price = row[category]
            
            # Find the corresponding row in previous day's DataFrame
            previous_row = previous_df[previous_df['Title'] == row['Title']]
            
            if not previous_row.empty:
                previous_price = previous_row.iloc[0][category]
                
                # Calculate percentage drop
                try:
                    current_price_float = float(current_price.strip('$').replace(',', ''))
                    previous_price_float = float(previous_price.strip('$').replace(',', ''))
                    price_drop_percentage = ((previous_price_float - current_price_float) / previous_price_float) * 100
                except ValueError:
                    price_drop_percentage = 0
                
                # Check if price drop exceeds threshold
                if price_drop_percentage >= PRICE_DROP_PERCENTAGE:
                    # Create a new dictionary with the required columns
                    row_to_include = {
                        'Title': row['Title'],
                        'Category': category,
                        'CurrentPrice': current_price,
                        'PreviousPrice': previous_price,
                        'PriceDropPercentage': price_drop_percentage
                    }
                    rows_to_include.append(row_to_include)
    except KeyError as e:
        print(f"KeyError: {e} - Make sure '{category}' column exists in the DataFrame.")
    except Exception as e:
        print(f"Error occurred while processing row: {e}")

# Create DataFrame from the list of rows to include
price_diff_df = pd.DataFrame(rows_to_include)

# Save to CSV
price_diff_df.to_csv('price_diff.csv', index=False)

print("Price difference data saved successfully to 'price_diff.csv'.")
