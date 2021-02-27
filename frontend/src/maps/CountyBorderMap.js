import React, { useEffect, useState } from 'react'
import BaseMap from './BaseMap'
import { GeoJSON } from 'react-leaflet'


function CountyBorderMap({ children, onChooseCounty }) {
    const [countyBorders, setCountyBorders] = useState(null)
    const [boundary, setBoundary] = useState(null)

    const grayPurpleFill = {
        fillColor: '#daf0ce', 
        weight: 0.5,
        opacity: 0.4,
        color: '#666',
        fillOpacity: 0.5
    }

    function onBoundaryMouseover(e) {
        const layer = e.target

        layer.setStyle({
            fillOpacity: 1,
        });
    }

    function resetBoundaryStyle(e) {
        e.target.setStyle(grayPurpleFill)
    }

    function onCountyClick(e) {
        const layer = e.target

        const layerFeature = (layer && layer.feature && layer.feature.properties) 
                                ? layer.feature.properties 
                                : null

        // send the information about the feature to the parent component
        onChooseCounty(layerFeature)
    }

    // todo: useMemo or useCallback. see: https://react-leaflet.js.org/docs/example-external-state
    function eventHandlersOnEachFeature(feature, layer) {
        // this doesn't seem right...
        // update: it's not! see https://reactjs.org/docs/refs-and-the-dom.html
        // or maybe it is? see node_modules/@types/leaflet/index.d.ts line 1209
    
        layer.on({
          mouseover: onBoundaryMouseover,
          mouseout: resetBoundaryStyle,
          click: onCountyClick
        })
    }

    useEffect(() => {
        fetch(`./geojson/county_borders_2020.geojson`, {
            headers: {'Accept': 'application/json'}
          }).then((res) => res.json())
            .then((counties) => {
                setCountyBorders(counties)
            })

    }, [setCountyBorders])

    return (
        <BaseMap 
            center={[32.56, -89.89]}
            zoom={7}>
            {countyBorders 
                && <GeoJSON
                    key='states-layer'
                    data={countyBorders}
                    style={grayPurpleFill}
                    onEachFeature={eventHandlersOnEachFeature} />
            }
        </BaseMap>
    )
}

export default CountyBorderMap
