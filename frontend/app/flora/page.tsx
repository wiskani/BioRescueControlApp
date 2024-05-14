"use client"

import bannerFlora from "../../public/images/banner-flora.gif"

//Next imports
import { useSession  } from 'next-auth/react'
import { redirect } from 'next/navigation';
import dynamic from 'next/dynamic'
import { useRouter } from 'next/navigation';

//React imports
import React, {
    useEffect,
    useState,
    useCallback,
    useMemo
} from "react"

//Apis imports
import {
    GetRescueFloraSpecie,
    GetRelocationFloraSpecie
} from "../libs/rescue_flora/ApiRescueFlora";
import { GetBarChartFloraByFamily } from "../libs/nivo/ApiBarChartFamily";

//Leaflet imports
import 'leaflet/dist/leaflet.css'
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css'

//Table imports
import { ColumnDef } from '@tanstack/react-table';

//Components imports
import { LineProyect } from '../components/Map/lineProyect';
import BarChartFamily from '../components/Nivo/BarChartFamily';
import { TableFilter } from '../components/Table/TableFilter';
import Loading from './loading';
import { dateFormat } from "../services/dateFormat";

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
    () => (import('../components/Map/Legend')),
    { ssr: false }
)

const FloraRescueSpecieMap = dynamic(
    () => (import('../components/RescueFlora/rescueFloraSpecieMap')),
    { ssr: false }
)

const FloraRelocationSpecieMap = dynamic(
    () => (import('../components/RescueFlora/relocationFloraSpecieMap')),
    { ssr: false }
)

interface BarChartFamilyDataFlex extends BarChartFamilyDataSpa {
    [key: string]: any;
}

//Types
interface FloraColumns extends FloraRescueSpeciesData{
    ver: string;
}


