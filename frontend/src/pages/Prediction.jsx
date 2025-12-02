import {useState, useEffect} from 'react'
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


}