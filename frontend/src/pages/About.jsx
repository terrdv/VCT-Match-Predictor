
import '../css/Home.css'

function About() {


    return (

    <div className="home">
        <div className="text-content">
            <h1>About</h1>
            <div className="about">
                <p>
                    My machine learning algorithm analyzes comprehensive team statistics including win rates, K/D ratios, damage per round, combat scores, and first blood percentages to predict the outcomes of Valorant Champions Tour matches. 
                    By processing historical performance data and current team form, my tool provides data-driven predictions to help fans and analysts understand which team has the statistical advantage going into each match.
                    <br />
                    <br></br>
                    This website uses a logistic regression model to make predictions, ans is trained on this Kaggle Dataset: 
                    <a src="https://www.kaggle.com/datasets/ryanluong1/valorant-champion-tour-2021-2023-data" target="_blank" rel="noopener noreferrer">
                     Valorant Champion Tour 2021-2025 Data by Ryan Luong
                    </a> 
                    <br></br>
                    <br></br>
                    Data last updated: 2025/07/14
                </p>
            </div>
        </div>
    </div>
    )
}


export default About