export default function Flora() {
    const { data: session } = useSession();
    const [rescueFloraData, setRescueFloraData] = useState<FloraRescueSpeciesData[]>([]);
    const [relocationFloraData, setRelocationFloraData] = useState<FloraRelocationWithSpecieData[]>([]);
    const [barChartData, setBarChartData] = useState<BarChartFamilyDataSpa[]>(
        [
        {
            Familia: "sin datos",
            Rescates: 0,
            color_rescate: "hsl(0, 100%, 50%)",
            Liberaciones: 0,
            color_reubicacion: "hsl(0, 100%, 50%)"

        },
        ]
    )

    const [loadingBarChart, setLoadingBarChart] = useState(true)
    const router = useRouter();

    const user = session?.user;

    const trasformedData = (data: BarChartFamilyData[]): BarChartFamilyDataSpa[] => {
        return data.map((item) => {
            return {
                Familia: item.family_name,
                Rescates: item.rescue_count,
                color_rescate: item.rescue_color,
                Liberaciones: item.relocation_count,
                color_reubicacion: item.relocation_color
            }
        })
    }

    const rescueDataFlora = useCallback(async (): Promise<FloraRescueSpeciesData[]>=>{
        if (user){
            const data= await GetRescueFloraSpecie({token: user?.token})
            return data
        }
        else{
            return []
        }
    }, [user])

    const relocationDataFlora = useCallback(async (): Promise<FloraRelocationWithSpecieData[]>=>{
        if (user){
            const data= await GetRelocationFloraSpecie({token: user?.token})
            return data
        }
        else{
            return []
        }
    }, [user])

    const barChartFloraData = useCallback(async (): Promise<BarChartFamilyData[]>=>{
        if (user){
            const data= await GetBarChartFloraByFamily({token: user?.token})
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
            rescueDataFlora().then((data)=>{
                setRescueFloraData(data)
            })
            relocationDataFlora().then((data)=>{
                setRelocationFloraData(data)
            })
            barChartFloraData().then((data)=>{
                setBarChartData(trasformedData(data))
                setLoadingBarChart(false)
            })
        }
    }, [session, rescueDataFlora, relocationDataFlora, barChartFloraData])


    const lineOptions = { color: 'red' }

    const legedColors = ['purple','blue', 'red' ]
    const legendLabels = [
        'Puntos de relocalización de Flora',
        'Puntos Rescates de Flora',
        'Proyecto 230 kV Mizque - Sehuencas'
    ]

    //make columns
    const columnsFlora = useMemo<ColumnDef<FloraColumns, any>[]>(
        () => [
            {
                accessorFn: row => row.rescue_date,
                id: 'rescue_date',
                cell: info => dateFormat(info.getValue() as Date),
                header: 'Fecha de rescate',
                meta: { searchable: true },
            },
            {
                accessorFn: row => row.epiphyte_number,
                id: 'epiphyte_number',
                cell: info => info.getValue(),
                header: 'Número de epífito',
                meta: { searchable: true },
            },
            {
                accessorFn: row => row.specie_name,
                id: 'specie_name',
                cell: info => <i>{info.getValue()}</i> || 'no identificado',
                header: 'Especie',
                meta: { searchable: true },
            },
            {
                accessorFn: row => row.genus_name,
                id: 'genus_name',
                cell: info => <i>{info.getValue()}</i> || 'no identificado',
                header: 'Género',
                meta: { searchable: true },
            },
            {
                accessorFn: row => row.family_name,
                id: 'family_name',
                cell: info => <i>{info.getValue()}</i> || 'no identificado',
                header: 'Familia',
                meta: { searchable: true },
            },
            {
                accessorKey: 'other_observations',
                header:'Observaciones',
            },

            {
                accessorFn: row => row.epiphyte_number,
                id: 'epiphyte_number',
                header: " ",
                cell: info => (
                    <div className='flex space-x-4'>
                        <button
                            className="
                            bg-yellow-500
                            hover:bg-yellow-700
                            text-white
                            font-bold
                            py-2 px-4
                            rounded"
                            onClick={() => {
                                router.push(`/flora/rescue/${info.getValue()}`)
                            }}
                        >
                            Ver 
                        </button>
                    </div>
                ),
            }

            
        ],
        [router]
    );
    return (
        <div>
            <div
                className="w-full bg-cover bg-center"
                style={{
                    height: "28rem",
                    backgroundImage: `url(${bannerFlora.src})`,
                }}
            >
                <div
                    className="
                    flex
                    items-center
                    justify-center
                    h-full w-full
                    bg-gray-900
                    bg-opacity-50
                    "
                >
                    <div className="text-center">
                        <h1
                            className="
                            text-white
                            text-2xl
                            font-semibold
                            uppercase md:text-3xl"
                        >
                            Rescate de <
                                span className="text-emerald-400"
                            >
                                Flora
                            </span>
                        </h1>
                    </div>
                </div>

            </div>
            <div
                className="
                flex
                flex-col
                h-full
                2xl:mb-52
                xl:mb-52
                lg:mb-52
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
                        <Polyline pathOptions={lineOptions} positions={LineProyect} >
                            <Tooltip>
                                <div>
                                    <h4>Detalles</h4>
                                    <p>Proyecto 230 kV Mizque - Sehuencas</p>
                                </div>
                            </Tooltip>
                        </Polyline>
                        <FloraRescueSpecieMap data={rescueFloraData}/>
                        <FloraRelocationSpecieMap data={relocationFloraData} radius={12}/>
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

                    {
                        loadingBarChart ? <Loading/> :
                            <BarChartFamily data={barChartData as BarChartFamilyDataFlex[]} />
                    }
                </div>
            </div>
            <TableFilter <FloraRescueSpeciesData>
                columns = {columnsFlora}
                data = {rescueFloraData}
            /> 
            <div
                className="flex justify-center"
            >
                <button 
                    type="button"
                    onClick={() => router.back()}
                    className="bg-emerald-900  hover:bg-emerald-500 text-white font-bold py-2 px-4 rounded"
                >
                    Volver
                </button>
            </div>
        </div>


    )
}
