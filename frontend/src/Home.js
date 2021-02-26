import React, { useState } from 'react'
import CountyBorderMap from './maps/CountyBorderMap'

function CountyDetails({ county }) {
    console.log('county', county)

    return (
        <div className="">
            <h2 className="text-4xl">{county['NAME']} County</h2>

            <div className="flex justify-around">
                <div>
                    <h3 className="text-xl font-bold">Total Population</h3>
                    <p>2000 Population: {county['POP2000']}</p>
                    <p>1990 Population: {county['POP2000']}</p>
                    <p>population time chart</p>
                </div>
                
                <div> 
                    <h3>Population by age</h3>
                    <p>under 5: {county['AGE_UNDER5']}</p>
                    <p>5 - 17: {county['AGE_5_17']}</p>
                    <p>18 - 29: {county['AGE_18_29']}</p>
                    <p>30 - 49: {county['AGE_30_49']}</p>
                    <p>50 - 64: {county['AGE_50_64']}</p>
                    <p>65+: {county['AGE_65_UP']}</p>
                </div>

                <div> 
                    <h3>Population by race and ethnicity</h3>
                    <p>Black: {county['BLACK']}</p>
                    <p>White: {county['WHITE']}</p>
                    <p>Hispanic: {county['HISPANIC']}</p>
                    <p>American Indian, Eskimo, or Aleut: {county['AMERI_ES']}</p>
                    <p>Asian or Pacific Islander: {county['ASIAN_PI']}</p>
                </div>
            </div>
            
            
        </div>
    )
}

function Home() {
    const [county, setCounty] = useState(null)

    return (
        <div className='grid grid-cols-6 mx-4'>
            <div className="col-span-2 m-2 rounded-lg border-2 border-blue-900 bg-red-50 p-4">
                <CountyBorderMap onChooseCounty={(county) => setCounty(county)} />
            </div>
            
            <div className="col-span-4 rounded-lg border-2 border-blue-900 bg-red-50 px-4 py-2 m-2">
                <h1 className="text-xl text-blue-900 font-mono">County Kiosk</h1>
                {county ? <CountyDetails county={county} /> : <p>Click on a county to see more.</p>}
            </div>
        </div>
    )
}

export default Home
