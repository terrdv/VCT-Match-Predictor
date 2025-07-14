

function Matchup(team1, team2) {

    if (isNaN(team1)) {
        return (
            <div>
                <div>
                    <p>Select Team</p>
                </div>
                <div>
                    <p>Select Team</p>
                </div>
            </div>    
        )
    } else if (isNaN(team1) && isNaN(team2)) {
        return (
            <div>
                <div>
                    <p>{team1}</p>
                </div>
                <div>
                    <p>Select Team</p>
                </div>
            </div>
        )
    } else {
        return (
            <div>
                <div>
                    <p>{team1}</p>
                </div>
                <div>
                    <p>{team2}</p>
                </div>
            </div>
        )
    }
}

export default Matchup