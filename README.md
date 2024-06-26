# Bet Basket Bot

Bet Basket Bot is a Discord bot written in Python tailored for NBA betting enthusiasts. It offers a suite of features to keep users informed, provide real-time odds, make predictions, and manage bets effectively.

## Features

- Today's NBA Games: Keep track of today's NBA matchups effortlessly.
- Money Line Odds: Access real-time money line odds for NBA matchups provided by FanDuel.
- Predict Matchups: Utilize a trained ML regression model to predict the winning team in a user-inputted NBA matchup.
- Team Acronyms: Get a handy list of NBA team acronyms for reference.
- Register Bets: Register bets in a database to track them conveniently.
- Dashboard: View and compare registered bets using a user-friendly dashboard.

## Setup

1. Clone this repository to your local machine.
2. Install dependencies listed in `requirements.txt`.
   
    ```
    pip install -r requirements.txt
    ```
3. Set up a Discord developer account and obtain its token.
4. Get a free API key for `prop_odds` at https://prop-odds.com/.
5. Set up a MongoDB instance and obtain the connection string.
6. Create a `keys.py` file in the directory and add all the keys and token obtained in the previous steps:

   ```
   prop_odds = 'your_prop_odds_api_key_here'
   token = 'your_discord_bot_token_here'
   mongo_uri = "your_mongodb_connection_string_here"
   ```
8. Run the bot by executing the following command in your command-line

   ```
   python3 main.py
   ```

## Usage

Once the bot is up and running on your Discord server, you can interact with it using the following commands:

- `today`: Display today's NBA matchups.
- `ml_odds`: Display real-time money line odds for NBA matchups.
- `predict [matchup]`: Predict the winning team in a specific NBA matchup.
- `team_acronyms`: View a list of NBA team acronyms for reference.
- `register [matchup] [team] [outcome]`: Register a bet in the database.
- `dashboard`: View and compare registered bets.
- `delete_db`: Delete bets from the database.

Here are some examples of the command outputs:

![](https://github.com/iamjny/Bet-Basket-Bot/blob/main/images/mlodds_sc.JPG)
![](https://github.com/iamjny/Bet-Basket-Bot/blob/main/images/predict_today_sc.JPG)

## Contributing

Contributions are welcome! If you have any suggestions, feature requests, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

