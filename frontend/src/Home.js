import React from 'react'
import GeneralMap from './maps/GeneralMap'

function Home() {
    return (
    <div className='grid grid-cols-6'>
        <div className="col-span-2">
            <GeneralMap />
        </div>
        
        <div className="col-span-2">counties</div>
    </div>
      
    )
}

export default Home
