import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { getTeamData, getPrediction } from '../services/api'
import Matchup from '../components/Matchup'
import Prediction from '../components/Prediction'
import '../css/Home.css'

function PredictionPage() {
    const { team1, team2 } = useParams()

    const [loading, setLoading] = useState(true)
    const [team1Data, setTeam1Data] = useState(null)
    const [team2Data, setTeam2Data] = useState(null)
    const [predictionResult, setPredictionResult] = useState(null)

    useEffect(() => {
        const fetchData = async () => {
            try {
            const prediction = await getPrediction(team1, team2)
            console.log(prediction)
            setPredictionResult(prediction)
            console.log("Fetching team 1")
            const t1 = await getTeamData(team1)
            console.log("Team 1 done")

            console.log("Fetching team 2")
            const t2 = await getTeamData(team2)
            console.log("Team 2 done")

            setTeam1Data(t1[0])
            setTeam2Data(t2[0])


            console.log("Prediction done")

            } catch (err) {
                console.error(err)
            } finally {
                setLoading(false)
            }
        }

        fetchData()
    }, [])


    if (loading) return <p>Loading...</p>

    return (
        <div className="prediction-page">
            <Matchup team1={team1Data} team2={team2Data} />
            <Prediction result={predictionResult} team1={team1Data} team2={team2Data} />
        </div>
    )
}

export default PredictionPage
