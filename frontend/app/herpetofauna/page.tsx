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
    useCallback,
    useMemo
} from "react"

//Apis imports
import {
    GetTransectHerpetofaunaWithSpecies,
    GetTransectTransHerpetofaunaWithSpecies,
    GetPointsTransHerpetofaunaWithSpecies,
    GetRescueHerpetofaunaWithSpecies,
} from '../libs/rescue_herpetofaina/ApiRescueHerpetofauna';
import {
    GetBarChartHerpetoFaunaByFamily
} from '../libs/nivo/ApiBarChartFamily'

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

const TransectHerpetofaunaSpecieMap = dynamic(
        () => (import('../components/HerpetoFauna/TransectoSpecieMap')),
        { ssr: false }
)

const TransectTransloHerpetofaunaSpecieMap = dynamic(
        () => (import('../components/HerpetoFauna/TransectoTransloSpecieMap')),
        { ssr: false }
)
const PointTransloHerpetofaunaSpecieMap = dynamic(
        () => (import('../components/HerpetoFauna/PointTransloSpecieMap')),
        { ssr: false }
)

//Types
interface HerpetoColumns extends RescueHerpetoWithSpeciesData {
    ver: string;
}

interface BarChartFamilyDataFlex extends BarChartFamilyDataSpa {
    [key: string]: any;
}

export default function HerpetoFauna() {
    const { data: session } = useSession();
    const [transectData, setTransectData] = useState<TransectHerpetoWithSpecies[]>([])
    const [transectTransData, setTransectTransData] = useState<TransectHerpetoTransWithSpeciesData[]>([])
    const [pointTransData, setPointTransData] = useState<PointHerpetoTransloWithSpeciesData[]>([])
    const [rescueData, setRescueData] = useState<RescueHerpetoWithSpeciesData[]>([])
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

    const transectDataHerpeto = useCallback(async (): Promise<TransectHerpetoWithSpecies[]>=>{
        if (user){
            const data= await GetTransectHerpetofaunaWithSpecies({token: user?.token})
            return data
        }
        else{
            return []
        }
    }, [user])

    const transectTransDataHerpeto = useCallback(async (): Promise<TransectHerpetoTransWithSpeciesData[]>=>{
        if (user){
            const data= await GetTransectTransHerpetofaunaWithSpecies({token: user?.token})
            return data
        }
        else{
            return []
        }
    }, [user])

    const pointTransDataHerpeto = useCallback(async (): Promise<PointHerpetoTransloWithSpeciesData[]>=>{
        if (user){
            const data= await GetPointsTransHerpetofaunaWithSpecies({token: user?.token})
            return data
        }
        else{
            return []
        }
    }, [user])

    const barChartHerpetoData = useCallback(async (): Promise<BarChartFamilyData[]>=>{
        if (user){
            const data= await GetBarChartHerpetoFaunaByFamily({token: user?.token})
            return data
        }
        else{
            return []
        }
    }, [user])

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
            transectDataHerpeto().then((data)=>{
                setTransectData(data)
            })
            transectTransDataHerpeto().then((data)=>{
                setTransectTransData(data)
            })
            pointTransDataHerpeto().then((data)=>{
                setPointTransData(data)
            })
            barChartHerpetoData().then((data)=>{
                setBarChartData(trasformedData(data))
                setLoadingBarChart(false)
            })
            rescueDataHerpeto().then((data)=>{
                setRescueData(data)
            })
        }

    }, [
            session,
            transectDataHerpeto,
            transectTransDataHerpeto,
            pointTransDataHerpeto,
            barChartHerpetoData,
            rescueDataHerpeto
        ])


    const lineOptions = { color: 'red' }

    const legedColors = ['brown', 'blue' ,'green', 'red' ]
    const legendLabels = [
        'Puntos de liberación',
        'Transectors de liberación',
        'Transcetors de rescate',
        'Proyecto 230 kV Mizque - Sehuencas'
    ]

    //make columns
    const columnsHerpeto = useMemo<ColumnDef<HerpetoColumns, any>[]>(
        () => [
            {
                accessorFn: row => row.date_rescue,
                id: 'rescue_date',
                cell: info => dateFormat(info.getValue() as Date),
                header: 'Fecha de rescate',
                meta: { searchable: true },
            },
            {
                accessorFn: row => row.number,
                id: 'number',
                cell: info => info.getValue(),
                header: 'Número',
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
                accessorFn: row => row.age_group_name,
                id: 'age_group_name',
                cell: info => <i>{info.getValue()}</i> || 'no identificado',
                header: 'Grupo de edad',
                meta: { searchable: true },
            },
            {
                accessorFn: row => row.number,
                id: 'number',
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
                                router.push(`/herpetofauna/rescue/${info.getValue()}`)
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
                    backgroundImage: `url(${bannerHerpeto.src})`,
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
                               Herpetofauna 
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
                        <PointTransloHerpetofaunaSpecieMap data={pointTransData} />
                        <TransectHerpetofaunaSpecieMap data={transectData}/>
                        <TransectTransloHerpetofaunaSpecieMap data={transectTransData} />
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

                    {
                        loadingBarChart ? <Loading/> :
                            <BarChartFamily data={barChartData as BarChartFamilyDataFlex[]} />
                    }
                </div>
            </div>
            <TableFilter <RescueHerpetoWithSpeciesData>
                columns = {columnsHerpeto}
                data = {rescueData}
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
