"use client"

//Next imports
import { useSession  } from 'next-auth/react'
import { redirect } from 'next/navigation';
import Link from 'next/link';


//React imports
import React,{useEffect, useState, useCallback}  from 'react';

//Apis imports
import { ApiRescueFloraSpecie } from "../api/rescue_flora/route";
import { ApiTransectHerpetofaunaWithSpecies } from '../api/rescue_herpetofaina/route';
import { ApiRescueMammalsWithSpecies } from '../api/rescue_mammals/router';
import { SpeciesItem } from '../api/species/route';
import { ApiSunburstByFamily } from '../api/nivo/route';

//Leaflet imports
import { MapContainer, TileLayer,Circle, Polyline, Tooltip } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css'
import "leaflet-defaulticon-compatibility"

//Components imports
import SpecieList from '../components/Species/SpecieList';
import FloraRescueSpecieMap from '../components/RescueFlora/rescueFloraSpecieMap'; 
import TransectHerpetofaunaSpecieMap from '../components/Transectors/TransectoSpecieMap';
import RescueMammalsSpecieMap from '../components/RescueMammals/RescueMammalsSpecieMap';
import { LineProyect } from '../components/Map/lineProyect';
import Legend from '../components/Map/Legend';
import SunburstFamily from '../components/Nivo/SunBurstFamily';


export default function Dashboard() {
    const { data: session } = useSession();
    const [rescueFloraData, setRescueFloraData] = useState<FloraRescueSpeciesData[]>([]);
    const [specieData, setSpecieData] = useState<SpecieItemData[]>([])
    const [transectData, setTransectData] = useState<TransectHerpetoWithSpecies[]>([])
    const [rescueMammalsData, setRescueMammalsData] = useState<RescueMammalsWithSpecieData[]>([])
    const [sunburstData, setSunburstData] = useState<SunBurstFamilyData>({name: "root", color: "hsl(0, 0%, 100%)", loc: 0, children: []}
)

    const user = session?.user;

    const rescueDataFlora = useCallback(async (): Promise<FloraRescueSpeciesData[]>=>{
      if (user){
       const data= await ApiRescueFloraSpecie({token: user?.token})
       return data
      }
      else{
        return []
      }
    }, [user])
    
    const speciesData = useCallback(async (): Promise<SpecieItemData[]>=>{
        if (user){
            const data= await SpeciesItem({token: user?.token})
            return data
        }
        else{
            return []
        }
    }, [user])

    const transectDataHerpeto = useCallback(async (): Promise<TransectHerpetoWithSpecies[]>=>{
        if (user){
            const data= await ApiTransectHerpetofaunaWithSpecies({token: user?.token})
            return data
        }
        else{
            return []
        }
    }, [user])

    const rescueDataMammals = useCallback(async (): Promise<RescueMammalsWithSpecieData[]>=>{
        if (user){
            const data= await ApiRescueMammalsWithSpecies({token: user?.token})
            return data
        }
        else{
            return []
        }
    }, [user])

    const sunburstDataApi = useCallback(async (): Promise<SunBurstFamilyData>=>{
        if (user){
                const data= await ApiSunburstByFamily({token: user?.token})
                return data
        }
        else{
                return  {name: "root", color: "hsl(0, 0%, 100%)", loc: 0, children: []}
        }
        }, [user])




    useEffect(() => {
        if (!session?.user) {
            redirect('/')
        }
        else{
            rescueDataFlora().then((data)=>{
                setRescueFloraData(data)
            })
            speciesData().then((data)=>{
                setSpecieData(data)
            })
            transectDataHerpeto().then((data)=>{
                setTransectData(data)
            })
            rescueDataMammals().then((data)=>{
                setRescueMammalsData(data)
            })

            sunburstDataApi().then((data)=>{
                setSunburstData(data)
            })

        }

    }, [session, rescueDataFlora, speciesData, transectDataHerpeto, rescueDataMammals, sunburstDataApi])


    const lineOptions = { color: 'red' }

    const legedColors = ['brown','green', 'blue', 'red' ]
    const legendLabels = ['Puntos Rescate de Mamiferos','Transcetors Herpetofauna', 'Puntos Rescates de Flora', 'Proyecto 230 kV Mizque - Sehuencas']
        return (
            <div>
                <div className="flex flex-col  h-full 2xl:mb-52 xl:mb-52 lg:mb-40 md:flex-row md:mb-0 sm:mb-0 justify-center">
                    <div className="h-96 p-0 z-50 md:w-1/2 p-4 md:h-[16rem] sd:h-[6rem]">
                        <MapContainer
                            center={[-17.489, -65.271]}
                            zoom={12}
                            scrollWheelZoom={false}
                            className='h-80 w-full 2xl:h-[40rem] xl:h-[40rem] lg:h-[35rem]'
                             >
                                <TileLayer
                                
                                url={`https://api.mapbox.com/styles/v1/mapbox/streets-v12/tiles/256/{z}/{x}/{y}@2x?access_token=${process.env.NEXT_PUBLIC_MAPBOX_TOKEN}`}
                                attribution='Map data &copy; <a href=&quot;https://www.openstreetmap.org/&quot;>OpenStreetMap</a> contributors, <a href=&quot;https://creativecommons.org/licenses/by-sa/2.0/&quot;>CC-BY-SA</a>, Imagery &copy; <a href=&quot;https://www.mapbox.com/&quot;>Mapbox</a>'
                                />
                                <RescueMammalsSpecieMap data={rescueMammalsData}/>
                                <TransectHerpetofaunaSpecieMap data={transectData}/>
                                <Polyline pathOptions={lineOptions} positions={LineProyect} >
                                        <Tooltip>
                                                <div>
                                                <h4>Detalles</h4>
                                                <p>Proyecto 230 kV Mizque - Sehuencas</p>
                                                </div>
                                        </Tooltip>
                                </Polyline>
                                <FloraRescueSpecieMap data={rescueFloraData}/>
                            <Legend colors={legedColors} labels={legendLabels} />
                        </MapContainer>
                    </div>
                    <div className='md:w-1/2 p-4 h-144 flex justify-center items-center 2xl:h-144 xl:h-128 md:h-96 sm:h-80'>
                        <SunburstFamily data={sunburstData} />
                    </div>
                </div>
                    <SpecieList species={specieData}  />

            </div>
        )

}
