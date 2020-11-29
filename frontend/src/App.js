import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { MapContainer, TileLayer, Marker, Popup, CircleMarker, Tooltip, GeoJSON } from 'react-leaflet'
// import statesGeoJSON from './us-states.geojson'
// import msCountiesGeoJson from './ms-counties.json'
// import msPrecinctsGeoJson from './ms-precincts-12.json'
import testJson from './test.json'
import 'leaflet/dist/leaflet.css'
import './App.css'
import './generated-styles.css'
import GreetingsFromForlorn from './GreetingsFromForlorn'

// function MapPlaceholder(message) {
//   return (
//     <div>
//     <p>{message ? message : 'The map is not working with your browser.'}</p>
//     <p><noscript>You need to enable JavaScript to see this map.</noscript></p>
//   )
// }

// // Map of Forlorn, Mississippi.{' '}

// <GeoJSON key='watershed-layer' data={this.props.geojson} style={this.getStyle} />

 // const MapPlaceholder = (<MapPlaceholder message={'Map of America.'} />)

function GenericMap({ center, zoom, children }) {
  return (
    <MapContainer
      center={center} 
      zoom={zoom}
      className=""
      >
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright" target="_parent">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions" target="_parent">CARTO</a>'
        />
        {children}
    </MapContainer>
    )
}

function getCounties() {
  axios.get(`/counties/`, {
    headers: {
      'Accept': 'application/json'
  }
  }).then(({data}) => {
      return data
    }).catch(err => console.log(err))
}

function getRedChoroplethStyle(feature) {
  function setDensityColor(d) {
    return d > 1000 ? '#800026' :
           d > 500  ? '#BD0026' :
           d > 200  ? '#E31A1C' :
           d > 100  ? '#FC4E2A' :
           d > 50   ? '#FD8D3C' :
           d > 20   ? '#FEB24C' :
           d > 10   ? '#FED976' :
                      '#63bf9b';
  }

  return {
      fillColor: setDensityColor(feature.properties.density),
      weight: 1,
      opacity: 1,
      color: '#666',
      dashArray: '3',
      fillOpacity: 0.7
  };
}

const choroplethStyle = function getRedChoroplethStyle(feature) {
  function setDensityColor(d) {
    return d > 1000 ? '#800026' :
           d > 500  ? '#BD0026' :
           d > 200  ? '#E31A1C' :
           d > 100  ? '#FC4E2A' :
           d > 50   ? '#FD8D3C' :
           d > 20   ? '#FEB24C' :
           d > 10   ? '#FED976' :
                      '#63bf9b';
  }

  return {
      fillColor: setDensityColor(feature.properties.density),
      weight: 1,
      opacity: 1,
      color: '#666',
      fillOpacity: 0.7
  };
}

function getGeoJsonPerCounty(countiesGeo, countyFips) {
  countiesGeo.features.map((feature) => {
    console.log(feature.properties)
    if (feature.properties.COUNTYFP10 == countyFips) {
      console.log("true,", feature)
      return feature
    }
  })
}

// county geojson guide? https://sampleserver6.arcgisonline.com/arcgis/rest/services/Census/MapServer/layers

function MapOfAmerica({ geoJSON = null}) {
  const america = {center: [37.8, -96], zoom: 4}
  const mississippiView = {center: [32.71492866908233, -89.49462890625], zoom: 7}
  const [view, setView] = useState(mississippiView)
  const [boundary, setBoundary] = useState(null)

  function mouseoverBoundary(e) {
    const layer = e.target

    const layerFeature = (layer && layer.feature && layer.feature.properties) 
                          ? layer.feature.properties 
                          : null

    setBoundary(() => layerFeature)

    layer.setStyle({
      fillOpacity: 1,
    });
  }

  function resetBoundaryStyle(e) {
    // get the original style from this.feature aka the <GeoJSON /> instance
    const originalStyle = getRedChoroplethStyle(this.feature)

    setBoundary(() => null)
    e.target.setStyle({
      fillOpacity: originalStyle.fillOpacity
    })
  }

  function handleClick(e) {
    console.log('click')
    console.log(e)
  }

  function eventHandlersOnEachFeature(feature, layer) {
    // this doesn't seem right...
    // update: it's not! see https://reactjs.org/docs/refs-and-the-dom.html
    // or maybe it is? see node_modules/@types/leaflet/index.d.ts line 1209

    layer.on({
      mouseover: mouseoverBoundary,
      mouseout: resetBoundaryStyle,
      click: handleClick
    })
  }

  return (
    <div className='w-full flex flex-row md:flex-col'>
      <div className="w-1/2 md:w-full m-4">
        <GenericMap
          center={view.center}
          zoom={view.zoom}
        >
          {
            geoJSON 
            ? <GeoJSON 
                key='states-layer' 
                data={geoJSON} 
                style={choroplethStyle} 
                onEachFeature={eventHandlersOnEachFeature} />
            : <GeoJSON />
          }
          <Tooltip direction="bottom" offset={[0, 20]} opacity={1} permanent>
            permanent Tooltip for Rectangle
          </Tooltip>
        </GenericMap>
      </div>
      <div className='m-4'>
        {geoJSON ? null 
          : <div>
              <p>loading county lines...</p>
            </div>
        }
        {boundary ? 
          <div>
            <h2>
              {boundary.NAME}
            </h2> 
            <p>Population in the year 2000: {boundary.POP2000}</p>
          </div>
          : (geoJSON ? <h2>Hover over a county to learn more about it.</h2> : null)}
      </div>
    </div>
  )
}

function App() {
  const [countiesGeo, setCountiesGeo] = useState(null)

  useEffect(() => {
    fetch(`/geo/`, {
      headers: {'Accept': 'application/json'}
    }).then((res) => res.json())
      .then((counties) => {
        setCountiesGeo(counties[0].geojson)
      })
  }, [setCountiesGeo])
  return (
    <div className="flex flex-wrap md items-center h-screen p-4">
      <MapOfAmerica geoJSON={countiesGeo} />
    </div>
  );
}

export default App;
