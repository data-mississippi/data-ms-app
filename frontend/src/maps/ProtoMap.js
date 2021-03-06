import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { MapContainer, TileLayer, Marker, Popup, CircleMarker, Tooltip, GeoJSON } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import '../styles/App.css'
import '../styles/generated-styles.css'
import BaseMap from './BaseMap'


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
        <BaseMap
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
        </BaseMap>
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

function ProtoMap() {
  const [countiesGeo, setCountiesGeo] = useState(null)
  const [countyPrecincts, setCountyPrecincts] = useState(null)

  const countyBordersUrl = '/counties/geojson/borders/'
  useEffect(() => {
    fetch(`/counties/precincts/081/`, {
      headers: {'Accept': 'application/json'}
    }).then((res) => res.json())
      .then((precincts) => {
        //setCountiesGeo(counties[0].geojson)
        const geo_json = {
          'type': 'FeatureCollection',
          'features': []
          }
        geo_json.features = precincts.map((precinct) => {
          console.log(precinct.geojson.features)
          return precinct.geojson.features[0]
        })
        console.log(geo_json)
        setCountyPrecincts(geo_json)
      })
  }, [setCountiesGeo])
  return (
    <div className="flex flex-wrap md items-center h-screen p-4">
      <MapOfAmerica geoJSON={countyPrecincts} />
    </div>
  );
}

export default ProtoMap;
