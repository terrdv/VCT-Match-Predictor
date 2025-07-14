
import '../css/TeamButton.css'

function TeamButton({ team }) {
    return (
        <div className="team-button">
            
            <button className="pick">
                <img className="button_icon" src={`http://localhost:5000${team["Image Path"]}`} alt={team["Team"]} />
                {team["Team"]}
            </button>
        </div>
    )
}


export default TeamButton