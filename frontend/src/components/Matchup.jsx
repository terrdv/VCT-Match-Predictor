import TeamCard from '../components/TeamCard'
import '../css/Matchup.css'

function Matchup({team1, team2}) {

    if (isNaN(team1)) {
        return (
            <div className="matchup">
                <div className="team-slot">
                    {team1 ? (
                        <TeamCard team={team1} />
                    ) : (
                        <div className="select-team-placeholder">
                            <p>Select Team 1</p>
                        </div>
                    )}

                </div>
                <div className="vs">
                    <span>VS</span>
                </div>
                <div className="team-slot">
                    {team2 ? (
                        <TeamCard team={team2} />
                    ) : (
                        <div className="select-team-placeholder">
                            <p>Select Team 2</p>
                        </div>
                    )}
                </div>
            </div>
            
        )
    }
}

export default Matchup