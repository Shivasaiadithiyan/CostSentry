# Wishlist Price Tracker

## Project Overview
This project is a price tracking tool for wishlist items from an online furniture store. It leverages Selenium for web scraping and SQLite for data storage. The tool monitors changes in prices of wishlist items, saves them to a database, and sends notifications when price drops are detected. It also provides functionality to visualize price trends over time using Matplotlib.

## Features
- **Web Scraping**: Automated extraction of wishlist items and their details.
- **Database Storage**: SQLite database for storing item details and price history.
- **Price Drop Detection**: Identifies and alerts when prices decrease.
- **Price Trend Visualization**: Generates and displays graphs showing price trends over time.
- **User Authentication**: Secure login using email and password (stored in an encrypted file).
- **Email Notifications**: Sends email alerts for price drops.

## Setup and Installation

### Prerequisites
- Python 3.x
- Google Chrome or Brave Browser (make sure to specify the path to the browser executable if using Brave)
- Email account for sending notifications (e.g., Gmail)

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Shivasaiadithiyan/wishlist-price-tracker.git
    ```

2. **Navigate to the project directory:**
    ```bash
    cd wishlist-price-tracker
    ```

3. **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your email credentials:**
   - Configure your email credentials and other settings by updating the `sendNotification` function in the `Notification.py` file. Replace `'enteryourmail@gmail.com'` and `'enteryourmailpassword'` with your actual email address and password.

5. **Run the scraper:**
    ```bash
    python run.py
    ```

## Usage
- **Initial Setup:** Run the script to create the database and delete any existing data:
    ```bash
    python run.py
    ```

- **Change User Details:** If you need to update the email and password used for logging in, use the `changeUserRun` method in the `Furniture` class.

## Contributing
Feel free to open issues or submit pull requests if you find bugs or have improvements.

## License
This project is licensed under the MIT License. See the [LICENSE](https://www.mit.edu/~amini/LICENSE.md) file for details.

## Contact
For questions or feedback, please contact [shivasaiadithiyan@gmail.com](mailto:shivasaiadithiyan@gmail.com).
