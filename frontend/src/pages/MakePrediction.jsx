import '../css/Home.css'
import { useState, useEffect, useNavigate } from "react"
import { getTeams } from '../services/api'
import Matchup from '../components/Matchup'
import '../css/Dropdowns.css'

function MakePrediction() {
    const [teams, setTeams] = useState([])
    const [loading, setLoading] = useState(true)

    // Use empty string instead of null so <select> resets correctly
    const [team1, setTeam1] = useState("")
    const [team2, setTeam2] = useState("")

    useEffect(() => {
        const loadTeams = async () => {
            try {
                const allteams = await getTeams()
                setTeams(allteams)
            } catch (err) {
                console.log(err)
            } finally {
                setLoading(false)
            }
        }
        loadTeams()
    }, [])

    const clearMatch = () => {
        setTeam1("")
        setTeam2("")
    }

    return (
        <div className="home">
            <div className="text-content">
                <h1>VCT Match Predictor</h1>
                <p>Predict the outcome of VCT matches using machine learning</p>
            </div>

            {/* Send actual team objects to Matchup */}
            <Matchup 
                team1={team1 !== "" ? teams[team1] : null} 
                team2={team2 !== "" ? teams[team2] : null} 
            />

            {loading ? (
                <p>Loading teams...</p>
            ) : (
                <div className="dropdowns">
                    {/* TEAM 1 */}
                    <select 
                        id="team1" 
                        value={team1} 
                        onChange={(e) => setTeam1(e.target.value)}
                    >
                        <option value="">Select Team 1</option>
                        {teams.map((team, index) => (
                            <option key={team.id} value={index}>
                                {team.Team}
                            </option>
                        ))}
                    </select>

                    {/* TEAM 2 */}
                    <select 
                        id="team2" 
                        value={team2} 
                        onChange={(e) => setTeam2(e.target.value)}
                    >
                        <option value="">Select Team 2</option>
                        {teams.map((team, index) => (
                            <option key={team.id} value={index}>
                                {team.Team}
                            </option>
                        ))}
                    </select>
                </div>
            )}

            {/* BUTTONS */}
            <div className="buttons">
                <button onClick={clearMatch}>Clear Match</button>

                <button 
                    disabled={team1 === "" || team2 === ""}
                    onClick={() => console.log("Predict pressed")}
                >
                    Predict
                </button>
            </div>
        </div>
    )
}

export default MakePrediction
