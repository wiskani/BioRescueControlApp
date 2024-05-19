"use client"

import bannerMammals from "../../public/images/banner-masto.gif"

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
    GetRescueMammalsWithSpecies,
    GetRealeaseMammalsWithSpecies
} from "../libs/rescue_mammals/ApiRescueMammalsWithSpecies";
import {
    GetBarChartMammalsByFamily
} from "../libs/nivo/ApiBarChartFamily";

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

const RescueMammalSpecieMap = dynamic(
    () => (import('../components/RescueMammals/RescueMammalsSpecieMap')),
    { ssr: false }
)

const RealeaseMammalSpecieMap = dynamic(
    () => (import('../components/RescueMammals/RealeaseMammalsSpecieMap')),
    { ssr: false }
)

//Types
interface MammalsColumns extends RescueMammalsWithSpecieData{
    ver: string;
}
interface BarChartFamilyDataFlex extends BarChartFamilyDataSpa {
    [key: string]: any;
}

export default function Flora() {
    const { data: session } = useSession();
    const [rescueMammals, setRescueMammals] = useState<RescueMammalsWithSpecieData[]>([]);
    const [realeaseMammals, setRealeaseMammals] = useState<ReleaseMammalsWithSpecieData[]>([]);
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

    const rescueDataMammals = useCallback(async (): Promise<RescueMammalsWithSpecieData[]>=>{
        if (user){
            const data= await GetRescueMammalsWithSpecies({token: user?.token})
            return data
        }
        else{
            return []
        }
    }, [user])

    const realeaseDataMammals = useCallback(async (): Promise<ReleaseMammalsWithSpecieData[]>=>{
        if (user){
            const data= await GetRealeaseMammalsWithSpecies({token: user?.token})
            return data
        }
        else{
            return []
        }
    }, [user])

    const barChartDataMammals = useCallback(async (): Promise<BarChartFamilyData[]>=>{
        if (user){
            const data= await GetBarChartMammalsByFamily({token: user?.token})
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
        else {
            rescueDataMammals().then((data) => {
                setRescueMammals(data)
            })
            realeaseDataMammals().then((data) => {
                setRealeaseMammals(data)
            })
            barChartDataMammals().then((data) => {
                setBarChartData(trasformedData(data))
                setLoadingBarChart(false)
            })
        }

    }, [session])


    const lineOptions = { color: 'red' }

    const legedColors = ['purple','brown', 'red' ]
    const legendLabels = [
        'Puntos de liberación de Mamiferos',
        'Puntos rescates de mamiferos',
        'Proyecto 230 kV Mizque - Sehuencas'
    ]

    //make columns
    const columnsMammals = useMemo<ColumnDef<MammalsColumns, any>[]>(
        () => [
            {
                accessorFn: row => row.date,
                id: 'date',
                cell: info => dateFormat(info.getValue() as Date),
                header: 'Fecha de rescate',
                meta: { searchable: true },
            },
            {
                accessorFn: row => row.cod,
                id: 'cod',
                cell: info => info.getValue(),
                header: 'Código',
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
                accessorFn: row => row.observation,
                id: 'observation',
                cell: info => <i>{info.getValue()}</i> || 'no identificado',
                header: 'Obersvación',
            },
            {
                accessorFn: row => row.cod,
                id: 'cod',
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
                                router.push(`/mammals/rescue/${info.getValue()}`)
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
                    backgroundImage: `url(${bannerMammals.src})`,
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
                              Maníferos 
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
                        <Polyline pathOptions={lineOptions} positions={LineProyect} >
                            <Tooltip>
                                <div>
                                    <h4>Detalles</h4>
                                    <p>Proyecto 230 kV Mizque - Sehuencas</p>
                                </div>
                            </Tooltip>
                        </Polyline>
                        <RescueMammalSpecieMap data={rescueMammals} />
                        <RealeaseMammalSpecieMap data={realeaseMammals} />
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
            <TableFilter <RescueMammalsWithSpecieData>
                columns = {columnsMammals}
                data = {rescueMammals}
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
