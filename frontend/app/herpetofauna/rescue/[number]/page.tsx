"use client"

import bannerHerpeto from "../../public/images/banner-herpeto.gif"

//Next imports
import { useSession  } from 'next-auth/react'
import { redirect } from 'next/navigation';
import dynamic from 'next/dynamic'

//React imports
import React, {
    useEffect,
    useState,
    useCallback
} from "react"

//Apis imports
import {
    GetRescueHerpetofaunaWithSpecies
} from '@/app/libs/rescue_herpetofaina/ApiRescueHerpetofauna';

//Leaflet imports
import 'leaflet/dist/leaflet.css'
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css'

//Components imports
import { LineProyect } from '@/app/components/Map/lineProyect';
import Loading from '../../loading';

//import with dynamic
const MapContainer = dynamic(
    async () => (await import('react-leaflet')).MapContainer,
    { ssr: false }
)

const TileLayer = dynamic(
    async () => (await import('react-leaflet')).TileLayer,
    { ssr: false }
)


const Polyline = dynamic(
    async () => (await import('react-leaflet')).Polyline,
    { ssr: false }
)

const Tooltip = dynamic(
    async () => (await import('react-leaflet')).Tooltip,
    { ssr: false }
)

const Legend = dynamic(
    () => (import('@/app/components/Map/Legend')),
    { ssr: false }
)

const RescueHerpetoSpecieMap = dynamic(
        () => (import('@/app/components/HerpetoFauna/RescueHerpetoSpecieMap')),
        { ssr: false }
)


export default function HerpetoFauna() {
    const { data: session } = useSession();
    const user = session?.user;
    const [rescueData, setRescueData] = useState<RescueHerpetoWithSpeciesData[]>([])


    const rescueDataHerpeto = useCallback(async (): Promise<RescueHerpetoWithSpeciesData[]>=>{
        if (user){
            const data= await GetRescueHerpetofaunaWithSpecies({token: user?.token})
            return data
        }
        else{
            return []
        }
    }, [user])


    useEffect(() => {
        if (!session?.user) {
                redirect('/')
            }

        else{
            rescueDataHerpeto().then((data)=>{
                setRescueData(data)
            })
        }

    }, [session, rescueDataHerpeto])


    const lineOptions = { color: 'red' }

    const legedColors = ['green', 'red' ]
    const legendLabels = [
        'Transcetors de rescate',
        'Proyecto 230 kV Mizque - Sehuencas'
    ]

    return (
        <div>
            <div
                className="
                flex
                flex-col
                h-full
                2xl:mb-52
                xl:mb-52
                lg:mb-40
                md:flex-row
                md:mb-0
                sm:mb-0
                justify-center"
            >
                <div className="
                    h-96
                    p-0
                    z-50
                    md:w-1/2
                    p-4 md:h-[16rem]
                    sd:h-[6rem]
                    "
                >
                    <MapContainer
                        center={[-17.489, -65.271]}
                        zoom={12}
                        scrollWheelZoom={false}
                        className='
                        h-80
                        w-full
                        2xl:h-[40rem]
                        xl:h-[40rem]
                        lg:h-[35rem]
                        '
                    >
                        <TileLayer

                            url={
                                `https://api.mapbox.com/styles/v1/mapbox/streets-v12/tiles/256/{z}/{x}/{y}@2x?access_token=${process.env.NEXT_PUBLIC_MAPBOX_TOKEN}`
                            }
                            attribution='Map data &copy; <a href=&quot;https://www.openstreetmap.org/&quot;>OpenStreetMap</a> contributors, <a href=&quot;https://creativecommons.org/licenses/by-sa/2.0/&quot;>CC-BY-SA</a>, Imagery &copy; <a href=&quot;https://www.mapbox.com/&quot;>Mapbox</a>'
                        />
                        <RescueHerpetoSpecieMap data={rescueData} />
                        <Polyline pathOptions={lineOptions} positions={LineProyect} >
                           <Tooltip>
                                <div>
                                    <h4>Detalles</h4>
                                    <p>Proyecto 230 kV Mizque - Sehuencas</p>
                                </div>
                            </Tooltip>
                        </Polyline>
                        <Legend colors={legedColors} labels={legendLabels} />
                    </MapContainer> 
                </div>
                <div className='
                    md:w-1/2
                    p-4 h-144
                    flex
                    justify-center
                    items-center
                    2xl:h-144
                    xl:h-128
                    md:h-96
                    sm:h-80
                    '
                >

                </div>
            </div>
        </div>


    )
}
