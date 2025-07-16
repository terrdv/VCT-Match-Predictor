from flask import Flask, request
from flask_restful import Resource, Api, abort
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import pandas as pd
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teamsdb.db'
CORS(app)
api = Api(app)


class Predictor:
    def __init__(self):
        self.lr_model = joblib.load('ml_models/logistic_regression_model.pkl')
        self.rf_model = joblib.load('ml_models/rf_augmented_model.pkl')
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
            return None
        wins = 0
        for match in match_set:
            if match ==(team1 + " won"):
                wins += 1
        return wins/len(match_set) * 100

    def build_pred_df(self, teama, teamb):
        # Get team data with proper error handling
        a_data = self.team_data.loc[self.team_data['Team'] == teama]
        b_data = self.team_data.loc[self.team_data['Team'] == teamb]
        
        # Check if teams exist
        if a_data.empty:
            raise ValueError(f"Team '{teama}' not found in team data")
        if b_data.empty:
            raise ValueError(f"Team '{teamb}' not found in team data")
        
        # Get first row and convert to scalar values
        a_row = a_data.iloc[0]
        b_row = b_data.iloc[0]

        winrate_team1 = self.get_winrate_team1(teama, teamb)
        if winrate_team1 is None:
            winrate_team1 = 0
            winrate_team2 = 0
        else:
            winrate_team2 = 100 - winrate_team1
        
        # Build prediction dictionary with scalar values
        pred_df = {
            'Team A Winrate vs B': [winrate_team1],
            'Team A Winrate': [a_row["Winrate"]],
            'Team A K/D Ratio': [a_row["K/D Ratio"]],
            'Team A Average Damage': [a_row["Average Damage"]],
            'Team A Average Combat Score': [a_row["Average Combat Score"]],
            'Team A Average First Kills': [a_row["Average First Kills"]],
            'Team A Average First Deaths Per Round': [a_row["Average First Deaths Per Round"]],
            'Team B Winrate vs A': [winrate_team2],
            'Team B Winrate': [b_row["Winrate"]],
            'Team B K/D Ratio': [b_row["K/D Ratio"]],
            'Team B Average Damage': [b_row["Average Damage"]],
            'Team B Average Combat Score': [b_row["Average Combat Score"]],
            'Team B Average First Kills': [b_row["Average First Kills"]],
            'Team B Average First Deaths Per Round': [b_row["Average First Deaths Per Round"]]
        }
        
        df = pd.DataFrame(pred_df)
        
        # Additional safety check - ensure all values are numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Fill any NaN values with 0 (or appropriate defaults)
        df = df.fillna(0)
        
        return df
    
        """Most robust approach - ensemble of both methods"""
        log_reg = self.lr_model
        scaler = self.scaler
        feature_cols = self.feature_cols
        
        # Method 1: Build both orientations
        df_ab = self.build_pred_df(teama, teamb)
        df_ba = self.build_pred_df(teamb, teama)
        
        data_ab_scaled = pd.DataFrame(scaler.transform(df_ab), columns=feature_cols)
        data_ba_scaled = pd.DataFrame(scaler.transform(df_ba), columns=feature_cols)
        
        prob_ab = log_reg.predict_proba(data_ab_scaled)[0][1]
        prob_ba = log_reg.predict_proba(data_ba_scaled)[0][1]
        
        method1_prob = (prob_ab + (1 - prob_ba)) / 2
        
        # Method 2: Feature swapping
        df = self.build_pred_df(teama, teamb)
        data_scaled = pd.DataFrame(scaler.transform(df), columns=feature_cols)
        prob_original = log_reg.predict_proba(data_scaled)[0][1]
        
        df_swapped = df.copy()
        team_a_cols = [col for col in feature_cols if 'Team A' in col]
        team_b_cols = [col for col in feature_cols if 'Team B' in col]
        
        for a_col, b_col in zip(team_a_cols, team_b_cols):
            df_swapped[a_col] = df[b_col]
            df_swapped[b_col] = df[a_col]
        
        data_swapped_scaled = pd.DataFrame(scaler.transform(df_swapped), columns=feature_cols)
        prob_swapped = log_reg.predict_proba(data_swapped_scaled)[0][1]
        
        method2_prob = (prob_original + (1 - prob_swapped)) / 2
        
        # Average both methods
        final_prob = (method1_prob + method2_prob) / 2
        
        return 1 if final_prob >= threshold else 0


    def prediction_probability(self, teama, teamb, threshold=0.5):
        # Test both team orders
        df_ab = self.build_pred_df(teama, teamb)
        
        rf = joblib.load('ml_models/rf.pkl')
        
        prob_a_wins_ab = rf.predict_proba(df_ab)[0][1]
        return 1 if prob_a_wins_ab>= threshold else 0


class TeamData(Resource):
    def get(self, team):
        if not team:
            return {'error': 'Query Parameter Required'}
        
        predictor = Predictor()
        return predictor.team_data[predictor.team_data['Team'] == team].to_json(orient="records")
    
class TeamsData(Resource):
    def get(self):
        
        predictor = Predictor()
        return predictor.team_data.to_json(orient="records")


class PredictorMatchup(Resource):
    def get(self, team1, team2):
        predictor = Predictor()
        if not team1 or not team2:
            return {'error': 'Both team1 and team2 query parameters are required'}, 400

        try:
            prediction = predictor.prediction_probability(team1, team2)
            return {
                'team1': team1,
                'team2': team2,
                'team1_win_prediction': bool(prediction)
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'Prediction failed: {str(e)}'}, 500

class MatchupData(Resource):
    def get(self, team1, team2):
        predictor = Predictor()

        if not team1 or not team2:
            return {'error': 'Both team1 and team2 query parameters are required'}, 400
        
        data = predictor.build_pred_df(team1, team2)

        return data.to_json(orient="records")

api.add_resource(TeamData, '/api/info/<team>')
api.add_resource(TeamsData, '/api/teams')
api.add_resource(PredictorMatchup, '/api/predict/<team1>/<team2>')
api.add_resource(MatchupData, '/api/matchup_data/<team1>/<team2>')


@app.route('/')
def home():
    return '<div></div>'


if __name__ == '__main__':
    
    app.run(debug=True)
