import {useState, useEffect, use} from 'react'
import {getPrediction, getMatchupData , getTeamData} from '../services/api'
import {useParams} from 'react-router-dom'
import Matchup from '../components/Matchup'
import Prediction from '../components/Prediction'
import TeamStatsDashboard from '../components/TeamDashboard'
import '../css/Home.css'

function PredictionPage() {

    const [loading, setLoading] = useState(true)
    const {team1, team2} = useParams()
    const [matchResult, setMatchResult] = useState(null)
    const [matchupData, setMatchupData] = useState(null)
    const [predicted, setPredicted] = useState(false)


    


    useEffect(() => {
        const fetchPrediction = async () => {
            try {
                const prediction = await getPrediction(team1, team2)
                const data = await getMatchupData(team1, team2)
                setMatchupData(data)
                setMatchResult(prediction)
                setPredicted(true)
            } catch (err) {
                console.log(err)
            } finally {
                setLoading(false)
            }
        }

        fetchPrediction()
    }, [])


    
    return loading ? (<p>Loading...</p>) : (
    predicted ? (
        <div className="prediction-page">
            <Matchup team1={team1} team2={team2} matchupData={matchupData} />
            <Prediction matchResult={matchResult} team1={team1} team2={team2} />
        </div>
    ) : (<p>hi</p>)
    
    )
}

export default PredictionPage