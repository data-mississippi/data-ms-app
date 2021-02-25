import React from 'react'
import BaseMap from './BaseMap'

function GeneralStateMap({ children }) {
    return (
        <BaseMap 
            center={[32.56, -89.89]}
            zoom={7}>
            {children}
        </BaseMap>
    )
}

export default GeneralStateMap
