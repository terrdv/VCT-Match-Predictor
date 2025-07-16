import '../css/Prediction.css'

function Prediction({ team1, team2, result, onReset }) {
    if (!team1 || !team2 || result === null || result === undefined) {
        return null; // Don't render if required props are missing
    }

    const winner = result.team1_win_prediction ? team1 : team2;
    const loser = result.team1_win_prediction ? team2 : team1;

    return (
        <div className="prediction-container">
            <div className="prediction-header">
                <h3>Match Prediction</h3>
            </div>
            
            <div className="prediction-content">
                <div className="teams-comparison">
                    <div className={`team-result ${result.team1_win_prediction ? 'winner' : 'loser'}`}>
                        <img 
                            src={`http://localhost:5000${team1["Image Path"]}`} 
                            alt={team1["Team"]}
                            className="team-logo"
                        />
                        <span className="team-name">{team1["Team"]}</span>
                        {result.team1_win_prediction && <div className="winner-crown">👑</div>}
                    </div>
                    
                    <div className="vs-section">
                        <span className="vs-text">VS</span>
                        <div className="prediction-arrow">
                            {result.team1_win_prediction ? '←' : '→'}
                        </div>
                    </div>
                    
                    <div className={`team-result ${!result.team1_win_prediction ? 'winner' : 'loser'}`}>
                        <img 
                            src={`http://localhost:5000${team2["Image Path"]}`} 
                            alt={team2["Team"]}
                            className="team-logo"
                        />
                        <span className="team-name">{team2["Team"]}</span>
                        {!result.team1_win_prediction && <div className="winner-crown">👑</div>}
                    </div>
                </div>
                
                <div className="prediction-result">
                    <div className="winner-announcement">
                        <span className="predicted-text">Predicted Winner:</span>
                        <span className="winner-name">{winner["Team"]}</span>
                    </div>
                    
                    {onReset && (
                        <button className="reset-button" onClick={onReset}>
                            Predict Another Match
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Prediction