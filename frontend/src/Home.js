import React, { useState } from 'react'
import CountyBorderMap from './maps/CountyBorderMap'

function CountyDetails({ county }) {
    console.log('county', county)

    return (
        <div className="">
            <h2 className="text-4xl">{county['NAME']} County</h2>
            <p>2000 Population: {county['POP2000']}</p>
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
            
            <div className="col-span-2 rounded-lg border-2 border-blue-900 bg-red-50 px-4 py-2 m-2">
                <h1 className="text-xl text-right text-blue-900 font-mono">County Kiosk</h1>
                {county ? <CountyDetails county={county} /> : <p className="text-right">Click on a county to see more.</p>}
            </div>
        </div>
    )
}

export default Home
