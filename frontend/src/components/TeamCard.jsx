import '../css/TeamCard.css'


function TeamCard({team}) {

    return (
        <div className="card">
            <img src={`https://vct-match-predictor-api.onrender.com/${team["Image Path"]}`}></img>
            <h2>{team["Team"]}</h2>
        </div>
    )
}

export default TeamCard