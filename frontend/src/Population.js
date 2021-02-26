import React, { useState } from 'react'
import CountyBorderMap from './maps/CountyBorderMap'

// todo:
// data visualizations
// more years of census data
// link to sources
// csv export
// compare

function CountyDetails({ county }) {
    console.log('county', county)

    return (
        <>
            <h2 className="text-4xl font-mono text-blue-900">{county['NAME']} County</h2>

            <div className="flex justify-around">
                <div className="text-center rounded-lg border border-blue-900 p-2">
                    <h3 className="text-xl font-bold">Population</h3>
                    <table className="table-auto">
                        <thead>
                            <tr>
                                <th>1990</th>
                                <th>2000</th>
                            </tr>
                            
                        </thead>
                        <tbody>
                            <tr>
                                <td>{county['POP2000']}</td>
                                <td>{county['POP2000']}</td>
                            </tr>
                            
                        </tbody>
                    </table>
                    <p>population time chart</p>
                </div>
                
                <div className="text-center"> 
                    <h3 className="text-xl font-bold">Population by age</h3>
                    <p>under 5: {county['AGE_UNDER5']}</p>
                    <p>5 - 17: {county['AGE_5_17']}</p>
                    <p>18 - 29: {county['AGE_18_29']}</p>
                    <p>30 - 49: {county['AGE_30_49']}</p>
                    <p>50 - 64: {county['AGE_50_64']}</p>
                    <p>65+: {county['AGE_65_UP']}</p>
                </div>

                <div className="text-center">
                    <h3 className="text-xl font-bold">Population by race and ethnicity</h3>
                    <p>Black: {county['BLACK']}</p>
                    <p>White: {county['WHITE']}</p>
                    <p>Hispanic: {county['HISPANIC']}</p>
                    <p>American Indian, Eskimo, or Aleut: {county['AMERI_ES']}</p>
                    <p>Asian or Pacific Islander: {county['ASIAN_PI']}</p>
                </div>
            </div>
        </>
    )
}

function Population() {
    const [county, setCounty] = useState(null)

    return (
        <div className='grid grid-cols-6 mx-4'>
            <div className="col-span-2 m-2 rounded-lg border-2 border-blue-900 p-4">
                <CountyBorderMap onChooseCounty={(county) => setCounty(county)} />
            </div>
            
            <div className="col-span-4 rounded-lg border-2 border-blue-900 px-4 py-2 m-2">
                
                {county 
                    ? <CountyDetails county={county} /> 
                    : 
                        <>
                            <h1 className="text-4xl text-blue-900 font-mono">County Kiosk</h1>
                            <p>Click on a county.</p>
                        </>
                }
            </div>
        </div>
    )
}

export default Population
