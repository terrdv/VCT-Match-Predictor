from flask import Flask, request
from flask_restful import Resource, Api, abort
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teamsdb.db'
api = Api(app)






class Predictor:
    def __init__(self):
        self.lr_model = joblib.load('ml_models/logistic_regression_model.pkl')
        self.scaler = joblib.load('ml_models/scaler.pkl')
        self.team_data = pd.read_csv('csv/team_data.csv')
        self.match_data = pd.read_csv('csv/scores.csv')
        self.feature_cols = [
        'Team A Winrate vs B', 'Team A Winrate', 'Team A K/D Ratio', 'Team A Average Damage',
        'Team A Average Combat Score', 'Team A Average First Kills', 'Team A Average First Deaths Per Round',
        'Team B Winrate vs A', 'Team B Winrate', 'Team B K/D Ratio', 'Team B Average Damage',
        'Team B Average Combat Score', 'Team B Average First Kills', 'Team B Average First Deaths Per Round'
        ]

    def get_past_matches(self, team1, team2):
        match_data = self.match_data
        match_data = match_data.dropna()
        filtered_df = match_data[(match_data['Match Name'] == team1 + " vs " + team2) | (match_data['Match Name'] == team2 + " vs " + team1)]

        matches = set()
        for i in range(len(filtered_df) - 1, -1, -1):
            matches.add((filtered_df.iloc[i]['Match Result']))

        return matches

    def get_winrate_team1(self, team1, team2):
        match_set = self.get_past_matches(team1, team2)
        if len(match_set) == 0:
            return 0
        wins = 0
        for match in match_set:
            if match ==(team1 + " won"):
                wins += 1
        return wins/len(match_set) * 100

    def build_pred_df(self, teama, teamb):
        a_row = self.team_data.loc[self.team_data['Team'] == teama].squeeze()
        b_row = self.team_data.loc[self.team_data['Team'] == teamb].squeeze()
        pred_df = {
            'Team A Winrate vs B' : [self.get_winrate_team1(teama, teamb)],
            'Team A Winrate' : [a_row["Winrate"]],
            'Team A K/D Ratio' : [a_row["K/D Ratio"]],
            'Team A Average Damage' : [a_row["Average Damage"]],
            'Team A Average Combat Score' : [a_row["Average Combat Score"]],
            'Team A Average First Kills' : [a_row["Average First Kills"]],
            'Team A Average First Deaths Per Round' : [a_row["Average First Deaths Per Round"]],
            'Team B Winrate vs A' : [self.get_winrate_team1(teamb, teama)],
            'Team B Winrate' : [b_row["Winrate"]],
            'Team B K/D Ratio' : [b_row["K/D Ratio"]],
            'Team B Average Damage' : [b_row["Average Damage"]],
            'Team B Average Combat Score' : [b_row["Average Combat Score"]],
            'Team B Average First Kills' : [b_row["Average First Kills"]],
            'Team B Average First Deaths Per Round' : [b_row["Average First Deaths Per Round"]]
        }
        df = pd.DataFrame(pred_df)
    
        return df
    
    def predictionLog_probability_order_invariant(self, teama, teamb, threshold=0.5):
        log_reg = self.lr_model
        scaler = self.scaler
        feature_cols = self.feature_cols
        df = self.build_pred_df(teama, teamb)
        """Order-invariant probability-based prediction"""
        # Make prediction with original order
        data_scaled = pd.DataFrame(scaler.transform(df), columns=feature_cols)
        prob_original = log_reg.predict_proba(data_scaled)[0][1]
        
        # Create swapped version
        df_swapped = df.copy()
        team_a_cols = [col for col in feature_cols if 'Team A' in col]
        team_b_cols = [col for col in feature_cols if 'Team B' in col]
        
        for a_col, b_col in zip(team_a_cols, team_b_cols):
            df_swapped[a_col] = df[b_col]
            df_swapped[b_col] = df[a_col]
        
        # Make prediction with swapped order
        data_swapped_scaled = pd.DataFrame(scaler.transform(df_swapped), columns=feature_cols)
        prob_swapped = log_reg.predict_proba(data_swapped_scaled)[0][1]
        
        # Average the predictions
        final_team_a_prob = (prob_original + (1 - prob_swapped)) / 2
        
        return 1 if final_team_a_prob >= threshold else 0





class PredictorMatchup(Resource):
    def get(self, team1, team2):
        predictor = Predictor()
        if not team1 or not team2:
            return {'error': 'Both team1 and team2 query parameters are required'}, 400

        prediction = predictor.predictionLog_probability_order_invariant(team1, team2)

        return {
            'team1': team1,
            'team2': team2,
            'team1_win_prediction': bool(prediction)
        }, 200

class MatchupData(Resource):
    def get(self, team1, team2):
        predictor = Predictor()

        if not team1 or not team2:
            return {'error': 'Both team1 and team2 query parameters are required'}, 400
        
        data = predictor.build_pred_df(team1, team2)

        return data.to_json()


api.add_resource(PredictorMatchup, '/api/predict/<team1>/<team2>')
api.add_resource(MatchupData, '/api/matchup_data/<team1>/<team2>')


@app.route('/')
def home():
    return '<h1>Valorant Predictor</h1>'


if __name__ == '__main__':
    
    app.run(debug=True)
