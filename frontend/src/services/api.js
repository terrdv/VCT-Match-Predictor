const BASE_URL = "http://localhost:5000/api"


export const getPrediction = async(team1, team2) => {
    console.log(`${BASE_URL}/predict/${team1["Team"]}/${team2["Team"]}`)
    const result = await fetch(`${BASE_URL}/predict/${encodeURIComponent(team1["Team"])}/${encodeURIComponent(team2["Team"])}`)
    if (!result.ok) throw new Error('Prediction failed');
    return await result.json()
}


export const getMatchupData = async(team1, team2) => {
    const result = await fetch(`${BASE_URL}/predict/${encodeURIComponent(team1["Team"])}/${encodeURIComponent(team2["Team"])}`)
    if (!result.ok) throw new Error('Prediction failed');
    return await result.json()
}


export const getTeams = async() => {
    const response = await fetch(`${BASE_URL}/teams`)
    const data = await response.json()
    const parsed = JSON.parse(data)
    return parsed
}


export const getTeamData = async(team) => {
    const response = await fetch(`${BASE_URL}/info/${encodeURIComponent(team)}`)
    const data = await response.json()
    const parsed = JSON.parse(data)
    return parsed
}