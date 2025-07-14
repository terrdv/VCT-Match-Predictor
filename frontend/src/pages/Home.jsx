import '../css/Home.css'
import {useState, useEffect} from "react"
import { getPrediction, getMatchupData , getTeamData, getTeams} from '../services/api'
import Matchup from '../components/Matchup'
import TeamButton from '../components/TeamButton'

function Home() {
    const [match, setMatch] = useState([null, null])
    const [teams, setTeams] = useState([])
    const [error, setError] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const loadTeams = async() => {
            try{
                const allteams = await getTeams();
                setTeams(allteams)
            } catch (err) {
                console.log(err)
                setError("Failed to load teams...")
            } finally {
                setLoading(false)
            }
        }
        loadTeams()
    }, [])


    
    return (
        <div className="home">
            <div className="text-content">
                <h1>VCT Match Predictor</h1>
                <p>Predict the outcome of VCT matches using machine learning</p>
                <Matchup team1={match[0]} team2={match[1]}></Matchup>
                <button >Predict</button>
            </div>
            {error && <div className="error-message">{error}</div>}

            {loading ? <div className="loading">Loading...</div> 
            : (
                <div className="button-grid">
                    {teams.map(team => (
                        <TeamButton team={team} key={team.id} />
                    ))

                    }
                </div>
            )}
        </div>
    )
}

export default Home