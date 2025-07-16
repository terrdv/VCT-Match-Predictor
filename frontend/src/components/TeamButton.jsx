

import '../css/TeamButton.css'

function TeamButton({ team, onTeamSelect, isSelected }) {
    const handleClick = () => {
        onTeamSelect(team);
    };

    return (
        <div className="team-button">
            <button 
                className={`pick ${isSelected ? 'selected' : ''}`}
                onClick={handleClick}
            >
                <img className="button_icon" src={`https://vct-match-predictor-api.onrender.com/${team["Image Path"]}`} alt={team["Team"]} />
                {team["Team"]}
            </button>
        </div>
    )
}

export default TeamButton