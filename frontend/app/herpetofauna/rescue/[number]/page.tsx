"use client"

import bannerHerpeto from "../../public/images/banner-herpeto.gif"

//Next imports
import { useSession  } from 'next-auth/react'
import { redirect } from 'next/navigation';
import dynamic from 'next/dynamic'
import { useRouter } from 'next/navigation';

//React imports
import React, {
    useEffect,
    useState,
    useCallback
} from "react"

//Apis imports
import {
    GetRescueHerpetofaunaWithSpecieByNumber
} from '@/app/libs/rescue_herpetofaina/ApiRescueHerpetofauna';

//Leaflet imports
import 'leaflet/dist/leaflet.css'
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css'

//Components imports
import { LineProyect } from '@/app/components/Map/lineProyect';
import { dateFormat } from "../../../services/dateFormat";

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


export default function Page({params}: {params: { number: string}}) {   
    const { data: session } = useSession();
    const user = session?.user;
    const [rescueData, setRescueData] = useState<RescueHerpetoWithSpeciesData | null>(null)
    const [errorMessage, SetErrorMessage]= useState<string>();

    const rescueDataHerpeto = useCallback(
        async (): Promise<RescueHerpetoWithSpeciesData| null>=>{
            if (user){
                try {
                    const data= await GetRescueHerpetofaunaWithSpecieByNumber({
                        token: user?.token,
                        number: params.number
                    });
                    return data;
                } catch (error) {
                    if (error instanceof Error) {
                        SetErrorMessage(error.message)
                        return null;
                    }
                    return null;
                }
            }
            else {
                return null
            }
        }, [user, params.number])


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
            <h1
                className="
                m-4
                text-gl
                text-center
                font-bold
                leading-none
                tracking-tight
                text-gray-600
                md:text-xl
                lg:text-xl
                dark:text-white
                "
            >Rescate y liberación para el rescate:&nbsp;
                <span
                    className='italic'
                >
                    {params.number}
                </span>
            </h1>
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
                    2xl:mb-52
                    xl:mb-52
                    lg:mb-40
                    md:w-1/2
                    p-4
                    md:h-[16rem]
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
                        <Polyline pathOptions={lineOptions} positions={LineProyect} >
                           <Tooltip>
                                <div>
                                    <h4>Detalles</h4>
                                    <p>Proyecto 230 kV Mizque - Sehuencas</p>
                                </div>
                            </Tooltip>
                        </Polyline>
                        {
                            rescueData?
                                <RescueHerpetoSpecieMap
                                data={[rescueData]}
                                /> : null
                        }
                        <Legend colors={legedColors} labels={legendLabels} />
                    </MapContainer> 
                </div>
            </div>
        </div>


    )
}
